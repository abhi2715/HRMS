import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "@/components/providers";

export const metadata: Metadata = {
  title: "HR Copilot — AI-Powered Human Resource Management",
  description:
    "Autonomous HR Copilot: An Enterprise AI-Powered HRMS featuring intelligent agents for recruitment, payroll, leave management, and employee support.",
  keywords: ["HRMS", "AI", "Human Resources", "Employee Management", "Recruitment", "Payroll"],
  authors: [{ name: "HR Copilot Team" }],
  openGraph: {
    title: "HR Copilot — AI-Powered HRMS",
    description: "Enterprise AI-Powered Human Resource Management System",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body className="min-h-screen bg-background font-sans antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
