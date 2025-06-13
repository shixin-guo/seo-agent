"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Search, Settings, FileText, Link2, BarChart2, User, CreditCard, LogOut } from "lucide-react";
import { signIn, signOut, useSession } from "next-auth/react";
import { trpc } from "@/lib/trpc";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export function MainNav() {
  const pathname = usePathname();
  const { data: session, status } = useSession();
  const { data: userInfo } = trpc.user.getUserInfo.useQuery(undefined, {
    enabled: !!session?.user,
  });

  const createBillingPortal = trpc.payment.createBillingPortalSession.useMutation({
    onSuccess: (data) => {
      window.open(data.url, '_blank');
    },
  });

  const handleBillingPortal = () => {
    createBillingPortal.mutate();
  };

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
            pathname === "/keyword-research" ? "text-primary" : "text-muted-foreground",
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
            pathname === "/content-optimizer" ? "text-primary" : "text-muted-foreground",
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
            pathname === "/site-auditor" ? "text-primary" : "text-muted-foreground",
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
            pathname === "/backlink-analyzer" ? "text-primary" : "text-muted-foreground",
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
            pathname === "/settings" ? "text-primary" : "text-muted-foreground",
          )}
        >
          <div className="flex items-center space-x-2">
            <Settings className="h-4 w-4" />
            <span>Settings</span>
          </div>
        </Link>
        
        {status === "loading" ? (
          <div className="h-8 w-8 animate-pulse bg-muted rounded-full" />
        ) : session ? (
          <div className="flex items-center space-x-2">
            {userInfo && (
              <div className="text-xs text-muted-foreground">
                {userInfo.planType} Plan
              </div>
            )}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={session.user?.image || ""} alt={session.user?.name || ""} />
                    <AvatarFallback>
                      {session.user?.name?.charAt(0) || session.user?.email?.charAt(0) || "U"}
                    </AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <div className="flex items-center justify-start gap-2 p-2">
                  <div className="flex flex-col space-y-1 leading-none">
                    {session.user?.name && <p className="font-medium">{session.user.name}</p>}
                    {session.user?.email && (
                      <p className="w-[200px] truncate text-sm text-muted-foreground">
                        {session.user.email}
                      </p>
                    )}
                  </div>
                </div>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleBillingPortal} disabled={createBillingPortal.isPending}>
                  <CreditCard className="mr-2 h-4 w-4" />
                  <span>Billing</span>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => signOut()}>
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Log out</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        ) : (
          <Button onClick={() => signIn("google")} variant="default" size="sm">
            Sign In
          </Button>
        )}
      </div>
    </div>
  );
}
