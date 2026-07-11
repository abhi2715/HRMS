"use client";

import { cn, formatCurrency, getInitials, stringToColor } from "@/lib/utils";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Briefcase,
  Building2,
  ChevronRight,
  ExternalLink,
  Filter,
  MapPin,
  MoreHorizontal,
  Plus,
  Search,
  Sparkles,
  Star,
  TrendingUp,
  User,
  Users,
} from "lucide-react";
import { useState } from "react";

const stages = ["applied", "screening", "shortlisted", "interview", "technical", "hr_round", "offer", "hired"];
const stageColors: Record<string, string> = {
  applied: "bg-slate-100 text-slate-700 dark:bg-slate-900 dark:text-slate-300",
  screening: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400",
  shortlisted: "bg-cyan-100 text-cyan-700 dark:bg-cyan-900/30 dark:text-cyan-400",
  interview: "bg-violet-100 text-violet-700 dark:bg-violet-900/30 dark:text-violet-400",
  technical: "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400",
  hr_round: "bg-pink-100 text-pink-700 dark:bg-pink-900/30 dark:text-pink-400",
  offer: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400",
  hired: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400",
  rejected: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
};

const jobPostings = [
  { id: "1", title: "Senior Full-Stack Engineer", dept: "Engineering", location: "Bangalore", positions: 2, applicants: 14, status: "open", salary: "₹25-45L", posted: "Jun 10" },
  { id: "2", title: "ML Engineer - NLP", dept: "Data Science", location: "Bangalore", positions: 1, applicants: 8, status: "open", salary: "₹20-40L", posted: "Jun 15" },
  { id: "3", title: "Product Manager", dept: "Product", location: "Mumbai", positions: 1, applicants: 11, status: "open", salary: "₹20-35L", posted: "Jun 20" },
  { id: "4", title: "DevOps Engineer", dept: "Engineering", location: "Gurgaon", positions: 1, applicants: 6, status: "open", salary: "₹18-32L", posted: "Jun 25" },
];

const candidates = [
  { id: "1", name: "Arjun Sharma", email: "arjun.s@gmail.com", role: "Senior Full-Stack Engineer", exp: 6, score: 92, stage: "technical", source: "LinkedIn", notice: "30 days" },
  { id: "2", name: "Sneha Patel", email: "sneha.p@gmail.com", role: "ML Engineer - NLP", exp: 4, score: 88, stage: "interview", source: "Referral", notice: "60 days" },
  { id: "3", name: "Deepak Joshi", email: "deepak.j@gmail.com", role: "Senior Full-Stack Engineer", exp: 7, score: 85, stage: "hr_round", source: "Naukri", notice: "90 days" },
  { id: "4", name: "Priyanka Gupta", email: "priyanka.g@gmail.com", role: "Product Manager", exp: 5, score: 82, stage: "shortlisted", source: "LinkedIn", notice: "30 days" },
  { id: "5", name: "Rohit Verma", email: "rohit.v@gmail.com", role: "DevOps Engineer", exp: 4, score: 79, stage: "screening", source: "Indeed", notice: "15 days" },
  { id: "6", name: "Kavita Mehta", email: "kavita.m@gmail.com", role: "Senior Full-Stack Engineer", exp: 5, score: 76, stage: "applied", source: "Website", notice: "30 days" },
  { id: "7", name: "Amit Singh", email: "amit.s@gmail.com", role: "ML Engineer - NLP", exp: 3, score: 73, stage: "offer", source: "Referral", notice: "0 days" },
  { id: "8", name: "Neha Reddy", email: "neha.r@gmail.com", role: "Product Manager", exp: 6, score: 70, stage: "interview", source: "LinkedIn", notice: "60 days" },
];

const pipelineStats = {
  applied: 12, screening: 8, shortlisted: 6, interview: 5, technical: 3, hr_round: 2, offer: 2, hired: 1,
};

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.05 } },
};
const itemVariants = {
  hidden: { opacity: 0, y: 12 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3 } },
};

