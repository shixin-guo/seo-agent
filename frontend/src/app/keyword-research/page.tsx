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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Download, Search, Tag } from "lucide-react";
import type * as React from "react";
import { useState } from "react";

interface Keyword {
  keyword: string;
  intent: string;
  competition: string;
}

interface KeywordResponse {
  seed_keyword: string;
  industry: string;
  total_keywords: number;
  keywords: Keyword[];
  intent_groups: Record<string, string[]>;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;
debugger
export default function KeywordResearch() {
  const [seedKeyword, setSeedKeyword] = useState("");
  const [industry, setIndustry] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<KeywordResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!seedKeyword) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Make API call to backend
      const response = await fetch(`${API_BASE_URL}/api/keywords`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ seed: seedKeyword, industry }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
        throw new Error(errorData.detail || `API error: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Error generating keywords:", error);

      // Show error message to user
      setError(
        error instanceof Error
          ? error.message
          : "Failed to generate keywords. Please check API keys and try again.",
      );
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
      const header = "keyword,intent,competition\n";
      const rows = results.keywords
        .map((kw) => `${kw.keyword},${kw.intent},${kw.competition}`)
        .join("\n");
      content = header + rows;
      filename = `keywords_${results.seed_keyword.replace(/\s+/g, "_")}.csv`;
    } else {
      // Create JSON content
      content = JSON.stringify(results, null, 2);
      filename = `keywords_${results.seed_keyword.replace(/\s+/g, "_")}.json`;
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
          <h1 className="text-3xl font-bold mb-8">Keyword Research</h1>

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
            <Card className="lg:col-span-1">
              <CardHeader>
                <CardTitle>Generate Keywords</CardTitle>
                <CardDescription>
                  Enter a seed keyword and optional industry to generate related keyword ideas.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="space-y-2">
                    <label htmlFor="seed-keyword" className="text-sm font-medium">
                      Seed Keyword
                    </label>
                    <div className="flex">
                      <Input
                        id="seed-keyword"
                        placeholder="e.g., digital marketing"
                        value={seedKeyword}
                        onChange={(e) => setSeedKeyword(e.target.value)}
                        required
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label htmlFor="industry" className="text-sm font-medium">
                      Industry (Optional)
                    </label>
                    <Input
                      id="industry"
                      placeholder="e.g., technology, healthcare"
                      value={industry}
                      onChange={(e) => setIndustry(e.target.value)}
                    />
                  </div>
                </form>
              </CardContent>
              <CardFooter className="flex flex-col items-stretch">
                <Button
                  onClick={handleSubmit}
                  disabled={!seedKeyword || isLoading}
                  className="w-full mb-2"
                >
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
                      Generating...
                    </span>
                  ) : (
                    <span className="flex items-center">
                      <Search className="mr-2 h-4 w-4" />
                      Generate Keywords
                    </span>
                  )}
                </Button>

                {error && (
                  <div className="w-full p-3 mt-2 text-sm text-red-800 bg-red-100 rounded-md">
                    {error}
                  </div>
                )}
              </CardFooter>
            </Card>

            {results && (
              <Card className="lg:col-span-2">
                <CardHeader>
                  <div className="flex justify-between items-center">
                    <div>
                      <CardTitle>Results for: {results.seed_keyword}</CardTitle>
                      <CardDescription>
                        Found {results.total_keywords} keywords for {results.industry}
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
                  <Tabs defaultValue="all" className="w-full">
                    <TabsList className="grid w-full grid-cols-5">
                      <TabsTrigger value="all">All</TabsTrigger>
                      <TabsTrigger value="informational">Informational</TabsTrigger>
                      <TabsTrigger value="commercial">Commercial</TabsTrigger>
                      <TabsTrigger value="transactional">Transactional</TabsTrigger>
                      <TabsTrigger value="navigational">Navigational</TabsTrigger>
                    </TabsList>

                    <TabsContent value="all" className="mt-4">
                      <div className="border rounded-md">
                        <div className="grid grid-cols-3 font-medium p-3 border-b">
                          <div>Keyword</div>
                          <div>Intent</div>
                          <div>Competition</div>
                        </div>
                        <div className="divide-y">
                          {results.keywords.map((keyword) => (
                            <div key={`${keyword.keyword}-${keyword.intent}`} className="grid grid-cols-3 p-3">
                              <div className="flex items-center">
                                <Tag className="mr-2 h-4 w-4 text-muted-foreground" />
                                {keyword.keyword}
                              </div>
                              <div>
                                <span
                                  className={`inline-flex items-center rounded-full px-2 py-1 text-xs ${
                                    keyword.intent === "informational"
                                      ? "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
                                      : keyword.intent === "commercial"
                                        ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
                                        : keyword.intent === "transactional"
                                          ? "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300"
                                          : "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300"
                                  }`}
                                >
                                  {keyword.intent}
                                </span>
                              </div>
                              <div>
                                <span
                                  className={`inline-flex items-center rounded-full px-2 py-1 text-xs ${
                                    keyword.competition === "low"
                                      ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
                                      : keyword.competition === "medium"
                                        ? "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300"
                                        : "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300"
                                  }`}
                                >
                                  {keyword.competition}
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </TabsContent>

                    {Object.entries(results.intent_groups).map(([intent, keywords]) => (
                      <TabsContent key={intent} value={intent} className="mt-4">
                        <div className="border rounded-md">
                          <div className="grid grid-cols-1 font-medium p-3 border-b">
                            <div>{intent.charAt(0).toUpperCase() + intent.slice(1)} Keywords</div>
                          </div>
                          <div className="divide-y">
                            {keywords.map((keyword) => (
                              <div key={keyword} className="p-3 flex items-center">
                                <Tag className="mr-2 h-4 w-4 text-muted-foreground" />
                                {keyword}
                              </div>
                            ))}
                          </div>
                        </div>
                      </TabsContent>
                    ))}
                  </Tabs>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
