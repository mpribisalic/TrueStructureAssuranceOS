"use client";

import { useRef } from "react";
import { useParams } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getTestCases, importTestCases } from "@/lib/api";
import { Badge, statusToBadgeVariant } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { LoadingPage } from "@/components/ui/LoadingSpinner";
import { Table, Thead, Th, Tbody, Tr, Td } from "@/components/ui/Table";
import { Upload } from "lucide-react";

export default function TestCasesPage() {
  const params = useParams();
  const id = params.id as string;
  const qc = useQueryClient();
  const fileRef = useRef<HTMLInputElement>(null);

  const { data: testCases, isLoading, error } = useQuery({
    queryKey: ["testCases", id],
    queryFn: () => getTestCases(id),
  });

  const importMut = useMutation({
    mutationFn: (file: File) => importTestCases(id, file),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["testCases", id] }),
  });

  return (
    <div>
      <Card>
        <CardHeader>
          <CardTitle>Test Cases</CardTitle>
          <Button size="sm" variant="secondary" onClick={() => fileRef.current?.click()} loading={importMut.isPending}>
            <Upload className="h-3.5 w-3.5" />
            Import CSV
          </Button>
          <input
            ref={fileRef}
            type="file"
            className="hidden"
            accept=".csv"
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
            Test cases imported successfully.
          </p>
        )}
        {isLoading && <LoadingPage />}
        {error && <p className="text-sm text-red-400">Failed to load test cases: {error.message}</p>}
        {testCases && (
          <Table>
            <Thead>
              <tr>
                <Th>ID</Th>
                <Th>Title</Th>
                <Th>Type</Th>
                <Th>Status</Th>
                <Th>Updated</Th>
              </tr>
            </Thead>
            <Tbody>
              {testCases.length === 0 && (
                <Tr>
                  <Td className="text-center text-slate-500" colSpan={5}>No test cases found. Import a CSV file.</Td>
                </Tr>
              )}
              {testCases.map((tc) => (
                <Tr key={tc.id}>
                  <Td className="font-mono text-xs text-slate-400">{tc.external_id}</Td>
                  <Td>
                    <span className="text-slate-200 font-medium">{tc.title}</span>
                    {tc.description && (
                      <p className="text-xs text-slate-500 mt-0.5 truncate">{tc.description}</p>
                    )}
                  </Td>
                  <Td className="capitalize">{tc.test_type}</Td>
                  <Td>
                    <Badge variant={statusToBadgeVariant(tc.status)}>{tc.status}</Badge>
                  </Td>
                  <Td className="text-xs text-slate-500">{new Date(tc.updated_at).toLocaleDateString()}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        )}
      </Card>
    </div>
  );
}
