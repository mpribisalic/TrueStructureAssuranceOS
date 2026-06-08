"use client";

import { useRouter } from "next/navigation";
import { removeToken } from "@/lib/auth";
import { ShieldCheck, LogOut } from "lucide-react";

export function TopBar() {
  const router = useRouter();

  const handleLogout = () => {
    removeToken();
    router.push("/login");
  };

  return (
    <header className="h-14 bg-slate-900 border-b border-slate-700/60 flex items-center justify-between px-6 fixed top-0 left-0 right-0 z-50">
      <div className="flex items-center gap-3">
        <ShieldCheck className="h-5 w-5 text-blue-400" />
        <span className="font-semibold text-slate-100 text-sm tracking-wide">
          TRUE STRUCTURE ASSURANCE OS
        </span>
        <span className="text-xs text-slate-500 ml-2 border border-slate-600 px-1.5 py-0.5 rounded">
          NATO DIANA TRL4
        </span>
      </div>
      <button
        onClick={handleLogout}
        className="flex items-center gap-2 text-slate-400 hover:text-slate-200 text-sm transition-colors"
      >
        <LogOut className="h-4 w-4" />
        Logout
      </button>
    </header>
  );
}
