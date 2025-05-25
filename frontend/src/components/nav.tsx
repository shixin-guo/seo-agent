"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Search, Settings, FileText, Link2, BarChart2 } from "lucide-react"

export function MainNav() {
  const pathname = usePathname()

  return (
    <div className="flex h-16 items-center px-4 border-b">
      <div className="mr-4 flex">
        <Link href="/" className="flex items-center space-x-2">
          <BarChart2 className="h-6 w-6" />
          <span className="font-bold text-xl">SEO Agent</span>
        </Link>
      </div>
      <nav className="flex items-center space-x-4 lg:space-x-6 mx-6">
        <Link
          href="/keyword-research"
          className={cn(
            "text-sm font-medium transition-colors hover:text-primary",
            pathname === "/keyword-research"
              ? "text-primary"
              : "text-muted-foreground"
          )}
        >
          <div className="flex items-center space-x-2">
            <Search className="h-4 w-4" />
            <span>Keyword Research</span>
          </div>
        </Link>
        <Link
          href="/content-optimizer"
          className={cn(
            "text-sm font-medium transition-colors hover:text-primary",
            pathname === "/content-optimizer"
              ? "text-primary"
              : "text-muted-foreground"
          )}
        >
          <div className="flex items-center space-x-2">
            <FileText className="h-4 w-4" />
            <span>Content Optimizer</span>
          </div>
        </Link>
        <Link
          href="/site-auditor"
          className={cn(
            "text-sm font-medium transition-colors hover:text-primary",
            pathname === "/site-auditor"
              ? "text-primary"
              : "text-muted-foreground"
          )}
        >
          <div className="flex items-center space-x-2">
            <BarChart2 className="h-4 w-4" />
            <span>Site Auditor</span>
          </div>
        </Link>
        <Link
          href="/backlink-analyzer"
          className={cn(
            "text-sm font-medium transition-colors hover:text-primary",
            pathname === "/backlink-analyzer"
              ? "text-primary"
              : "text-muted-foreground"
          )}
        >
          <div className="flex items-center space-x-2">
            <Link2 className="h-4 w-4" />
            <span>Backlink Analyzer</span>
          </div>
        </Link>
      </nav>
      <div className="ml-auto flex items-center space-x-4">
        <Link
          href="/settings"
          className={cn(
            "text-sm font-medium transition-colors hover:text-primary",
            pathname === "/settings"
              ? "text-primary"
              : "text-muted-foreground"
          )}
        >
          <div className="flex items-center space-x-2">
            <Settings className="h-4 w-4" />
            <span>Settings</span>
          </div>
        </Link>
      </div>
    </div>
  )
}
