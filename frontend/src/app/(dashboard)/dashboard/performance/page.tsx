"use client";

import { cn, getInitials, stringToColor } from "@/lib/utils";
import { motion } from "framer-motion";
import {
  Award,
  ChevronRight,
  MessageSquare,
  Plus,
  Sparkles,
  Star,
  Target,
  TrendingUp,
  Users,
} from "lucide-react";
import { useState } from "react";

const goals = [
  { id: "1", title: "Improve code quality metrics by 20%", progress: 75, status: "in_progress", period: "Q2 2026", weight: 30 },
  { id: "2", title: "Complete AWS Solutions Architect certification", progress: 40, status: "in_progress", period: "Q2 2026", weight: 20 },
  { id: "3", title: "Mentor 2 junior engineers through onboarding", progress: 100, status: "completed", period: "Q2 2026", weight: 25 },
  { id: "4", title: "Deliver user analytics module on time", progress: 60, status: "in_progress", period: "Q2 2026", weight: 25 },
];

const reviews = [
  { period: "Q1 2026", type: "Quarterly", selfRating: 4.2, managerRating: 4.0, finalRating: 4.1, status: "completed" },
  { period: "Annual 2025", type: "Annual", selfRating: 4.5, managerRating: 4.3, finalRating: 4.4, status: "completed" },
];

const teamPerformance = [
  { name: "Arjun Sharma", role: "Senior Engineer", rating: 4.5, goals: "4/4", status: "exceptional" },
  { name: "Priya Gupta", role: "Recruiter", rating: 4.2, goals: "3/4", status: "meets" },
  { name: "Deepak Verma", role: "ML Engineer", rating: 4.0, goals: "3/3", status: "meets" },
  { name: "Sneha Nair", role: "Lead Designer", rating: 4.8, goals: "5/5", status: "exceptional" },
  { name: "Rohit Singh", role: "DevOps Engineer", rating: 3.5, goals: "2/4", status: "needs_improvement" },
];

const ratingColors: Record<string, string> = {
  exceptional: "text-emerald-500",
  meets: "text-blue-500",
  needs_improvement: "text-amber-500",
};
const ratingBadges: Record<string, string> = {
  exceptional: "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400",
  meets: "bg-blue-50 text-blue-700 dark:bg-blue-950/30 dark:text-blue-400",
  needs_improvement: "bg-amber-50 text-amber-700 dark:bg-amber-950/30 dark:text-amber-400",
};

const containerVariants = { hidden: {}, visible: { transition: { staggerChildren: 0.05 } } };
const itemVariants = { hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0, transition: { duration: 0.3 } } };

