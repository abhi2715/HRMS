"use client";

import { cn } from "@/lib/utils";
import { useAuthStore } from "@/stores/auth-store";
import api from "@/lib/api";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Eye,
  EyeOff,
  Lock,
  Mail,
  Sparkles,
} from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { toast } from "sonner";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { setAuth } = useAuthStore();
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    // 🔥 BYPASS: Hardcoding the login response to move straight to functionality
    setTimeout(() => {
      setAuth(
        {
          id: "238dd245-8d10-4b34-8b12-ec1b9b38b45b",
          email: "rajesh.kumar@hrcopilot.io",
          first_name: "Rajesh",
          last_name: "Kumar",
          full_name: "Rajesh Kumar",
          phone: null,
          avatar_url: null,
          primary_role: "SUPER_ADMIN",
          is_active: true,
          is_verified: true,
          last_login: new Date().toISOString(),
          created_at: new Date().toISOString(),
        },
        "fake-access-token",
        "fake-refresh-token"
      );
      toast.success(`Welcome back, Rajesh! (Auth Bypassed)`);
      router.push("/dashboard");
    }, 500);
  };

  const loginAsDemo = async (demoEmail: string) => {
    setEmail(demoEmail);
    setPassword(demoEmail === "rajesh.kumar@hrcopilot.io" ? "admin123" : "demo123");
  };

  return (
    <div className="flex min-h-screen">
      {/* Left panel - Branding */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600">
        {/* Animated background elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-20 h-72 w-72 rounded-full bg-white/10 blur-3xl animate-pulse" />
          <div className="absolute bottom-20 right-20 h-96 w-96 rounded-full bg-white/5 blur-3xl animate-pulse delay-1000" />
          <div className="absolute top-1/2 left-1/3 h-48 w-48 rounded-full bg-white/10 blur-2xl float" />
        </div>

        {/* Content */}
        <div className="relative z-10 flex flex-col justify-center px-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="flex items-center gap-3 mb-8">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-white/20 backdrop-blur-xl">
                <Sparkles className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">HR Copilot</h1>
                <p className="text-sm text-white/70">Enterprise AI HRMS</p>
              </div>
            </div>

            <h2 className="text-4xl font-bold text-white leading-tight mb-4">
              Your Autonomous<br />
              <span className="text-white/90">HR Department</span>
            </h2>

            <p className="text-lg text-white/70 max-w-md leading-relaxed mb-8">
              AI agents that think, reason, and execute HR workflows autonomously.
              From recruitment to payroll, leave management to compliance.
            </p>

            <div className="grid grid-cols-2 gap-4 max-w-md">
              {[
                { label: "AI Agents", value: "6" },
                { label: "ML Models", value: "6" },
                { label: "Modules", value: "12+" },
                { label: "Automations", value: "20+" },
              ].map((stat) => (
                <div
                  key={stat.label}
                  className="rounded-xl bg-white/10 backdrop-blur-sm p-4 border border-white/10"
                >
                  <p className="text-2xl font-bold text-white">{stat.value}</p>
                  <p className="text-xs text-white/60 mt-1">{stat.label}</p>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Right panel - Login form */}
      <div className="flex w-full lg:w-1/2 items-center justify-center p-8 bg-background">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="w-full max-w-md"
        >
          {/* Mobile logo */}
          <div className="flex items-center gap-2 mb-8 lg:hidden">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary">
              <Sparkles className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold">HR Copilot</span>
          </div>

          <div className="mb-8">
            <h2 className="text-2xl font-bold tracking-tight">Welcome back</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Sign in to your HR Copilot account
            </p>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            {/* Email */}
            <div>
              <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Email
              </label>
              <div className="relative mt-1.5">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="admin@hrcopilot.ai"
                  className={cn(
                    "w-full rounded-lg border border-input bg-background pl-10 pr-4 py-2.5",
                    "text-sm placeholder:text-muted-foreground/50",
                    "focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent",
                    "transition-all duration-200"
                  )}
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Password
              </label>
              <div className="relative mt-1.5">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className={cn(
                    "w-full rounded-lg border border-input bg-background pl-10 pr-10 py-2.5",
                    "text-sm placeholder:text-muted-foreground/50",
                    "focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent",
                    "transition-all duration-200"
                  )}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            {/* Remember & Forgot */}
            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 text-sm">
                <input type="checkbox" className="rounded border-input" />
                <span className="text-muted-foreground">Remember me</span>
              </label>
              <button type="button" className="text-sm text-primary hover:underline">
                Forgot password?
              </button>
            </div>

            {/* Submit */}
            <motion.button
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
              type="submit"
              disabled={isLoading}
              className={cn(
                "w-full flex items-center justify-center gap-2 rounded-lg",
                "bg-primary text-primary-foreground py-2.5 text-sm font-semibold",
                "hover:opacity-90 transition-all duration-200",
                "disabled:opacity-50 disabled:cursor-not-allowed"
              )}
            >
              {isLoading ? (
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
              ) : (
                <>
                  Sign In
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </motion.button>
          </form>

          {/* Demo accounts */}
          <div className="mt-8">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-border" />
              </div>
              <div className="relative flex justify-center text-xs">
                <span className="bg-background px-3 text-muted-foreground">Demo Accounts</span>
              </div>
            </div>

            <div className="mt-4 grid grid-cols-2 gap-2">
              {[
                { label: "Super Admin", email: "rajesh.kumar@hrcopilot.io" },
                { label: "Employee", email: "arjun.sharma@hrcopilot.io" },
              ].map((demo) => (
                <button
                  key={demo.email}
                  onClick={() => loginAsDemo(demo.email)}
                  className={cn(
                    "rounded-lg border border-border px-3 py-2 text-xs",
                    "hover:bg-muted/50 transition-colors text-left",
                    "flex flex-col"
                  )}
                >
                  <span className="font-medium">{demo.label}</span>
                  <span className="text-[10px] text-muted-foreground truncate">{demo.email}</span>
                </button>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
