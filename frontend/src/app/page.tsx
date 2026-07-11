"use client";

import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import {
  ArrowRight,
  BarChart3,
  Bot,
  Brain,
  Briefcase,
  Calendar,
  CheckCircle2,
  ChevronRight,
  Clock,
  FileText,
  Fingerprint,
  GraduationCap,
  Heart,
  LayoutDashboard,
  Lock,
  MessageSquare,
  Sparkles,
  Target,
  Timer,
  TrendingUp,
  Users,
  Wallet,
  Zap,
} from "lucide-react";
import Link from "next/link";

const features = [
  { icon: Users, title: "Employee Management", desc: "Complete lifecycle management with AI-generated summaries" },
  { icon: Briefcase, title: "AI Recruitment", desc: "Resume parsing, skill matching, and candidate ranking" },
  { icon: Wallet, title: "Smart Payroll", desc: "Automated salary processing with anomaly detection" },
  { icon: Calendar, title: "Leave Intelligence", desc: "AI-powered leave evaluation with abuse detection" },
  { icon: Timer, title: "Attendance Insights", desc: "Fraud detection and pattern analysis" },
  { icon: Target, title: "Performance OKRs", desc: "Goal tracking with 360° feedback and AI reviews" },
  { icon: GraduationCap, title: "Training Paths", desc: "AI-recommended courses and skill development" },
  { icon: Lock, title: "Compliance Engine", desc: "Policy management with automated violation detection" },
  { icon: BarChart3, title: "Predictive Analytics", desc: "Attrition prediction and workforce planning" },
  { icon: Brain, title: "6 AI Agents", desc: "Autonomous agents for every HR function" },
  { icon: MessageSquare, title: "Employee Support", desc: "RAG-powered chatbot for HR queries" },
  { icon: Zap, title: "n8n Automation", desc: "20+ automated workflows for HR operations" },
];

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08 } },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.25, 0.1, 0.25, 1] as const } },
};

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <nav className="fixed top-0 z-50 w-full border-b border-border/50 bg-background/80 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
          <div className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary">
              <Sparkles className="h-4.5 w-4.5 text-primary-foreground" />
            </div>
            <span className="text-lg font-bold tracking-tight">HR Copilot</span>
          </div>
          <div className="flex items-center gap-3">
            <Link
              href="/login"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              Sign In
            </Link>
            <Link
              href="/login"
              className="flex items-center gap-1.5 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity"
            >
              Get Started
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-1/4 left-1/4 h-96 w-96 rounded-full bg-primary/10 blur-[128px]" />
          <div className="absolute bottom-1/4 right-1/4 h-96 w-96 rounded-full bg-purple-500/10 blur-[128px]" />
        </div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          className="mx-auto max-w-4xl text-center px-6"
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-border bg-muted/50 px-4 py-1.5 text-xs font-medium text-muted-foreground mb-6">
            <Sparkles className="h-3.5 w-3.5 text-primary" />
            Powered by Agentic AI & LangGraph
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1] mb-6">
            Your{" "}
            <span className="gradient-text">Autonomous</span>
            <br />
            HR Department
          </h1>

          <p className="text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed mb-8">
            An enterprise AI-powered HRMS where intelligent agents think, reason, and execute.
            From recruitment to payroll, attendance to compliance — everything runs autonomously.
          </p>

          <div className="flex items-center justify-center gap-4">
            <Link
              href="/login"
              className="flex items-center gap-2 rounded-xl bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity shadow-lg shadow-primary/20"
            >
              Launch Dashboard
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="#features"
              className="flex items-center gap-2 rounded-xl border border-border px-6 py-3 text-sm font-semibold hover:bg-muted transition-colors"
            >
              Explore Features
            </Link>
          </div>

          {/* Stats */}
          <div className="mt-16 grid grid-cols-2 sm:grid-cols-4 gap-6 max-w-2xl mx-auto">
            {[
              { value: "6", label: "AI Agents" },
              { value: "12+", label: "HR Modules" },
              { value: "6", label: "ML Models" },
              { value: "50+", label: "Automations" },
            ].map((stat) => (
              <div key={stat.label}>
                <p className="text-3xl font-bold gradient-text">{stat.value}</p>
                <p className="text-xs text-muted-foreground mt-1">{stat.label}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-20 bg-muted/30">
        <div className="mx-auto max-w-7xl px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold tracking-tight mb-3">
              Everything Your HR Team Needs
            </h2>
            <p className="text-muted-foreground max-w-xl mx-auto">
              12+ fully integrated modules powered by autonomous AI agents
            </p>
          </motion.div>

          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
          >
            {features.map((feature) => (
              <motion.div
                key={feature.title}
                variants={itemVariants}
                whileHover={{ y: -4, transition: { duration: 0.2 } }}
                className="group rounded-xl border border-border bg-card p-5 hover:shadow-lg hover:border-primary/20 transition-all duration-300"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 mb-3 group-hover:bg-primary/20 transition-colors">
                  <feature.icon className="h-5 w-5 text-primary" />
                </div>
                <h3 className="text-sm font-semibold mb-1">{feature.title}</h3>
                <p className="text-xs text-muted-foreground leading-relaxed">{feature.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="mx-auto max-w-3xl text-center px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-bold tracking-tight mb-4">
              Ready to Transform Your HR?
            </h2>
            <p className="text-muted-foreground mb-8">
              Get started with the most advanced AI-powered HRMS platform.
            </p>
            <Link
              href="/login"
              className="inline-flex items-center gap-2 rounded-xl bg-primary px-8 py-3.5 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity shadow-lg shadow-primary/20"
            >
              Start Free Trial
              <ArrowRight className="h-4 w-4" />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="mx-auto max-w-7xl px-6 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-primary" />
            <span className="text-sm font-semibold">HR Copilot</span>
          </div>
          <p className="text-xs text-muted-foreground">
            © 2026 HR Copilot. Enterprise AI-Powered HRMS.
          </p>
        </div>
      </footer>
    </div>
  );
}
