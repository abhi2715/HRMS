"use client";

import { cn, formatCurrency } from "@/lib/utils";
import { motion } from "framer-motion";
import {
  ArrowDownRight,
  ArrowUpRight,
  Banknote,
  Calculator,
  ChevronRight,
  Download,
  FileText,
  IndianRupee,
  Play,
  Receipt,
  TrendingUp,
  Wallet,
} from "lucide-react";
import { useState } from "react";
import { AreaChart, Area, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, BarChart, Bar } from "recharts";

const payrollSummary = {
  totalPayroll: 8250000, netPayout: 6980000, totalDeductions: 1270000, avgSalary: 185000,
  processed: 45, pending: 2, month: "July 2026",
};

const monthlyData = [
  { month: "Jan", payroll: 7800000, headcount: 230 },
  { month: "Feb", payroll: 7950000, headcount: 233 },
  { month: "Mar", payroll: 8100000, headcount: 236 },
  { month: "Apr", payroll: 8200000, headcount: 240 },
  { month: "May", payroll: 8150000, headcount: 242 },
  { month: "Jun", payroll: 8250000, headcount: 245 },
  { month: "Jul", payroll: 8250000, headcount: 247 },
];

const componentBreakdown = [
  { name: "Basic", amount: 3300000, pct: 40, color: "#6366f1" },
  { name: "HRA", amount: 1650000, pct: 20, color: "#8b5cf6" },
  { name: "Special", amount: 1897500, pct: 23, color: "#a855f7" },
  { name: "DA", amount: 412500, pct: 5, color: "#c084fc" },
  { name: "PF (Employer)", amount: 990000, pct: 12, color: "#ddd6fe" },
];

const recentPayslips = [
  { month: "June 2026", gross: 185000, deductions: 28500, net: 156500, status: "paid" },
  { month: "May 2026", gross: 185000, deductions: 28500, net: 156500, status: "paid" },
  { month: "April 2026", gross: 185000, deductions: 27800, net: 157200, status: "paid" },
];

const containerVariants = { hidden: {}, visible: { transition: { staggerChildren: 0.05 } } };
const itemVariants = { hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0, transition: { duration: 0.3 } } };

export default function PayrollPage() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Payroll</h1>
          <p className="text-sm text-muted-foreground mt-0.5">Salary processing & compensation management</p>
        </div>
        <div className="flex items-center gap-2">
          <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
            className="flex items-center gap-2 rounded-lg border border-border px-3 py-2 text-sm font-medium hover:bg-muted">
            <Download className="h-4 w-4" /> Export
          </motion.button>
          <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
            className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:opacity-90">
            <Play className="h-4 w-4" /> Run Payroll
          </motion.button>
        </div>
      </div>

      {/* KPI Cards */}
      <motion.div variants={containerVariants} initial="hidden" animate="visible"
        className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {[
          { label: "Total Payroll", value: formatCurrency(payrollSummary.totalPayroll), icon: IndianRupee, color: "text-indigo-500", bg: "bg-indigo-50 dark:bg-indigo-950/30", trend: "+3.2%" },
          { label: "Net Payout", value: formatCurrency(payrollSummary.netPayout), icon: Wallet, color: "text-emerald-500", bg: "bg-emerald-50 dark:bg-emerald-950/30", trend: "+2.8%" },
          { label: "Deductions", value: formatCurrency(payrollSummary.totalDeductions), icon: Calculator, color: "text-amber-500", bg: "bg-amber-50 dark:bg-amber-950/30", trend: "+1.5%" },
          { label: "Avg Salary", value: formatCurrency(payrollSummary.avgSalary), icon: Banknote, color: "text-purple-500", bg: "bg-purple-50 dark:bg-purple-950/30", trend: "+4.1%" },
        ].map((kpi) => (
          <motion.div key={kpi.label} variants={itemVariants}
            className={cn("rounded-xl border border-border p-4", kpi.bg)}>
            <div className="flex items-center justify-between">
              <kpi.icon className={cn("h-4 w-4", kpi.color)} />
              <span className="flex items-center gap-0.5 text-[10px] font-semibold text-emerald-500">
                <ArrowUpRight className="h-3 w-3" /> {kpi.trend}
              </span>
            </div>
            <p className={cn("text-lg font-bold mt-2", kpi.color)}>{kpi.value}</p>
            <p className="text-xs text-muted-foreground mt-0.5">{kpi.label}</p>
          </motion.div>
        ))}
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Payroll Trend */}
        <motion.div variants={itemVariants} initial="hidden" animate="visible"
          className="rounded-xl border border-border bg-card p-5">
          <h3 className="text-sm font-semibold mb-4">Monthly Payroll Trend</h3>
          <ResponsiveContainer width="100%" height={240}>
            <AreaChart data={monthlyData}>
              <defs>
                <linearGradient id="payrollGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--color-border))" opacity={0.5} />
              <XAxis dataKey="month" tick={{ fontSize: 11 }} stroke="hsl(var(--color-muted-foreground))" />
              <YAxis tick={{ fontSize: 11 }} stroke="hsl(var(--color-muted-foreground))"
                tickFormatter={(v) => `₹${(v / 1000000).toFixed(1)}M`} />
              <Tooltip contentStyle={{
                backgroundColor: "hsl(var(--color-card))",
                border: "1px solid hsl(var(--color-border))",
                borderRadius: "8px", fontSize: "12px",
              }} formatter={(v: any) => [formatCurrency(v), "Payroll"]} />
              <Area type="monotone" dataKey="payroll" stroke="#6366f1" fill="url(#payrollGrad)" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Component Breakdown */}
        <motion.div variants={itemVariants} initial="hidden" animate="visible"
          className="rounded-xl border border-border bg-card p-5">
          <h3 className="text-sm font-semibold mb-4">Salary Component Breakdown</h3>
          <div className="space-y-3">
            {componentBreakdown.map((comp) => (
              <div key={comp.name}>
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-2">
                    <div className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: comp.color }} />
                    <span className="text-xs font-medium">{comp.name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold">{formatCurrency(comp.amount)}</span>
                    <span className="text-[10px] text-muted-foreground">({comp.pct}%)</span>
                  </div>
                </div>
                <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
                  <motion.div initial={{ width: 0 }} animate={{ width: `${comp.pct}%` }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    className="h-full rounded-full" style={{ backgroundColor: comp.color }} />
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* My Payslips */}
      <motion.div variants={itemVariants} initial="hidden" animate="visible"
        className="rounded-xl border border-border bg-card p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold">Recent Payslips</h3>
          <button className="text-xs text-primary hover:underline">View All</button>
        </div>
        <div className="space-y-2">
          {recentPayslips.map((slip, i) => (
            <div key={i} className="flex items-center gap-4 rounded-lg p-3 hover:bg-muted/50 transition-colors">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10">
                <Receipt className="h-5 w-5 text-primary" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-semibold">{slip.month}</p>
                <p className="text-xs text-muted-foreground">
                  Gross: {formatCurrency(slip.gross)} • Deductions: {formatCurrency(slip.deductions)}
                </p>
              </div>
              <p className="text-sm font-bold text-emerald-500">{formatCurrency(slip.net)}</p>
              <span className="rounded-full bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400 px-2.5 py-0.5 text-[10px] font-semibold uppercase">
                {slip.status}
              </span>
              <button className="text-muted-foreground hover:text-primary">
                <Download className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  );
}
