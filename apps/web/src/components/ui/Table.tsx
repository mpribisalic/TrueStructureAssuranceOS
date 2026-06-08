import { clsx } from "clsx";

interface TableProps {
  children?: React.ReactNode;
  className?: string;
  colSpan?: number;
}

export function Table({ children, className }: TableProps) {
  return (
    <div className={clsx("overflow-x-auto", className)}>
      <table className="w-full text-sm text-left">{children}</table>
    </div>
  );
}

export function Thead({ children }: { children: React.ReactNode }) {
  return (
    <thead className="bg-slate-900/50 border-b border-slate-700">
      {children}
    </thead>
  );
}

export function Th({ children, className }: TableProps) {
  return (
    <th
      className={clsx(
        "px-4 py-3 text-xs font-semibold uppercase tracking-wider text-slate-400",
        className
      )}
    >
      {children}
    </th>
  );
}

export function Tbody({ children }: { children: React.ReactNode }) {
  return (
    <tbody className="divide-y divide-slate-700/50">{children}</tbody>
  );
}

export function Tr({ children, className }: TableProps) {
  return (
    <tr className={clsx("hover:bg-slate-700/20 transition-colors", className)}>
      {children}
    </tr>
  );
}

export function Td({ children, className, colSpan }: TableProps) {
  return (
    <td colSpan={colSpan} className={clsx("px-4 py-3 text-slate-300", className)}>{children}</td>
  );
}
