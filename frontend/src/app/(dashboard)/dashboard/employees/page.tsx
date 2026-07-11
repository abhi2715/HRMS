"use client";

import { cn, formatCurrency, formatDate, getInitials, stringToColor } from "@/lib/utils";
import { motion } from "framer-motion";
import {
  Building2,
  ChevronDown,
  Download,
  Filter,
  MapPin,
  MoreHorizontal,
  Plus,
  Search,
  SlidersHorizontal,
  UserPlus,
  Users,
  X,
} from "lucide-react";
import { useState } from "react";

// Mock data for the employee list
const employees = [
  { id: "1", code: "EMP001", name: "System Administrator", email: "admin@hrcopilot.ai", department: "Human Resources", designation: "HR Manager", type: "full_time", status: "active", location: "Bangalore", joining: "2020-01-01", avatar: null },
  { id: "2", code: "EMP002", name: "Kavita Sharma", email: "hr@hrcopilot.ai", department: "Human Resources", designation: "HR Manager", type: "full_time", status: "active", location: "Bangalore", joining: "2021-03-15", avatar: null },
  { id: "3", code: "EMP003", name: "Priya Gupta", email: "recruiter@hrcopilot.ai", department: "Human Resources", designation: "Recruiter", type: "full_time", status: "active", location: "Mumbai", joining: "2021-06-20", avatar: null },
  { id: "4", code: "EMP004", name: "Sanjay Mehta", email: "payroll@hrcopilot.ai", department: "Finance", designation: "Finance Manager", type: "full_time", status: "active", location: "Bangalore", joining: "2021-01-10", avatar: null },
  { id: "5", code: "EMP005", name: "Vikram Reddy", email: "manager@hrcopilot.ai", department: "Engineering", designation: "Engineering Manager", type: "full_time", status: "active", location: "Hyderabad", joining: "2021-08-01", avatar: null },
  { id: "6", code: "EMP006", name: "Rahul Kumar", email: "employee@hrcopilot.ai", department: "Engineering", designation: "Software Engineer", type: "full_time", status: "active", location: "Bangalore", joining: "2022-02-15", avatar: null },
  { id: "7", code: "EMP007", name: "Deepak Verma", email: "deepak.verma@hrcopilot.ai", department: "Data Science", designation: "ML Engineer", type: "full_time", status: "active", location: "Pune", joining: "2022-04-01", avatar: null },
  { id: "8", code: "EMP008", name: "Sneha Nair", email: "sneha.nair@hrcopilot.ai", department: "Design", designation: "Lead Designer", type: "full_time", status: "active", location: "Bangalore", joining: "2021-11-15", avatar: null },
  { id: "9", code: "EMP009", name: "Ananya Patel", email: "ananya.patel@hrcopilot.ai", department: "Product", designation: "Product Manager", type: "full_time", status: "active", location: "Mumbai", joining: "2022-07-01", avatar: null },
  { id: "10", code: "EMP010", name: "Rohit Singh", email: "rohit.singh@hrcopilot.ai", department: "Engineering", designation: "DevOps Engineer", type: "full_time", status: "active", location: "Gurgaon", joining: "2023-01-09", avatar: null },
  { id: "11", code: "EMP011", name: "Meera Iyer", email: "meera.iyer@hrcopilot.ai", department: "Marketing", designation: "Marketing Manager", type: "full_time", status: "active", location: "Chennai", joining: "2022-05-16", avatar: null },
  { id: "12", code: "EMP012", name: "Karan Chauhan", email: "karan.c@hrcopilot.ai", department: "Sales", designation: "Sales Executive", type: "full_time", status: "active", location: "Delhi", joining: "2023-03-20", avatar: null },
  { id: "13", code: "EMP013", name: "Divya Kapoor", email: "divya.k@hrcopilot.ai", department: "Engineering", designation: "Senior Software Engineer", type: "full_time", status: "active", location: "Bangalore", joining: "2021-09-12", avatar: null },
  { id: "14", code: "EMP014", name: "Nikhil Saxena", email: "nikhil.s@hrcopilot.ai", department: "Quality Assurance", designation: "QA Engineer", type: "full_time", status: "active", location: "Noida", joining: "2023-06-05", avatar: null },
  { id: "15", code: "EMP015", name: "Pallavi Joshi", email: "pallavi.j@hrcopilot.ai", department: "Operations", designation: "Project Manager", type: "full_time", status: "on_notice", location: "Pune", joining: "2022-01-18", avatar: null },
];

