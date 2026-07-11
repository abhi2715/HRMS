"use client";

import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import {
  AlertTriangle,
  Check,
  CheckCircle2,
  ChevronRight,
  Clock,
  Eye,
  FileCheck,
  FileText,
  Search,
  Shield,
  ShieldAlert,
  ShieldCheck,
  XCircle,
} from "lucide-react";
import { useState } from "react";

const policies = [
  { id: "1", title: "Code of Conduct", category: "Ethics", version: "3.0", effective: "Jan 1, 2026", mandatory: true, acknowledged: true },
  { id: "2", title: "Anti-Harassment Policy (POSH)", category: "Legal", version: "2.1", effective: "Apr 1, 2026", mandatory: true, acknowledged: true },
  { id: "3", title: "Data Privacy & Security Policy", category: "IT", version: "1.5", effective: "Mar 1, 2026", mandatory: true, acknowledged: false },
  { id: "4", title: "Remote Work Policy", category: "HR", version: "2.0", effective: "Jan 15, 2026", mandatory: false, acknowledged: true },
  { id: "5", title: "Leave & Attendance Policy", category: "HR", version: "4.0", effective: "Jan 1, 2026", mandatory: true, acknowledged: true },
  { id: "6", title: "Expense Reimbursement Policy", category: "Finance", version: "1.2", effective: "Feb 1, 2026", mandatory: false, acknowledged: false },
  { id: "7", title: "Whistleblower Protection Policy", category: "Legal", version: "1.0", effective: "Jan 1, 2026", mandatory: true, acknowledged: true },
  { id: "8", title: "Social Media Usage Policy", category: "HR", version: "1.1", effective: "May 1, 2026", mandatory: false, acknowledged: false },
];

const violations = [
  { id: "1", employee: "Rohit Singh", type: "Late Attendance", desc: "Consistently late check-in (>15 min) for 8 days in June", severity: "medium", status: "investigating", date: "Jul 3" },
  { id: "2", employee: "Karan Chauhan", type: "Policy Violation", desc: "Used personal email for client communication", severity: "high", status: "reported", date: "Jul 5" },
  { id: "3", employee: "Pallavi Joshi", type: "Data Access", desc: "Accessed restricted HR files without authorization", severity: "critical", status: "investigating", date: "Jul 7" },
  { id: "4", employee: "Amit Kumar", type: "Expense Fraud", desc: "Duplicate expense claims detected", severity: "high", status: "resolved", date: "Jun 20" },
];

const severityColors: Record<string, string> = {
  low: "bg-blue-50 text-blue-700 dark:bg-blue-950/30 dark:text-blue-400",
  medium: "bg-amber-50 text-amber-700 dark:bg-amber-950/30 dark:text-amber-400",
  high: "bg-orange-50 text-orange-700 dark:bg-orange-950/30 dark:text-orange-400",
  critical: "bg-red-50 text-red-700 dark:bg-red-950/30 dark:text-red-400",
};
const statusColors: Record<string, string> = {
  reported: "bg-amber-50 text-amber-700 dark:bg-amber-950/30 dark:text-amber-400",
  investigating: "bg-blue-50 text-blue-700 dark:bg-blue-950/30 dark:text-blue-400",
  resolved: "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400",
};

const containerVariants = { hidden: {}, visible: { transition: { staggerChildren: 0.04 } } };
const itemVariants = { hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0, transition: { duration: 0.3 } } };

