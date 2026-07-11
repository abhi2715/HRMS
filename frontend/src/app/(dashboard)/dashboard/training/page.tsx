"use client";

import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import {
  Award,
  BookOpen,
  ChevronRight,
  Clock,
  GraduationCap,
  Play,
  Plus,
  Search,
  Sparkles,
  Star,
  TrendingUp,
  Users,
} from "lucide-react";
import { useState } from "react";

const courses = [
  { id: "1", title: "Advanced Python for ML Engineers", category: "Technical", difficulty: "Advanced", hours: 40, provider: "Internal", progress: 65, enrolled: true, mandatory: false, aiRecommended: true },
  { id: "2", title: "Leadership Essentials", category: "Leadership", difficulty: "Intermediate", hours: 20, provider: "LinkedIn Learning", progress: 100, enrolled: true, mandatory: true, aiRecommended: false },
  { id: "3", title: "POSH Training", category: "Compliance", difficulty: "Beginner", hours: 4, provider: "Internal", progress: 100, enrolled: true, mandatory: true, aiRecommended: false },
  { id: "4", title: "Cloud Architecture with AWS", category: "Technical", difficulty: "Advanced", hours: 60, provider: "Coursera", progress: 30, enrolled: true, mandatory: false, aiRecommended: true },
  { id: "5", title: "Data Privacy & GDPR", category: "Compliance", difficulty: "Beginner", hours: 8, provider: "Internal", progress: 0, enrolled: false, mandatory: true, aiRecommended: false },
  { id: "6", title: "Effective Communication", category: "Soft Skills", difficulty: "Beginner", hours: 12, provider: "Udemy", progress: 0, enrolled: false, mandatory: false, aiRecommended: true },
  { id: "7", title: "React & Next.js Masterclass", category: "Technical", difficulty: "Advanced", hours: 45, provider: "Frontend Masters", progress: 0, enrolled: false, mandatory: false, aiRecommended: true },
  { id: "8", title: "Agile & Scrum Certification", category: "Management", difficulty: "Intermediate", hours: 30, provider: "PMI", progress: 0, enrolled: false, mandatory: false, aiRecommended: false },
];

const categories = ["All", "Technical", "Leadership", "Compliance", "Soft Skills", "Management"];
const difficultyColors: Record<string, string> = {
  Beginner: "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400",
  Intermediate: "bg-blue-50 text-blue-700 dark:bg-blue-950/30 dark:text-blue-400",
  Advanced: "bg-purple-50 text-purple-700 dark:bg-purple-950/30 dark:text-purple-400",
};

const containerVariants = { hidden: {}, visible: { transition: { staggerChildren: 0.04 } } };
const itemVariants = { hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0, transition: { duration: 0.3 } } };

