"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getReports, createReport, downloadReport } from "@/lib/api";
import { Badge, statusToBadgeVariant } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { LoadingPage } from "@/components/ui/LoadingSpinner";
import { Table, Thead, Th, Tbody, Tr, Td } from "@/components/ui/Table";
import { FileText, Download, Plus } from "lucide-react";

export default function ReportsPage() {
  const params = useParams();
  const id = params.id as string;
  const qc = useQueryClient();
  const [title, setTitle] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [downloadingId, setDownloadingId] = useState<string | null>(null);

  const { data: reports, isLoading, error } = useQuery({
    queryKey: ["reports", id],
    queryFn: () => getReports(id),
  });

  const createMut = useMutation({
    mutationFn: () => createReport(id, { title }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["reports", id] });
      setTitle("");
      setShowForm(false);
    },
  });

  const handleDownload = async (reportId: string, reportTitle: string) => {
    setDownloadingId(reportId);
    try {
      const blob = await downloadReport(reportId);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${reportTitle.replace(/\s+/g, "_")}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error("Download failed", e);
    } finally {
      setDownloadingId(null);
    }
  };

  return (
    <div>
      <Card>
        <CardHeader>
          <CardTitle>Reports</CardTitle>
          <Button size="sm" variant="secondary" onClick={() => setShowForm(!showForm)}>
            <Plus className="h-3.5 w-3.5" />
            Generate Report
          </Button>
        </CardHeader>

        {showForm && (
          <div className="mb-6 p-4 bg-slate-900/50 border border-slate-700 rounded-lg">
            <p className="text-sm font-medium text-slate-300 mb-3">New Report</p>
            <div className="flex gap-2">
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="flex-1 bg-slate-900 border border-slate-600 rounded px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Report title..."
              />
              <Button
                size="sm"
                onClick={() => createMut.mutate()}
                loading={createMut.isPending}
                disabled={!title.trim()}
              >
                <FileText className="h-3.5 w-3.5" />
                Generate
              </Button>
              <Button size="sm" variant="ghost" onClick={() => setShowForm(false)}>Cancel</Button>
            </div>
            {createMut.isError && (
              <p className="text-xs text-red-400 mt-2">{createMut.error.message}</p>
            )}
          </div>
        )}

        {isLoading && <LoadingPage />}
        {error && <p className="text-sm text-red-400">Failed to load reports: {error.message}</p>}
        {reports && (
          <Table>
            <Thead>
              <tr>
                <Th>Title</Th>
                <Th>Status</Th>
                <Th>Created</Th>
                <Th>Download</Th>
              </tr>
            </Thead>
            <Tbody>
              {reports.length === 0 && (
                <Tr>
                  <Td className="text-center text-slate-500" colSpan={4}>No reports yet. Generate a report above.</Td>
                </Tr>
              )}
              {reports.map((report) => (
                <Tr key={report.id}>
                  <Td>
                    <span className="text-slate-200 font-medium">{report.title}</span>
                  </Td>
                  <Td>
                    <Badge variant={statusToBadgeVariant(report.status)}>{report.status}</Badge>
                  </Td>
                  <Td className="text-xs text-slate-500">{new Date(report.created_at).toLocaleString()}</Td>
                  <Td>
                    <Button
                      size="sm"
                      variant="ghost"
                      loading={downloadingId === report.id}
                      onClick={() => handleDownload(report.id, report.title)}
                      className="text-blue-400 hover:text-blue-300"
                    >
                      <Download className="h-3.5 w-3.5" />
                      Download
                    </Button>
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