export default function RecruitmentPage() {
  const [activeTab, setActiveTab] = useState<"pipeline" | "postings" | "candidates">("pipeline");
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Recruitment</h1>
          <p className="text-sm text-muted-foreground mt-0.5">AI-powered hiring pipeline</p>
        </div>
        <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
          className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity">
          <Plus className="h-4 w-4" /> Post Job
        </motion.button>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Open Positions", value: "14", icon: Briefcase, color: "text-indigo-500", bg: "bg-indigo-50 dark:bg-indigo-950/30" },
          { label: "Total Applicants", value: "39", icon: Users, color: "text-blue-500", bg: "bg-blue-50 dark:bg-blue-950/30" },
          { label: "Interviews", value: "8", icon: User, color: "text-violet-500", bg: "bg-violet-50 dark:bg-violet-950/30" },
          { label: "Offers Sent", value: "2", icon: Star, color: "text-amber-500", bg: "bg-amber-50 dark:bg-amber-950/30" },
        ].map((kpi) => (
          <div key={kpi.label} className={cn("rounded-xl border border-border p-4 flex items-center gap-3", kpi.bg)}>
            <div className={cn("flex h-10 w-10 items-center justify-center rounded-xl bg-white/60 dark:bg-white/5", kpi.color)}>
              <kpi.icon className="h-5 w-5" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground">{kpi.label}</p>
              <p className={cn("text-xl font-bold", kpi.color)}>{kpi.value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-1 border-b border-border">
        {(["pipeline", "postings", "candidates"] as const).map((tab) => (
          <button key={tab} onClick={() => setActiveTab(tab)}
            className={cn(
              "px-4 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors capitalize",
              activeTab === tab
                ? "border-primary text-primary"
                : "border-transparent text-muted-foreground hover:text-foreground"
            )}>
            {tab}
          </button>
        ))}
      </div>

      {/* Pipeline View */}
      {activeTab === "pipeline" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible">
          <div className="rounded-xl border border-border bg-card p-5">
            <h3 className="text-sm font-semibold mb-4">Hiring Pipeline</h3>
            <div className="grid grid-cols-4 lg:grid-cols-8 gap-2">
              {stages.map((stage) => (
                <motion.div key={stage} variants={itemVariants}
                  className="rounded-lg border border-border p-3 text-center hover:border-primary/30 transition-colors">
                  <p className="text-2xl font-bold">{pipelineStats[stage as keyof typeof pipelineStats]}</p>
                  <p className="text-[10px] text-muted-foreground capitalize mt-1">{stage.replace("_", " ")}</p>
                  <div className="mt-2 h-1.5 w-full rounded-full bg-muted overflow-hidden">
                    <motion.div initial={{ width: 0 }} animate={{ width: `${(pipelineStats[stage as keyof typeof pipelineStats] / 12) * 100}%` }}
                      transition={{ duration: 0.8, delay: 0.2 }}
                      className="h-full rounded-full bg-primary" />
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Top Candidates with AI Score */}
          <div className="mt-6 rounded-xl border border-border bg-card p-5">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="h-4 w-4 text-primary" />
              <h3 className="text-sm font-semibold">AI-Ranked Candidates</h3>
            </div>
            <div className="space-y-2">
              {candidates.slice(0, 5).map((cand, i) => (
                <motion.div key={cand.id} variants={itemVariants}
                  className="flex items-center gap-3 rounded-lg p-3 hover:bg-muted/50 transition-colors">
                  <span className="text-xs font-bold text-muted-foreground w-5">#{i + 1}</span>
                  <div className={cn("flex h-9 w-9 items-center justify-center rounded-full text-white text-xs font-bold", stringToColor(cand.name))}>
                    {getInitials(cand.name)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium">{cand.name}</p>
                    <p className="text-xs text-muted-foreground">{cand.role} • {cand.exp} yrs • {cand.source}</p>
                  </div>
                  <span className={cn("rounded-full px-2.5 py-0.5 text-[10px] font-semibold capitalize", stageColors[cand.stage])}>
                    {cand.stage.replace("_", " ")}
                  </span>
                  <div className="flex items-center gap-1.5 rounded-full bg-primary/10 px-2.5 py-1 text-xs font-bold text-primary">
                    <Sparkles className="h-3 w-3" />
                    {cand.score}%
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      )}

      {/* Job Postings View */}
      {activeTab === "postings" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible"
          className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {jobPostings.map((job) => (
            <motion.div key={job.id} variants={itemVariants}
              whileHover={{ y: -2, transition: { duration: 0.2 } }}
              className="rounded-xl border border-border bg-card p-5 hover:shadow-lg hover:border-primary/20 transition-all cursor-pointer">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-sm font-semibold">{job.title}</h3>
                  <div className="flex items-center gap-3 mt-1.5 text-xs text-muted-foreground">
                    <span className="flex items-center gap-1"><Building2 className="h-3 w-3" /> {job.dept}</span>
                    <span className="flex items-center gap-1"><MapPin className="h-3 w-3" /> {job.location}</span>
                  </div>
                </div>
                <span className="rounded-full bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400 px-2 py-0.5 text-[10px] font-semibold uppercase">
                  {job.status}
                </span>
              </div>
              <div className="mt-4 grid grid-cols-3 gap-3">
                <div className="text-center rounded-lg bg-muted/50 p-2">
                  <p className="text-lg font-bold">{job.positions}</p>
                  <p className="text-[10px] text-muted-foreground">Positions</p>
                </div>
                <div className="text-center rounded-lg bg-muted/50 p-2">
                  <p className="text-lg font-bold">{job.applicants}</p>
                  <p className="text-[10px] text-muted-foreground">Applicants</p>
                </div>
                <div className="text-center rounded-lg bg-muted/50 p-2">
                  <p className="text-lg font-bold text-primary">{job.salary}</p>
                  <p className="text-[10px] text-muted-foreground">Salary</p>
                </div>
              </div>
              <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
                <span>Posted {job.posted}</span>
                <button className="flex items-center gap-1 text-primary font-medium hover:underline">
                  View Pipeline <ChevronRight className="h-3 w-3" />
                </button>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* Candidates View */}
      {activeTab === "candidates" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible">
          <div className="mb-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input type="text" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search candidates..." className="w-full rounded-lg border border-input bg-background pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring transition-all" />
            </div>
          </div>
          <div className="rounded-xl border border-border overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border bg-muted/50">
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase py-3 px-4">Candidate</th>
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase py-3 px-4">Role</th>
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase py-3 px-4">Experience</th>
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase py-3 px-4">Source</th>
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase py-3 px-4">Stage</th>
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase py-3 px-4">AI Score</th>
                  <th className="text-right text-xs font-medium text-muted-foreground uppercase py-3 px-4"></th>
                </tr>
              </thead>
              <tbody>
                {candidates
                  .filter(c => c.name.toLowerCase().includes(searchQuery.toLowerCase()) || c.role.toLowerCase().includes(searchQuery.toLowerCase()))
                  .map((cand) => (
                  <motion.tr key={cand.id} variants={itemVariants} className="border-b border-border/50 hover:bg-muted/30 transition-colors">
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-3">
                        <div className={cn("flex h-8 w-8 items-center justify-center rounded-full text-white text-xs font-bold", stringToColor(cand.name))}>
                          {getInitials(cand.name)}
                        </div>
                        <div>
                          <p className="text-sm font-medium">{cand.name}</p>
                          <p className="text-[11px] text-muted-foreground">{cand.email}</p>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-sm">{cand.role}</td>
                    <td className="py-3 px-4 text-sm">{cand.exp} years</td>
                    <td className="py-3 px-4 text-sm text-muted-foreground">{cand.source}</td>
                    <td className="py-3 px-4">
                      <span className={cn("rounded-full px-2.5 py-0.5 text-[10px] font-semibold capitalize", stageColors[cand.stage])}>
                        {cand.stage.replace("_", " ")}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-1.5">
                        <div className="w-16 h-1.5 rounded-full bg-muted overflow-hidden">
                          <div className="h-full rounded-full bg-primary" style={{ width: `${cand.score}%` }} />
                        </div>
                        <span className="text-xs font-semibold text-primary">{cand.score}%</span>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button className="text-muted-foreground hover:text-foreground"><MoreHorizontal className="h-4 w-4" /></button>
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
