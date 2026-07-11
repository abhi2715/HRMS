"use client";

import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Bot,
  Brain,
  Briefcase,
  Calendar,
  FileText,
  MessageSquare,
  Send,
  Shield,
  Sparkles,
  Timer,
  TrendingUp,
  Users,
  Wallet,
  Zap,
} from "lucide-react";
import { useState, useRef, useEffect } from "react";

const aiAgents = [
  { name: "Recruitment Agent", icon: Briefcase, status: "active", desc: "Screens resumes, ranks candidates, schedules interviews", tasks: 12, color: "from-indigo-500 to-blue-600" },
  { name: "Payroll Agent", icon: Wallet, status: "active", desc: "Processes salaries, detects anomalies, generates payslips", tasks: 4, color: "from-emerald-500 to-teal-600" },
  { name: "Leave Agent", icon: Calendar, status: "active", desc: "Evaluates leave requests, detects abuse patterns", tasks: 8, color: "from-amber-500 to-orange-600" },
  { name: "Attendance Agent", icon: Timer, status: "idle", desc: "Monitors attendance patterns, detects fraud", tasks: 0, color: "from-purple-500 to-violet-600" },
  { name: "Performance Agent", icon: TrendingUp, status: "active", desc: "Generates reviews, suggests promotions, tracks goals", tasks: 6, color: "from-pink-500 to-rose-600" },
  { name: "Compliance Agent", icon: Shield, status: "idle", desc: "Monitors policy adherence, tracks violations", tasks: 0, color: "from-cyan-500 to-blue-600" },
];

const chatHistory = [
  { role: "assistant", content: "Hello! I'm your HR Copilot. I can help you with employee queries, leave policies, payroll questions, recruitment status, and more. What would you like to know?" },
  { role: "user", content: "How many employees are on leave today?" },
  { role: "assistant", content: "Based on today's data:\n\n• **7 employees** are on approved leave today\n• 3 on Casual Leave\n• 2 on Sick Leave\n• 2 on Work From Home\n\nWould you like to see the list of employees on leave?" },
  { role: "user", content: "What's the attrition risk in the engineering team?" },
  { role: "assistant", content: "🔍 **Engineering Team Attrition Analysis**\n\nBased on engagement patterns, performance data, and historical trends:\n\n• **3 employees** flagged as high risk\n• **Key factors**: Low engagement score, pending appraisals, compensation below market median\n• **Recommended actions**:\n  1. Schedule 1-on-1s with flagged employees\n  2. Review compensation for Engineering dept\n  3. Implement retention bonus program\n\nWould you like me to draft a retention plan?" },
];

const suggestedQueries = [
  "Who are the top performers this quarter?",
  "Generate payroll summary for June",
  "Show me pending leave approvals",
  "What's the recruitment pipeline status?",
  "Summarize attendance trends this month",
  "Find employees due for appraisal",
];

export default function AICopilotPage() {
  const [messages, setMessages] = useState(chatHistory);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: "user", content: input }]);
    setInput("");
    setIsTyping(true);

    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "I'm processing your request using our AI agents. In a production environment, this would query the LangGraph agentic pipeline to generate a real-time response based on your HR data. 🚀",
        },
      ]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-purple-600">
            <Brain className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">AI Copilot</h1>
            <p className="text-sm text-muted-foreground mt-0.5">
              Your autonomous HR assistant powered by LangGraph
            </p>
          </div>
        </div>
        <span className="flex items-center gap-1.5 rounded-full bg-emerald-50 dark:bg-emerald-950/30 px-3 py-1 text-xs font-semibold text-emerald-600 dark:text-emerald-400">
          <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          6 Agents Online
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chat Panel */}
        <div className="lg:col-span-2 rounded-xl border border-border bg-card flex flex-col h-[600px]">
          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto custom-scrollbar p-5 space-y-4">
            {messages.map((msg, i) => (
              <motion.div key={i}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className={cn("flex gap-3", msg.role === "user" ? "justify-end" : "")}>
                {msg.role === "assistant" && (
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10 shrink-0 mt-0.5">
                    <Sparkles className="h-4 w-4 text-primary" />
                  </div>
                )}
                <div className={cn(
                  "max-w-[80%] rounded-xl px-4 py-3 text-sm leading-relaxed",
                  msg.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted/50 border border-border/50"
                )}>
                  <div className="whitespace-pre-wrap" dangerouslySetInnerHTML={{
                    __html: msg.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'),
                  }} />
                </div>
              </motion.div>
            ))}
            {isTyping && (
              <div className="flex gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10 shrink-0">
                  <Sparkles className="h-4 w-4 text-primary animate-pulse" />
                </div>
                <div className="bg-muted/50 border border-border/50 rounded-xl px-4 py-3">
                  <div className="flex items-center gap-1">
                    <div className="h-2 w-2 rounded-full bg-primary/50 animate-bounce" style={{ animationDelay: "0ms" }} />
                    <div className="h-2 w-2 rounded-full bg-primary/50 animate-bounce" style={{ animationDelay: "150ms" }} />
                    <div className="h-2 w-2 rounded-full bg-primary/50 animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* Suggested Queries */}
          <div className="px-5 py-2 border-t border-border/50">
            <div className="flex gap-2 overflow-x-auto custom-scrollbar pb-1">
              {suggestedQueries.map((q, i) => (
                <button key={i} onClick={() => setInput(q)}
                  className="shrink-0 rounded-full border border-border bg-background px-3 py-1 text-[11px] text-muted-foreground hover:border-primary/30 hover:text-foreground transition-colors">
                  {q}
                </button>
              ))}
            </div>
          </div>

          {/* Input */}
          <div className="p-4 border-t border-border">
            <div className="flex items-center gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                placeholder="Ask anything about your HR data..."
                className="flex-1 rounded-lg border border-input bg-background px-4 py-2.5 text-sm placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-ring transition-all"
              />
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={sendMessage}
                className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary text-primary-foreground hover:opacity-90 transition-opacity"
              >
                <Send className="h-4 w-4" />
              </motion.button>
            </div>
          </div>
        </div>

        {/* Agents Panel */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold">Active AI Agents</h3>
          {aiAgents.map((agent) => (
            <motion.div key={agent.name}
              whileHover={{ y: -2, transition: { duration: 0.2 } }}
              className="rounded-xl border border-border bg-card p-4 hover:shadow-md transition-all cursor-pointer">
              <div className="flex items-center gap-3">
                <div className={cn("flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br text-white", agent.color)}>
                  <agent.icon className="h-5 w-5" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h4 className="text-sm font-semibold truncate">{agent.name}</h4>
                    <span className={cn("h-2 w-2 rounded-full shrink-0",
                      agent.status === "active" ? "bg-emerald-500 animate-pulse" : "bg-muted-foreground/30"
                    )} />
                  </div>
                  <p className="text-[11px] text-muted-foreground truncate mt-0.5">{agent.desc}</p>
                </div>
              </div>
              {agent.tasks > 0 && (
                <div className="mt-3 flex items-center gap-2 text-xs text-muted-foreground">
                  <Zap className="h-3 w-3 text-amber-500" />
                  {agent.tasks} tasks processed today
                </div>
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
