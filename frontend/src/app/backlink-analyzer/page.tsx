"use client";

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
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import {
  Download,
  ExternalLink,
  Link2,
  Mail,
} from "lucide-react";
import type * as React from "react";
import { useState } from "react";

interface BacklinkSummary {
  total_backlinks: number;
  unique_domains: number;
  dofollow_count: number;
  nofollow_count: number;
}

interface BacklinkOpportunity {
  source_domain: string;
  source_url: string;
  domain_authority: string | number;
  link_type: string;
  competitor: string;
  opportunity_score: number;
}

interface CompetitorData {
  [key: string]: {
    backlinks?: any[];
    domain_authority?: number;
  };
}

interface BacklinkAnalysisResult {
  domain: string;
  summary: BacklinkSummary;
  opportunities: BacklinkOpportunity[];
  competitors: CompetitorData;
  templates?: Record<string, string>;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export default function BacklinkAnalyzer() {
  const [domain, setDomain] = useState("");
  const [competitors, setCompetitors] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<BacklinkAnalysisResult | null>(null);
  const [activeTab, setActiveTab] = useState("input");
  const [generateTemplates, setGenerateTemplates] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!domain) {
      return;
    }

    setIsLoading(true);
    try {
      const competitorsList = competitors.split(",").map(c => c.trim()).filter(Boolean);
      const response = await fetch(`${API_BASE_URL}/api/backlink-analysis`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          domain,
          competitors: competitorsList,
          generate_templates: generateTemplates
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
      setActiveTab("results");
    } catch (error) {
      console.error("Error analyzing backlinks:", error);
      // You might want to show an error message to the user here
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = (format: "csv" | "json") => {
    if (!results) {
      return;
    }

    let content: string;
    let filename: string;

    if (format === "csv") {
      // Create CSV content
      const header =
        "source_domain,source_url,domain_authority,link_type,competitor,opportunity_score\n";
      const rows = results.opportunities
        .map(
          (opp) =>
            `${opp.source_domain},${opp.source_url},${opp.domain_authority},${opp.link_type},${opp.competitor},${opp.opportunity_score}`,
        )
        .join("\n");
      content = header + rows;
      filename = `backlink_opportunities_${results.domain.replace(/\./g, "_")}.csv`;
    } else {
      // Create JSON content
      content = JSON.stringify(results, null, 2);
      filename = `backlink_analysis_${results.domain.replace(/\./g, "_")}.json`;
    }

    // Create download link
    const blob = new Blob([content], { type: format === "csv" ? "text/csv" : "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex min-h-screen flex-col">
      <MainNav />
      <main className="flex-1 p-6">
        <div className="container mx-auto">
          <h1 className="text-3xl font-bold mb-8">Backlink Analyzer</h1>

          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
            <TabsList>
              <TabsTrigger value="input">Input</TabsTrigger>
              <TabsTrigger value="results" disabled={!results}>
                Results
              </TabsTrigger>
              {results?.templates && Object.keys(results.templates).length > 0 && (
                <TabsTrigger value="templates">Outreach Templates</TabsTrigger>
              )}
            </TabsList>

            <TabsContent value="input">
              <Card>
                <CardHeader>
                  <CardTitle>Backlink Analysis Configuration</CardTitle>
                  <CardDescription>
                    Enter your domain and competitor domains to analyze backlink opportunities.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-2">
                      <label htmlFor="domain" className="text-sm font-medium">
                        Your Domain
                      </label>
                      <Input
                        id="domain"
                        placeholder="yourdomain.com"
                        value={domain}
                        onChange={(e) => setDomain(e.target.value)}
                        required
                      />
                      <p className="text-xs text-muted-foreground">
                        Enter the domain without http:// or https://
                      </p>
                    </div>

                    <div className="space-y-2">
                      <label htmlFor="competitors" className="text-sm font-medium">
                        Competitor Domains
                      </label>
                      <Input
                        id="competitors"
                        placeholder="competitor1.com, competitor2.com"
                        value={competitors}
                        onChange={(e) => setCompetitors(e.target.value)}
                      />
                      <p className="text-xs text-muted-foreground">
                        Enter competitor domains separated by commas
                      </p>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <label htmlFor="templates" className="text-sm font-medium">
                          Generate Outreach Templates
                        </label>
                        <p className="text-xs text-muted-foreground">
                          Create email templates for outreach to potential link sources
                        </p>
                      </div>
                      <Switch
                        id="templates"
                        checked={generateTemplates}
                        onCheckedChange={setGenerateTemplates}
                      />
                    </div>
                  </form>
                </CardContent>
                <CardFooter>
                  <Button onClick={handleSubmit} disabled={!domain || isLoading} className="w-full">
                    {isLoading ? (
                      <span className="flex items-center">
                        <svg
                          className="animate-spin -ml-1 mr-2 h-4 w-4"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          />
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          />
                        </svg>
                        Analyzing...
                      </span>
                    ) : (
                      <span className="flex items-center">
                        <Link2 className="mr-2 h-4 w-4" />
                        Analyze Backlinks
                      </span>
                    )}
                  </Button>
                </CardFooter>
              </Card>
            </TabsContent>

            <TabsContent value="results">
              {results && (
                <div className="space-y-6">
                  <Card>
                    <CardHeader>
                      <div className="flex justify-between items-center">
                        <div>
                          <CardTitle>Backlink Analysis for {results.domain}</CardTitle>
                          <CardDescription>
                            Overview of your current backlink profile
                          </CardDescription>
                        </div>
                        <div className="flex space-x-2">
                          <Button variant="outline" size="sm" onClick={() => handleExport("csv")}>
                            <Download className="mr-2 h-4 w-4" />
                            CSV
                          </Button>
                          <Button variant="outline" size="sm" onClick={() => handleExport("json")}>
                            <Download className="mr-2 h-4 w-4" />
                            JSON
                          </Button>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-2 gap-6 md:grid-cols-4">
                        <div className="flex flex-col items-center space-y-2">
                          <div className="text-4xl font-bold">
                            {results.summary.total_backlinks}
                          </div>
                          <div className="text-sm font-medium text-center">Total Backlinks</div>
                        </div>

                        <div className="flex flex-col items-center space-y-2">
                          <div className="text-4xl font-bold">{results.summary.unique_domains}</div>
                          <div className="text-sm font-medium text-center">
                            Unique Referring Domains
                          </div>
                        </div>

                        <div className="flex flex-col items-center space-y-2">
                          <div className="text-4xl font-bold">{results.summary.dofollow_count}</div>
                          <div className="text-sm font-medium text-center">Dofollow Links</div>
                        </div>

                        <div className="flex flex-col items-center space-y-2">
                          <div className="text-4xl font-bold">{results.summary.nofollow_count}</div>
                          <div className="text-sm font-medium text-center">Nofollow Links</div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {Object.keys(results.competitors).length > 0 && (
                    <Card>
                      <CardHeader>
                        <CardTitle>Competitor Analysis</CardTitle>
                        <CardDescription>
                          Comparing your backlink profile with competitors
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="border rounded-md">
                          <div className="grid grid-cols-2 font-medium p-3 border-b">
                            <div>Domain</div>
                            <div>Estimated Backlinks</div>
                          </div>
                          <div className="divide-y">
                            <div className="grid grid-cols-2 p-3 bg-muted/50">
                              <div className="font-medium">{results.domain}</div>
                              <div>{results.summary.total_backlinks}</div>
                            </div>
                            {Object.entries(results.competitors).map(([competitor, data]) => (
                              <div key={competitor} className="grid grid-cols-2 p-3">
                                <div>{competitor}</div>
                                <div>{data.backlinks?.length || 0}</div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  )}

                  <Card>
                    <CardHeader>
                      <CardTitle>Backlink Opportunities</CardTitle>
                      <CardDescription>
                        Potential sites that might link to your content
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="border rounded-md">
                        <div className="grid grid-cols-6 font-medium p-3 border-b">
                          <div className="col-span-2">Source</div>
                          <div>DA</div>
                          <div>Type</div>
                          <div>Competitor</div>
                          <div>Score</div>
                        </div>
                        <div className="divide-y">
                          {results.opportunities.map((opp) => (
                            <div key={`${opp.source_domain}-${opp.source_url}`} className="grid grid-cols-6 p-3">
                              <div className="col-span-2">
                                <div className="font-medium">{opp.source_domain}</div>
                                <div className="text-xs text-muted-foreground flex items-center mt-1">
                                  <ExternalLink className="h-3 w-3 mr-1" />
                                  <a
                                    href={opp.source_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="hover:underline truncate"
                                  >
                                    {opp.source_url}
                                  </a>
                                </div>
                              </div>
                              <div>{opp.domain_authority}</div>
                              <div>
                                <span
                                  className={`inline-flex items-center rounded-full px-2 py-1 text-xs ${
                                    opp.link_type === "dofollow"
                                      ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
                                      : "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300"
                                  }`}
                                >
                                  {opp.link_type}
                                </span>
                              </div>
                              <div className="truncate">{opp.competitor}</div>
                              <div>
                                <span
                                  className={`inline-flex items-center rounded-full px-2 py-1 text-xs ${
                                    opp.opportunity_score >= 70
                                      ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
                                      : opp.opportunity_score >= 40
                                        ? "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300"
                                        : "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300"
                                  }`}
                                >
                                  {opp.opportunity_score}
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}
            </TabsContent>

            {results?.templates && (
              <TabsContent value="templates">
                <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
                  <Card className="lg:col-span-1">
                    <CardHeader>
                      <CardTitle>Template Types</CardTitle>
                      <CardDescription>Select a template type to view</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        {Object.keys(results.templates).map((templateType) => (
                          <Button
                            key={templateType}
                            variant={selectedTemplate === templateType ? "default" : "outline"}
                            className="w-full justify-start"
                            onClick={() => setSelectedTemplate(templateType)}
                          >
                            {templateType === "resource_mention" ? (
                              <Link2 className="mr-2 h-4 w-4" />
                            ) : templateType === "broken_link" ? (
                              <ExternalLink className="mr-2 h-4 w-4" />
                            ) : (
                              <Mail className="mr-2 h-4 w-4" />
                            )}
                            {templateType.replace(/_/g, " ")}
                          </Button>
                        ))}
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="lg:col-span-2">
                    <CardHeader>
                      <CardTitle>
                        {selectedTemplate
                          ? `${selectedTemplate.replace(/_/g, " ")} Template`
                          : "Select a Template"}
                      </CardTitle>
                      <CardDescription>
                        {selectedTemplate
                          ? "Customize this template for your outreach efforts"
                          : "Choose a template type from the left"}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      {selectedTemplate ? (
                        <Textarea
                          className="min-h-[400px] font-mono"
                          value={results.templates[selectedTemplate]}
                          readOnly
                        />
                      ) : (
                        <div className="flex flex-col items-center justify-center h-[400px] border rounded-md p-6">
                          <Mail className="h-16 w-16 text-muted-foreground mb-4" />
                          <p className="text-center text-muted-foreground">
                            Select a template type to view the email template
                          </p>
                        </div>
                      )}
                    </CardContent>
                    {selectedTemplate && (
                      <CardFooter>
                        <Button
                          onClick={() => {
                            if (!results?.templates) { return; }
                            // Create download link
                            const content = results.templates[selectedTemplate];
                            const filename = `${selectedTemplate.replace(/_/g, "-")}-template.txt`;
                            const blob = new Blob([content], { type: "text/plain" });
                            const url = URL.createObjectURL(blob);
                            const a = document.createElement("a");
                            a.href = url;
                            a.download = filename;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                            URL.revokeObjectURL(url);
                          }}
                          className="w-full"
                        >
                          <Download className="mr-2 h-4 w-4" />
                          Download Template
                        </Button>
                      </CardFooter>
                    )}
                  </Card>
                </div>
              </TabsContent>
            )}
          </Tabs>
        </div>
      </main>
    </div>
  );
}
