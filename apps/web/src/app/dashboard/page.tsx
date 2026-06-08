"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getProjects, createProject } from "@/lib/api";
import { isAuthenticated } from "@/lib/auth";
import { TopBar } from "@/components/layout/TopBar";
import { DashboardSidebar } from "@/components/layout/Sidebar";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge, statusToBadgeVariant } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { LoadingPage } from "@/components/ui/LoadingSpinner";
import { Plus, FolderOpen, ChevronRight } from "lucide-react";
import Link from "next/link";

export default function DashboardPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [showCreate, setShowCreate] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [createError, setCreateError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated()) router.replace("/login");
  }, [router]);

  const { data: projects, isLoading, error } = useQuery({
    queryKey: ["projects"],
    queryFn: getProjects,
    enabled: isAuthenticated(),
  });

  const createMutation = useMutation({
    mutationFn: () => createProject({ name, description }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
      setShowCreate(false);
      setName("");
      setDescription("");
      setCreateError(null);
    },
    onError: (err: Error) => setCreateError(err.message),
  });

  return (
    <div className="min-h-screen bg-slate-950">
      <TopBar />
      <DashboardSidebar />
      <main className="ml-56 pt-14 p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-100">Projects</h1>
            <p className="text-sm text-slate-500 mt-0.5">Mission assurance certification projects</p>
          </div>
          <Button onClick={() => setShowCreate(true)} size="sm">
            <Plus className="h-4 w-4" />
            New Project
          </Button>
        </div>

        {showCreate && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Create Project</CardTitle>
            </CardHeader>
            <div className="space-y-3">
              <div>
                <label className="block text-xs text-slate-400 mb-1">Project Name</label>
                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-600 rounded px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g. UAV Navigation System v2"
                />
              </div>
              <div>
                <label className="block text-xs text-slate-400 mb-1">Description (optional)</label>
                <input
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-600 rounded px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Brief description..."
                />
              </div>
              {createError && (
                <p className="text-xs text-red-400 bg-red-900/20 border border-red-700/40 px-3 py-2 rounded">
                  {createError}
                </p>
              )}
              <div className="flex gap-2">
                <Button
                  onClick={() => createMutation.mutate()}
                  loading={createMutation.isPending}
                  disabled={!name.trim()}
                  size="sm"
                >
                  Create
                </Button>
                <Button variant="ghost" size="sm" onClick={() => { setShowCreate(false); setCreateError(null); }}>
                  Cancel
                </Button>
              </div>
            </div>
          </Card>
        )}

        {isLoading && <LoadingPage />}
        {error && (
          <div className="bg-red-900/20 border border-red-700/40 rounded-lg px-4 py-3 text-sm text-red-400">
            Failed to load projects: {error.message}
          </div>
        )}
        {projects && projects.length === 0 && (
          <div className="text-center py-20">
            <FolderOpen className="h-12 w-12 text-slate-600 mx-auto mb-4" />
            <p className="text-slate-400 text-sm">No projects yet. Create your first project.</p>
          </div>
        )}
        {projects && projects.length > 0 && (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {projects.map((project) => (
              <Link key={project.id} href={`/projects/${project.id}/requirements`}>
                <Card className="hover:border-blue-600/40 hover:bg-slate-700/30 transition-all cursor-pointer group">
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-slate-100 truncate group-hover:text-blue-300 transition-colors">
                        {project.name}
                      </h3>
                      {project.description && (
                        <p className="text-xs text-slate-500 mt-0.5 truncate">{project.description}</p>
                      )}
                    </div>
                    <ChevronRight className="h-4 w-4 text-slate-600 group-hover:text-blue-400 flex-shrink-0 ml-2 mt-0.5" />
                  </div>
                  <div className="mt-4 flex items-center justify-between">
                    <Badge variant={statusToBadgeVariant(project.status)}>{project.status}</Badge>
                    <span className="text-xs text-slate-500">
                      {new Date(project.updated_at).toLocaleDateString()}
                    </span>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
