"use client"

import { useState } from "react"
import { MainNav } from "@/components/nav"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { BarChart2, Download, Search, CheckCircle, AlertCircle, XCircle, ExternalLink } from "lucide-react"

interface Issue {
  type: string
  severity: "high" | "medium" | "low"
  affected_pages: string[]
  description: string
}

interface Recommendation {
  issue_type: string
  priority: string
  recommendation: string
  affected_pages: string[]
}

interface SiteAuditResult {
  domain: string
  pages_crawled: number
  total_issues: number
  issues_by_severity: {
    high: number
    medium: number
    low: number
  }
  issues: Issue[]
  recommendations: Recommendation[]
  broken_links?: string[]
  summary?: {
    total_pages: number
    total_issues: number
    severity_counts: {
      high: number
      medium: number
      low: number
    }
  }
  action_plan: string
}

export default function SiteAuditor() {
  const [domain, setDomain] = useState("")
  const [maxPages, setMaxPages] = useState(50)
  const [isLoading, setIsLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [results, setResults] = useState<SiteAuditResult | null>(null)
  const [activeTab, setActiveTab] = useState("input")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!domain) return

    setIsLoading(true)
    setProgress(0)
    setActiveTab("results")

    // Simulate progress updates
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 95) {
          clearInterval(progressInterval)
          return prev
        }
        return prev + 5
      })
    }, 500)

    try {
      // In a real implementation, this would call the actual API
      // For now, simulating the response
      setTimeout(() => {
        const mockIssues: Issue[] = [
          {
            type: "missing_meta_description",
            severity: "medium",
            affected_pages: [`https://${domain}/about`, `https://${domain}/contact`],
            description: "Pages missing meta descriptions"
          },
          {
            type: "slow_page_speed",
            severity: "high",
            affected_pages: [`https://${domain}/products`],
            description: "Pages with slow loading times"
          },
          {
            type: "missing_alt_tags",
            severity: "low",
            affected_pages: [`https://${domain}/gallery`, `https://${domain}/blog/post1`],
            description: "Images missing alt text"
          },
          {
            type: "broken_links",
            severity: "high",
            affected_pages: [`https://${domain}/resources/old-page`],
            description: "Pages with broken links"
          }
        ]

        const mockRecommendations: Recommendation[] = issuesWithSeverity.map((issue) => ({
          issue_type: issue.type,
          priority: issue.severity,
          recommendation: `Fix ${issue.type.replace(/_/g, ' ')} on affected pages`,
          affected_pages: issue.affected_pages
        }))

        const mockResult: SiteAuditResult = {
          domain,
          pages_crawled: maxPages,
          total_issues: mockIssues.length,
          issues_by_severity: {
            high: mockIssues.filter(i => i.severity === "high").length,
            medium: mockIssues.filter(i => i.severity === "medium").length,
            low: mockIssues.filter(i => i.severity === "low").length
          },
          issues: mockIssues,
          recommendations: mockRecommendations,
          broken_links: [`https://${domain}/resources/old-page`],
          summary: {
            total_pages: maxPages,
            total_issues: mockIssues.length,
            severity_counts: {
              high: mockIssues.filter(i => i.severity === "high").length,
              medium: mockIssues.filter(i => i.severity === "medium").length,
              low: mockIssues.filter(i => i.severity === "low").length
            }
          },
          action_plan: `# SEO Action Plan for ${domain}

## High Priority Items

- Fix slow page speed on https://${domain}/products
- Fix broken links on https://${domain}/resources/old-page

## Medium Priority Items

- Add meta descriptions to https://${domain}/about and https://${domain}/contact

## Low Priority Items

- Add alt text to images on https://${domain}/gallery and https://${domain}/blog/post1
`
        }

        clearInterval(progressInterval)
        setProgress(100)
        setResults(mockResult)
        setIsLoading(false)
      }, 3000)

      // Actual API call would look like this:
      // const response = await fetch('http://localhost:8000/api/audit-site', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify({ domain, max_pages: maxPages }),
      // })
      // const data = await response.json()
      // clearInterval(progressInterval)
      // setProgress(100)
      // setResults(data)
    } catch (error) {
      clearInterval(progressInterval)
      console.error('Error auditing site:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDownload = () => {
    if (!results) return

    const content = results.action_plan
    const filename = `seo_action_plan_${results.domain.replace(/\./g, '_')}.md`

    // Create download link
    const blob = new Blob([content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  // Ensure we have issues with severity
  const issuesWithSeverity = [
    {
      type: "missing_meta_description",
      severity: "medium",
      affected_pages: [`https://${domain}/about`, `https://${domain}/contact`],
      description: "Pages missing meta descriptions"
    },
    {
      type: "slow_page_speed",
      severity: "high",
      affected_pages: [`https://${domain}/products`],
      description: "Pages with slow loading times"
    },
    {
      type: "missing_alt_tags",
      severity: "low",
      affected_pages: [`https://${domain}/gallery`, `https://${domain}/blog/post1`],
      description: "Images missing alt text"
    },
    {
      type: "broken_links",
      severity: "high",
      affected_pages: [`https://${domain}/resources/old-page`],
      description: "Pages with broken links"
    }
  ]

  return (
    <div className="flex min-h-screen flex-col">
      <MainNav />
      <main className="flex-1 p-6">
        <div className="container mx-auto">
          <h1 className="text-3xl font-bold mb-8">Site Auditor</h1>

          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
            <TabsList>
              <TabsTrigger value="input">Input</TabsTrigger>
              <TabsTrigger value="results" disabled={!results && !isLoading}>Results</TabsTrigger>
            </TabsList>

            <TabsContent value="input">
              <Card>
                <CardHeader>
                  <CardTitle>Audit Configuration</CardTitle>
                  <CardDescription>
                    Enter the domain to audit and configure crawl settings.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-2">
                      <label htmlFor="domain" className="text-sm font-medium">
                        Domain
                      </label>
                      <Input
                        id="domain"
                        placeholder="example.com"
                        value={domain}
                        onChange={(e) => setDomain(e.target.value)}
                        required
                      />
                      <p className="text-xs text-muted-foreground">
                        Enter the domain without http:// or https://
                      </p>
                    </div>

                    <div className="space-y-2">
                      <label htmlFor="max-pages" className="text-sm font-medium">
                        Maximum Pages to Crawl
                      </label>
                      <Input
                        id="max-pages"
                        type="number"
                        min={1}
                        max={200}
                        value={maxPages}
                        onChange={(e) => setMaxPages(parseInt(e.target.value))}
                      />
                      <p className="text-xs text-muted-foreground">
                        Higher values provide more thorough audits but take longer.
                      </p>
                    </div>
                  </form>
                </CardContent>
                <CardFooter>
                  <Button
                    onClick={handleSubmit}
                    disabled={!domain || isLoading}
                    className="w-full"
                  >
                    {isLoading ? (
                      <span className="flex items-center">
                        <svg className="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Starting Audit...
                      </span>
                    ) : (
                      <span className="flex items-center">
                        <BarChart2 className="mr-2 h-4 w-4" />
                        Start Audit
                      </span>
                    )}
                  </Button>
                </CardFooter>
              </Card>
            </TabsContent>

            <TabsContent value="results">
              {isLoading && (
                <Card>
                  <CardHeader>
                    <CardTitle>Auditing {domain}</CardTitle>
                    <CardDescription>
                      Crawling and analyzing your website. This may take a few minutes...
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm font-medium">
                        <span>Progress</span>
                        <span>{progress}%</span>
                      </div>
                      <Progress value={progress} className="h-2" />
                      <p className="text-xs text-muted-foreground text-center mt-4">
                        Currently crawling pages and checking for issues...
                      </p>
                    </div>
                  </CardContent>
                </Card>
              )}

              {!isLoading && results && (
                <div className="space-y-6">
                  <Card>
                    <CardHeader>
                      <div className="flex justify-between items-center">
                        <div>
                          <CardTitle>Audit Summary for {results.domain}</CardTitle>
                          <CardDescription>
                            Analyzed {results.pages_crawled} pages and found {results.total_issues} issues.
                          </CardDescription>
                        </div>
                        <Button variant="outline" size="sm" onClick={handleDownload}>
                          <Download className="mr-2 h-4 w-4" />
                          Download Action Plan
                        </Button>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
                        <div className="flex flex-col items-center space-y-2">
                          <div className="text-5xl font-bold">{results.issues_by_severity.high}</div>
                          <div className="flex items-center">
                            <AlertCircle className="h-4 w-4 text-red-500 mr-1" />
                            <span className="text-sm font-medium">High Priority Issues</span>
                          </div>
                        </div>

                        <div className="flex flex-col items-center space-y-2">
                          <div className="text-5xl font-bold">{results.issues_by_severity.medium}</div>
                          <div className="flex items-center">
                            <AlertCircle className="h-4 w-4 text-yellow-500 mr-1" />
                            <span className="text-sm font-medium">Medium Priority Issues</span>
                          </div>
                        </div>

                        <div className="flex flex-col items-center space-y-2">
                          <div className="text-5xl font-bold">{results.issues_by_severity.low}</div>
                          <div className="flex items-center">
                            <AlertCircle className="h-4 w-4 text-blue-500 mr-1" />
                            <span className="text-sm font-medium">Low Priority Issues</span>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                    <Card>
                      <CardHeader>
                        <CardTitle>Issues Found</CardTitle>
                        <CardDescription>
                          Technical SEO issues detected during the audit.
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          {results.issues.map((issue, index) => (
                            <div key={index} className="border rounded-md p-4">
                              <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center">
                                  {issue.severity === "high" ? (
                                    <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
                                  ) : issue.severity === "medium" ? (
                                    <AlertCircle className="h-5 w-5 text-yellow-500 mr-2" />
                                  ) : (
                                    <AlertCircle className="h-5 w-5 text-blue-500 mr-2" />
                                  )}
                                  <span className="font-medium">
                                    {issue.type.replace(/_/g, ' ')}
                                  </span>
                                </div>
                                <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                                  issue.severity === 'high'
                                    ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
                                    : issue.severity === 'medium'
                                    ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
                                    : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
                                }`}>
                                  {issue.severity}
                                </span>
                              </div>
                              <p className="text-sm text-muted-foreground mb-2">
                                {issue.description}
                              </p>
                              <div className="text-xs text-muted-foreground">
                                <div className="font-medium mb-1">Affected Pages:</div>
                                <ul className="space-y-1">
                                  {issue.affected_pages.map((page, i) => (
                                    <li key={i} className="flex items-center">
                                      <ExternalLink className="h-3 w-3 mr-1" />
                                      <span>{page}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>

                    <Card>
                      <CardHeader>
                        <CardTitle>Action Plan</CardTitle>
                        <CardDescription>
                          Prioritized recommendations to improve your site's SEO.
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <Textarea
                          className="min-h-[400px] font-mono"
                          value={results.action_plan}
                          readOnly
                        />
                      </CardContent>
                    </Card>
                  </div>
                </div>
              )}
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  )
}
