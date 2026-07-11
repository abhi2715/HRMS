"use client";

import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import {
  ArrowDownRight,
  ArrowUpRight,
  Clock,
  LogIn,
  LogOut,
  MapPin,
  Timer,
  TrendingUp,
  UserCheck,
  UserMinus,
  Users,
} from "lucide-react";
import { useState } from "react";
import {
  BarChart, Bar, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid,
} from "recharts";

const todayStats = {
  total: 247, present: 218, absent: 14, late: 8, onLeave: 7, wfh: 22,
  attendanceRate: 88.3,
};

const weeklyData = [
  { day: "Mon", present: 220, absent: 12, late: 8 },
  { day: "Tue", present: 225, absent: 10, late: 6 },
  { day: "Wed", present: 218, absent: 14, late: 9 },
  { day: "Thu", present: 222, absent: 11, late: 7 },
  { day: "Fri", present: 218, absent: 14, late: 8 },
];

const recentCheckIns = [
  { name: "Arjun Sharma", time: "09:02 AM", status: "on-time", dept: "Engineering", type: "office" },
  { name: "Priya Gupta", time: "09:08 AM", status: "on-time", dept: "HR", type: "remote" },
  { name: "Deepak Verma", time: "09:15 AM", status: "on-time", dept: "Data Science", type: "office" },
  { name: "Sneha Nair", time: "09:22 AM", status: "late", dept: "Design", type: "office" },
  { name: "Rohit Singh", time: "09:35 AM", status: "late", dept: "Engineering", type: "remote" },
  { name: "Kavita Sharma", time: "09:45 AM", status: "late", dept: "HR", type: "office" },
  { name: "Rahul Kumar", time: "10:02 AM", status: "late", dept: "Engineering", type: "office" },
];

const myAttendance = {
  checkIn: "09:08 AM", checkOut: null, workHours: "6h 32m", status: "present",
  month: { present: 18, absent: 0, late: 2, leave: 1, wfh: 3, avgHours: 8.4 },
};

const containerVariants = { hidden: {}, visible: { transition: { staggerChildren: 0.05 } } };
const itemVariants = { hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0, transition: { duration: 0.3 } } };

