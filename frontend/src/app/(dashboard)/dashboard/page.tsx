"use client";

import { useEffect, useState } from "react";
import { cn, formatCurrency, formatCompact, getInitials, stringToColor } from "@/lib/utils";
import { motion } from "framer-motion";
import {
  ArrowDownRight,
  ArrowUpRight,
  Brain,
  Briefcase,
  Calendar,
  Clock,
  Gift,
  Sparkles,
  Target,
  TrendingUp,
  UserCheck,
  UserMinus,
  UserPlus,
  Users,
  Wallet,
} from "lucide-react";
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

// ── KPI Data ──────────────────────────────────────────────────
const kpiCards = [
  {
    title: "Total Employees",
    value: "247",
    change: "+12",
    changePercent: "+5.1%",
    trend: "up" as const,
    icon: Users,
    color: "from-indigo-500 to-purple-600",
    bgLight: "bg-indigo-50 dark:bg-indigo-950/30",
    textColor: "text-indigo-600 dark:text-indigo-400",
  },
  {
    title: "Present Today",
    value: "218",
    change: "+3",
    changePercent: "88.3%",
    trend: "up" as const,
    icon: UserCheck,
    color: "from-emerald-500 to-teal-600",
    bgLight: "bg-emerald-50 dark:bg-emerald-950/30",
    textColor: "text-emerald-600 dark:text-emerald-400",
  },
  {
    title: "Open Positions",
    value: "14",
    change: "+4",
    changePercent: "+40%",
    trend: "up" as const,
    icon: Briefcase,
    color: "from-amber-500 to-orange-600",
    bgLight: "bg-amber-50 dark:bg-amber-950/30",
    textColor: "text-amber-600 dark:text-amber-400",
  },
  {
    title: "Pending Leaves",
    value: "8",
    change: "-2",
    changePercent: "-20%",
    trend: "down" as const,
    icon: Calendar,
    color: "from-rose-500 to-pink-600",
    bgLight: "bg-rose-50 dark:bg-rose-950/30",
    textColor: "text-rose-600 dark:text-rose-400",
  },
];

// ── Chart Data ────────────────────────────────────────────────
const employeeGrowthData = [
  { month: "Jan", count: 210, hires: 8, exits: 3 },
  { month: "Feb", count: 215, hires: 7, exits: 2 },
  { month: "Mar", count: 220, hires: 9, exits: 4 },
  { month: "Apr", count: 228, hires: 12, exits: 4 },
  { month: "May", count: 235, hires: 10, exits: 3 },
  { month: "Jun", count: 241, hires: 9, exits: 3 },
  { month: "Jul", count: 247, hires: 8, exits: 2 },
];

const departmentData = [
  { name: "Engineering", value: 82, color: "#6366f1" },
  { name: "Product", value: 24, color: "#8b5cf6" },
  { name: "Design", value: 18, color: "#ec4899" },
  { name: "Marketing", value: 22, color: "#f97316" },
  { name: "Sales", value: 35, color: "#22c55e" },
  { name: "HR", value: 15, color: "#06b6d4" },
  { name: "Finance", value: 12, color: "#eab308" },
  { name: "Data Science", value: 20, color: "#a855f7" },
  { name: "QA", value: 10, color: "#14b8a6" },
  { name: "Operations", value: 9, color: "#64748b" },
];

const attendanceWeekData = [
  { day: "Mon", present: 220, absent: 12, leave: 15 },
  { day: "Tue", present: 225, absent: 10, leave: 12 },
  { day: "Wed", present: 218, absent: 14, leave: 15 },
  { day: "Thu", present: 222, absent: 11, leave: 14 },
  { day: "Fri", present: 210, absent: 15, leave: 22 },
];

const leaveStats = [
  { type: "Casual Leave", used: 45, total: 120, color: "#6366f1" },
  { type: "Sick Leave", used: 28, total: 120, color: "#ef4444" },
  { type: "Privilege Leave", used: 32, total: 150, color: "#22c55e" },
  { type: "WFH", used: 180, total: 600, color: "#8b5cf6" },
];

const recentHires = [
  { name: "Arjun Sharma", role: "Senior Engineer", dept: "Engineering", date: "Jul 1, 2026" },
  { name: "Priya Patel", role: "Product Manager", dept: "Product", date: "Jun 28, 2026" },
  { name: "Deepak Verma", role: "ML Engineer", dept: "Data Science", date: "Jun 25, 2026" },
  { name: "Sneha Nair", role: "UX Designer", dept: "Design", date: "Jun 22, 2026" },
  { name: "Rohit Singh", role: "DevOps Engineer", dept: "Engineering", date: "Jun 20, 2026" },
];

