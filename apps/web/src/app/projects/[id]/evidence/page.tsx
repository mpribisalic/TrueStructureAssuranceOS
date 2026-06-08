"use client";

import { useRef } from "react";
import { useParams } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getEvidence, importEvidence } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { LoadingPage } from "@/components/ui/LoadingSpinner";
import { Table, Thead, Th, Tbody, Tr, Td } from "@/components/ui/Table";
import { Upload } from "lucide-react";

export default function EvidencePage() {
  const params = useParams();
  const id = params.id as string;
  const qc = useQueryClient();
  const fileRef = useRef<HTMLInputElement>(null);

  const { data: evidence, isLoading, error } = useQuery({
    queryKey: ["evidence", id],
    queryFn: () => getEvidence(id),
  });

  const importMut = useMutation({
    mutationFn: (file: File) => importEvidence(id, file),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["evidence", id] }),
  });

  return (
    <div>
      <Card>
        <CardHeader>
          <CardTitle>Evidence</CardTitle>
          <Button size="sm" variant="secondary" onClick={() => fileRef.current?.click()} loading={importMut.isPending}>
            <Upload className="h-3.5 w-3.5" />
            Import JSON
          </Button>
          <input
            ref={fileRef}
            type="file"
            className="hidden"
            accept=".json"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) importMut.mutate(file);
            }}
          />
        </CardHeader>
        {importMut.isError && (
          <p className="text-xs text-red-400 bg-red-900/20 border border-red-700/30 rounded px-3 py-2 mb-4">
            Import failed: {importMut.error.message}
          </p>
        )}
        {importMut.isSuccess && (
          <p className="text-xs text-green-400 bg-green-900/20 border border-green-700/30 rounded px-3 py-2 mb-4">
            Evidence imported successfully.
          </p>
        )}
        {isLoading && <LoadingPage />}
        {error && <p className="text-sm text-red-400">Failed to load evidence: {error.message}</p>}
        {evidence && (
          <Table>
            <Thead>
              <tr>
                <Th>Title</Th>
                <Th>Source</Th>
                <Th>Type</Th>
                <Th>Created</Th>
              </tr>
            </Thead>
            <Tbody>
              {evidence.length === 0 && (
                <Tr>
                  <Td className="text-center text-slate-500" colSpan={4}>No evidence items found. Import a JSON file.</Td>
                </Tr>
              )}
              {evidence.map((ev) => (
                <Tr key={ev.id}>
                  <Td>
                    <span className="text-slate-200 font-medium">{ev.title}</span>
                    {ev.description && (
                      <p className="text-xs text-slate-500 mt-0.5 truncate">{ev.description}</p>
                    )}
                  </Td>
                  <Td className="text-xs font-mono text-slate-400">{ev.source}</Td>
                  <Td className="capitalize">{ev.evidence_type ?? "—"}</Td>
                  <Td className="text-xs text-slate-500">{new Date(ev.created_at).toLocaleDateString()}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        )}
      </Card>
    </div>
  );
}
