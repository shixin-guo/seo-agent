"use client";

import { MainNav } from "@/components/nav";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Sparkles } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { generateArticle, type ArticleGenerateRequest } from "@/lib/api/api-client";

export default function GenerateArticlePage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [formData, setFormData] = useState<ArticleGenerateRequest>({
    seed_keyword: "",
    industry: "",
    title: "",
    min_length: 800,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.seed_keyword.trim()) {
      setError("Seed keyword is required");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const article = await generateArticle({
        seed_keyword: formData.seed_keyword,
        industry: formData.industry || undefined,
        title: formData.title || undefined,
        min_length: formData.min_length,
      });

      router.push(`/cms/articles/${article.id}/edit`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate article");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen flex-col">
      <MainNav />
      <main className="flex-1 p-6">
        <div className="container mx-auto max-w-2xl">
          <div className="flex items-center mb-8">
            <Link href="/cms">
              <Button variant="outline" size="sm" className="mr-4">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to CMS
              </Button>
            </Link>
            <div>
              <h1 className="text-3xl font-bold">Generate Article</h1>
              <p className="text-muted-foreground mt-2">
                Create SEO-optimized articles using AI and keyword research
              </p>
            </div>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Sparkles className="mr-2 h-5 w-5" />
                AI Article Generation
              </CardTitle>
              <CardDescription>
                Provide a seed keyword and let AI generate a comprehensive SEO article
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="seed_keyword">Seed Keyword *</Label>
                  <Input
                    id="seed_keyword"
                    placeholder="e.g., digital marketing, SEO optimization, content strategy"
                    value={formData.seed_keyword}
                    onChange={(e) =>
                      setFormData({ ...formData, seed_keyword: e.target.value })
                    }
                    required
                  />
                  <p className="text-xs text-muted-foreground">
                    The main keyword to build the article around
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="industry">Industry (Optional)</Label>
                  <Input
                    id="industry"
                    placeholder="e.g., technology, healthcare, finance, e-commerce"
                    value={formData.industry}
                    onChange={(e) =>
                      setFormData({ ...formData, industry: e.target.value })
                    }
                  />
                  <p className="text-xs text-muted-foreground">
                    Industry context for better targeting and relevance
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="title">Custom Title (Optional)</Label>
                  <Input
                    id="title"
                    placeholder="Leave empty to auto-generate title"
                    value={formData.title}
                    onChange={(e) =>
                      setFormData({ ...formData, title: e.target.value })
                    }
                  />
                  <p className="text-xs text-muted-foreground">
                    If not provided, a title will be generated automatically
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="min_length">Minimum Word Count</Label>
                  <Input
                    id="min_length"
                    type="number"
                    min="300"
                    max="3000"
                    value={formData.min_length}
                    onChange={(e) =>
                      setFormData({ ...formData, min_length: parseInt(e.target.value) || 800 })
                    }
                  />
                  <p className="text-xs text-muted-foreground">
                    Target word count for the generated article (300-3000 words)
                  </p>
                </div>

                {error && (
                  <div className="p-4 text-sm text-red-800 bg-red-100 rounded-md">
                    {error}
                  </div>
                )}

                <div className="bg-blue-50 p-4 rounded-md">
                  <h4 className="font-medium text-blue-900 mb-2">What happens next?</h4>
                  <ul className="text-sm text-blue-800 space-y-1">
                    <li>• AI will research related keywords for your seed keyword</li>
                    <li>• A comprehensive article outline will be created</li>
                    <li>• Content will be generated and optimized for SEO</li>
                    <li>• You'll be redirected to edit the generated article</li>
                  </ul>
                </div>

                <div className="flex justify-end space-x-4">
                  <Link href="/cms">
                    <Button variant="outline" type="button">
                      Cancel
                    </Button>
                  </Link>
                  <Button type="submit" disabled={isLoading}>
                    {isLoading ? (
                      <span className="flex items-center">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Generating Article...
                      </span>
                    ) : (
                      <span className="flex items-center">
                        <Sparkles className="mr-2 h-4 w-4" />
                        Generate Article
                      </span>
                    )}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
