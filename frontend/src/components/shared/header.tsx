"use client";

import { cn } from "@/lib/utils";
import { useAuthStore } from "@/stores/auth-store";
import {
  Bell,
  Command,
  Menu,
  MessageSquare,
  Search,
  Sparkles,
} from "lucide-react";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export function Header() {
  const { user } = useAuthStore();
  const [showSearch, setShowSearch] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-border bg-background/80 backdrop-blur-xl px-6">
      {/* Left section */}
      <div className="flex items-center gap-4">
        <div className="relative">
          <button
            onClick={() => setShowSearch(true)}
            className={cn(
              "flex items-center gap-2 rounded-lg border border-input bg-muted/50 px-3 py-2",
              "text-sm text-muted-foreground hover:bg-muted transition-colors",
              "w-64 justify-start"
            )}
          >
            <Search className="h-4 w-4" />
            <span>Search anything...</span>
            <kbd className="ml-auto hidden rounded border border-border bg-background px-1.5 py-0.5 text-[10px] font-mono text-muted-foreground sm:inline-block">
              ⌘K
            </kbd>
          </button>
        </div>
      </div>

      {/* Right section */}
      <div className="flex items-center gap-2">
        {/* AI Copilot quick access */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className={cn(
            "flex items-center gap-2 rounded-lg px-3 py-2",
            "bg-primary/10 text-primary hover:bg-primary/20",
            "text-sm font-medium transition-colors"
          )}
        >
          <Sparkles className="h-4 w-4" />
          <span className="hidden sm:inline">Ask AI</span>
        </motion.button>

        {/* Notifications */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className={cn(
              "flex h-9 w-9 items-center justify-center rounded-lg",
              "text-muted-foreground hover:text-foreground hover:bg-muted",
              "transition-colors relative"
            )}
          >
            <Bell className="h-[18px] w-[18px]" />
            <span className="absolute -top-0.5 -right-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-destructive text-[9px] font-bold text-white">
              3
            </span>
          </button>

          <AnimatePresence>
            {showNotifications && (
              <motion.div
                initial={{ opacity: 0, y: 8, scale: 0.96 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 8, scale: 0.96 }}
                transition={{ duration: 0.15 }}
                className="absolute right-0 top-12 w-80 rounded-xl border border-border bg-popover p-4 shadow-xl"
              >
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-sm font-semibold">Notifications</h3>
                  <button className="text-xs text-primary hover:underline">
                    Mark all read
                  </button>
                </div>
                <div className="space-y-2">
                  {[
                    {
                      title: "Leave Request Approved",
                      desc: "Your casual leave for Jul 15-16 has been approved",
                      time: "2 min ago",
                      type: "success",
                    },
                    {
                      title: "New Candidate Applied",
                      desc: "Arjun Sharma applied for Senior Full-Stack Engineer",
                      time: "1 hour ago",
                      type: "info",
                    },
                    {
                      title: "Performance Review Due",
                      desc: "Complete your Q2 self-review by July 15",
                      time: "3 hours ago",
                      type: "warning",
                    },
                  ].map((notif, i) => (
                    <div
                      key={i}
                      className="flex gap-3 rounded-lg p-2.5 hover:bg-muted/50 transition-colors cursor-pointer"
                    >
                      <div
                        className={cn(
                          "mt-0.5 h-2 w-2 rounded-full shrink-0",
                          notif.type === "success" && "bg-success",
                          notif.type === "info" && "bg-info",
                          notif.type === "warning" && "bg-warning"
                        )}
                      />
                      <div className="min-w-0">
                        <p className="text-xs font-medium truncate">
                          {notif.title}
                        </p>
                        <p className="text-[11px] text-muted-foreground truncate">
                          {notif.desc}
                        </p>
                        <p className="text-[10px] text-muted-foreground mt-0.5">
                          {notif.time}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
                <button className="mt-2 w-full rounded-lg bg-muted/50 py-2 text-xs font-medium text-muted-foreground hover:bg-muted transition-colors">
                  View all notifications
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Messages */}
        <button
          className={cn(
            "flex h-9 w-9 items-center justify-center rounded-lg",
            "text-muted-foreground hover:text-foreground hover:bg-muted",
            "transition-colors"
          )}
        >
          <MessageSquare className="h-[18px] w-[18px]" />
        </button>
      </div>
    </header>
  );
}
