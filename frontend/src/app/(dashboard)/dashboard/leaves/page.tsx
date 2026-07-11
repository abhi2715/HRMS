"use client";

import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import {
  Calendar,
  CalendarCheck,
  CalendarClock,
  CalendarDays,
  CalendarX,
  Check,
  ChevronDown,
  Clock,
  FileText,
  Plus,
  Sparkles,
  X,
} from "lucide-react";
import { useState } from "react";

const leaveTypes = [
  { code: "CL", name: "Casual Leave", total: 12, used: 4, pending: 1, color: "#6366f1" },
  { code: "SL", name: "Sick Leave", total: 12, used: 2, pending: 0, color: "#ef4444" },
  { code: "PL", name: "Privilege Leave", total: 15, used: 5, pending: 0, color: "#22c55e" },
  { code: "WFH", name: "Work From Home", total: 60, used: 18, pending: 2, color: "#8b5cf6" },
  { code: "CO", name: "Comp Off", total: 5, used: 1, pending: 0, color: "#f59e0b" },
  { code: "LOP", name: "Loss of Pay", total: 365, used: 0, pending: 0, color: "#94a3b8" },
];

const leaveRequests = [
  { id: "1", type: "CL", typeName: "Casual Leave", from: "Jul 15, 2026", to: "Jul 16, 2026", days: 2, reason: "Family function", status: "approved", color: "#6366f1" },
  { id: "2", type: "SL", typeName: "Sick Leave", from: "Jun 28, 2026", to: "Jun 28, 2026", days: 1, reason: "Health checkup", status: "approved", color: "#ef4444" },
  { id: "3", type: "WFH", typeName: "Work From Home", from: "Jul 10, 2026", to: "Jul 10, 2026", days: 1, reason: "Internet installation at home", status: "pending", color: "#8b5cf6" },
  { id: "4", type: "PL", typeName: "Privilege Leave", from: "Aug 1, 2026", to: "Aug 5, 2026", days: 5, reason: "Vacation - Goa trip", status: "pending", color: "#22c55e" },
  { id: "5", type: "CL", typeName: "Casual Leave", from: "May 20, 2026", to: "May 20, 2026", days: 1, reason: "Personal work", status: "rejected", color: "#6366f1" },
];

const pendingApprovals = [
  { id: "p1", employee: "Arjun Sharma", type: "Casual Leave", from: "Jul 18", to: "Jul 19", days: 2, reason: "Wedding ceremony", aiRisk: "low" },
  { id: "p2", employee: "Sneha Nair", type: "Sick Leave", from: "Jul 12", to: "Jul 14", days: 3, reason: "Dengue recovery", aiRisk: "low" },
  { id: "p3", employee: "Rohit Singh", type: "Privilege Leave", from: "Jul 21", to: "Jul 30", days: 8, reason: "International vacation", aiRisk: "medium" },
];

const holidays = [
  { name: "Independence Day", date: "Aug 15, 2026", type: "public" },
  { name: "Janmashtami", date: "Aug 25, 2026", type: "restricted" },
  { name: "Gandhi Jayanti", date: "Oct 2, 2026", type: "public" },
  { name: "Dussehra", date: "Oct 12, 2026", type: "public" },
  { name: "Diwali", date: "Oct 31, 2026", type: "public" },
];

const statusColors: Record<string, string> = {
  approved: "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400",
  pending: "bg-amber-50 text-amber-700 dark:bg-amber-950/30 dark:text-amber-400",
  rejected: "bg-red-50 text-red-700 dark:bg-red-950/30 dark:text-red-400",
};
const statusIcons: Record<string, typeof Check> = {
  approved: Check,
  pending: Clock,
  rejected: X,
};

const containerVariants = { hidden: {}, visible: { transition: { staggerChildren: 0.04 } } };
const itemVariants = { hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0, transition: { duration: 0.3 } } };

