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
import { BookOpen, FileText, Plus, Search } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import { getArticles, type Article } from "@/lib/api/api-client";

export default function CMSPage() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const response = await getArticles(10, 0);
        setArticles(response.articles);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch articles");
      } finally {
        setIsLoading(false);
      }
    };

    fetchArticles();
  }, []);

  return (
    <div className="flex min-h-screen flex-col">
      <MainNav />
      <main className="flex-1 p-6">
        <div className="container mx-auto">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold">Content Management</h1>
              <p className="text-muted-foreground mt-2">
                Manage your SEO articles and generate new content
              </p>
            </div>
            <div className="flex space-x-4">
              <Link href="/cms/articles/new">
                <Button>
                  <Plus className="mr-2 h-4 w-4" />
                  New Article
                </Button>
              </Link>
              <Link href="/cms/generate">
                <Button variant="outline">
                  <Search className="mr-2 h-4 w-4" />
                  Generate from Keywords
                </Button>
              </Link>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3 mb-8">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <FileText className="mr-2 h-5 w-5" />
                  All Articles
                </CardTitle>
                <CardDescription>
                  View and manage all your SEO articles
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Link href="/cms/articles">
                  <Button className="w-full">View Articles</Button>
                </Link>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Plus className="mr-2 h-5 w-5" />
                  Create Article
                </CardTitle>
                <CardDescription>
                  Write a new SEO-optimized article from scratch
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Link href="/cms/articles/new">
                  <Button className="w-full">Create New</Button>
                </Link>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Search className="mr-2 h-5 w-5" />
                  Generate Content
                </CardTitle>
                <CardDescription>
                  Generate articles using AI and keyword research
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Link href="/cms/generate">
                  <Button className="w-full">Generate Article</Button>
                </Link>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Recent Articles</CardTitle>
              <CardDescription>
                Your most recently updated articles
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
                  <p className="mt-2 text-muted-foreground">Loading articles...</p>
                </div>
              ) : error ? (
                <div className="text-center py-8">
                  <p className="text-red-600">{error}</p>
                </div>
              ) : articles.length === 0 ? (
                <div className="text-center py-8">
                  <BookOpen className="mx-auto h-12 w-12 text-muted-foreground" />
                  <p className="mt-4 text-lg font-medium">No articles yet</p>
                  <p className="text-muted-foreground">
                    Create your first article to get started
                  </p>
                  <Link href="/cms/articles/new" className="mt-4 inline-block">
                    <Button>
                      <Plus className="mr-2 h-4 w-4" />
                      Create Article
                    </Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-4">
                  {articles.map((article) => (
                    <div
                      key={article.id}
                      className="flex items-center justify-between p-4 border rounded-lg"
                    >
                      <div className="flex-1">
                        <h3 className="font-medium">{article.title}</h3>
                        <p className="text-sm text-muted-foreground">
                          {article.keywords.slice(0, 3).join(", ")}
                          {article.keywords.length > 3 && "..."}
                        </p>
                        <p className="text-xs text-muted-foreground mt-1">
                          Status: {article.status} • Updated:{" "}
                          {article.updated_at
                            ? new Date(article.updated_at).toLocaleDateString()
                            : "Unknown"}
                        </p>
                      </div>
                      <div className="flex space-x-2">
                        <Link href={`/cms/articles/${article.id}/edit`}>
                          <Button variant="outline" size="sm">
                            Edit
                          </Button>
                        </Link>
                      </div>
                    </div>
                  ))}
                  {articles.length >= 10 && (
                    <div className="text-center pt-4">
                      <Link href="/cms/articles">
                        <Button variant="outline">View All Articles</Button>
                      </Link>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