export default function PerformancePage() {
  const [activeTab, setActiveTab] = useState<"goals" | "reviews" | "team">("goals");

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Performance</h1>
          <p className="text-sm text-muted-foreground mt-0.5">OKRs, reviews, and team performance</p>
        </div>
        <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
          className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:opacity-90">
          <Plus className="h-4 w-4" /> Set Goal
        </motion.button>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Overall Rating", value: "4.1", icon: Star, color: "text-amber-500", bg: "bg-amber-50 dark:bg-amber-950/30" },
          { label: "Goals Completed", value: "3/4", icon: Target, color: "text-emerald-500", bg: "bg-emerald-50 dark:bg-emerald-950/30" },
          { label: "Team Avg", value: "4.0", icon: Users, color: "text-indigo-500", bg: "bg-indigo-50 dark:bg-indigo-950/30" },
          { label: "360° Feedback", value: "12", icon: MessageSquare, color: "text-purple-500", bg: "bg-purple-50 dark:bg-purple-950/30" },
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
        {(["goals", "reviews", "team"] as const).map((tab) => (
          <button key={tab} onClick={() => setActiveTab(tab)}
            className={cn("px-4 py-2.5 text-sm font-medium border-b-2 -mb-px capitalize transition-colors",
              activeTab === tab ? "border-primary text-primary" : "border-transparent text-muted-foreground hover:text-foreground")}>
            {tab === "team" ? "Team Performance" : tab}
          </button>
        ))}
      </div>

      {/* Goals */}
      {activeTab === "goals" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible" className="space-y-3">
          {goals.map((goal) => (
            <motion.div key={goal.id} variants={itemVariants}
              className="rounded-xl border border-border bg-card p-5 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-sm font-semibold">{goal.title}</h3>
                  <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground">
                    <span>{goal.period}</span>
                    <span>Weight: {goal.weight}%</span>
                  </div>
                </div>
                <span className={cn("rounded-full px-2.5 py-0.5 text-[10px] font-semibold capitalize",
                  goal.status === "completed" ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400" :
                  "bg-blue-50 text-blue-700 dark:bg-blue-950/30 dark:text-blue-400")}>
                  {goal.status.replace("_", " ")}
                </span>
              </div>
              <div className="mt-3 flex items-center gap-3">
                <div className="flex-1 h-2 rounded-full bg-muted overflow-hidden">
                  <motion.div initial={{ width: 0 }} animate={{ width: `${goal.progress}%` }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    className={cn("h-full rounded-full",
                      goal.progress === 100 ? "bg-emerald-500" : goal.progress >= 50 ? "bg-primary" : "bg-amber-500"
                    )} />
                </div>
                <span className="text-sm font-semibold text-primary">{goal.progress}%</span>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* Reviews */}
      {activeTab === "reviews" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible" className="space-y-4">
          {reviews.map((r, i) => (
            <motion.div key={i} variants={itemVariants}
              className="rounded-xl border border-border bg-card p-5 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-sm font-semibold">{r.period} — {r.type} Review</h3>
                  <p className="text-xs text-muted-foreground capitalize">{r.status}</p>
                </div>
                <div className="flex items-center gap-1 rounded-full bg-amber-50 dark:bg-amber-950/30 px-3 py-1">
                  <Star className="h-4 w-4 text-amber-500 fill-amber-500" />
                  <span className="text-sm font-bold text-amber-600 dark:text-amber-400">{r.finalRating}</span>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4">
                {[
                  { label: "Self Rating", value: r.selfRating },
                  { label: "Manager Rating", value: r.managerRating },
                  { label: "Final Rating", value: r.finalRating },
                ].map((rating) => (
                  <div key={rating.label} className="text-center rounded-lg bg-muted/50 p-3">
                    <p className="text-xl font-bold">{rating.value}</p>
                    <p className="text-[10px] text-muted-foreground">{rating.label}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}

          {/* AI Summary */}
          <div className="rounded-xl border border-border bg-gradient-to-br from-primary/5 to-purple-500/5 p-5">
            <div className="flex items-center gap-2 mb-3">
              <Sparkles className="h-4 w-4 text-primary" />
              <h3 className="text-sm font-semibold">AI Performance Summary</h3>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Based on Q1 review data, your overall performance is <strong className="text-foreground">above average</strong>.
              Key strengths include mentoring ability and technical delivery. Areas for growth:
              certification completion and knowledge sharing. Recommendation: <strong className="text-foreground">Eligible for promotion discussion</strong>.
            </p>
          </div>
        </motion.div>
      )}

      {/* Team Performance */}
      {activeTab === "team" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible">
          <div className="rounded-xl border border-border overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border bg-muted/50">
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase py-3 px-4">Employee</th>
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase py-3 px-4">Rating</th>
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase py-3 px-4">Goals</th>
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase py-3 px-4">Status</th>
                </tr>
              </thead>
              <tbody>
                {teamPerformance.map((tp) => (
                  <motion.tr key={tp.name} variants={itemVariants}
                    className="border-b border-border/50 hover:bg-muted/30 transition-colors">
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-3">
                        <div className={cn("flex h-8 w-8 items-center justify-center rounded-full text-white text-xs font-bold", stringToColor(tp.name))}>
                          {getInitials(tp.name)}
                        </div>
                        <div>
                          <p className="text-sm font-medium">{tp.name}</p>
                          <p className="text-[11px] text-muted-foreground">{tp.role}</p>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-1">
                        <Star className="h-3.5 w-3.5 text-amber-500 fill-amber-500" />
                        <span className="text-sm font-semibold">{tp.rating}</span>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-sm">{tp.goals}</td>
                    <td className="py-3 px-4">
                      <span className={cn("rounded-full px-2.5 py-0.5 text-[10px] font-semibold capitalize",
                        ratingBadges[tp.status])}>
                        {tp.status.replace("_", " ")}
                      </span>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}
