"use client";

import { cn, formatCurrency, formatCompact } from "@/lib/utils";
import { motion } from "framer-motion";
import {
  ArrowDownRight,
  ArrowUpRight,
  BarChart3,
  Brain,
  Calendar,
  Clock,
  Download,
  Filter,
  IndianRupee,
  Sparkles,
  TrendingDown,
  TrendingUp,
  UserMinus,
  Users,
} from "lucide-react";
import {
  AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, LineChart, Line,
  ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend,
} from "recharts";

const headcountTrend = [
  { month: "Jan", count: 210, hires: 8, exits: 3 },
  { month: "Feb", count: 215, hires: 7, exits: 2 },
  { month: "Mar", count: 220, hires: 9, exits: 4 },
  { month: "Apr", count: 228, hires: 12, exits: 4 },
  { month: "May", count: 235, hires: 10, exits: 3 },
  { month: "Jun", count: 241, hires: 9, exits: 3 },
  { month: "Jul", count: 247, hires: 8, exits: 2 },
];

const attritionData = [
  { month: "Jan", rate: 4.2 }, { month: "Feb", rate: 3.8 }, { month: "Mar", rate: 4.5 },
  { month: "Apr", rate: 3.2 }, { month: "May", rate: 2.8 }, { month: "Jun", rate: 3.0 },
  { month: "Jul", rate: 2.5 },
];

const genderDistribution = [
  { name: "Male", value: 145, color: "#6366f1" },
  { name: "Female", value: 92, color: "#ec4899" },
  { name: "Other", value: 10, color: "#8b5cf6" },
];

const ageDistribution = [
  { range: "18-25", count: 32, color: "#6366f1" },
  { range: "26-30", count: 78, color: "#8b5cf6" },
  { range: "31-35", count: 65, color: "#a855f7" },
  { range: "36-40", count: 42, color: "#c084fc" },
  { range: "41-50", count: 22, color: "#ddd6fe" },
  { range: "50+", count: 8, color: "#ede9fe" },
];

const costPerDept = [
  { dept: "Engineering", cost: 3200000 },
  { dept: "Product", cost: 950000 },
  { dept: "Data Science", cost: 1100000 },
  { dept: "Sales", cost: 800000 },
  { dept: "Marketing", cost: 650000 },
  { dept: "HR", cost: 580000 },
  { dept: "Finance", cost: 420000 },
  { dept: "Design", cost: 520000 },
];

const aiPredictions = [
  { title: "Projected Attrition", value: "6 employees", risk: "medium", desc: "Expected exits in next 90 days based on engagement scores and market trends" },
  { title: "Hiring Need", value: "12 positions", risk: "info", desc: "Projected hiring requirement for Q3 based on growth plan and attrition forecast" },
  { title: "Salary Budget Impact", value: "+8.5%", risk: "warning", desc: "Expected increase in salary costs due to annual increments and new hires" },
];

const containerVariants = { hidden: {}, visible: { transition: { staggerChildren: 0.06 } } };
const itemVariants = { hidden: { opacity: 0, y: 12 }, visible: { opacity: 1, y: 0, transition: { duration: 0.4 } } };