export default function LeavesPage() {
  const [activeTab, setActiveTab] = useState<"balance" | "requests" | "approvals" | "holidays">("balance");

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Leave Management</h1>
          <p className="text-sm text-muted-foreground mt-0.5">Track your leaves and approvals</p>
        </div>
        <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
          className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity">
          <Plus className="h-4 w-4" /> Apply Leave
        </motion.button>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Total Allocated", value: "44", icon: CalendarDays, color: "text-indigo-500", bg: "bg-indigo-50 dark:bg-indigo-950/30" },
          { label: "Used", value: "11", icon: CalendarCheck, color: "text-emerald-500", bg: "bg-emerald-50 dark:bg-emerald-950/30" },
          { label: "Pending", value: "3", icon: CalendarClock, color: "text-amber-500", bg: "bg-amber-50 dark:bg-amber-950/30" },
          { label: "Available", value: "30", icon: Calendar, color: "text-blue-500", bg: "bg-blue-50 dark:bg-blue-950/30" },
        ].map((s) => (
          <div key={s.label} className={cn("rounded-xl border border-border p-4", s.bg)}>
            <div className="flex items-center gap-2">
              <s.icon className={cn("h-4 w-4", s.color)} />
              <p className="text-xs text-muted-foreground">{s.label}</p>
            </div>
            <p className={cn("text-2xl font-bold mt-1", s.color)}>{s.value}</p>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-1 border-b border-border">
        {(["balance", "requests", "approvals", "holidays"] as const).map((tab) => (
          <button key={tab} onClick={() => setActiveTab(tab)}
            className={cn("px-4 py-2.5 text-sm font-medium border-b-2 -mb-px capitalize transition-colors",
              activeTab === tab ? "border-primary text-primary" : "border-transparent text-muted-foreground hover:text-foreground")}>
            {tab}
          </button>
        ))}
      </div>

      {/* Balance View */}
      {activeTab === "balance" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible"
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {leaveTypes.map((lt) => {
            const available = lt.total - lt.used - lt.pending;
            const pct = lt.total > 0 ? ((lt.used / lt.total) * 100) : 0;
            return (
              <motion.div key={lt.code} variants={itemVariants}
                className="rounded-xl border border-border bg-card p-5 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <div className="h-3 w-3 rounded-full" style={{ backgroundColor: lt.color }} />
                    <h3 className="text-sm font-semibold">{lt.name}</h3>
                  </div>
                  <span className="text-xs font-mono text-muted-foreground">{lt.code}</span>
                </div>
                <div className="grid grid-cols-3 gap-2 mb-3">
                  <div className="text-center rounded-lg bg-muted/50 p-2">
                    <p className="text-lg font-bold">{lt.total}</p>
                    <p className="text-[10px] text-muted-foreground">Total</p>
                  </div>
                  <div className="text-center rounded-lg bg-muted/50 p-2">
                    <p className="text-lg font-bold">{lt.used}</p>
                    <p className="text-[10px] text-muted-foreground">Used</p>
                  </div>
                  <div className="text-center rounded-lg bg-muted/50 p-2">
                    <p className="text-lg font-bold text-primary">{available}</p>
                    <p className="text-[10px] text-muted-foreground">Available</p>
                  </div>
                </div>
                <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
                  <motion.div initial={{ width: 0 }} animate={{ width: `${pct}%` }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    className="h-full rounded-full" style={{ backgroundColor: lt.color }} />
                </div>
                {lt.pending > 0 && (
                  <p className="text-[10px] text-amber-500 mt-2">
                    {lt.pending} day{lt.pending > 1 ? "s" : ""} pending approval
                  </p>
                )}
              </motion.div>
            );
          })}
        </motion.div>
      )}

      {/* Requests View */}
      {activeTab === "requests" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible" className="space-y-3">
          {leaveRequests.map((lr) => {
            const StatusIcon = statusIcons[lr.status];
            return (
              <motion.div key={lr.id} variants={itemVariants}
                className="flex items-center gap-4 rounded-xl border border-border bg-card p-4 hover:shadow-md transition-shadow">
                <div className="h-10 w-10 rounded-xl flex items-center justify-center shrink-0" style={{ backgroundColor: lr.color + "15" }}>
                  <FileText className="h-5 w-5" style={{ color: lr.color }} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h3 className="text-sm font-semibold">{lr.typeName}</h3>
                    <span className="text-xs text-muted-foreground">({lr.days} day{lr.days > 1 ? "s" : ""})</span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-0.5">{lr.from} — {lr.to}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">Reason: {lr.reason}</p>
                </div>
                <span className={cn("flex items-center gap-1 rounded-full px-2.5 py-1 text-[10px] font-semibold capitalize", statusColors[lr.status])}>
                  <StatusIcon className="h-3 w-3" />
                  {lr.status}
                </span>
              </motion.div>
            );
          })}
        </motion.div>
      )}

      {/* Approvals View */}
      {activeTab === "approvals" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible" className="space-y-3">
          {pendingApprovals.map((pa) => (
            <motion.div key={pa.id} variants={itemVariants}
              className="rounded-xl border border-border bg-card p-5 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-sm font-semibold">{pa.employee}</h3>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    {pa.type} • {pa.from} — {pa.to} ({pa.days} days)
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">Reason: {pa.reason}</p>
                </div>
                <div className="flex items-center gap-2">
                  <span className={cn("flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-semibold",
                    pa.aiRisk === "low" ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400" :
                    "bg-amber-50 text-amber-700 dark:bg-amber-950/30 dark:text-amber-400")}>
                    <Sparkles className="h-3 w-3" />
                    AI: {pa.aiRisk} risk
                  </span>
                </div>
              </div>
              <div className="mt-3 flex items-center gap-2">
                <button className="flex items-center gap-1 rounded-lg bg-emerald-500 text-white px-3 py-1.5 text-xs font-semibold hover:bg-emerald-600 transition-colors">
                  <Check className="h-3.5 w-3.5" /> Approve
                </button>
                <button className="flex items-center gap-1 rounded-lg bg-red-500 text-white px-3 py-1.5 text-xs font-semibold hover:bg-red-600 transition-colors">
                  <X className="h-3.5 w-3.5" /> Reject
                </button>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* Holidays View */}
      {activeTab === "holidays" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible" className="space-y-2">
          {holidays.map((h, i) => (
            <motion.div key={i} variants={itemVariants}
              className="flex items-center gap-4 rounded-xl border border-border bg-card p-4 hover:bg-muted/30 transition-colors">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 shrink-0">
                <CalendarDays className="h-5 w-5 text-primary" />
              </div>
              <div className="flex-1">
                <h3 className="text-sm font-semibold">{h.name}</h3>
                <p className="text-xs text-muted-foreground">{h.date}</p>
              </div>
              <span className={cn("rounded-full px-2.5 py-0.5 text-[10px] font-semibold uppercase",
                h.type === "public" ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400" :
                "bg-blue-50 text-blue-700 dark:bg-blue-950/30 dark:text-blue-400")}>
                {h.type}
              </span>
            </motion.div>
          ))}
        </motion.div>
      )}
    </motion.div>
  );
}
