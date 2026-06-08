"use client";

import { useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { getProject } from "@/lib/api";
import { isAuthenticated } from "@/lib/auth";
import { TopBar } from "@/components/layout/TopBar";
import { ProjectSidebar } from "@/components/layout/Sidebar";

export default function ProjectLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const params = useParams();
  const id = params.id as string;

  useEffect(() => {
    if (!isAuthenticated()) router.replace("/login");
  }, [router]);

  const { data: project } = useQuery({
    queryKey: ["project", id],
    queryFn: () => getProject(id),
    enabled: !!id && isAuthenticated(),
  });

  return (
    <div className="min-h-screen bg-slate-950">
      <TopBar />
      <ProjectSidebar projectId={id} projectName={project?.name} />
      <main className="ml-56 pt-14 p-6">{children}</main>
    </div>
  );
}