const departments = ["All", "Engineering", "Product", "Design", "Marketing", "Sales", "Human Resources", "Finance", "Data Science", "Quality Assurance", "Operations"];
const statuses = ["All", "active", "on_notice", "probation", "terminated"];

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.03 } },
};

const itemVariants = {
  hidden: { opacity: 0, y: 8 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3 } },
};

export default function EmployeesPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedDept, setSelectedDept] = useState("All");
  const [selectedStatus, setSelectedStatus] = useState("All");
  const [viewMode, setViewMode] = useState<"table" | "grid">("table");

  const filteredEmployees = employees.filter((emp) => {
    const matchesSearch =
      emp.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      emp.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
      emp.code.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDept = selectedDept === "All" || emp.department === selectedDept;
    const matchesStatus = selectedStatus === "All" || emp.status === selectedStatus;
    return matchesSearch && matchesDept && matchesStatus;
  });

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Employees</h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            Manage your workforce — {employees.length} total employees
          </p>
        </div>
        <div className="flex items-center gap-2">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center gap-2 rounded-lg border border-border px-3 py-2 text-sm font-medium hover:bg-muted transition-colors"
          >
            <Download className="h-4 w-4" />
            Export
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity"
          >
            <UserPlus className="h-4 w-4" />
            Add Employee
          </motion.button>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Total", value: employees.length, color: "text-indigo-500", bg: "bg-indigo-50 dark:bg-indigo-950/30" },
          { label: "Active", value: employees.filter(e => e.status === "active").length, color: "text-emerald-500", bg: "bg-emerald-50 dark:bg-emerald-950/30" },
          { label: "On Notice", value: employees.filter(e => e.status === "on_notice").length, color: "text-amber-500", bg: "bg-amber-50 dark:bg-amber-950/30" },
          { label: "Departments", value: new Set(employees.map(e => e.department)).size, color: "text-purple-500", bg: "bg-purple-50 dark:bg-purple-950/30" },
        ].map((stat) => (
          <div key={stat.label} className={cn("rounded-xl border border-border p-4", stat.bg)}>
            <p className="text-xs text-muted-foreground">{stat.label}</p>
            <p className={cn("text-2xl font-bold mt-1", stat.color)}>{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Filters Bar */}
      <div className="flex flex-col sm:flex-row gap-3">
        {/* Search */}
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by name, email, or code..."
            className="w-full rounded-lg border border-input bg-background pl-10 pr-4 py-2.5 text-sm placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-ring transition-all"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>

        {/* Department Filter */}
        <div className="relative">
          <select
            value={selectedDept}
            onChange={(e) => setSelectedDept(e.target.value)}
            className="appearance-none rounded-lg border border-input bg-background pl-3 pr-8 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring cursor-pointer"
          >
            {departments.map((d) => (
              <option key={d} value={d}>
                {d === "All" ? "All Departments" : d}
              </option>
            ))}
          </select>
          <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
        </div>

        {/* Status Filter */}
        <div className="relative">
          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="appearance-none rounded-lg border border-input bg-background pl-3 pr-8 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring cursor-pointer"
          >
            {statuses.map((s) => (
              <option key={s} value={s}>
                {s === "All" ? "All Status" : s.replace("_", " ").replace(/\b\w/g, (c) => c.toUpperCase())}
              </option>
            ))}
          </select>
          <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
        </div>

        {/* View Toggle */}
        <div className="flex rounded-lg border border-border overflow-hidden">
          <button
            onClick={() => setViewMode("table")}
            className={cn(
              "px-3 py-2.5 text-sm transition-colors",
              viewMode === "table" ? "bg-primary text-primary-foreground" : "bg-background hover:bg-muted"
            )}
          >
            <SlidersHorizontal className="h-4 w-4" />
          </button>
          <button
            onClick={() => setViewMode("grid")}
            className={cn(
              "px-3 py-2.5 text-sm transition-colors",
              viewMode === "grid" ? "bg-primary text-primary-foreground" : "bg-background hover:bg-muted"
            )}
          >
            <Users className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Results Count */}
      <div className="flex items-center justify-between text-sm">
        <p className="text-muted-foreground">
          Showing <span className="font-medium text-foreground">{filteredEmployees.length}</span> of{" "}
          {employees.length} employees
        </p>
      </div>

      {/* Table View */}
      {viewMode === "table" && (
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="rounded-xl border border-border overflow-hidden"
        >
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border bg-muted/50">
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase tracking-wider py-3 px-4">Employee</th>
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase tracking-wider py-3 px-4">Department</th>
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase tracking-wider py-3 px-4">Designation</th>
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase tracking-wider py-3 px-4">Location</th>
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase tracking-wider py-3 px-4">Joined</th>
                  <th className="text-left text-xs font-medium text-muted-foreground uppercase tracking-wider py-3 px-4">Status</th>
                  <th className="text-right text-xs font-medium text-muted-foreground uppercase tracking-wider py-3 px-4"></th>
                </tr>
              </thead>
              <tbody>
                {filteredEmployees.map((emp) => (
                  <motion.tr
                    key={emp.id}
                    variants={itemVariants}
                    className="border-b border-border/50 hover:bg-muted/30 transition-colors cursor-pointer"
                  >
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-3">
                        <div className={cn(
                          "flex h-9 w-9 items-center justify-center rounded-full text-white text-xs font-bold shrink-0",
                          stringToColor(emp.name)
                        )}>
                          {getInitials(emp.name)}
                        </div>
                        <div>
                          <p className="text-sm font-medium">{emp.name}</p>
                          <p className="text-xs text-muted-foreground">{emp.code} • {emp.email}</p>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-1.5">
                        <Building2 className="h-3.5 w-3.5 text-muted-foreground" />
                        <span className="text-sm">{emp.department}</span>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-sm">{emp.designation}</span>
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-1.5">
                        <MapPin className="h-3.5 w-3.5 text-muted-foreground" />
                        <span className="text-sm">{emp.location}</span>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-sm text-muted-foreground">
                        {formatDate(emp.joining)}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={cn(
                        "inline-flex items-center rounded-full px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider",
                        emp.status === "active" && "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400",
                        emp.status === "on_notice" && "bg-amber-50 text-amber-700 dark:bg-amber-950/30 dark:text-amber-400",
                        emp.status === "probation" && "bg-blue-50 text-blue-700 dark:bg-blue-950/30 dark:text-blue-400",
                        emp.status === "terminated" && "bg-red-50 text-red-700 dark:bg-red-950/30 dark:text-red-400",
                      )}>
                        {emp.status.replace("_", " ")}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button className="text-muted-foreground hover:text-foreground transition-colors">
                        <MoreHorizontal className="h-4 w-4" />
                      </button>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      )}

      {/* Grid View */}
      {viewMode === "grid" && (
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
        >
          {filteredEmployees.map((emp) => (
            <motion.div
              key={emp.id}
              variants={itemVariants}
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
              className="group rounded-xl border border-border bg-card p-5 hover:shadow-lg hover:border-primary/20 transition-all duration-300 cursor-pointer"
            >
              <div className="flex items-start justify-between">
                <div className={cn(
                  "flex h-12 w-12 items-center justify-center rounded-xl text-white text-sm font-bold",
                  stringToColor(emp.name)
                )}>
                  {getInitials(emp.name)}
                </div>
                <span className={cn(
                  "inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase",
                  emp.status === "active" && "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400",
                  emp.status === "on_notice" && "bg-amber-50 text-amber-700 dark:bg-amber-950/30 dark:text-amber-400",
                )}>
                  {emp.status.replace("_", " ")}
                </span>
              </div>

              <div className="mt-3">
                <h3 className="text-sm font-semibold">{emp.name}</h3>
                <p className="text-xs text-muted-foreground mt-0.5">{emp.designation}</p>
              </div>

              <div className="mt-3 space-y-1.5">
                <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                  <Building2 className="h-3 w-3" />
                  {emp.department}
                </div>
                <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                  <MapPin className="h-3 w-3" />
                  {emp.location}
                </div>
              </div>

              <div className="mt-3 pt-3 border-t border-border/50 flex items-center justify-between">
                <span className="text-[10px] text-muted-foreground">{emp.code}</span>
                <span className="text-[10px] text-muted-foreground">{formatDate(emp.joining)}</span>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* Empty State */}
      {filteredEmployees.length === 0 && (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <Users className="h-12 w-12 text-muted-foreground/30 mb-4" />
          <h3 className="text-sm font-semibold">No employees found</h3>
          <p className="text-xs text-muted-foreground mt-1">
            Try adjusting your search or filters
          </p>
        </div>
      )}
    </motion.div>
  );
}
