import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse, urljoin

class WebScraper:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
    
    def fetch_url(self, url: str) -> Optional[str]:
        """Fetch content from a URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(html, 'html.parser')
    
    def extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all links from a page"""
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Convert relative URLs to absolute
            if not bool(urlparse(href).netloc):
                href = urljoin(base_url, href)
            links.append(href)
        return links
    
    def extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract metadata from a page"""
        metadata = {}
        
        # Title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.string.strip()
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and 'content' in meta_desc.attrs:
            metadata['description'] = meta_desc['content'].strip()
        
        # H1
        h1_tag = soup.find('h1')
        if h1_tag:
            metadata['h1'] = h1_tag.get_text().strip()
        
        # Canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if canonical and 'href' in canonical.attrs:
            metadata['canonical'] = canonical['href'].strip()
        
        return metadata
    
    def extract_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract all headings from a page"""
        headings = {}
        for level in range(1, 7):
            tags = soup.find_all(f'h{level}')
            if tags:
                headings[f'h{level}'] = [tag.get_text().strip() for tag in tags]
        
        return headings
    
    def extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from a page"""
        # This is a simplified implementation
        # In a real implementation, this would use more sophisticated content extraction
        main_content = ""
        
        # Try to find main content area
        main_tags = soup.find_all(['article', 'main', 'div'], class_=['content', 'main-content', 'post-content'])
        if main_tags:
            for tag in main_tags:
                main_content += tag.get_text(separator='\n').strip() + "\n\n"
        else:
            # Fallback to body content
            body = soup.find('body')
            if body:
                main_content = body.get_text(separator='\n').strip()
        
        return main_content