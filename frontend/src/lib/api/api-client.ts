/**
 * API client for interacting with the SEO Agent backend.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

/**
 * Generates keyword research based on a seed keyword.
 */
export async function generateKeywords(seed: string, industry?: string) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/keywords`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ seed, industry }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error generating keywords:", error);
    throw error;
  }
}

/**
 * Optimizes content for SEO.
 */
export async function optimizeContent(
  contentFile: File,
  keywordsFile?: File,
  useAdvanced = true,
  creative = false,
) {
  try {
    const formData = new FormData();
    formData.append("content_file", contentFile);

    if (keywordsFile) {
      formData.append("keywords_file", keywordsFile);
    }

    formData.append("use_advanced", String(useAdvanced));
    formData.append("creative", String(creative));

    const response = await fetch(`${API_BASE_URL}/api/optimize-content`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error optimizing content:", error);
    throw error;
  }
}

/**
 * Performs a technical SEO audit on a website.
 */
export async function auditSite(domain: string, maxPages = 50) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/audit-site`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ domain, max_pages: maxPages }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error auditing site:", error);
    throw error;
  }
}

/**
 * Analyzes backlink opportunities.
 */
export async function analyzeBacklinks(
  domain: string,
  competitors?: string[],
  generateTemplates = false,
) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/backlink-analysis`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        domain,
        competitors,
        generate_templates: generateTemplates,
      }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error analyzing backlinks:", error);
    throw error;
  }
}

/**
 * Checks if the API server is running.
 */
export async function checkApiStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/`);
    return response.ok;
  } catch (error) {
    console.error("API server not reachable:", error);
    return false;
  }
}

/**
 * Article management API functions
 */

export interface Article {
  id?: number;
  title: string;
  content: string;
  keywords: string[];
  meta_description?: string;
  status: string;
  created_at?: string;
  updated_at?: string;
}

export interface ArticleGenerateRequest {
  seed_keyword: string;
  industry?: string;
  title?: string;
  min_length?: number;
}

export async function getArticles(limit = 100, offset = 0, status?: string) {
  try {
    const params = new URLSearchParams({
      limit: limit.toString(),
      offset: offset.toString(),
    });
    
    if (status) {
      params.append("status", status);
    }

    const response = await fetch(`${API_BASE_URL}/api/articles?${params}`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching articles:", error);
    throw error;
  }
}

export async function getArticle(id: number) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/articles/${id}`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching article:", error);
    throw error;
  }
}

export async function createArticle(article: Omit<Article, "id" | "created_at" | "updated_at">) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/articles`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(article),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error creating article:", error);
    throw error;
  }
}

export async function updateArticle(id: number, article: Partial<Article>) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/articles/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(article),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error updating article:", error);
    throw error;
  }
}

export async function deleteArticle(id: number) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/articles/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error deleting article:", error);
    throw error;
  }
}

export async function generateArticle(request: ArticleGenerateRequest) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/articles/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error generating article:", error);
    throw error;
  }
}

export async function searchArticles(query: string, limit = 50) {
  try {
    const params = new URLSearchParams({
      q: query,
      limit: limit.toString(),
    });

    const response = await fetch(`${API_BASE_URL}/api/articles/search?${params}`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error searching articles:", error);
    throw error;
  }
}
