import Link from "next/link";
import { MainNav } from "@/components/nav";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Search, FileText, BarChart2, Link2 } from "lucide-react";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <MainNav />
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl">
                SEO Agent - AI-powered SEO Automation
              </h1>
              <p className="max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400">
                Optimize your content, research keywords, analyze backlinks, and audit your site
                with AI-powered SEO tools.
              </p>
            </div>
          </div>
        </section>

        <section className="w-full py-12 md:py-24 lg:py-32 bg-muted/50">
          <div className="container px-4 md:px-6">
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
              <Card>
                <CardHeader>
                  <Search className="h-8 w-8 mb-2" />
                  <CardTitle>Keyword Research</CardTitle>
                  <CardDescription>
                    Generate and analyze SEO keywords with AI-powered suggestions.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm">
                    Expand seed keywords, analyze competition, and export to CSV/JSON.
                  </p>
                </CardContent>
                <CardFooter>
                  <Link href="/keyword-research" className="w-full">
                    <Button className="w-full">Start Research</Button>
                  </Link>
                </CardFooter>
              </Card>

              <Card>
                <CardHeader>
                  <FileText className="h-8 w-8 mb-2" />
                  <CardTitle>Content Optimizer</CardTitle>
                  <CardDescription>
                    Optimize your content for search engines with AI suggestions.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm">
                    Analyze content, receive optimization suggestions, and improve SEO factors.
                  </p>
                </CardContent>
                <CardFooter>
                  <Link href="/content-optimizer" className="w-full">
                    <Button className="w-full">Optimize Content</Button>
                  </Link>
                </CardFooter>
              </Card>

              <Card>
                <CardHeader>
                  <BarChart2 className="h-8 w-8 mb-2" />
                  <CardTitle>Site Auditor</CardTitle>
                  <CardDescription>
                    Perform technical SEO audits on your website automatically.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm">
                    Detect technical issues, receive prioritized recommendations, and generate
                    action plans.
                  </p>
                </CardContent>
                <CardFooter>
                  <Link href="/site-auditor" className="w-full">
                    <Button className="w-full">Audit Site</Button>
                  </Link>
                </CardFooter>
              </Card>

              <Card>
                <CardHeader>
                  <Link2 className="h-8 w-8 mb-2" />
                  <CardTitle>Backlink Analyzer</CardTitle>
                  <CardDescription>
                    Research backlink opportunities and analyze competitor profiles.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm">
                    Identify opportunities, compare with competitors, and generate outreach
                    templates.
                  </p>
                </CardContent>
                <CardFooter>
                  <Link href="/backlink-analyzer" className="w-full">
                    <Button className="w-full">Analyze Backlinks</Button>
                  </Link>
                </CardFooter>
              </Card>
            </div>
          </div>
        </section>
      </main>

      <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full border-t items-center justify-between px-8 md:px-16">
        <p className="text-xs text-gray-500 dark:text-gray-400">
          © 2025 SEO Agent. All rights reserved.
        </p>
        <p className="text-xs text-gray-500 dark:text-gray-400">
          Built with Next.js, shadcn/ui, and FastAPI
        </p>
      </footer>
    </div>
  );
}
