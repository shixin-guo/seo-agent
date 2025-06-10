#!/usr/bin/env python3
"""
Generate llm.txt and llm-full.txt files for SEO Agent documentation.
Similar to Mastra's approach but adapted for Python ecosystem.
"""

import re
from pathlib import Path
from typing import Dict, List


def extract_frontmatter(content: str) -> Dict[str, str]:
    """Extract title and description from markdown frontmatter."""
    frontmatter_pattern = r"^---\n(.*?)\n---"
    match = re.search(frontmatter_pattern, content, re.DOTALL)
    if not match:
        return {}

    frontmatter_str = match.group(1)
    result = {}

    for field in ["title", "description"]:
        field_pattern = rf"{field}:\s*([^\n]+)"
        field_match = re.search(field_pattern, frontmatter_str)
        if field_match:
            result[field] = field_match.group(1).strip().strip("\"'")

    return result


def path_to_url(
    file_path: str, base_url: str = "https://github.com/shixin-guo/seo-agent/blob/main"
) -> str:
    """Convert file path to GitHub URL."""
    return f"{base_url}/{file_path}"


def extract_title_from_content(content: str, file_path: str) -> str:
    """Extract title from markdown content or use filename as fallback."""
    h1_match = re.search(r"^# (.+)$", content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()

    return Path(file_path).stem.replace("_", " ").replace("-", " ").title()


def process_markdown_files(root_dir: Path) -> List[Dict[str, str]]:
    """Process all markdown files in the project."""
    markdown_files = []

    doc_files = [
        ("README.md", "overview"),
        ("NEXT_STEPS.md", "development"),
        ("development.md", "development"),
        ("frontend/README.md", "frontend"),
    ]

    for file_path, category in doc_files:
        full_path = root_dir / file_path
        if full_path.exists():
            try:
                content = full_path.read_text(encoding="utf-8")
                frontmatter = extract_frontmatter(content)
                title = frontmatter.get("title") or extract_title_from_content(
                    content, file_path
                )

                markdown_files.append(
                    {
                        "path": file_path,
                        "content": content,
                        "title": title,
                        "description": frontmatter.get("description", ""),
                        "category": category,
                        "url": path_to_url(file_path),
                    }
                )
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue

    return markdown_files


def generate_llm_files(root_dir: Path) -> None:
    """Generate both llm.txt (index) and llm-full.txt (complete docs)."""
    print(f"Generating LLM documentation files from: {root_dir}")

    markdown_files = process_markdown_files(root_dir)

    if not markdown_files:
        print("No markdown files found!")
        return

    full_content_parts = []
    for file_info in markdown_files:
        content = file_info["content"]
        source_url = file_info["url"]

        title_match = re.search(r"^(#{1,2}\s+.+)$", content, re.MULTILINE)
        if title_match:
            title_line = title_match.group(1)
            title_index = content.find(title_line)
            before_title = content[: title_index + len(title_line)]
            after_title = content[title_index + len(title_line) :]
            content_with_source = f"{before_title}\nSource: {source_url}{after_title}"
        else:
            content_with_source = f"Source: {source_url}\n\n{content}"

        full_content_parts.append(content_with_source)

    full_content = "\n\n".join(full_content_parts)

    full_file_path = root_dir / "llm-full.txt"
    full_file_path.write_text(full_content, encoding="utf-8")
    print(f"Generated {full_file_path}")

    index_content = [
        "# SEO Agent\n",
        "> SEO Agent is a comprehensive AI-powered SEO automation tool designed to streamline and enhance search engine optimization workflows. "
        + "It serves SEO professionals, content marketers, digital agencies, and website owners by providing intelligent analysis and recommendations across four core SEO domains: "
        + "keyword research, content optimization, technical site auditing, and backlink analysis.\n\n"
        + "The tool leverages advanced AI capabilities through the DSPy framework and OpenAI's language models to deliver actionable insights that traditionally require manual expertise and time-consuming analysis. "
        + "Users can interact with the system through multiple interfaces - a command-line interface for automation and scripting, a REST API for programmatic integration, and a modern web application for interactive use.\n\n"
        + "Key capabilities include:\n"
        + "- **Intelligent Keyword Research**: Expands seed keywords using AI to identify related terms, analyze search intent, and assess competition levels\n"
        + "- **Content Optimization**: Analyzes existing content and provides AI-powered suggestions for SEO improvement\n"
        + "- **Technical SEO Auditing**: Crawls websites to identify technical issues and provides prioritized action plans\n"
        + "- **Backlink Analysis**: Identifies backlink opportunities and generates personalized outreach templates\n\n"
        + "This documentation covers all aspects of SEO Agent from installation and usage to development and deployment.\n",
    ]

    categories: Dict[str, List[Dict[str, str]]] = {}
    for file_info in markdown_files:
        category = file_info["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(file_info)

    category_titles = {
        "overview": "Overview",
        "development": "Development",
        "frontend": "Frontend",
    }

    for category, files in categories.items():
        category_title = category_titles.get(category, category.title())
        index_content.append(f"\n## {category_title}")

        for file_info in files:
            url = file_info["url"]
            title = file_info["title"]
            description = file_info["description"]

            line = f"- [{title}]({url})"
            if description:
                line += f": {description}"

            index_content.append(line)

    index_file_path = root_dir / "llm.txt"
    index_file_path.write_text("\n".join(index_content), encoding="utf-8")
    print(f"Generated {index_file_path}")


if __name__ == "__main__":
    root_dir = Path(__file__).parent.parent
    generate_llm_files(root_dir)