export default function TrainingPage() {
  const [activeTab, setActiveTab] = useState<"catalog" | "my-learning" | "programs">("catalog");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");

  const filteredCourses = courses.filter((c) => {
    const matchesSearch = c.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === "All" || c.category === selectedCategory;
    const matchesTab = activeTab === "catalog" ? !c.enrolled : c.enrolled;
    return matchesSearch && matchesCategory && (activeTab === "programs" || matchesTab);
  });

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Training & Development</h1>
          <p className="text-sm text-muted-foreground mt-0.5">AI-recommended learning paths</p>
        </div>
        <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
          className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:opacity-90">
          <Plus className="h-4 w-4" /> Add Course
        </motion.button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Enrolled", value: "4", icon: BookOpen, color: "text-indigo-500", bg: "bg-indigo-50 dark:bg-indigo-950/30" },
          { label: "Completed", value: "2", icon: Award, color: "text-emerald-500", bg: "bg-emerald-50 dark:bg-emerald-950/30" },
          { label: "In Progress", value: "2", icon: TrendingUp, color: "text-blue-500", bg: "bg-blue-50 dark:bg-blue-950/30" },
          { label: "Hours Logged", value: "48", icon: Clock, color: "text-amber-500", bg: "bg-amber-50 dark:bg-amber-950/30" },
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
        {(["my-learning", "catalog", "programs"] as const).map((tab) => (
          <button key={tab} onClick={() => setActiveTab(tab)}
            className={cn("px-4 py-2.5 text-sm font-medium border-b-2 -mb-px capitalize transition-colors",
              activeTab === tab ? "border-primary text-primary" : "border-transparent text-muted-foreground hover:text-foreground")}>
            {tab.replace("-", " ")}
          </button>
        ))}
      </div>

      {/* Filters */}
      {activeTab !== "programs" && (
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input type="text" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search courses..." className="w-full rounded-lg border border-input bg-background pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
          </div>
          <div className="flex gap-1.5">
            {categories.map((cat) => (
              <button key={cat} onClick={() => setSelectedCategory(cat)}
                className={cn("rounded-lg px-3 py-2 text-xs font-medium transition-colors",
                  selectedCategory === cat ? "bg-primary text-primary-foreground" : "bg-muted hover:bg-muted/80")}>
                {cat}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Course Grid */}
      {activeTab !== "programs" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible"
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredCourses.map((course) => (
            <motion.div key={course.id} variants={itemVariants}
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
              className="rounded-xl border border-border bg-card p-5 hover:shadow-lg hover:border-primary/20 transition-all cursor-pointer">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-2">
                  <span className={cn("rounded-full px-2 py-0.5 text-[10px] font-semibold", difficultyColors[course.difficulty])}>
                    {course.difficulty}
                  </span>
                  {course.mandatory && (
                    <span className="rounded-full bg-red-50 text-red-700 dark:bg-red-950/30 dark:text-red-400 px-2 py-0.5 text-[10px] font-semibold">
                      Mandatory
                    </span>
                  )}
                </div>
                {course.aiRecommended && (
                  <div className="flex items-center gap-1 text-primary">
                    <Sparkles className="h-3.5 w-3.5" />
                    <span className="text-[10px] font-semibold">AI Pick</span>
                  </div>
                )}
              </div>

              <h3 className="text-sm font-semibold mt-3">{course.title}</h3>
              <div className="flex items-center gap-3 mt-1.5 text-xs text-muted-foreground">
                <span>{course.category}</span>
                <span>{course.hours}h</span>
                <span>{course.provider}</span>
              </div>

              {course.enrolled && (
                <div className="mt-4">
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs text-muted-foreground">Progress</span>
                    <span className="text-xs font-semibold text-primary">{course.progress}%</span>
                  </div>
                  <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
                    <motion.div initial={{ width: 0 }} animate={{ width: `${course.progress}%` }}
                      transition={{ duration: 0.8, delay: 0.2 }}
                      className={cn("h-full rounded-full",
                        course.progress === 100 ? "bg-emerald-500" : "bg-primary")} />
                  </div>
                </div>
              )}

              {!course.enrolled && (
                <button className="mt-4 flex items-center gap-1.5 rounded-lg bg-primary/10 text-primary px-3 py-1.5 text-xs font-semibold hover:bg-primary/20 transition-colors">
                  <Play className="h-3.5 w-3.5" /> Enroll Now
                </button>
              )}
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* Programs View */}
      {activeTab === "programs" && (
        <motion.div variants={containerVariants} initial="hidden" animate="visible" className="space-y-4">
          {[
            { name: "New Hire Onboarding Program", desc: "4-week comprehensive onboarding for new joiners", courses: 6, status: "active", start: "Jul 1, 2026" },
            { name: "Leadership Development Track", desc: "6-month leadership program for managers", courses: 8, status: "upcoming", start: "Aug 15, 2026" },
            { name: "Technical Excellence Program", desc: "Quarterly tech skill upgrade for engineering", courses: 5, status: "active", start: "Jun 1, 2026" },
          ].map((prog, i) => (
            <motion.div key={i} variants={itemVariants}
              className="rounded-xl border border-border bg-card p-5 hover:shadow-md transition-shadow cursor-pointer">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-sm font-semibold">{prog.name}</h3>
                  <p className="text-xs text-muted-foreground mt-0.5">{prog.desc}</p>
                </div>
                <span className={cn("rounded-full px-2.5 py-0.5 text-[10px] font-semibold capitalize",
                  prog.status === "active" ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400" :
                  "bg-blue-50 text-blue-700 dark:bg-blue-950/30 dark:text-blue-400")}>
                  {prog.status}
                </span>
              </div>
              <div className="mt-3 flex items-center gap-4 text-xs text-muted-foreground">
                <span className="flex items-center gap-1"><BookOpen className="h-3 w-3" /> {prog.courses} courses</span>
                <span className="flex items-center gap-1"><Clock className="h-3 w-3" /> Started {prog.start}</span>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}
    </motion.div>
  );
}
