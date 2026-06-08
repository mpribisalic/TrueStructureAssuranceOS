"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { clsx } from "clsx";
import {
  LayoutDashboard,
  FileText,
  TestTube,
  Archive,
  Link2,
  AlertTriangle,
  BarChart3,
  FileDown,
  ChevronLeft,
} from "lucide-react";

interface SidebarProps {
  projectId?: string;
  projectName?: string;
}

export function DashboardSidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-56 bg-slate-900 border-r border-slate-700/60 fixed left-0 top-14 bottom-0 flex flex-col overflow-y-auto">
      <nav className="flex-1 p-3 space-y-1">
        <NavItem href="/dashboard" icon={<LayoutDashboard className="h-4 w-4" />} active={pathname === "/dashboard"}>
          Dashboard
        </NavItem>
      </nav>
    </aside>
  );
}

export function ProjectSidebar({ projectId, projectName }: SidebarProps) {
  const pathname = usePathname();
  const base = `/projects/${projectId}`;

  const navItems = [
    { href: `${base}/requirements`, label: "Requirements", icon: <FileText className="h-4 w-4" /> },
    { href: `${base}/test-cases`, label: "Test Cases", icon: <TestTube className="h-4 w-4" /> },
    { href: `${base}/evidence`, label: "Evidence", icon: <Archive className="h-4 w-4" /> },
    { href: `${base}/trace-links`, label: "Trace Links", icon: <Link2 className="h-4 w-4" /> },
    { href: `${base}/gaps`, label: "Gaps", icon: <AlertTriangle className="h-4 w-4" /> },
    { href: `${base}/readiness`, label: "Readiness", icon: <BarChart3 className="h-4 w-4" /> },
    { href: `${base}/reports`, label: "Reports", icon: <FileDown className="h-4 w-4" /> },
  ];

  return (
    <aside className="w-56 bg-slate-900 border-r border-slate-700/60 fixed left-0 top-14 bottom-0 flex flex-col overflow-y-auto">
      <div className="p-4 border-b border-slate-700/60">
        <Link
          href="/dashboard"
          className="flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-300 mb-3 transition-colors"
        >
          <ChevronLeft className="h-3 w-3" />
          All Projects
        </Link>
        <p className="text-xs text-slate-500 uppercase tracking-wider font-medium mb-1">Project</p>
        <p className="text-sm text-slate-200 font-medium truncate">{projectName ?? "..."}</p>
      </div>
      <nav className="flex-1 p-3 space-y-1">
        {navItems.map((item) => (
          <NavItem
            key={item.href}
            href={item.href}
            icon={item.icon}
            active={pathname === item.href}
          >
            {item.label}
          </NavItem>
        ))}
      </nav>
    </aside>
  );
}

interface NavItemProps {
  href: string;
  icon: React.ReactNode;
  active: boolean;
  children: React.ReactNode;
}

function NavItem({ href, icon, active, children }: NavItemProps) {
  return (
    <Link
      href={href}
      className={clsx(
        "flex items-center gap-3 px-3 py-2 rounded text-sm transition-colors",
        active
          ? "bg-blue-600/20 text-blue-300 border border-blue-600/30"
          : "text-slate-400 hover:text-slate-200 hover:bg-slate-800"
      )}
    >
      {icon}
      {children}
    </Link>
  );
}