export default function AttendancePage() {
  const [checkedIn, setCheckedIn] = useState(true);
  const [checkedOut, setCheckedOut] = useState(false);

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Attendance</h1>
          <p className="text-sm text-muted-foreground mt-0.5">Real-time attendance tracking & insights</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Clock className="h-4 w-4" />
          {new Date().toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" })}
        </div>
      </div>

      {/* Check In/Out Card */}
      <motion.div variants={itemVariants} initial="hidden" animate="visible"
        className="rounded-xl border border-border bg-gradient-to-r from-primary/5 to-purple-500/5 p-6">
        <div className="flex flex-col sm:flex-row items-center gap-6">
          <div className="flex-1">
            <h3 className="text-sm font-semibold">Today&apos;s Status</h3>
            <div className="mt-2 flex items-center gap-4 text-sm">
              <span className="flex items-center gap-1 text-emerald-500">
                <LogIn className="h-4 w-4" /> Check-in: {myAttendance.checkIn}
              </span>
              {myAttendance.checkOut ? (
                <span className="flex items-center gap-1 text-blue-500">
                  <LogOut className="h-4 w-4" /> Check-out: {myAttendance.checkOut}
                </span>
              ) : (
                <span className="flex items-center gap-1 text-muted-foreground">
                  <Timer className="h-4 w-4" /> Working: {myAttendance.workHours}
                </span>
              )}
            </div>
          </div>
          <div className="flex items-center gap-2">
            {!checkedIn ? (
              <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
                onClick={() => setCheckedIn(true)}
                className="flex items-center gap-2 rounded-lg bg-emerald-500 px-6 py-3 text-sm font-semibold text-white hover:bg-emerald-600 transition-colors">
                <LogIn className="h-4 w-4" /> Check In
              </motion.button>
            ) : !checkedOut ? (
              <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
                onClick={() => setCheckedOut(true)}
                className="flex items-center gap-2 rounded-lg bg-red-500 px-6 py-3 text-sm font-semibold text-white hover:bg-red-600 transition-colors">
                <LogOut className="h-4 w-4" /> Check Out
              </motion.button>
            ) : (
              <span className="text-sm text-emerald-500 font-semibold">✓ Day Complete</span>
            )}
          </div>
        </div>
      </motion.div>

      {/* KPI Cards */}
      <motion.div variants={containerVariants} initial="hidden" animate="visible"
        className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          { label: "Total", value: todayStats.total, color: "text-foreground", bg: "" },
          { label: "Present", value: todayStats.present, color: "text-emerald-500", bg: "bg-emerald-50 dark:bg-emerald-950/30" },
          { label: "Absent", value: todayStats.absent, color: "text-red-500", bg: "bg-red-50 dark:bg-red-950/30" },
          { label: "Late", value: todayStats.late, color: "text-amber-500", bg: "bg-amber-50 dark:bg-amber-950/30" },
          { label: "On Leave", value: todayStats.onLeave, color: "text-blue-500", bg: "bg-blue-50 dark:bg-blue-950/30" },
          { label: "WFH", value: todayStats.wfh, color: "text-violet-500", bg: "bg-violet-50 dark:bg-violet-950/30" },
        ].map((s) => (
          <motion.div key={s.label} variants={itemVariants}
            className={cn("rounded-xl border border-border p-4 text-center", s.bg)}>
            <p className="text-xs text-muted-foreground">{s.label}</p>
            <p className={cn("text-2xl font-bold mt-1", s.color)}>{s.value}</p>
          </motion.div>
        ))}
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Weekly Chart */}
        <motion.div variants={itemVariants} initial="hidden" animate="visible"
          className="rounded-xl border border-border bg-card p-5">
          <h3 className="text-sm font-semibold mb-4">This Week&apos;s Attendance</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={weeklyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--color-border))" opacity={0.5} />
              <XAxis dataKey="day" tick={{ fontSize: 11 }} stroke="hsl(var(--color-muted-foreground))" />
              <YAxis tick={{ fontSize: 11 }} stroke="hsl(var(--color-muted-foreground))" />
              <Tooltip contentStyle={{
                backgroundColor: "hsl(var(--color-card))",
                border: "1px solid hsl(var(--color-border))",
                borderRadius: "8px", fontSize: "12px",
              }} />
              <Bar dataKey="present" fill="#22c55e" radius={[3, 3, 0, 0]} barSize={20} />
              <Bar dataKey="absent" fill="#ef4444" radius={[3, 3, 0, 0]} barSize={20} />
              <Bar dataKey="late" fill="#f59e0b" radius={[3, 3, 0, 0]} barSize={20} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* My Monthly Summary */}
        <motion.div variants={itemVariants} initial="hidden" animate="visible"
          className="rounded-xl border border-border bg-card p-5">
          <h3 className="text-sm font-semibold mb-4">My Monthly Summary</h3>
          <div className="grid grid-cols-3 gap-3">
            {[
              { label: "Present", value: myAttendance.month.present, total: 22, color: "#22c55e" },
              { label: "Late", value: myAttendance.month.late, total: 22, color: "#f59e0b" },
              { label: "Leave", value: myAttendance.month.leave, total: 22, color: "#3b82f6" },
              { label: "WFH", value: myAttendance.month.wfh, total: 22, color: "#8b5cf6" },
              { label: "Absent", value: myAttendance.month.absent, total: 22, color: "#ef4444" },
              { label: "Avg Hours", value: myAttendance.month.avgHours, total: 9, color: "#6366f1" },
            ].map((s) => (
              <div key={s.label} className="rounded-lg border border-border p-3 text-center">
                <p className="text-lg font-bold" style={{ color: s.color }}>{s.value}</p>
                <p className="text-[10px] text-muted-foreground mt-0.5">{s.label}</p>
                <div className="mt-2 h-1.5 w-full rounded-full bg-muted overflow-hidden">
                  <div className="h-full rounded-full" style={{
                    backgroundColor: s.color,
                    width: `${Math.min(100, (Number(s.value) / s.total) * 100)}%`,
                  }} />
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Recent Check-ins */}
      <motion.div variants={itemVariants} initial="hidden" animate="visible"
        className="rounded-xl border border-border bg-card p-5">
        <h3 className="text-sm font-semibold mb-4">Recent Check-ins Today</h3>
        <div className="space-y-2">
          {recentCheckIns.map((c, i) => (
            <div key={i} className="flex items-center gap-3 rounded-lg p-2.5 hover:bg-muted/50 transition-colors">
              <div className={cn(
                "h-2 w-2 rounded-full shrink-0",
                c.status === "on-time" ? "bg-emerald-500" : "bg-amber-500"
              )} />
              <span className="text-sm font-medium w-40 truncate">{c.name}</span>
              <span className="text-xs text-muted-foreground w-20">{c.time}</span>
              <span className="text-xs text-muted-foreground w-28">{c.dept}</span>
              <span className={cn("rounded-full px-2 py-0.5 text-[10px] font-semibold",
                c.type === "remote" ? "bg-violet-50 text-violet-700 dark:bg-violet-950/30 dark:text-violet-400" :
                "bg-blue-50 text-blue-700 dark:bg-blue-950/30 dark:text-blue-400")}>
                {c.type === "remote" ? "🏠 Remote" : "🏢 Office"}
              </span>
              <span className={cn("ml-auto rounded-full px-2 py-0.5 text-[10px] font-semibold",
                c.status === "on-time" ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400" :
                "bg-amber-50 text-amber-700 dark:bg-amber-950/30 dark:text-amber-400")}>
                {c.status}
              </span>
            </div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  );
}
