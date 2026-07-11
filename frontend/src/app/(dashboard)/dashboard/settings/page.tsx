"use client";

import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import {
  Bell,
  Building2,
  ChevronRight,
  Globe,
  Key,
  Lock,
  Mail,
  Moon,
  Palette,
  Save,
  Shield,
  Smartphone,
  Sun,
  User,
  Users,
} from "lucide-react";
import { useTheme } from "next-themes";
import { useState } from "react";

const settingsSections = [
  { id: "profile", title: "Profile", icon: User, desc: "Personal information and account settings" },
  { id: "security", title: "Security", icon: Shield, desc: "Password, 2FA, and session management" },
  { id: "notifications", title: "Notifications", icon: Bell, desc: "Email and push notification preferences" },
  { id: "appearance", title: "Appearance", icon: Palette, desc: "Theme and display settings" },
  { id: "company", title: "Company", icon: Building2, desc: "Organization-wide settings" },
];

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState("profile");
  const { theme, setTheme } = useTheme();

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Settings</h1>
        <p className="text-sm text-muted-foreground mt-0.5">Manage your account and preferences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar Nav */}
        <div className="lg:col-span-1 space-y-1">
          {settingsSections.map((section) => (
            <button key={section.id} onClick={() => setActiveSection(section.id)}
              className={cn("flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all",
                activeSection === section.id
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground")}>
              <section.icon className="h-4 w-4" />
              {section.title}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="lg:col-span-3">
          {/* Profile */}
          {activeSection === "profile" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
              <div className="rounded-xl border border-border bg-card p-6">
                <h3 className="text-sm font-semibold mb-4">Personal Information</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {[
                    { label: "First Name", value: "System", type: "text" },
                    { label: "Last Name", value: "Administrator", type: "text" },
                    { label: "Email", value: "admin@hrcopilot.ai", type: "email" },
                    { label: "Phone", value: "+91 98765 43210", type: "tel" },
                    { label: "Department", value: "Human Resources", type: "text" },
                    { label: "Designation", value: "HR Manager", type: "text" },
                  ].map((field) => (
                    <div key={field.label}>
                      <label className="text-xs font-medium text-muted-foreground">{field.label}</label>
                      <input type={field.type} defaultValue={field.value}
                        className="mt-1 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
                    </div>
                  ))}
                </div>
                <div className="mt-4 flex justify-end">
                  <button className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:opacity-90">
                    <Save className="h-4 w-4" /> Save Changes
                  </button>
                </div>
              </div>
            </motion.div>
          )}

          {/* Security */}
          {activeSection === "security" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
              <div className="rounded-xl border border-border bg-card p-6">
                <h3 className="text-sm font-semibold mb-4">Change Password</h3>
                <div className="space-y-3 max-w-sm">
                  <div>
                    <label className="text-xs font-medium text-muted-foreground">Current Password</label>
                    <input type="password" className="mt-1 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
                  </div>
                  <div>
                    <label className="text-xs font-medium text-muted-foreground">New Password</label>
                    <input type="password" className="mt-1 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
                  </div>
                  <div>
                    <label className="text-xs font-medium text-muted-foreground">Confirm Password</label>
                    <input type="password" className="mt-1 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
                  </div>
                  <button className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:opacity-90">
                    <Key className="h-4 w-4" /> Update Password
                  </button>
                </div>
              </div>

              <div className="rounded-xl border border-border bg-card p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-semibold">Two-Factor Authentication</h3>
                    <p className="text-xs text-muted-foreground mt-0.5">Add an extra layer of security</p>
                  </div>
                  <button className="rounded-lg border border-border px-3 py-1.5 text-xs font-semibold hover:bg-muted">
                    Enable 2FA
                  </button>
                </div>
              </div>

              <div className="rounded-xl border border-border bg-card p-6">
                <h3 className="text-sm font-semibold mb-3">Active Sessions</h3>
                <div className="space-y-2">
                  {[
                    { device: "Chrome on macOS", location: "Bangalore, India", time: "Current session", current: true },
                    { device: "Safari on iPhone", location: "Bangalore, India", time: "2 hours ago", current: false },
                  ].map((session, i) => (
                    <div key={i} className="flex items-center gap-3 rounded-lg p-3 border border-border/50">
                      <Smartphone className="h-4 w-4 text-muted-foreground" />
                      <div className="flex-1">
                        <p className="text-sm font-medium">{session.device}</p>
                        <p className="text-xs text-muted-foreground">{session.location} • {session.time}</p>
                      </div>
                      {session.current ? (
                        <span className="rounded-full bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400 px-2 py-0.5 text-[10px] font-semibold">
                          Current
                        </span>
                      ) : (
                        <button className="text-xs text-red-500 hover:underline">Revoke</button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {/* Notifications */}
          {activeSection === "notifications" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <div className="rounded-xl border border-border bg-card p-6">
                <h3 className="text-sm font-semibold mb-4">Notification Preferences</h3>
                <div className="space-y-4">
                  {[
                    { title: "Leave Approvals", desc: "Get notified when leave requests need approval", email: true, push: true },
                    { title: "Attendance Alerts", desc: "Late check-in and anomaly notifications", email: true, push: false },
                    { title: "Payroll Processing", desc: "Payroll run completion and payslip availability", email: true, push: true },
                    { title: "Performance Reviews", desc: "Review cycle reminders and feedback requests", email: true, push: true },
                    { title: "Compliance Updates", desc: "New policy publications and acknowledgment reminders", email: true, push: false },
                    { title: "AI Agent Alerts", desc: "AI agent findings and recommendations", email: false, push: true },
                  ].map((pref) => (
                    <div key={pref.title} className="flex items-center justify-between py-2 border-b border-border/50 last:border-0">
                      <div>
                        <p className="text-sm font-medium">{pref.title}</p>
                        <p className="text-xs text-muted-foreground">{pref.desc}</p>
                      </div>
                      <div className="flex items-center gap-4">
                        <label className="flex items-center gap-1.5 text-xs">
                          <input type="checkbox" defaultChecked={pref.email} className="rounded" />
                          <Mail className="h-3.5 w-3.5 text-muted-foreground" /> Email
                        </label>
                        <label className="flex items-center gap-1.5 text-xs">
                          <input type="checkbox" defaultChecked={pref.push} className="rounded" />
                          <Bell className="h-3.5 w-3.5 text-muted-foreground" /> Push
                        </label>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {/* Appearance */}
          {activeSection === "appearance" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <div className="rounded-xl border border-border bg-card p-6">
                <h3 className="text-sm font-semibold mb-4">Theme</h3>
                <div className="grid grid-cols-3 gap-3">
                  {[
                    { value: "light", label: "Light", icon: Sun },
                    { value: "dark", label: "Dark", icon: Moon },
                    { value: "system", label: "System", icon: Globe },
                  ].map((t) => (
                    <button key={t.value} onClick={() => setTheme(t.value)}
                      className={cn("flex flex-col items-center gap-2 rounded-xl border p-4 transition-all",
                        theme === t.value ? "border-primary bg-primary/5" : "border-border hover:border-primary/30")}>
                      <t.icon className={cn("h-6 w-6", theme === t.value ? "text-primary" : "text-muted-foreground")} />
                      <span className="text-xs font-medium">{t.label}</span>
                    </button>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {/* Company */}
          {activeSection === "company" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
              <div className="rounded-xl border border-border bg-card p-6">
                <h3 className="text-sm font-semibold mb-4">Organization Details</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {[
                    { label: "Company Name", value: "HR Copilot Pvt. Ltd." },
                    { label: "Industry", value: "Technology" },
                    { label: "Employees", value: "247" },
                    { label: "Founded", value: "2020" },
                    { label: "Headquarters", value: "Bangalore, India" },
                    { label: "Website", value: "hrcopilot.ai" },
                  ].map((field) => (
                    <div key={field.label}>
                      <label className="text-xs font-medium text-muted-foreground">{field.label}</label>
                      <input type="text" defaultValue={field.value}
                        className="mt-1 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
                    </div>
                  ))}
                </div>
                <div className="mt-4 flex justify-end">
                  <button className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:opacity-90">
                    <Save className="h-4 w-4" /> Save Changes
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
