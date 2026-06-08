"use client";

import { clsx } from "clsx";

type BadgeVariant =
  | "critical"
  | "high"
  | "medium"
  | "low"
  | "passed"
  | "failed"
  | "pending"
  | "approved"
  | "rejected"
  | "open"
  | "resolved"
  | "accepted"
  | "default";

interface BadgeProps {
  variant?: BadgeVariant;
  children: React.ReactNode;
  className?: string;
}

const variantClasses: Record<BadgeVariant, string> = {
  critical: "bg-red-600/20 text-red-400 border border-red-600/40",
  high: "bg-orange-500/20 text-orange-400 border border-orange-500/40",
  medium: "bg-yellow-500/20 text-yellow-400 border border-yellow-500/40",
  low: "bg-gray-500/20 text-gray-400 border border-gray-500/40",
  passed: "bg-green-500/20 text-green-400 border border-green-500/40",
  failed: "bg-red-600/20 text-red-400 border border-red-600/40",
  pending: "bg-yellow-500/20 text-yellow-400 border border-yellow-500/40",
  approved: "bg-green-500/20 text-green-400 border border-green-500/40",
  rejected: "bg-red-600/20 text-red-400 border border-red-600/40",
  open: "bg-blue-500/20 text-blue-400 border border-blue-500/40",
  resolved: "bg-green-500/20 text-green-400 border border-green-500/40",
  accepted: "bg-gray-500/20 text-gray-400 border border-gray-500/40",
  default: "bg-slate-700/50 text-slate-300 border border-slate-600/40",
};

export function Badge({ variant = "default", children, className }: BadgeProps) {
  return (
    <span
      className={clsx(
        "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium uppercase tracking-wider",
        variantClasses[variant],
        className
      )}
    >
      {children}
    </span>
  );
}

export function statusToBadgeVariant(status: string): BadgeVariant {
  const map: Record<string, BadgeVariant> = {
    pending: "pending",
    approved: "approved",
    rejected: "rejected",
    passed: "passed",
    failed: "failed",
    open: "open",
    resolved: "resolved",
    accepted: "accepted",
    critical: "critical",
    high: "high",
    medium: "medium",
    low: "low",
  };
  return map[status?.toLowerCase()] ?? "default";
}
