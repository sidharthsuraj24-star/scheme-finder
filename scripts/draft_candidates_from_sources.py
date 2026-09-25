#!/usr/bin/env python3
"""Auto-draft catalogue candidates from official sources (Phase 4 automation).

Scans official listings / feeds, dedupes against the catalogue and the existing
candidate queue (id, name and URL fuzzy match) and appends NEW rows to
``data/catalogue_candidates.json`` with ``status: "needs_review"``.

Hard rules (see docs/CATALOGUE_OPS.md):
- NEVER writes ``schemes.json``. Candidates are leads for a human reviewer.
- NEVER invents eligibility. Only fields present verbatim on the official
  page / feed are copied, each wrapped as ``{"value", "verified": false,
  "source_field"}``.
- Polite: robots.txt honoured, per-host delay (default 2 s), 15 s timeout,
  5 MB response cap, capped items per source and new rows per run.

Sources (``--sources``; default = all except the opt-in myScheme API):
  pib-en, pib-hi         PIB press-release RSS (English / Hindi) — leads only
  myscheme               myScheme listing: ``--myscheme-json FILE`` (search-API
                         JSON export) or, opt-in, ``MYSCHEME_API_KEY`` env
  gov-uk                 GOV.UK news Atom (keyword "scheme")
  canada-news            Canada News Centre Atom (news releases)
  us-federal-register    Federal Register API (final rules mentioning programs)

Examples:
  # Daily routine (writes the queue + digest):
  python3 scripts/draft_candidates_from_sources.py \
      --digest-md /tmp/candidate-digest.md --summary-json /tmp/candidate-digest.json

  # Preview only (no writes):
  python3 scripts/draft_candidates_from_sources.py --dry-run --digest

  # Offline / tests: read <source_id>.xml|.json from a fixtures dir
  python3 scripts/draft_candidates_from_sources.py --offline-dir tests/fixtures \
      --dry-run --today 2026-09-25

Exit codes: 0 = ran (even if some sources were blocked; see summary),
2 = bad arguments / unreadable catalogue.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import html
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Callable, Iterable
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = REPO_ROOT / "data" / "catalogue_candidates.json"
FE_CANDIDATES = REPO_ROOT / "frontend" / "data" / "catalogue_candidates.json"
SCHEMES = REPO_ROOT / "data" / "schemes.json"
IST = ZoneInfo("Asia/Kolkata")

ACTOR = "draft_candidates_from_sources"
USER_AGENT = (
    "scheme-finder-candidate-drafter/1.0 "
    "(+https://github.com/sidharthsuraj24-star/scheme-finder; polite; human-reviewed)"
)
TIMEOUT_SEC = 15.0
MAX_BYTES = 5 * 1024 * 1024
NAME_FUZZY_THRESHOLD = 0.88

ATOM = "{http://www.w3.org/2005/Atom}"


# --------------------------------------------------------------------------
# Source registry
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Source:
    id: str
    label: str
    country: str
    url: str
    kind: str  # rss | atom | fr-json | myscheme-json
    candidate_kind: str  # scheme_listing | press_release_lead | notice_lead
    lang: str = "en"
    opt_in: bool = False


SOURCES: dict[str, Source] = {
    s.id: s
    for s in [
        Source(
            "pib-en",
            "PIB press releases (English RSS)",
            "India",
            "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3",
            "rss",
            "press_release_lead",
        ),
        Source(
            "pib-hi",
            "PIB press releases (Hindi RSS)",
            "India",
            "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=3",
            "rss",
            "press_release_lead",
            lang="hi",
        ),
        Source(
            "myscheme",
            "myScheme scheme listing (search API export)",
            "India",
            "https://api.myscheme.gov.in/search/v5/schemes?lang=en&q=%5B%5D&keyword=&sort=&from=0&size=50",
            "myscheme-json",
            "scheme_listing",
            opt_in=True,
        ),
        Source(
            "gov-uk",
            "GOV.UK news and communications (Atom, keyword: scheme)",
            "United Kingdom",
            "https://www.gov.uk/search/news-and-communications.atom?keywords=scheme&order=updated-newest",
            "atom",
            "press_release_lead",
        ),
        Source(
            "canada-news",
            "Canada News Centre (Atom)",
            "Canada",
            "https://api.io.canada.ca/io-server/gc/news/en/v2?sort=publishedDate&orderBy=desc&pick=50&format=atom",
            "atom",
            "press_release_lead",
        ),
        Source(
            "us-federal-register",
            "Federal Register final rules (API, term: program)",
            "United States",
            "https://www.federalregister.gov/api/v1/documents.json?per_page=50&order=newest"
            "&conditions%5Btype%5D%5B%5D=RULE&conditions%5Bterm%5D=program"
            "&fields%5B%5D=title&fields%5B%5D=html_url&fields%5B%5D=publication_date"
            "&fields%5B%5D=agencies&fields%5B%5D=abstract&fields%5B%5D=document_number",
            "fr-json",
            "notice_lead",
        ),
    ]
}
DEFAULT_SOURCES = [s.id for s in SOURCES.values() if not s.opt_in]

# A lead must name something on offer (scheme/programme/benefit...) ...
OFFER_RE = re.compile(
    r"\b(schemes?|yojana|programmes?|programs?|grants?|funds?|benefits?|allowances?|"
    r"pensions?|scholarships?|subsid(?:y|ies)|tax credits?|assistance|bursar(?:y|ies)|"
    r"loans?|mission|abhiyan|support payments?|rebates?|vouchers?)\b",
    re.I,
)
OFFER_HI_RE = re.compile(r"(योजना|योजनाओं|कार्यक्रम|मिशन|अभियान|छात्रवृत्ति|पेंशन|सब्सिडी|अनुदान|सहायता)")
# ... and signal that it is new / opening (not a routine update or statement).
NOVELTY_RE = re.compile(
    r"\b(launch(?:es|ed)?|new|introduc(?:es|ed|ing)|unveil(?:s|ed)?|announc(?:es|ed)|"
    r"opens?|now open|call for (?:proposals|applications)|roll(?:s|ed)? out|expands?|"
    r"establish(?:es|ed|ing|ment)?|approves?|approved|creat(?:es|ed|ion of))\b",
    re.I,
)
NOVELTY_HI_RE = re.compile(r"(शुभारंभ|शुरू|आरंभ|नई|नया|घोषणा|मंजूरी|स्वीकृति|लॉन्च)")
# Routine / non-offer noise.
EXCLUDE_RE = re.compile(
    r"\b(correction|corrigendum|rescind(?:s|ing)?|nondiscrimination|statement by|"
    r"media advisory|seizure|escape|assault|condolence|greets|obituary|visit of|"
    r"fees for|technical amendment|delay of effective date)\b",
    re.I,
)

TITLE_STOPWORDS = {
    "the", "of", "for", "and", "a", "an", "to", "in", "scheme", "schemes", "yojana",
    "programme", "program", "mission", "abhiyan", "national", "central", "state",
    "government", "govt", "india", "indian", "sector", "new",
}
ALIASES = [
    (re.compile(r"\bpradhan mantri\b"), "pm"),
    (re.compile(r"\bprime minister'?s?\b"), "pm"),
    (re.compile(r"\bmukhya ?mantri\b"), "cm"),
    (re.compile(r"\bchief minister'?s?\b"), "cm"),
]


# --------------------------------------------------------------------------
# Normalisation + dedupe
# --------------------------------------------------------------------------

def norm_text(s: str) -> str:
    s = unicodedata.normalize("NFKC", html.unescape(s or "")).lower()
    for pat, rep in ALIASES:
        s = pat.sub(rep, s)
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def name_key(s: str) -> str:
    return " ".join(t for t in norm_text(s).split() if t not in TITLE_STOPWORDS)


def norm_url(u: str) -> str:
    if not u:
        return ""
    try:
        p = urllib.parse.urlsplit(u.strip())
    except ValueError:
        return u.strip().lower()
    host = (p.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    path = re.sub(r"/+$", "", p.path or "")
    path = re.sub(r"/(index|default)\.(html?|aspx?|php)$", "", path, flags=re.I)
    q = urllib.parse.parse_qsl(p.query, keep_blank_values=False)
    q = [(k, v) for k, v in q if not k.lower().startswith("utm_")]
    query = urllib.parse.urlencode(sorted(q))
    return f"{host}{path.lower()}" + (f"?{query}" if query else "")


def strip_parens(s: str) -> str:
    return re.sub(r"\([^)]*\)", " ", s or "")


def acronyms(name: str) -> set[str]:
    """Explicit acronyms written in the name, e.g. 'PM-KISAN', '(PMAY-G)'."""
    out = set()
    for m in re.findall(r"\(([A-Z][A-Z0-9\-]{2,15})\)", name or ""):
        out.add(m.replace("-", "").lower())
    for m in re.findall(r"\b([A-Z]{2,}(?:-[A-Z0-9]{2,})+)\b", name or ""):
        out.add(m.replace("-", "").lower())
    return {a for a in out if len(a) >= 4}


def name_variants(v: Any) -> list[str]:
    """Catalogue names may be plain strings or {"en": ..., "hi": ..., "ml": ...}."""
    if isinstance(v, dict):
        return [str(x) for x in v.values() if isinstance(x, str) and x.strip()]
    if isinstance(v, str) and v.strip():
        return [v]
    return []


@dataclass
class KnownEntry:
    kind: str  # scheme | candidate
    id: str
    names: list[str]
    urls: list[str]
    name_keys: list[str] = field(default_factory=list)
    full_norms: list[str] = field(default_factory=list)
    acr: set[str] = field(default_factory=set)

    @property
    def name(self) -> str:
        return self.names[0] if self.names else ""


class Catalogue:
    def __init__(self, schemes: list[dict[str, Any]], candidates: list[dict[str, Any]]):
        self.entries: list[KnownEntry] = []
        self.by_id: dict[str, KnownEntry] = {}
        self.url_index: dict[str, KnownEntry] = {}
        for s in schemes:
            if not isinstance(s, dict) or not s.get("id"):
                continue
            self.add(
                KnownEntry(
                    "scheme",
                    str(s["id"]),
                    name_variants(s.get("scheme_name") or s.get("name")),
                    [str(s.get(k) or "") for k in ("official_source_url", "apply_url")],
                )
            )
        for c in candidates:
            if not isinstance(c, dict) or not c.get("id"):
                continue
            self.add(
                KnownEntry(
                    "candidate",
                    str(c["id"]),
                    name_variants(c.get("name")),
                    [str(c.get(k) or "") for k in ("official_source_url", "source_url")],
                )
            )

    def add(self, e: KnownEntry) -> None:
        keys = [name_key(n) for n in e.names] + [name_key(strip_parens(n)) for n in e.names]
        e.name_keys = list(dict.fromkeys(k for k in keys if k))
        forms: list[str] = []
        for n in e.names:
            forms.append(norm_text(n))
            # Also the name without a parenthesised acronym: "... Nidhi (PM-KISAN)".
            forms.append(norm_text(strip_parens(n)))
        e.full_norms = list(dict.fromkeys(f for f in forms if f))
        e.acr = set().union(*(acronyms(n) for n in e.names)) if e.names else set()
        self.entries.append(e)
        self.by_id.setdefault(e.id, e)
        for u in e.urls:
            nu = norm_url(u)  # exact normalised match only (no prefix matching)
            if nu and nu not in self.url_index:
                self.url_index[nu] = e

    def match(self, cand_id: str, name: str, urls: Iterable[str]) -> tuple[str, KnownEntry | None]:
        """Return (reason, entry) for a duplicate, or ("", None) if new."""
        if cand_id in self.by_id:
            return "id", self.by_id[cand_id]
        for u in urls:
            nu = norm_url(u)
            if nu and nu in self.url_index:
                return "url", self.url_index[nu]
        cand_keys = {k for k in (name_key(name), name_key(strip_parens(name))) if k}
        if cand_keys:
            best, best_e = 0.0, None
            for e in self.entries:
                for k in e.name_keys:
                    for ck in cand_keys:
                        r = difflib.SequenceMatcher(None, ck, k).ratio()
                        if r > best:
                            best, best_e = r, e
            if best >= NAME_FUZZY_THRESHOLD:
                return f"name~{best:.2f}", best_e
            # Same explicit acronym, e.g. "(PM-KISAN)" in both names.
            a = acronyms(name)
            if a:
                for e in self.entries:
                    if e.acr & a:
                        return "acronym", e
        return "", None

    def mentions(self, text: str) -> KnownEntry | None:
        """Existing scheme explicitly named in a headline (update, not new)."""
        t_acr = {a.replace("-", "").lower() for a in re.findall(r"\b[A-Z][A-Z0-9\-]{3,15}\b", text or "")}
        t_norm = f" {norm_text(text)} "
        for e in self.entries:
            if e.kind != "scheme":
                continue
            if e.acr & t_acr:
                return e
            for full in e.full_norms:
                if len(full) >= 12 and f" {full} " in t_norm:
                    return e
        return None


# --------------------------------------------------------------------------
# Fetching (polite)
# --------------------------------------------------------------------------

class PoliteFetcher:
    def __init__(self, delay_sec: float = 2.0, timeout: float = TIMEOUT_SEC, headers: dict | None = None):
        self.delay = delay_sec
        self.timeout = timeout
        self.extra_headers = headers or {}
        self._last: dict[str, float] = {}
        self._robots: dict[str, urllib.robotparser.RobotFileParser | None] = {}
        self.requests = 0

    def _wait(self, host: str) -> None:
        last = self._last.get(host)
        if last is not None:
            gap = time.monotonic() - last
            if gap < self.delay:
                time.sleep(self.delay - gap)
        self._last[host] = time.monotonic()

    def _raw(self, url: str, headers: dict | None = None) -> tuple[int, bytes]:
        host = urllib.parse.urlsplit(url).hostname or ""
        self._wait(host)
        h = {"User-Agent": USER_AGENT, "Accept": "*/*", **self.extra_headers, **(headers or {})}
        req = urllib.request.Request(url, headers=h, method="GET")
        self.requests += 1
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read(MAX_BYTES + 1)
                if len(body) > MAX_BYTES:
                    raise ValueError(f"response exceeds {MAX_BYTES} bytes")
                return resp.status, body
        except urllib.error.HTTPError as e:
            return e.code, b""

    def allowed(self, url: str) -> bool:
        p = urllib.parse.urlsplit(url)
        base = f"{p.scheme}://{p.netloc}"
        if base not in self._robots:
            rp = urllib.robotparser.RobotFileParser()
            try:
                status, body = self._raw(f"{base}/robots.txt")
                if status == 200:
                    rp.parse(body.decode("utf-8", "replace").splitlines())
                    self._robots[base] = rp
                else:
                    self._robots[base] = None  # no robots / blocked → no restriction stated
            except Exception:  # noqa: BLE001
                self._robots[base] = None
        rp = self._robots[base]
        return True if rp is None else rp.can_fetch(USER_AGENT, url)

    def get(self, url: str, headers: dict | None = None) -> tuple[int, bytes]:
        if not self.allowed(url):
            return -1, b""
        return self._raw(url, headers)


# --------------------------------------------------------------------------
# Parsers → raw items {title, link, published, summary, extra fields}
# --------------------------------------------------------------------------

def _clean(s: str | None, limit: int = 600) -> str:
    s = html.unescape(s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:limit]


def _parse_date(s: str | None) -> str:
    if not s:
        return ""
    s = s.strip()
    try:
        return parsedate_to_datetime(s).date().isoformat()
    except (TypeError, ValueError, IndexError):
        pass
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        pass
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
    return m.group(1) if m else ""


def parse_rss(body: bytes) -> list[dict[str, Any]]:
    root = ET.fromstring(body)
    out = []
    for it in root.iter("item"):
        out.append(
            {
                "title": _clean(it.findtext("title"), 300),
                "link": (it.findtext("link") or "").strip(),
                "published": _parse_date(it.findtext("pubDate")),
                "summary": _clean(it.findtext("description")),
                "fields": {"rss:title": "title", "rss:pubDate": "published", "rss:description": "summary"},
            }
        )
    return out


def parse_atom(body: bytes) -> list[dict[str, Any]]:
    root = ET.fromstring(body)
    out = []
    for e in root.iter(f"{ATOM}entry"):
        link = ""
        for ln in e.findall(f"{ATOM}link"):
            if ln.get("rel", "alternate") == "alternate" and ln.get("href"):
                link = ln.get("href", "")
                break
        cats = [c.get("term", "") for c in e.findall(f"{ATOM}category") if c.get("term")]
        out.append(
            {
                "title": _clean(e.findtext(f"{ATOM}title"), 300),
                "link": link.strip(),
                "published": _parse_date(e.findtext(f"{ATOM}updated") or e.findtext(f"{ATOM}published")),
                "summary": _clean(e.findtext(f"{ATOM}summary") or e.findtext(f"{ATOM}content")),
                "category": ", ".join(cats),
            }
        )
    return out


def parse_federal_register(body: bytes) -> list[dict[str, Any]]:
    d = json.loads(body)
    out = []
    for r in d.get("results") or []:
        agencies = [a.get("name") or a.get("raw_name") or "" for a in (r.get("agencies") or []) if isinstance(a, dict)]
        out.append(
            {
                "title": _clean(r.get("title"), 300),
                "link": (r.get("html_url") or "").strip(),
                "published": _parse_date(r.get("publication_date")),
                "summary": _clean(r.get("abstract")),
                "agency": ", ".join(a for a in agencies if a),
                "document_number": str(r.get("document_number") or ""),
            }
        )
    return out


def parse_myscheme(body: bytes) -> list[dict[str, Any]]:
    """Tolerant parser for the myScheme search API JSON (data.hits.items[].fields)."""
    d = json.loads(body)
    items = (
        (((d.get("data") or {}).get("hits") or {}).get("items"))
        if isinstance(d, dict)
        else d
    ) or []
    out = []
    for it in items:
        f = (it or {}).get("fields") or it or {}
        slug = f.get("slug") or ""
        name = f.get("schemeName") or f.get("name") or ""
        if not name:
            continue

        def joined(v: Any) -> str:
            if isinstance(v, list):
                return ", ".join(str(x) for x in v if x)
            return str(v or "")

        out.append(
            {
                "title": _clean(name, 300),
                "link": f"https://www.myscheme.gov.in/schemes/{slug}" if slug else "",
                "published": "",
                "summary": _clean(f.get("briefDescription")),
                "ministry": _clean(f.get("nodalMinistryName")),
                "level": _clean(f.get("level")),
                "beneficiary_state": _clean(joined(f.get("beneficiaryState"))),
                "category": _clean(joined(f.get("schemeCategory"))),
                "slug": slug,
            }
        )
    return out


PARSERS: dict[str, Callable[[bytes], list[dict[str, Any]]]] = {
    "rss": parse_rss,
    "atom": parse_atom,
    "fr-json": parse_federal_register,
    "myscheme-json": parse_myscheme,
}

# Which raw keys become extracted fields, and the source field they came from.
FIELD_SOURCES: dict[str, dict[str, str]] = {
    "rss": {"title": "rss:item/title", "published": "rss:item/pubDate", "summary": "rss:item/description"},
    "atom": {
        "title": "atom:entry/title",
        "published": "atom:entry/updated",
        "summary": "atom:entry/summary",
        "category": "atom:entry/category@term",
    },
    "fr-json": {
        "title": "federalregister:title",
        "published": "federalregister:publication_date",
        "summary": "federalregister:abstract",
        "agency": "federalregister:agencies[].name",
        "document_number": "federalregister:document_number",
    },
    "myscheme-json": {
        "title": "myscheme:schemeName",
        "summary": "myscheme:briefDescription",
        "ministry": "myscheme:nodalMinistryName",
        "level": "myscheme:level",
        "beneficiary_state": "myscheme:beneficiaryState",
        "category": "myscheme:schemeCategory",
    },
}


# --------------------------------------------------------------------------
# Drafting
# --------------------------------------------------------------------------

def is_relevant(src: Source, item: dict[str, Any]) -> tuple[bool, str]:
    title = item.get("title") or ""
    if not title or not item.get("link"):
        return False, "missing title/link"
    if src.candidate_kind == "scheme_listing":
        return True, ""
    if src.id == "canada-news" and item.get("category") and "news release" not in item["category"].lower():
        return False, f"category={item['category']}"
    if EXCLUDE_RE.search(title):
        return False, "routine/noise"
    # Title only: summaries mention "new" too loosely to be a signal.
    if src.lang == "hi":
        offer = OFFER_HI_RE.search(title) or OFFER_RE.search(title)
        novel = NOVELTY_HI_RE.search(title) or NOVELTY_RE.search(title)
    else:
        offer = OFFER_RE.search(title)
        novel = NOVELTY_RE.search(title)
    if not offer:
        return False, "no scheme/programme term in title"
    if not novel:
        return False, "no launch/new/open signal"
    return True, ""


def slugify(s: str, n: int = 40) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:n].strip("-")


def candidate_id(src: Source, item: dict[str, Any]) -> str:
    base = slugify(item.get("slug") or item.get("title") or "", 36)
    h = hashlib.sha1(norm_url(item.get("link", "")).encode()).hexdigest()[:8]
    return f"cand-auto-{src.id}-{base or 'item'}-{h}"


def build_candidate(src: Source, item: dict[str, Any], found_at: str, noted_at: str) -> dict[str, Any]:
    extracted: dict[str, Any] = {}
    for key, source_field in FIELD_SOURCES[src.kind].items():
        val = item.get(key)
        if val:
            extracted[key] = {"value": val, "verified": False, "source_field": source_field}
    return {
        "id": candidate_id(src, item),
        "name": item["title"],
        "country": src.country,
        "official_source_url": item["link"],
        "status": "needs_review",
        "reason": f"Auto-drafted from {src.label} on {found_at}. Unverified lead — human review required.",
        "noted_at": noted_at,
        "actor": ACTOR,
        "notes": (
            "AUTO-DRAFT: every extracted field is unverified and copied verbatim from the source. "
            "No eligibility was inferred. Verify on the official scheme page before any "
            "schemes.json PR; reject if this is not a citizen-facing scheme."
        ),
        "auto_drafted": True,
        "verified": False,
        "candidate_kind": src.candidate_kind,
        "source": {"id": src.id, "label": src.label, "feed_url": src.url, "lang": src.lang},
        "source_url": item["link"],
        "found_at": found_at,
        "extracted": extracted,
    }


@dataclass
class SourceResult:
    id: str
    label: str
    status: str = "ok"  # ok | blocked | error | skipped
    detail: str = ""
    items_seen: int = 0
    relevant: int = 0
    new: list[dict[str, Any]] = field(default_factory=list)
    duplicates: list[dict[str, str]] = field(default_factory=list)
    known_mentions: list[dict[str, str]] = field(default_factory=list)
    skipped_old: int = 0


def load_source_body(
    src: Source,
    fetcher: PoliteFetcher | None,
    offline_dir: Path | None,
    myscheme_json: Path | None,
) -> tuple[str, str, bytes]:
    """Return (status, detail, body)."""
    if src.id == "myscheme" and myscheme_json:
        return "ok", f"file {myscheme_json.name}", myscheme_json.read_bytes()
    if offline_dir is not None:
        for ext in (".xml", ".json"):
            p = offline_dir / f"{src.id}{ext}"
            if p.is_file():
                return "ok", f"fixture {p.name}", p.read_bytes()
        return "skipped", "no fixture", b""
    if src.id == "myscheme":
        key = os.environ.get("MYSCHEME_API_KEY", "").strip()
        if not key:
            return (
                "skipped",
                "myScheme listing is client-rendered behind a keyed API; pass --myscheme-json "
                "(saved search export) or set MYSCHEME_API_KEY if you are authorised to use one",
                b"",
            )
        assert fetcher is not None
        status, body = fetcher.get(src.url, headers={"x-api-key": key, "Accept": "application/json"})
    else:
        assert fetcher is not None
        status, body = fetcher.get(src.url)
    if status == -1:
        return "blocked", "disallowed by robots.txt", b""
    if status in (401, 403, 429):
        return "blocked", f"HTTP {status} (source blocks this network/agent; retry from India or later)", b""
    if status != 200:
        return "error", f"HTTP {status}", b""
    return "ok", f"HTTP 200, {len(body)} bytes", body


def _recent(item: dict[str, Any], cutoff: date) -> bool:
    pub = item.get("published")
    if not pub:
        return True
    try:
        return date.fromisoformat(pub) >= cutoff
    except ValueError:
        return True


def run(
    source_ids: list[str],
    catalogue: Catalogue,
    *,
    today: date,
    since_days: int,
    max_items: int,
    max_new: int,
    fetcher: PoliteFetcher | None,
    offline_dir: Path | None = None,
    myscheme_json: Path | None = None,
) -> list[SourceResult]:
    found_at = today.isoformat()
    noted_at = datetime.now(IST).isoformat(timespec="seconds")
    cutoff = today - timedelta(days=since_days)
    results: list[SourceResult] = []
    new_total = 0
    for sid in source_ids:
        src = SOURCES[sid]
        res = SourceResult(sid, src.label)
        results.append(res)
        try:
            status, detail, body = load_source_body(src, fetcher, offline_dir, myscheme_json)
        except Exception as exc:  # noqa: BLE001 — one source failing never stops the run
            res.status, res.detail = "error", f"{type(exc).__name__}: {exc}"[:200]
            continue
        res.status, res.detail = status, detail
        if status != "ok":
            continue
        try:
            items = PARSERS[src.kind](body)[:max_items]
        except Exception as exc:  # noqa: BLE001
            res.status, res.detail = "error", f"parse failed: {type(exc).__name__}"
            continue
        res.items_seen = len(items)
        for item in items:
            if (
                src.candidate_kind != "scheme_listing"
                and item.get("title")
                and not EXCLUDE_RE.search(item["title"])
            ):
                known = catalogue.mentions(item["title"])
                if known and known.kind == "scheme":
                    # Headline about a scheme we already carry: a freshness
                    # signal for the digest, never a new candidate.
                    if _recent(item, cutoff):
                        res.known_mentions.append(
                            {"title": item["title"], "scheme_id": known.id, "url": item.get("link", "")}
                        )
                    continue
            ok, _why = is_relevant(src, item)
            if not ok:
                continue
            pub = item.get("published")
            if pub and src.candidate_kind != "scheme_listing":
                try:
                    if date.fromisoformat(pub) < cutoff:
                        res.skipped_old += 1
                        continue
                except ValueError:
                    pass
            res.relevant += 1
            cid = candidate_id(src, item)
            reason, hit = catalogue.match(cid, item["title"], [item["link"]])
            if reason:
                res.duplicates.append(
                    {"title": item["title"], "matched": hit.id if hit else "", "by": reason, "url": item["link"]}
                )
                continue
            if new_total >= max_new:
                res.detail += f"; max_new={max_new} reached"
                break
            cand = build_candidate(src, item, found_at, noted_at)
            res.new.append(cand)
            new_total += 1
            # Later sources dedupe against drafts from earlier ones too.
            catalogue.add(KnownEntry("candidate", cand["id"], [cand["name"]], [cand["source_url"]]))
    return results


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def summary_dict(results: list[SourceResult], *, dry_run: bool, today: date, written: bool) -> dict[str, Any]:
    return {
        "generated_at": datetime.now(IST).isoformat(timespec="seconds"),
        "found_at": today.isoformat(),
        "dry_run": dry_run,
        "queue_written": written,
        "new_candidates": sum(len(r.new) for r in results),
        "duplicates_skipped": sum(len(r.duplicates) for r in results),
        "known_scheme_mentions": sum(len(r.known_mentions) for r in results),
        "sources": [
            {
                "id": r.id,
                "label": r.label,
                "status": r.status,
                "detail": r.detail,
                "items_seen": r.items_seen,
                "relevant": r.relevant,
                "skipped_old": r.skipped_old,
                "new": [
                    {"id": c["id"], "name": c["name"], "country": c["country"], "source_url": c["source_url"]}
                    for c in r.new
                ],
                "duplicates": r.duplicates,
                "known_mentions": r.known_mentions,
            }
            for r in results
        ],
    }


def digest_markdown(summary: dict[str, Any]) -> str:
    mode = "DRY RUN — queue not written" if summary["dry_run"] else (
        "queue updated" if summary["queue_written"] else "no new rows"
    )
    lines = [
        f"### Candidate auto-draft — {summary['found_at']} ({mode})",
        "",
        f"- New `needs_review` candidates: **{summary['new_candidates']}**",
        f"- Duplicates skipped (id/name/URL match): {summary['duplicates_skipped']}",
        f"- Headlines about schemes already in the catalogue (check freshness): {summary['known_scheme_mentions']}",
        "",
        "| Source | Status | Seen | Relevant | New | Dupes | Known |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for s in summary["sources"]:
        lines.append(
            f"| {s['id']} | {s['status']}{(' — ' + s['detail']) if s['status'] != 'ok' else ''} | "
            f"{s['items_seen']} | {s['relevant']} | {len(s['new'])} | {len(s['duplicates'])} | "
            f"{len(s['known_mentions'])} |"
        )
    new = [(s["id"], c) for s in summary["sources"] for c in s["new"]]
    if new:
        lines += ["", "**New leads (unverified — review in `data/catalogue_candidates.json`):**"]
        for sid, c in new:
            lines.append(f"- [{sid}] {c['name']} — {c['source_url']} (`{c['id']}`)")
    known = [(s["id"], k) for s in summary["sources"] for k in s["known_mentions"]]
    if known:
        lines += ["", "**Existing schemes in the news (consider re-verifying):**"]
        for sid, k in known[:15]:
            lines.append(f"- [{sid}] `{k['scheme_id']}` ← {k['title']} — {k['url']}")
    lines += [
        "",
        "_Auto-drafts are leads only: nothing was added to schemes.json and no eligibility was inferred._",
    ]
    return "\n".join(lines) + "\n"


def write_queue(path: Path, fe_path: Path | None, data: dict[str, Any], new: list[dict[str, Any]]) -> None:
    data.setdefault("candidates", []).extend(new)
    data["updated_at"] = datetime.now(IST).isoformat(timespec="seconds")
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)
    if fe_path is not None and fe_path.parent.is_dir():
        fe_path.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", default=",".join(DEFAULT_SOURCES), help=f"Comma list from: {', '.join(SOURCES)}")
    ap.add_argument("--dry-run", action="store_true", help="Do not write the candidate queue")
    ap.add_argument("--digest", action="store_true", help="Print the markdown digest to stdout")
    ap.add_argument("--digest-md", type=Path, help="Write the markdown digest here")
    ap.add_argument("--summary-json", type=Path, help="Write the machine summary here")
    ap.add_argument("--offline-dir", type=Path, help="Read <source_id>.xml|.json fixtures instead of the network")
    ap.add_argument("--myscheme-json", type=Path, help="myScheme search-API JSON export to scan (enables myscheme)")
    ap.add_argument("--candidates", type=Path, default=CANDIDATES)
    ap.add_argument("--frontend-candidates", type=Path, default=FE_CANDIDATES)
    ap.add_argument("--schemes", type=Path, default=SCHEMES)
    ap.add_argument("--today", default="", help="Override found_at date (YYYY-MM-DD; default today IST)")
    ap.add_argument("--since-days", type=int, default=3, help="Ignore feed items older than N days (default 3)")
    ap.add_argument("--max-items", type=int, default=50, help="Max items read per source (default 50)")
    ap.add_argument("--max-new", type=int, default=20, help="Max new candidates per run (default 20)")
    ap.add_argument("--delay", type=float, default=2.0, help="Seconds between requests to one host (default 2)")
    ap.add_argument("--timeout", type=float, default=TIMEOUT_SEC)
    args = ap.parse_args(argv)

    source_ids = [s.strip() for s in args.sources.split(",") if s.strip()]
    if args.myscheme_json and "myscheme" not in source_ids:
        source_ids.append("myscheme")
    unknown = [s for s in source_ids if s not in SOURCES]
    if unknown:
        print(f"Unknown source(s): {unknown}", file=sys.stderr)
        return 2
    try:
        today = date.fromisoformat(args.today) if args.today else datetime.now(IST).date()
    except ValueError:
        print("--today must be YYYY-MM-DD", file=sys.stderr)
        return 2

    try:
        schemes = json.loads(args.schemes.read_text(encoding="utf-8"))
        if isinstance(schemes, dict):
            schemes = schemes.get("schemes") or []
    except (OSError, ValueError) as exc:
        print(f"Cannot read catalogue {args.schemes}: {exc}", file=sys.stderr)
        return 2
    if args.candidates.is_file():
        data = json.loads(args.candidates.read_text(encoding="utf-8"))
    else:
        data = {"schema_version": 1, "timezone": "Asia/Kolkata", "note": "Human-verify candidate queue.", "candidates": []}
    cands = data.get("candidates") or []

    cat = Catalogue(schemes, cands)
    fetcher = None if args.offline_dir else PoliteFetcher(delay_sec=args.delay, timeout=args.timeout)
    results = run(
        source_ids,
        cat,
        today=today,
        since_days=args.since_days,
        max_items=args.max_items,
        max_new=args.max_new,
        fetcher=fetcher,
        offline_dir=args.offline_dir,
        myscheme_json=args.myscheme_json,
    )
    new = [c for r in results for c in r.new]
    written = False
    if new and not args.dry_run:
        write_queue(args.candidates, args.frontend_candidates, data, new)
        written = True
        try:
            sys.path.insert(0, str(REPO_ROOT / "scripts"))
            from append_catalogue_audit import append_audit  # noqa: PLC0415

            if args.candidates.resolve() == CANDIDATES.resolve():
                append_audit(
                    action="note",
                    scheme_ids=[c["id"] for c in new],
                    notes=f"auto-drafted {len(new)} needs_review candidate(s) from official sources",
                    actor=ACTOR,
                    extra={"candidate_status": "needs_review"},
                )
        except Exception as exc:  # noqa: BLE001
            print(f"warning: audit append failed: {exc}", file=sys.stderr)

    summary = summary_dict(results, dry_run=args.dry_run, today=today, written=written)
    md = digest_markdown(summary)
    if args.summary_json:
        args.summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.digest_md:
        args.digest_md.write_text(md, encoding="utf-8")
    if args.digest or not (args.summary_json or args.digest_md):
        print(md, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
