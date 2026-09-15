"use client";

import { useEffect, useRef, useState } from "react";
import { t } from "@/lib/i18n";
import type { Lang } from "@/lib/types";

export type LifeStageKey =
  | "stage_baby"
  | "stage_child"
  | "stage_teen"
  | "stage_young_adult"
  | "stage_adult"
  | "stage_senior";

export function getLifeStage(age: number): { emoji: string; key: LifeStageKey } {
  if (age <= 2) return { emoji: "👶", key: "stage_baby" };
  if (age <= 12) return { emoji: "🧒", key: "stage_child" };
  if (age <= 17) return { emoji: "🧑", key: "stage_teen" };
  if (age <= 29) return { emoji: "🧑‍💼", key: "stage_young_adult" };
  if (age <= 59) return { emoji: "🧑", key: "stage_adult" };
  return { emoji: "🧓", key: "stage_senior" };
}

function prefersReducedMotion(): boolean {
  if (typeof window === "undefined") return false;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

interface Props {
  age: number | null;
  lang: Lang;
}

export default function AgeLifeStage({ age, lang }: Props) {
  const valid =
    age != null && Number.isFinite(age) && age >= 0 && age <= 120;

  const [displayAge, setDisplayAge] = useState(0);
  const [stagePop, setStagePop] = useState(false);
  const [popNonce, setPopNonce] = useState(0);
  const rafRef = useRef<number | null>(null);
  const stageRef = useRef<LifeStageKey | null>(null);
  const popTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (!valid || age == null) {
      stageRef.current = null;
      return;
    }

    const cancelRaf = () => {
      if (rafRef.current != null) {
        cancelAnimationFrame(rafRef.current);
        rafRef.current = null;
      }
    };

    const bumpStagePop = (key: LifeStageKey) => {
      if (stageRef.current === key) return;
      stageRef.current = key;
      setPopNonce((n) => n + 1);
      setStagePop(true);
      if (popTimerRef.current) clearTimeout(popTimerRef.current);
      popTimerRef.current = setTimeout(() => setStagePop(false), 320);
    };

    if (prefersReducedMotion()) {
      cancelRaf();
      setDisplayAge(age);
      bumpStagePop(getLifeStage(age).key);
      return;
    }

    cancelRaf();
    stageRef.current = null;

    const from = 0;
    const to = age;
    const duration = Math.min(1200, Math.max(800, 800 + to * 3));
    const start = performance.now();

    const easeOutCubic = (x: number) => 1 - Math.pow(1 - x, 3);

    const tick = (now: number) => {
      const p = Math.min(1, (now - start) / duration);
      const current = Math.round(from + (to - from) * easeOutCubic(p));
      setDisplayAge(current);
      bumpStagePop(getLifeStage(current).key);
      if (p < 1) {
        rafRef.current = requestAnimationFrame(tick);
      } else {
        rafRef.current = null;
        setDisplayAge(to);
        bumpStagePop(getLifeStage(to).key);
      }
    };

    rafRef.current = requestAnimationFrame(tick);

    return () => {
      cancelRaf();
      if (popTimerRef.current) clearTimeout(popTimerRef.current);
    };
  }, [age, valid]);

  if (!valid) return null;

  const stage = getLifeStage(displayAge);

  return (
    <div
      className="age-life-stage mt-3 flex flex-col items-center rounded-2xl border border-brand-200 bg-gradient-to-b from-brand-50 to-white px-4 py-5 shadow-sm animate-pop-in"
      aria-live="polite"
      aria-atomic="true"
    >
      <div
        key={`${stage.key}-${popNonce}`}
        className={`text-5xl leading-none ${stagePop ? "animate-stage-pop" : ""}`}
        aria-hidden
      >
        {stage.emoji}
      </div>
      <div className="mt-2 animate-number-fade text-4xl font-extrabold tabular-nums tracking-tight text-brand-900">
        {displayAge}
      </div>
      <p className="mt-1 text-sm font-semibold text-brand-800">
        {t(lang, stage.key)}
      </p>
    </div>
  );
}
