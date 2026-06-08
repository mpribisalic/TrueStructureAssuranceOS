"use client";

import { useRef, useState } from "react";
import { useParams } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getRequirements,
  approveRequirement,
  rejectRequirement,
  uploadDocument,
  extractRequirements,
} from "@/lib/api";
import { Badge, statusToBadgeVariant } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { LoadingPage } from "@/components/ui/LoadingSpinner";
import { Table, Thead, Th, Tbody, Tr, Td } from "@/components/ui/Table";
import { Upload, Cpu, CheckCircle, XCircle } from "lucide-react";

export default function RequirementsPage() {
  const params = useParams();
  const id = params.id as string;
  const qc = useQueryClient();
  const fileRef = useRef<HTMLInputElement>(null);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const [lastDocId, setLastDocId] = useState<string | null>(null);

  const { data: reqs, isLoading, error } = useQuery({
    queryKey: ["requirements", id],
    queryFn: () => getRequirements(id),
  });

  const approveMut = useMutation({
    mutationFn: approveRequirement,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["requirements", id] }),
  });

  const rejectMut = useMutation({
    mutationFn: rejectRequirement,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["requirements", id] }),
  });

  const uploadMut = useMutation({
    mutationFn: (file: File) => uploadDocument(id, file),
    onSuccess: (doc) => {
      setLastDocId(doc.id);
      setUploadStatus(`Uploaded: ${doc.filename}`);
    },
    onError: (e: Error) => setUploadStatus(`Upload failed: ${e.message}`),
  });

  const extractMut = useMutation({
    mutationFn: () => extractRequirements(lastDocId!),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["requirements", id] });
      setUploadStatus("Requirements extracted successfully.");
    },
    onError: (e: Error) => setUploadStatus(`Extract failed: ${e.message}`),
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) uploadMut.mutate(file);
  };

  return (
    <div>
      <Card>
        <CardHeader>
          <CardTitle>Requirements</CardTitle>
          <div className="flex gap-2">
            <Button size="sm" variant="secondary" onClick={() => fileRef.current?.click()} loading={uploadMut.isPending}>
              <Upload className="h-3.5 w-3.5" />
              Upload Document
            </Button>
            <input ref={fileRef} type="file" className="hidden" onChange={handleFileChange} accept=".pdf,.docx,.txt" />
            {lastDocId && (
              <Button size="sm" variant="secondary" onClick={() => extractMut.mutate()} loading={extractMut.isPending}>
                <Cpu className="h-3.5 w-3.5" />
                Extract Requirements
              </Button>
            )}
          </div>
        </CardHeader>
        {uploadStatus && (
          <p className="text-xs text-blue-400 bg-blue-900/20 border border-blue-700/30 rounded px-3 py-2 mb-4">
            {uploadStatus}
          </p>
        )}
        {isLoading && <LoadingPage />}
        {error && <p className="text-sm text-red-400">Failed to load requirements: {error.message}</p>}
        {reqs && (
          <Table>
            <Thead>
              <tr>
                <Th>ID</Th>
                <Th>Title</Th>
                <Th>Category</Th>
                <Th>Criticality</Th>
                <Th>Status</Th>
                <Th>Actions</Th>
              </tr>
            </Thead>
            <Tbody>
              {reqs.length === 0 && (
                <Tr>
                  <Td className="text-center text-slate-500" colSpan={6}>No requirements found.</Td>
                </Tr>
              )}
              {reqs.map((req) => (
                <Tr key={req.id}>
                  <Td className="font-mono text-xs text-slate-400">{req.external_id}</Td>
                  <Td className="max-w-xs">
                    <span className="text-slate-200 font-medium">{req.title}</span>
                    {req.description && (
                      <p className="text-xs text-slate-500 mt-0.5 truncate">{req.description}</p>
                    )}
                  </Td>
                  <Td>{req.category ?? "—"}</Td>
                  <Td>
                    <Badge variant={statusToBadgeVariant(req.criticality)}>{req.criticality}</Badge>
                  </Td>
                  <Td>
                    <Badge variant={statusToBadgeVariant(req.status)}>{req.status}</Badge>
                  </Td>
                  <Td>
                    {req.status === "pending" && (
                      <div className="flex gap-1.5">
                        <Button
                          size="sm"
                          variant="ghost"
                          loading={approveMut.isPending && approveMut.variables === req.id}
                          onClick={() => approveMut.mutate(req.id)}
                          className="text-green-400 hover:text-green-300 hover:bg-green-900/20"
                        >
                          <CheckCircle className="h-3.5 w-3.5" />
                          Approve
                        </Button>
                        <Button
                          size="sm"
                          variant="ghost"
                          loading={rejectMut.isPending && rejectMut.variables === req.id}
                          onClick={() => rejectMut.mutate(req.id)}
                          className="text-red-400 hover:text-red-300 hover:bg-red-900/20"
                        >
                          <XCircle className="h-3.5 w-3.5" />
                          Reject
                        </Button>
                      </div>
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
