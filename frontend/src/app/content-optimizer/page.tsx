"use client"

import { useState, useRef } from "react"
import { MainNav } from "@/components/nav"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { FileText, Upload, Download, BarChart, PieChart, Tag, CheckCircle, AlertTriangle, XCircle, Lightbulb } from "lucide-react"

interface ContentAnalysis {
  word_count: number
  keyword_density: Record<string, { count: number, density: number }>
  readability: string
  headings: number
  meta_tags: Record<string, string>
  avg_word_length: number
}

interface ContentSuggestion {
  type: string
  suggestion: string
}

interface ContentOptimizationResult {
  original_content: string
  optimized_content: string
  analysis: ContentAnalysis
  suggestions: ContentSuggestion[]
}

export default function ContentOptimizer() {
  const [content, setContent] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState<ContentOptimizationResult | null>(null)
  const [activeTab, setActiveTab] = useState("editor")
  const [useAdvanced, setUseAdvanced] = useState(true)
  const [creative, setCreative] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [keywordsFile, setKeywordsFile] = useState<File | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const keywordsFileInputRef = useRef<HTMLInputElement>(null)

  const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setContent(e.target.value)
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])

      // Read file content
      const reader = new FileReader()
      reader.onload = (event) => {
        if (event.target?.result) {
          setContent(event.target.result as string)
        }
      }
      reader.readAsText(e.target.files[0])
    }
  }

  const handleKeywordsFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setKeywordsFile(e.target.files[0])
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!content && !file) return

    setIsLoading(true)
    try {
      // In a real implementation, this would call the actual API
      // For now, simulating the response
      setTimeout(() => {
        const mockAnalysis: ContentAnalysis = {
          word_count: content.split(/\s+/).filter(Boolean).length,
          keyword_density: {
            "seo": { count: 5, density: 2.5 },
            "content": { count: 8, density: 4.0 },
            "optimization": { count: 3, density: 1.5 }
          },
          readability: "medium",
          headings: (content.match(/^#+\s+.+$/gm) || []).length,
          meta_tags: {},
          avg_word_length: 5.2
        }

        const mockSuggestions: ContentSuggestion[] = [
          { type: "heading", suggestion: "Add more headings to structure your content better." },
          { type: "keyword", suggestion: "Increase usage of keywords: SEO, optimization." },
          { type: "readability", suggestion: "Content has a medium readability score. Consider simplifying some sentences." }
        ]

        const mockResponse: ContentOptimizationResult = {
          original_content: content,
          optimized_content: `# SEO OPTIMIZATION NOTES\nThe following suggestions should be applied to improve SEO:\n\n1. [HEADING] Add more headings to structure your content better.\n2. [KEYWORD] Increase usage of keywords: SEO, optimization.\n3. [READABILITY] Content has a medium readability score. Consider simplifying some sentences.\n\n${content}`,
          analysis: mockAnalysis,
          suggestions: mockSuggestions
        }

        setResults(mockResponse)
        setIsLoading(false)
        setActiveTab("results")
      }, 2000)

      // Actual API call would look like this:
      // const formData = new FormData()
      // if (file) {
      //   formData.append('content_file', file)
      // } else {
      //   const contentBlob = new Blob([content], { type: 'text/plain' })
      //   formData.append('content_file', contentBlob, 'content.txt')
      // }
      //
      // if (keywordsFile) {
      //   formData.append('keywords_file', keywordsFile)
      // }
      //
      // formData.append('use_advanced', useAdvanced.toString())
      // formData.append('creative', creative.toString())
      //
      // const response = await fetch('http://localhost:8000/api/optimize-content', {
      //   method: 'POST',
      //   body: formData,
      // })
      // const data = await response.json()
      // setResults(data)
    } catch (error) {
      console.error('Error optimizing content:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDownload = () => {
    if (!results) return

    const content = results.optimized_content
    const filename = 'optimized-content.txt'

    // Create download link
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="flex min-h-screen flex-col">
      <MainNav />
      <main className="flex-1 p-6">
        <div className="container mx-auto">
          <h1 className="text-3xl font-bold mb-8">Content Optimizer</h1>

          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
            <TabsList>
              <TabsTrigger value="editor">Editor</TabsTrigger>
              <TabsTrigger value="results" disabled={!results}>Results</TabsTrigger>
            </TabsList>

            <TabsContent value="editor">
              <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
                <Card className="lg:col-span-2">
                  <CardHeader>
                    <CardTitle>Content Editor</CardTitle>
                    <CardDescription>
                      Enter your content or upload a file for SEO optimization.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <Button
                          variant="outline"
                          onClick={() => fileInputRef.current?.click()}
                        >
                          <Upload className="mr-2 h-4 w-4" />
                          Upload Content
                        </Button>
                        <input
                          type="file"
                          ref={fileInputRef}
                          className="hidden"
                          accept=".txt,.md"
                          onChange={handleFileChange}
                        />
                        {file && (
                          <div className="text-sm text-muted-foreground">
                            File: {file.name}
                          </div>
                        )}
                      </div>

                      <Textarea
                        placeholder="Enter your content here or upload a file..."
                        className="min-h-[400px] font-mono"
                        value={content}
                        onChange={handleContentChange}
                      />
                    </div>
                  </CardContent>
                </Card>

                <Card className="lg:col-span-1">
                  <CardHeader>
                    <CardTitle>Optimization Settings</CardTitle>
                    <CardDescription>
                      Configure optimization options and add keywords.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-6">
                      <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                          <label htmlFor="advanced" className="text-sm font-medium">
                            Advanced AI Optimization
                          </label>
                          <p className="text-xs text-muted-foreground">
                            Use advanced AI to generate fully optimized content.
                          </p>
                        </div>
                        <Switch
                          id="advanced"
                          checked={useAdvanced}
                          onCheckedChange={setUseAdvanced}
                        />
                      </div>

                      {useAdvanced && (
                        <div className="flex items-center justify-between">
                          <div className="space-y-0.5">
                            <label htmlFor="creative" className="text-sm font-medium">
                              Creative Mode
                            </label>
                            <p className="text-xs text-muted-foreground">
                              Use higher creativity for more varied output.
                            </p>
                          </div>
                          <Switch
                            id="creative"
                            checked={creative}
                            onCheckedChange={setCreative}
                          />
                        </div>
                      )}

                      <div className="space-y-2">
                        <label htmlFor="keywords-file" className="text-sm font-medium">
                          Keywords (Optional)
                        </label>
                        <p className="text-xs text-muted-foreground mb-2">
                          Upload a keywords JSON file to target specific keywords.
                        </p>
                        <Button
                          variant="outline"
                          className="w-full"
                          onClick={() => keywordsFileInputRef.current?.click()}
                        >
                          <Upload className="mr-2 h-4 w-4" />
                          Upload Keywords File
                        </Button>
                        <input
                          type="file"
                          ref={keywordsFileInputRef}
                          className="hidden"
                          accept=".json"
                          onChange={handleKeywordsFileChange}
                        />
                        {keywordsFile && (
                          <div className="text-sm text-muted-foreground mt-2">
                            File: {keywordsFile.name}
                          </div>
                        )}
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button
                      onClick={handleSubmit}
                      disabled={(!content && !file) || isLoading}
                      className="w-full"
                    >
                      {isLoading ? (
                        <span className="flex items-center">
                          <svg className="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Optimizing...
                        </span>
                      ) : (
                        <span className="flex items-center">
                          <FileText className="mr-2 h-4 w-4" />
                          Optimize Content
                        </span>
                      )}
                    </Button>
                  </CardFooter>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="results">
              {results && (
                <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
                  <Card className="lg:col-span-2">
                    <CardHeader>
                      <div className="flex justify-between items-center">
                        <CardTitle>Optimized Content</CardTitle>
                        <Button variant="outline" size="sm" onClick={handleDownload}>
                          <Download className="mr-2 h-4 w-4" />
                          Download
                        </Button>
                      </div>
                      <CardDescription>
                        The optimized version of your content with SEO improvements.
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <Textarea
                        className="min-h-[400px] font-mono"
                        value={results.optimized_content}
                        readOnly
                      />
                    </CardContent>
                  </Card>

                  <div className="space-y-6 lg:col-span-1">
                    <Card>
                      <CardHeader>
                        <CardTitle>Content Analysis</CardTitle>
                        <CardDescription>
                          SEO metrics and content statistics.
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-1">
                              <p className="text-sm font-medium">Word Count</p>
                              <p className="text-2xl font-bold">{results.analysis.word_count}</p>
                            </div>
                            <div className="space-y-1">
                              <p className="text-sm font-medium">Headings</p>
                              <p className="text-2xl font-bold">{results.analysis.headings}</p>
                            </div>
                          </div>

                          <div className="space-y-1">
                            <p className="text-sm font-medium">Readability</p>
                            <div className="flex items-center">
                              <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                                results.analysis.readability === 'simple'
                                  ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
                                  : results.analysis.readability === 'medium'
                                  ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
                                  : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
                              }`}>
                                {results.analysis.readability}
                              </span>
                              <span className="ml-2 text-sm text-muted-foreground">
                                (Avg. word length: {results.analysis.avg_word_length})
                              </span>
                            </div>
                          </div>

                          <div className="space-y-2">
                            <p className="text-sm font-medium">Keyword Density</p>
                            <div className="space-y-2">
                              {Object.entries(results.analysis.keyword_density).map(([keyword, data]) => (
                                <div key={keyword} className="flex justify-between items-center">
                                  <p className="text-sm">{keyword}</p>
                                  <div className="flex items-center">
                                    <span className="text-sm font-medium">{data.count}x</span>
                                    <span className="ml-2 text-xs text-muted-foreground">
                                      ({data.density}%)
                                    </span>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    <Card>
                      <CardHeader>
                        <CardTitle>Optimization Suggestions</CardTitle>
                        <CardDescription>
                          Recommendations to improve your content for SEO.
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          {results.suggestions.map((suggestion, index) => (
                            <div key={index} className="flex">
                              <div className="mr-3 mt-0.5">
                                {suggestion.type === 'heading' ? (
                                  <BarChart className="h-5 w-5 text-blue-500" />
                                ) : suggestion.type === 'keyword' ? (
                                  <Tag className="h-5 w-5 text-green-500" />
                                ) : suggestion.type === 'length' ? (
                                  <FileText className="h-5 w-5 text-purple-500" />
                                ) : suggestion.type === 'readability' ? (
                                  <AlertTriangle className="h-5 w-5 text-yellow-500" />
                                ) : suggestion.type === 'keyword_stuffing' ? (
                                  <XCircle className="h-5 w-5 text-red-500" />
                                ) : (
                                  <Lightbulb className="h-5 w-5 text-amber-500" />
                                )}
                              </div>
                              <div>
                                <p className="text-sm">
                                  {suggestion.suggestion}
                                </p>
                              </div>
                            </div>
                          ))}

                          {results.suggestions.length === 0 && (
                            <div className="flex items-center">
                              <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                              <p className="text-sm">
                                Great job! Your content is already well-optimized.
                              </p>
                            </div>
                          )}
                        </div>
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
