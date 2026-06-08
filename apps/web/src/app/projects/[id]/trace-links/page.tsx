"use client";

import { useParams } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getTraceLinks, suggestTraceLinks, approveTraceLink } from "@/lib/api";
import { Badge, statusToBadgeVariant } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { LoadingPage } from "@/components/ui/LoadingSpinner";
import { Table, Thead, Th, Tbody, Tr, Td } from "@/components/ui/Table";
import { Sparkles, CheckCircle } from "lucide-react";

export default function TraceLinksPage() {
  const params = useParams();
  const id = params.id as string;
  const qc = useQueryClient();

  const { data: links, isLoading, error } = useQuery({
    queryKey: ["traceLinks", id],
    queryFn: () => getTraceLinks(id),
  });

  const suggestMut = useMutation({
    mutationFn: () => suggestTraceLinks(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["traceLinks", id] }),
  });

  const approveMut = useMutation({
    mutationFn: approveTraceLink,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["traceLinks", id] }),
  });

  return (
    <div>
      <Card>
        <CardHeader>
          <CardTitle>Trace Links</CardTitle>
          <Button size="sm" variant="secondary" onClick={() => suggestMut.mutate()} loading={suggestMut.isPending}>
            <Sparkles className="h-3.5 w-3.5" />
            AI Suggest Links
          </Button>
        </CardHeader>
        {suggestMut.isError && (
          <p className="text-xs text-red-400 bg-red-900/20 border border-red-700/30 rounded px-3 py-2 mb-4">
            Suggestion failed: {suggestMut.error.message}
          </p>
        )}
        {suggestMut.isSuccess && (
          <p className="text-xs text-green-400 bg-green-900/20 border border-green-700/30 rounded px-3 py-2 mb-4">
            AI suggestions generated.
          </p>
        )}
        {isLoading && <LoadingPage />}
        {error && <p className="text-sm text-red-400">Failed to load trace links: {error.message}</p>}
        {links && (
          <Table>
            <Thead>
              <tr>
                <Th>Requirement</Th>
                <Th>Test Case</Th>
                <Th>Confidence</Th>
                <Th>Status</Th>
                <Th>Actions</Th>
              </tr>
            </Thead>
            <Tbody>
              {links.length === 0 && (
                <Tr>
                  <Td className="text-center text-slate-500" colSpan={5}>No trace links yet. Use AI Suggest to generate links.</Td>
                </Tr>
              )}
              {links.map((link) => (
                <Tr key={link.id}>
                  <Td>
                    {link.requirement ? (
                      <div>
                        <span className="text-xs font-mono text-slate-400">{link.requirement.external_id}</span>
                        <p className="text-sm text-slate-200 truncate max-w-xs">{link.requirement.title}</p>
                      </div>
                    ) : (
                      <span className="font-mono text-xs text-slate-400">{link.requirement_id}</span>
                    )}
                  </Td>
                  <Td>
                    {link.test_case ? (
                      <div>
                        <span className="text-xs font-mono text-slate-400">{link.test_case.external_id}</span>
                        <p className="text-sm text-slate-200 truncate max-w-xs">{link.test_case.title}</p>
                      </div>
                    ) : (
                      <span className="font-mono text-xs text-slate-400">{link.test_case_id}</span>
                    )}
                  </Td>
                  <Td>
                    {link.confidence_score != null ? (
                      <span className="text-sm font-mono">
                        {(link.confidence_score * 100).toFixed(0)}%
                      </span>
                    ) : "—"}
                  </Td>
                  <Td>
                    <Badge variant={statusToBadgeVariant(link.status)}>{link.status}</Badge>
                  </Td>
                  <Td>
                    {link.status === "pending" && (
                      <Button
                        size="sm"
                        variant="ghost"
                        loading={approveMut.isPending && approveMut.variables === link.id}
                        onClick={() => approveMut.mutate(link.id)}
                        className="text-green-400 hover:text-green-300 hover:bg-green-900/20"
                      >
                        <CheckCircle className="h-3.5 w-3.5" />
                        Approve
                      </Button>
                    )}
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        )}
      </Card>
    </div>
  );
}