export default function AnalyticsPage() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Analytics</h1>
          <p className="text-sm text-muted-foreground mt-0.5">Workforce insights & predictive analytics</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 rounded-lg border border-border px-3 py-2 text-sm font-medium hover:bg-muted">
            <Filter className="h-4 w-4" /> Filters
          </button>
          <button className="flex items-center gap-2 rounded-lg border border-border px-3 py-2 text-sm font-medium hover:bg-muted">
            <Download className="h-4 w-4" /> Export
          </button>
        </div>
      </div>

      {/* KPI Row */}
      <motion.div variants={containerVariants} initial="hidden" animate="visible"
        className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {[
          { label: "Total Headcount", value: "247", change: "+5.1%", trend: "up", icon: Users, color: "text-indigo-500", bg: "bg-indigo-50 dark:bg-indigo-950/30" },
          { label: "Attrition Rate", value: "2.5%", change: "-1.7%", trend: "down", icon: UserMinus, color: "text-emerald-500", bg: "bg-emerald-50 dark:bg-emerald-950/30" },
          { label: "Avg Tenure", value: "2.8 yrs", change: "+0.3", trend: "up", icon: Clock, color: "text-blue-500", bg: "bg-blue-50 dark:bg-blue-950/30" },
          { label: "Payroll Cost", value: formatCurrency(8250000), change: "+3.2%", trend: "up", icon: IndianRupee, color: "text-amber-500", bg: "bg-amber-50 dark:bg-amber-950/30" },
        ].map((kpi) => (
          <motion.div key={kpi.label} variants={itemVariants}
            className={cn("rounded-xl border border-border p-4", kpi.bg)}>
            <div className="flex items-center justify-between">
              <kpi.icon className={cn("h-4 w-4", kpi.color)} />
              <span className={cn("flex items-center gap-0.5 text-[10px] font-semibold",
                kpi.trend === "up" && kpi.label !== "Attrition Rate" ? "text-emerald-500" :
                kpi.trend === "down" && kpi.label === "Attrition Rate" ? "text-emerald-500" :
                "text-amber-500")}>
                {kpi.trend === "up" ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />}
                {kpi.change}
              </span>
            </div>
            <p className={cn("text-lg font-bold mt-2", kpi.color)}>{kpi.value}</p>
            <p className="text-xs text-muted-foreground mt-0.5">{kpi.label}</p>
          </motion.div>
        ))}
      </motion.div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div variants={itemVariants} initial="hidden" animate="visible"
          className="rounded-xl border border-border bg-card p-5">
          <h3 className="text-sm font-semibold mb-4">Headcount & Hiring Trend</h3>
          <ResponsiveContainer width="100%" height={240}>
            <AreaChart data={headcountTrend}>
              <defs>
                <linearGradient id="hcGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--color-border))" opacity={0.5} />
              <XAxis dataKey="month" tick={{ fontSize: 11 }} stroke="hsl(var(--color-muted-foreground))" />
              <YAxis tick={{ fontSize: 11 }} stroke="hsl(var(--color-muted-foreground))" />
              <Tooltip contentStyle={{ backgroundColor: "hsl(var(--color-card))", border: "1px solid hsl(var(--color-border))", borderRadius: "8px", fontSize: "12px" }} />
              <Area type="monotone" dataKey="count" stroke="#6366f1" fill="url(#hcGrad)" strokeWidth={2} />
              <Bar dataKey="hires" fill="#22c55e" radius={[2, 2, 0, 0]} barSize={6} />
              <Bar dataKey="exits" fill="#ef4444" radius={[2, 2, 0, 0]} barSize={6} />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div variants={itemVariants} initial="hidden" animate="visible"
          className="rounded-xl border border-border bg-card p-5">
          <h3 className="text-sm font-semibold mb-4">Attrition Rate Trend</h3>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={attritionData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--color-border))" opacity={0.5} />
              <XAxis dataKey="month" tick={{ fontSize: 11 }} stroke="hsl(var(--color-muted-foreground))" />
              <YAxis tick={{ fontSize: 11 }} stroke="hsl(var(--color-muted-foreground))" tickFormatter={(v) => `${v}%`} />
              <Tooltip contentStyle={{ backgroundColor: "hsl(var(--color-card))", border: "1px solid hsl(var(--color-border))", borderRadius: "8px", fontSize: "12px" }}
                formatter={(v: any) => [`${v}%`, "Attrition"]} />
              <Line type="monotone" dataKey="rate" stroke="#ef4444" strokeWidth={2} dot={{ fill: "#ef4444", r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div variants={itemVariants} initial="hidden" animate="visible"
          className="rounded-xl border border-border bg-card p-5">
          <h3 className="text-sm font-semibold mb-4">Gender Distribution</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={genderDistribution} cx="50%" cy="50%" innerRadius={50} outerRadius={75} paddingAngle={4} dataKey="value">
                {genderDistribution.map((entry, i) => <Cell key={i} fill={entry.color} />)}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: "hsl(var(--color-card))", border: "1px solid hsl(var(--color-border))", borderRadius: "8px", fontSize: "12px" }} />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex justify-center gap-4">
            {genderDistribution.map((g) => (
              <div key={g.name} className="flex items-center gap-1.5 text-xs">
                <div className="h-2 w-2 rounded-full" style={{ backgroundColor: g.color }} />
                <span className="text-muted-foreground">{g.name}: {g.value}</span>
              </div>
            ))}
          </div>
        </motion.div>

        <motion.div variants={itemVariants} initial="hidden" animate="visible"
          className="rounded-xl border border-border bg-card p-5">
          <h3 className="text-sm font-semibold mb-4">Age Distribution</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={ageDistribution}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--color-border))" opacity={0.5} />
              <XAxis dataKey="range" tick={{ fontSize: 10 }} stroke="hsl(var(--color-muted-foreground))" />
              <YAxis tick={{ fontSize: 10 }} stroke="hsl(var(--color-muted-foreground))" />
              <Tooltip contentStyle={{ backgroundColor: "hsl(var(--color-card))", border: "1px solid hsl(var(--color-border))", borderRadius: "8px", fontSize: "12px" }} />
              <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                {ageDistribution.map((entry, i) => <Cell key={i} fill={entry.color} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div variants={itemVariants} initial="hidden" animate="visible"
          className="rounded-xl border border-border bg-card p-5">
          <h3 className="text-sm font-semibold mb-4">Cost Per Department</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={costPerDept} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--color-border))" opacity={0.5} />
              <XAxis type="number" tick={{ fontSize: 10 }} stroke="hsl(var(--color-muted-foreground))"
                tickFormatter={(v) => `₹${(v / 1000000).toFixed(1)}M`} />
              <YAxis type="category" dataKey="dept" tick={{ fontSize: 10 }} stroke="hsl(var(--color-muted-foreground))" width={80} />
              <Tooltip contentStyle={{ backgroundColor: "hsl(var(--color-card))", border: "1px solid hsl(var(--color-border))", borderRadius: "8px", fontSize: "12px" }}
                formatter={(v: any) => [formatCurrency(v), "Monthly Cost"]} />
              <Bar dataKey="cost" fill="#6366f1" radius={[0, 4, 4, 0]} barSize={14} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* AI Predictions */}
      <motion.div variants={itemVariants} initial="hidden" animate="visible"
        className="rounded-xl border border-border bg-gradient-to-br from-primary/5 to-purple-500/5 p-5">
        <div className="flex items-center gap-2 mb-4">
          <Brain className="h-4 w-4 text-primary" />
          <h3 className="text-sm font-semibold">AI Predictions & Forecasts</h3>
          <span className="ml-auto flex h-5 items-center rounded-full bg-primary/10 px-2 text-[10px] font-semibold text-primary">
            <Sparkles className="h-3 w-3 mr-1" /> ML Models
          </span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {aiPredictions.map((pred) => (
            <div key={pred.title} className="rounded-lg border border-border/50 bg-background/50 p-4">
              <p className="text-lg font-bold">{pred.value}</p>
              <p className="text-xs font-semibold mt-0.5">{pred.title}</p>
              <p className="text-[11px] text-muted-foreground mt-2 leading-relaxed">{pred.desc}</p>
            </div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  );
}