export default function CompliancePage() {
  const [activeTab, setActiveTab] = useState<"policies" | "violations" | "audit">("policies");

  const pendingAcknowledgments = policies.filter(p => p.mandatory && !p.acknowledged);

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Compliance</h1>
          <p className="text-sm text-muted-foreground mt-0.5">Policy management & violation tracking</p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Total Policies", value: policies.length, icon: FileText, color: "text-indigo-500", bg: "bg-indigo-50 dark:bg-indigo-950/30" },
          { label: "Acknowledged", value: policies.filter(p => p.acknowledged).length, icon: ShieldCheck, color: "text-emerald-500", bg: "bg-emerald-50 dark:bg-emerald-950/30" },
          { label: "Pending Action", value: pendingAcknowledgments.length, icon: Clock, color: "text-amber-500", bg: "bg-amber-50 dark:bg-amber-950/30" },
          { label: "Open Violations", value: violations.filter(v => v.status !== "resolved").length, icon: ShieldAlert, color: "text-red-500", bg: "bg-red-50 dark:bg-red-950/30" },
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

      {/* Pending Alert */}
      {pendingAcknowledgments.length > 0 && (
        <div className="rounded-xl border border-amber-200 dark:border-amber-800 bg-amber-50/50 dark:bg-amber-950/20 p-4 flex items-center gap-3">
          <AlertTriangle className="h-5 w-5 text-amber-500 shrink-0" />
          <div className="flex-1">
            <p className="text-sm font-semibold">Action Required</p>
            <p className="text-xs text-muted-foreground">
              You have {pendingAcknowledgments.length} mandatory policy acknowledgment{pendingAcknowledgments.length > 1 ? "s" : ""} pending
            </p>
          </div>
          <button className="rounded-lg bg-amber-500 text-white px-3 py-1.5 text-xs font-semibold hover:bg-amber-600">
            Review Now
          </button>
        </div>
      )}

      {/* Tabs */}
      <div className="flex items-center gap-1 border-b border-border">
        {(["policies", "violations", "audit"] as const).map((tab) => (
          <button key={tab} onClick={() => setActiveTab(tab)}
            className={cn("px-4 py-2.5 text-sm font-medium border-b-2 -mb-px capitalize transition-colors",
              activeTab === tab ? "border-primary text-primary" : "border-transparent text-muted-foreground hover:text-foreground")}>
            {tab === "audit" ? "Audit Log" : tab}
          </button>
        ))}
      </div>

      {/* Policies */}
      {activeTab === "policies" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible" className="space-y-2">
          {policies.map((policy) => (
            <motion.div key={policy.id} variants={itemVariants}
              className="flex items-center gap-4 rounded-xl border border-border bg-card p-4 hover:shadow-md transition-shadow cursor-pointer">
              <div className={cn("flex h-10 w-10 items-center justify-center rounded-xl shrink-0",
                policy.acknowledged ? "bg-emerald-50 dark:bg-emerald-950/30" : "bg-amber-50 dark:bg-amber-950/30")}>
                {policy.acknowledged ? (
                  <ShieldCheck className="h-5 w-5 text-emerald-500" />
                ) : (
                  <Shield className="h-5 w-5 text-amber-500" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-semibold truncate">{policy.title}</h3>
                  {policy.mandatory && (
                    <span className="rounded-full bg-red-50 text-red-700 dark:bg-red-950/30 dark:text-red-400 px-1.5 py-0.5 text-[9px] font-semibold shrink-0">
                      Mandatory
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-3 mt-0.5 text-xs text-muted-foreground">
                  <span>{policy.category}</span>
                  <span>v{policy.version}</span>
                  <span>Effective: {policy.effective}</span>
                </div>
              </div>
              {policy.acknowledged ? (
                <span className="flex items-center gap-1 text-xs font-semibold text-emerald-500">
                  <CheckCircle2 className="h-3.5 w-3.5" /> Acknowledged
                </span>
              ) : (
                <button className="rounded-lg bg-primary text-primary-foreground px-3 py-1.5 text-xs font-semibold hover:opacity-90">
                  Acknowledge
                </button>
              )}
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* Violations */}
      {activeTab === "violations" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible" className="space-y-3">
          {violations.map((v) => (
            <motion.div key={v.id} variants={itemVariants}
              className="rounded-xl border border-border bg-card p-5 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-sm font-semibold">{v.type}</h3>
                    <span className={cn("rounded-full px-2 py-0.5 text-[10px] font-semibold capitalize", severityColors[v.severity])}>
                      {v.severity}
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-0.5">{v.employee} • {v.date}</p>
                  <p className="text-xs text-muted-foreground mt-1">{v.desc}</p>
                </div>
                <span className={cn("rounded-full px-2.5 py-0.5 text-[10px] font-semibold capitalize", statusColors[v.status])}>
                  {v.status}
                </span>
              </div>
              {v.status !== "resolved" && (
                <div className="mt-3 flex items-center gap-2">
                  <button className="flex items-center gap-1 rounded-lg bg-blue-500 text-white px-3 py-1.5 text-xs font-semibold hover:bg-blue-600">
                    <Eye className="h-3.5 w-3.5" /> Investigate
                  </button>
                  <button className="flex items-center gap-1 rounded-lg bg-emerald-500 text-white px-3 py-1.5 text-xs font-semibold hover:bg-emerald-600">
                    <Check className="h-3.5 w-3.5" /> Resolve
                  </button>
                </div>
              )}
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* Audit Log */}
      {activeTab === "audit" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible" className="space-y-2">
          {[
            { action: "Policy Acknowledged", user: "Rahul Kumar", target: "Code of Conduct v3.0", time: "2 hours ago", icon: FileCheck },
            { action: "Violation Reported", user: "System", target: "Late Attendance - Rohit Singh", time: "5 hours ago", icon: ShieldAlert },
            { action: "Policy Updated", user: "Kavita Sharma", target: "Remote Work Policy v2.0", time: "1 day ago", icon: FileText },
            { action: "Violation Resolved", user: "Sanjay Mehta", target: "Expense Fraud - Amit Kumar", time: "2 days ago", icon: ShieldCheck },
            { action: "Policy Published", user: "Kavita Sharma", target: "Social Media Usage Policy v1.1", time: "5 days ago", icon: FileText },
          ].map((log, i) => (
            <motion.div key={i} variants={itemVariants}
              className="flex items-center gap-3 rounded-lg p-3 hover:bg-muted/50 transition-colors">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-muted shrink-0">
                <log.icon className="h-4 w-4 text-muted-foreground" />
              </div>
              <div className="flex-1">
                <p className="text-sm"><span className="font-semibold">{log.action}</span> — {log.target}</p>
                <p className="text-xs text-muted-foreground">by {log.user} • {log.time}</p>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}
    </motion.div>
  );
}