const upcomingBirthdays = [
  { name: "Kavita Mehta", date: "Jul 12", dept: "HR" },
  { name: "Amit Gupta", date: "Jul 14", dept: "Engineering" },
  { name: "Swati Reddy", date: "Jul 15", dept: "Marketing" },
  { name: "Rahul Joshi", date: "Jul 18", dept: "Finance" },
];

const aiInsights = [
  {
    type: "warning",
    title: "Attrition Risk Detected",
    desc: "3 employees in Engineering show high attrition risk based on engagement patterns.",
    action: "Review Details",
  },
  {
    type: "info",
    title: "Payroll Anomaly",
    desc: "Overtime costs increased 23% in June. Top contributors: QA team.",
    action: "Analyze",
  },
  {
    type: "success",
    title: "Hiring Pipeline Healthy",
    desc: "14 positions filled this quarter, 28% faster than Q1.",
    action: "View Pipeline",
  },
];

const containerVariants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.06 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 16 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.25, 0.1, 0.25, 1] as const } },
};

export default function DashboardPage() {
  const [summaryData, setSummaryData] = useState<{
    kpis: {
      totalEmployees: number;
      presentToday: number;
      pendingLeaves: number;
      openPositions: number;
    };
    departmentDistribution: { name: string; value: number }[];
    recentHires: { name: string; date: string; dept: string; role: string }[];
  } | null>(null);
  
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/dashboard/summary`);
        if (response.ok) {
          const data = await response.json();
          setSummaryData(data);
        }
      } catch (error) {
        console.error("Failed to fetch dashboard summary", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchSummary();
  }, []);

  // Update KPI cards with real data if available
  const dynamicKpiCards = kpiCards.map(card => {
    if (card.title === "Total Employees" && summaryData) {
      return { ...card, value: summaryData.kpis.totalEmployees.toString() };
    }
    if (card.title === "Present Today" && summaryData) {
      return { ...card, value: summaryData.kpis.presentToday.toString() };
    }
    if (card.title === "Pending Leaves" && summaryData) {
      return { ...card, value: summaryData.kpis.pendingLeaves.toString() };
    }
    if (card.title === "Open Positions" && summaryData) {
      return { ...card, value: summaryData.kpis.openPositions.toString() };
    }
    return card;
  });

  const dynamicDeptData = summaryData ? summaryData.departmentDistribution.map((d, i) => ({
    ...d,
    color: departmentData[i % departmentData.length].color
  })) : departmentData;

  const dynamicHires = summaryData && summaryData.recentHires.length > 0 ? summaryData.recentHires : recentHires;

  if (isLoading) {
    return <div className="flex h-full items-center justify-center p-12">
      <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
    </div>;
  }

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      {/* Page Header */}
      <motion.div variants={itemVariants} className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            Welcome back! Here&apos;s your HR overview for today.
          </p>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Clock className="h-4 w-4" />
          {new Date().toLocaleDateString("en-IN", {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric",
          })}
        </div>
      </motion.div>

      {/* KPI Cards */}
      <motion.div variants={itemVariants} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {dynamicKpiCards.map((kpi, i) => (
          <motion.div
            key={kpi.title}
            whileHover={{ y: -2, transition: { duration: 0.2 } }}
            className="group relative overflow-hidden rounded-xl border border-border bg-card p-5 transition-shadow hover:shadow-lg"
          >
            {/* Gradient accent */}
            <div className={cn("absolute top-0 left-0 right-0 h-1 bg-gradient-to-r", kpi.color)} />

            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                  {kpi.title}
                </p>
                <p className="mt-2 text-3xl font-bold tracking-tight">{kpi.value}</p>
                <div className="mt-1.5 flex items-center gap-1">
                  {kpi.trend === "up" ? (
                    <ArrowUpRight className="h-3.5 w-3.5 text-emerald-500" />
                  ) : (
                    <ArrowDownRight className="h-3.5 w-3.5 text-rose-500" />
                  )}
                  <span
                    className={cn(
                      "text-xs font-medium",
                      kpi.trend === "up" ? "text-emerald-500" : "text-rose-500"
                    )}
                  >
                    {kpi.changePercent}
                  </span>
                  <span className="text-xs text-muted-foreground">vs last month</span>
                </div>
              </div>
              <div className={cn("flex h-11 w-11 items-center justify-center rounded-xl", kpi.bgLight)}>
                <kpi.icon className={cn("h-5 w-5", kpi.textColor)} />
              </div>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Employee Growth Chart */}
        <motion.div
          variants={itemVariants}
          className="lg:col-span-2 rounded-xl border border-border bg-card p-5"
        >
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold">Employee Growth</h3>
              <p className="text-xs text-muted-foreground mt-0.5">Headcount trend this year</p>
            </div>
            <div className="flex items-center gap-4 text-xs">
              <div className="flex items-center gap-1.5">
                <div className="h-2 w-2 rounded-full bg-indigo-500" />
                <span className="text-muted-foreground">Headcount</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="h-2 w-2 rounded-full bg-emerald-500" />
                <span className="text-muted-foreground">Hires</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="h-2 w-2 rounded-full bg-rose-500" />
                <span className="text-muted-foreground">Exits</span>
              </div>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={employeeGrowthData}>
              <defs>
                <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--color-border))" opacity={0.5} />
              <XAxis dataKey="month" tick={{ fontSize: 12 }} stroke="hsl(var(--color-muted-foreground))" />
              <YAxis tick={{ fontSize: 12 }} stroke="hsl(var(--color-muted-foreground))" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--color-card))",
                  border: "1px solid hsl(var(--color-border))",
                  borderRadius: "8px",
                  fontSize: "12px",
                }}
              />
              <Area
                type="monotone"
                dataKey="count"
                stroke="#6366f1"
                fill="url(#colorCount)"
                strokeWidth={2}
              />
              <Bar dataKey="hires" fill="#22c55e" radius={[2, 2, 0, 0]} barSize={6} />
              <Bar dataKey="exits" fill="#ef4444" radius={[2, 2, 0, 0]} barSize={6} />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Department Distribution */}
        <motion.div
          variants={itemVariants}
          className="rounded-xl border border-border bg-card p-5"
        >
          <h3 className="text-sm font-semibold mb-4">Department Distribution</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={dynamicDeptData}
                cx="50%"
                cy="50%"
                innerRadius={55}
                outerRadius={80}
                paddingAngle={3}
                dataKey="value"
              >
                {dynamicDeptData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--color-card))",
                  border: "1px solid hsl(var(--color-border))",
                  borderRadius: "8px",
                  fontSize: "12px",
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-2 grid grid-cols-2 gap-1.5">
            {dynamicDeptData.slice(0, 6).map((dept) => (
              <div key={dept.name} className="flex items-center gap-1.5 text-xs">
                <div
                  className="h-2 w-2 rounded-full shrink-0"
                  style={{ backgroundColor: dept.color }}
                />
                <span className="text-muted-foreground truncate">{dept.name}</span>
                <span className="font-medium ml-auto">{dept.value}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Second Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Weekly Attendance */}
        <motion.div variants={itemVariants} className="rounded-xl border border-border bg-card p-5">
          <h3 className="text-sm font-semibold mb-4">This Week&apos;s Attendance</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={attendanceWeekData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--color-border))" opacity={0.5} />
              <XAxis dataKey="day" tick={{ fontSize: 11 }} stroke="hsl(var(--color-muted-foreground))" />
              <YAxis tick={{ fontSize: 11 }} stroke="hsl(var(--color-muted-foreground))" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--color-card))",
                  border: "1px solid hsl(var(--color-border))",
                  borderRadius: "8px",
                  fontSize: "12px",
                }}
              />
              <Bar dataKey="present" fill="#22c55e" radius={[3, 3, 0, 0]} barSize={16} />
              <Bar dataKey="absent" fill="#ef4444" radius={[3, 3, 0, 0]} barSize={16} />
              <Bar dataKey="leave" fill="#f59e0b" radius={[3, 3, 0, 0]} barSize={16} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Leave Stats */}
        <motion.div variants={itemVariants} className="rounded-xl border border-border bg-card p-5">
          <h3 className="text-sm font-semibold mb-4">Leave Utilization</h3>
          <div className="space-y-4">
            {leaveStats.map((stat) => (
              <div key={stat.type}>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs text-muted-foreground">{stat.type}</span>
                  <span className="text-xs font-medium">
                    {stat.used}/{stat.total}
                  </span>
                </div>
                <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${(stat.used / stat.total) * 100}%` }}
                    transition={{ duration: 0.8, ease: "easeOut", delay: 0.3 }}
                    className="h-full rounded-full"
                    style={{ backgroundColor: stat.color }}
                  />
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* AI Insights */}
        <motion.div
          variants={itemVariants}
          className="rounded-xl border border-border bg-card p-5 relative overflow-hidden"
        >
          {/* Subtle gradient bg */}
          <div className="absolute inset-0 bg-gradient-to-br from-primary/3 to-transparent pointer-events-none" />

          <div className="relative">
            <div className="flex items-center gap-2 mb-4">
              <div className="flex h-6 w-6 items-center justify-center rounded-md bg-primary/10">
                <Brain className="h-3.5 w-3.5 text-primary" />
              </div>
              <h3 className="text-sm font-semibold">AI Insights</h3>
              <span className="ml-auto flex h-5 items-center rounded-full bg-primary/10 px-2 text-[10px] font-semibold text-primary">
                <Sparkles className="h-3 w-3 mr-1" />
                Live
              </span>
            </div>
            <div className="space-y-3">
              {aiInsights.map((insight, i) => (
                <div
                  key={i}
                  className="rounded-lg border border-border/50 bg-background/50 p-3 hover:bg-muted/30 transition-colors cursor-pointer"
                >
                  <div className="flex items-start gap-2">
                    <div
                      className={cn(
                        "mt-0.5 h-1.5 w-1.5 rounded-full shrink-0",
                        insight.type === "warning" && "bg-warning",
                        insight.type === "info" && "bg-info",
                        insight.type === "success" && "bg-success"
                      )}
                    />
                    <div>
                      <p className="text-xs font-medium">{insight.title}</p>
                      <p className="text-[11px] text-muted-foreground mt-0.5 leading-relaxed">
                        {insight.desc}
                      </p>
                      <button className="mt-1.5 text-[11px] font-medium text-primary hover:underline">
                        {insight.action} →
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>

      {/* Third Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Hires */}
        <motion.div variants={itemVariants} className="rounded-xl border border-border bg-card p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold">Recent Hires</h3>
            <button className="text-xs text-primary hover:underline">View all</button>
          </div>
          <div className="space-y-4">
            {dynamicHires.map((hire, i) => (
              <motion.div
                key={i}
                className="flex items-center gap-3 rounded-lg p-2 hover:bg-muted/50 transition-colors"
              >
                <div
                  className={cn(
                    "flex h-9 w-9 items-center justify-center rounded-full text-white text-xs font-bold",
                    stringToColor(hire.name)
                  )}
                >
                  {getInitials(hire.name)}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{hire.name}</p>
                  <p className="text-xs text-muted-foreground">
                    {hire.role} • {hire.dept}
                  </p>
                </div>
                <div className="text-xs text-muted-foreground whitespace-nowrap">{hire.date}</div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Upcoming Birthdays */}
        <motion.div variants={itemVariants} className="rounded-xl border border-border bg-card p-5">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Gift className="h-4 w-4 text-pink-500" />
              <h3 className="text-sm font-semibold">Upcoming Birthdays</h3>
            </div>
          </div>
          <div className="space-y-3">
            {upcomingBirthdays.map((birthday, i) => (
              <div
                key={i}
                className="flex items-center gap-3 rounded-lg p-2 hover:bg-muted/50 transition-colors"
              >
                <div
                  className={cn(
                    "flex h-9 w-9 items-center justify-center rounded-full text-white text-xs font-bold",
                    stringToColor(birthday.name)
                  )}
                >
                  {getInitials(birthday.name)}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{birthday.name}</p>
                  <p className="text-xs text-muted-foreground">{birthday.dept}</p>
                </div>
                <div className="flex items-center gap-1.5 rounded-full bg-pink-50 dark:bg-pink-950/30 px-2.5 py-1 text-xs font-medium text-pink-600 dark:text-pink-400">
                  <Gift className="h-3 w-3" />
                  {birthday.date}
                </div>
              </div>
            ))}
          </div>

          {/* Quick Actions */}
          <div className="mt-5 pt-4 border-t border-border">
            <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
              Quick Actions
            </h4>
            <div className="grid grid-cols-2 gap-2">
              {[
                { icon: UserPlus, label: "Add Employee", color: "text-indigo-500" },
                { icon: Briefcase, label: "Post Job", color: "text-amber-500" },
                { icon: Wallet, label: "Run Payroll", color: "text-emerald-500" },
                { icon: Target, label: "Set Goals", color: "text-purple-500" },
              ].map((action, i) => (
                <button
                  key={i}
                  className="flex items-center gap-2 rounded-lg border border-border p-2.5 text-xs font-medium hover:bg-muted/50 transition-colors"
                >
                  <action.icon className={cn("h-4 w-4", action.color)} />
                  {action.label}
                </button>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
}
