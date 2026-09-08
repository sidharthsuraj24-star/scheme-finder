"""Pydantic request/response models for Scheme Finder API."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


StatusLiteral = Literal["likely_eligible", "uncertain", "not_eligible"]


class LocalizedText(BaseModel):
    en: str = ""
    ml: str = ""


class MatchProfile(BaseModel):
    """User profile used for deterministic matching."""

    age: int | None = None
    gender: str | None = None
    state: str = "Kerala"
    district: str | None = None
    marital_status: str | None = None
    annual_income: float | None = None
    monthly_household_income: float | None = None
    occupations: list[str] = Field(default_factory=list)
    categories: list[str] = Field(default_factory=list)
    disability: bool | None = None
    disability_percent: float | None = None
    land_ownership: bool | str | None = None
    language: str | None = None
    is_student: bool | None = None
    is_pregnant: bool | None = None
    pregnancy_order: int | None = None
    is_lactating: bool | None = None
    child_age_months: int | None = None
    housing_status: str | None = None
    residence_type: str | None = None
    income_tax_payer: bool | None = None
    kawwf_member: bool | None = None
    agri_labour_years: int | None = None
    primary_breadwinner_deceased: bool | None = None
    deceased_breadwinner_age: int | None = None
    flags: dict[str, Any] = Field(default_factory=dict)

    @field_validator("occupations", mode="before")
    @classmethod
    def _coerce_occupations(cls, v: Any) -> list[str]:
        if v is None:
            return []
        if isinstance(v, str):
            parts = [p.strip() for p in v.replace(";", ",").split(",")]
            return [p for p in parts if p]
        if isinstance(v, list):
            return [str(x) for x in v]
        return [str(v)]

    @field_validator("categories", mode="before")
    @classmethod
    def _coerce_categories(cls, v: Any) -> list[str]:
        if v is None:
            return []
        if isinstance(v, str):
            parts = [p.strip() for p in v.replace(";", ",").split(",")]
            return [p for p in parts if p]
        if isinstance(v, list):
            return [str(x) for x in v]
        return [str(v)]

    @model_validator(mode="after")
    def _derive_income_and_disability(self) -> MatchProfile:
        # Derive annual from monthly*12 when only monthly provided.
        if self.annual_income is None and self.monthly_household_income is not None:
            self.annual_income = float(self.monthly_household_income) * 12
        # Derive monthly from annual/12 when only annual provided (for monthly-cap schemes).
        if self.monthly_household_income is None and self.annual_income is not None:
            self.monthly_household_income = float(self.annual_income) / 12

        # disability bool from percent if unset
        if self.disability is None and self.disability_percent is not None:
            self.disability = float(self.disability_percent) > 0
        if self.disability is True and self.disability_percent is None:
            # unknown percent — leave percent None; matcher handles missing
            pass

        # Student occupation hint
        if self.is_student and "student" not in [o.lower() for o in self.occupations]:
            self.occupations = list(self.occupations) + ["student"]

        return self


class MatchOptions(BaseModel):
    include_verify_uncertain: bool = True
    lang: str = "en"
    max_results: int = 50


class MatchRequest(BaseModel):
    """Accepts flat profile fields OR nested {profile, options} from API_CONTRACT."""

    profile: MatchProfile | None = None
    options: MatchOptions | None = None

    # Flat aliases (Phase 2 user contract)
    age: int | None = None
    gender: str | None = None
    state: str | None = None
    district: str | None = None
    marital_status: str | None = None
    annual_income: float | None = None
    monthly_household_income: float | None = None
    occupations: list[str] | str | None = None
    categories: list[str] | str | None = None
    disability: bool | None = None
    disability_percent: float | None = None
    land_ownership: bool | str | None = None
    language: str | None = None
    is_student: bool | None = None
    is_pregnant: bool | None = None
    pregnancy_order: int | None = None
    is_lactating: bool | None = None
    child_age_months: int | None = None
    housing_status: str | None = None
    residence_type: str | None = None
    income_tax_payer: bool | None = None
    kawwf_member: bool | None = None
    agri_labour_years: int | None = None
    primary_breadwinner_deceased: bool | None = None
    deceased_breadwinner_age: int | None = None
    flags: dict[str, Any] | None = None
    lang: str | None = None

    def resolved_profile(self) -> MatchProfile:
        if self.profile is not None:
            base = self.profile.model_dump()
        else:
            base = {}
        flat_keys = [
            "age",
            "gender",
            "state",
            "district",
            "marital_status",
            "annual_income",
            "monthly_household_income",
            "occupations",
            "categories",
            "disability",
            "disability_percent",
            "land_ownership",
            "language",
            "is_student",
            "is_pregnant",
            "pregnancy_order",
            "is_lactating",
            "child_age_months",
            "housing_status",
            "residence_type",
            "income_tax_payer",
            "kawwf_member",
            "agri_labour_years",
            "primary_breadwinner_deceased",
            "deceased_breadwinner_age",
            "flags",
        ]
        for key in flat_keys:
            val = getattr(self, key)
            if val is not None:
                base[key] = val
        if "state" not in base or base.get("state") is None:
            base["state"] = "Kerala"
        return MatchProfile(**base)

    def resolved_options(self) -> MatchOptions:
        opts = self.options.model_dump() if self.options else {}
        if self.lang:
            opts["lang"] = self.lang
        if self.language and "lang" not in opts:
            opts["lang"] = self.language
        return MatchOptions(**opts)


class MatchedScheme(BaseModel):
    scheme_id: str
    score: float = 0.0
    status: StatusLiteral
    matched_rules: list[str] = Field(default_factory=list)
    unmatched_rules: list[str] = Field(default_factory=list)
    missing_profile_fields: list[str] = Field(default_factory=list)
    verify: bool = False
    verify_notes: str = ""
    explanation: LocalizedText = Field(default_factory=LocalizedText)
    scheme_name: dict[str, str] = Field(default_factory=dict)
    description: dict[str, str] | None = None
    benefits: dict[str, Any] | None = None
    documents: dict[str, Any] | None = None
    how_to_apply: dict[str, Any] | None = None
    apply_url: str | None = None
    official_source_url: str | None = None
    tags: list[str] = Field(default_factory=list)


class ExcludedScheme(BaseModel):
    scheme_id: str
    status: StatusLiteral = "not_eligible"
    reasons: list[str] = Field(default_factory=list)


class NeedsVerificationItem(BaseModel):
    scheme_id: str
    status: StatusLiteral = "uncertain"
    verify_notes: str = ""


class MatchResponse(BaseModel):
    matched: list[MatchedScheme] = Field(default_factory=list)
    excluded: list[ExcludedScheme] = Field(default_factory=list)
    needs_verification: list[NeedsVerificationItem] = Field(default_factory=list)
    message: str | None = None
    count: int = 0


class SchemeSummary(BaseModel):
    id: str
    scheme_name: dict[str, str]
    tags: list[str] = Field(default_factory=list)
    official_source_url: str | None = None
    verify: bool = False


class SchemeListResponse(BaseModel):
    count: int
    schemes: list[SchemeSummary]


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"


class ErrorBody(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorBody


class ExplainRequest(BaseModel):
    scheme_id: str
    profile: MatchProfile
    lang: str = "en"


class ExplainResponse(BaseModel):
    scheme_id: str
    explanation: LocalizedText
    disclaimer: str = (
        "Based on published eligibility rules; confirm with the implementing office. "
        "Not legal advice."
    )
    generator: Literal["template", "llm"] = "template"
