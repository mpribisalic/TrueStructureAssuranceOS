"use client";

import { useParams } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getReadiness, calculateReadiness } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { LoadingPage } from "@/components/ui/LoadingSpinner";
import { Calculator, ShieldCheck } from "lucide-react";
import { clsx } from "clsx";

function ScoreBar({ label, value }: { label: string; value: number }) {
  const pct = Math.round(value * 100);
  const color =
    pct >= 80 ? "bg-green-500" : pct >= 60 ? "bg-yellow-500" : pct >= 40 ? "bg-orange-500" : "bg-red-600";
  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs text-slate-400 capitalize">{label.replace(/_/g, " ")}</span>
        <span className="text-xs font-mono font-medium text-slate-200">{pct}%</span>
      </div>
      <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
        <div className={clsx("h-full rounded-full transition-all", color)} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

function OverallScore({ score }: { score: number }) {
  const pct = Math.round(score * 100);
  const color =
    pct >= 80 ? "text-green-400 border-green-500/40 bg-green-500/10"
    : pct >= 60 ? "text-yellow-400 border-yellow-500/40 bg-yellow-500/10"
    : pct >= 40 ? "text-orange-400 border-orange-500/40 bg-orange-500/10"
    : "text-red-400 border-red-600/40 bg-red-600/10";

  return (
    <div className={clsx("rounded-xl border p-8 text-center", color)}>
      <ShieldCheck className="h-10 w-10 mx-auto mb-3 opacity-80" />
      <div className="text-6xl font-bold font-mono">{pct}</div>
      <div className="text-sm mt-1 opacity-75">Overall Readiness Score</div>
    </div>
  );
}

export default function ReadinessPage() {
  const params = useParams();
  const id = params.id as string;
  const qc = useQueryClient();

  const { data: readiness, isLoading, error } = useQuery({
    queryKey: ["readiness", id],
    queryFn: () => getReadiness(id),
  });

  const calcMut = useMutation({
    mutationFn: () => calculateReadiness(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["readiness", id] }),
  });

  const subScores: Array<[string, string]> = [
    ["Coverage", "coverage_score"],
    ["Test Pass", "test_pass_score"],
    ["Evidence", "evidence_score"],
    ["Risk", "risk_score"],
    ["Freshness", "freshness_score"],
    ["Human Review", "human_review_score"],
  ];

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <Button size="sm" variant="secondary" onClick={() => calcMut.mutate()} loading={calcMut.isPending}>
          <Calculator className="h-3.5 w-3.5" />
          Calculate Readiness
        </Button>
      </div>

      {calcMut.isError && (
        <p className="text-xs text-red-400 bg-red-900/20 border border-red-700/30 rounded px-3 py-2">
          Calculation failed: {calcMut.error.message}
        </p>
      )}

      {isLoading && <LoadingPage />}
      {error && (
        <div className="text-center py-12">
          <p className="text-sm text-slate-400 mb-4">No readiness score yet.</p>
          <Button size="sm" onClick={() => calcMut.mutate()} loading={calcMut.isPending}>
            <Calculator className="h-3.5 w-3.5" />
            Calculate Now
          </Button>
        </div>
      )}

      {readiness && (
        <div className="grid gap-4 lg:grid-cols-2">
          <OverallScore score={readiness.overall_score} />

          <Card>
            <CardHeader>
              <CardTitle>Sub-scores</CardTitle>
            </CardHeader>
            <div className="space-y-4">
              {subScores.map(([label, key]) => (
                <ScoreBar
                  key={key as string}
                  label={label}
                  value={(readiness[key as keyof typeof readiness] as number) ?? 0}
                />
              ))}
            </div>
          </Card>

          {readiness.caps_applied && readiness.caps_applied.length > 0 && (
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle>Caps Applied</CardTitle>
              </CardHeader>
              <div className="flex flex-wrap gap-2">
                {readiness.caps_applied.map((cap) => (
                  <span
                    key={cap}
                    className="bg-orange-900/20 border border-orange-700/30 text-orange-400 text-xs px-3 py-1 rounded"
                  >
                    {cap}
                  </span>
                ))}
              </div>
            </Card>
          )}

          <Card className="lg:col-span-2">
            <p className="text-xs text-slate-500">
              Last calculated: {new Date(readiness.calculated_at).toLocaleString()}
            </p>
          </Card>
        </div>
      )}
    </div>
  );
}
