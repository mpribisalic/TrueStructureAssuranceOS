"use client";

import { useParams } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getGaps, detectGaps } from "@/lib/api";
import { Badge, statusToBadgeVariant } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { LoadingPage } from "@/components/ui/LoadingSpinner";
import { Table, Thead, Th, Tbody, Tr, Td } from "@/components/ui/Table";
import { ScanSearch } from "lucide-react";

export default function GapsPage() {
  const params = useParams();
  const id = params.id as string;
  const qc = useQueryClient();

  const { data: gaps, isLoading, error } = useQuery({
    queryKey: ["gaps", id],
    queryFn: () => getGaps(id),
  });

  const detectMut = useMutation({
    mutationFn: () => detectGaps(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["gaps", id] }),
  });

  const severityCounts = gaps?.reduce(
    (acc, g) => { acc[g.severity] = (acc[g.severity] ?? 0) + 1; return acc; },
    {} as Record<string, number>
  );

  return (
    <div className="space-y-4">
      {gaps && gaps.length > 0 && (
        <div className="grid grid-cols-4 gap-3">
          {(["critical", "high", "medium", "low"] as const).map((s) => (
            <div key={s} className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-3">
              <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">{s}</p>
              <p className="text-2xl font-bold text-slate-100">{severityCounts?.[s] ?? 0}</p>
            </div>
          ))}
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Certification Gaps</CardTitle>
          <Button size="sm" variant="secondary" onClick={() => detectMut.mutate()} loading={detectMut.isPending}>
            <ScanSearch className="h-3.5 w-3.5" />
            Detect Gaps
          </Button>
        </CardHeader>
        {detectMut.isError && (
          <p className="text-xs text-red-400 bg-red-900/20 border border-red-700/30 rounded px-3 py-2 mb-4">
            Detection failed: {detectMut.error.message}
          </p>
        )}
        {detectMut.isSuccess && (
          <p className="text-xs text-green-400 bg-green-900/20 border border-green-700/30 rounded px-3 py-2 mb-4">
            Gap detection complete.
          </p>
        )}
        {isLoading && <LoadingPage />}
        {error && <p className="text-sm text-red-400">Failed to load gaps: {error.message}</p>}
        {gaps && (
          <Table>
            <Thead>
              <tr>
                <Th>Title</Th>
                <Th>Type</Th>
                <Th>Severity</Th>
                <Th>Status</Th>
                <Th>Created</Th>
              </tr>
            </Thead>
            <Tbody>
              {gaps.length === 0 && (
                <Tr>
                  <Td className="text-center text-slate-500" colSpan={5}>No gaps detected. Run gap detection to analyse coverage.</Td>
                </Tr>
              )}
              {gaps.map((gap) => (
                <Tr key={gap.id}>
                  <Td>
                    <span className="text-slate-200 font-medium">{gap.title}</span>
                    {gap.description && (
                      <p className="text-xs text-slate-500 mt-0.5 truncate max-w-xs">{gap.description}</p>
                    )}
                  </Td>
                  <Td className="capitalize text-xs">{gap.gap_type.replace(/_/g, " ")}</Td>
                  <Td>
                    <Badge variant={statusToBadgeVariant(gap.severity)}>{gap.severity}</Badge>
                  </Td>
                  <Td>
                    <Badge variant={statusToBadgeVariant(gap.status)}>{gap.status}</Badge>
                  </Td>
                  <Td className="text-xs text-slate-500">{new Date(gap.created_at).toLocaleDateString()}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        )}
      </Card>
    </div>
  );
}
