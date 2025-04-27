from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import hashlib
import json

# Constants
DATA_PATH = "data/"
CACHE_DIR = os.path.join(DATA_PATH, "cache")
DB_FAISS_PATH = "vectorstore/db_faiss"
USER_AGENT = "AshaBot/1.0 (Educational Project)"
MIN_SCRAPE_DELAY = 10  # seconds

# Create necessary directories
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

class WebContentScraper:
    """Responsible for fetching and parsing website content"""
    def __init__(self, cache_dir=CACHE_DIR):
        self.cache_dir = cache_dir
        self.domain_last_access = {}

    def fetch_url(self, url, force_refresh=False):
        """Fetch URL content with caching and rate limiting"""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        cache_file = os.path.join(self.cache_dir, f"{url_hash}.html")

        if os.path.exists(cache_file) and not force_refresh:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return f.read()

        # Rate limit by domain
        domain = urlparse(url).netloc
        if domain in self.domain_last_access:
            time_since_last = time.time() - self.domain_last_access[domain]
            if time_since_last < MIN_SCRAPE_DELAY:
                time.sleep(MIN_SCRAPE_DELAY - time_since_last)

        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            self.domain_last_access[domain] = time.time()

            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(response.text)

            return response.text

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_content(self, html, content_selectors=None):
        """Extract meaningful text content"""
        soup = BeautifulSoup(html, 'html.parser')

        # Remove junk
        for element in soup.select('script, style, nav, footer, header, [class*="ads"], [id*="ads"]'):
            element.decompose()

        if content_selectors:
            extracted_content = []
            for selector in content_selectors:
                elements = soup.select(selector)
                for element in elements:
                    extracted_content.append(element.get_text(strip=True, separator=' '))
            if extracted_content:
                return ' '.join(extracted_content)

        # Default fallback
        main_content = soup.select('main, article, .content, #content, .post, .article')
        if main_content:
            return ' '.join([el.get_text(strip=True, separator=' ') for el in main_content])

        body = soup.find('body')
        return body.get_text(strip=True, separator=' ') if body else ''

def load_website_data(urls_file="data/urls.json", force_refresh=False):
    """Load website data from URLs"""
    documents = []
    scraper = WebContentScraper()

    try:
        with open(urls_file, 'r') as f:
            urls_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: Could not load {urls_file}")
        urls_data = []

    for url_info in urls_data:
        url = url_info.get("url")
        print(f"Fetching {url}...")

        html = scraper.fetch_url(url, force_refresh=force_refresh)
        if html:
            content = scraper.extract_content(html, url_info.get("selectors"))
            if content:
                metadata = {
                    "source": url,
                    "type": url_info.get("type", "general"),
                    "title": url_info.get("title", url),
                }
                documents.append({"page_content": content, "metadata": metadata})

    return documents

def create_chunks(documents):
    """Split text into chunks"""
    from langchain.schema import Document
    langchain_docs = [Document(page_content=doc["page_content"], metadata=doc["metadata"]) for doc in documents]

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(langchain_docs)
    return chunks

def get_embedding_model():
    """Load HuggingFace Embedding Model"""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def main():
    documents = load_website_data(force_refresh=True)
    print(f"Loaded {len(documents)} documents.")

    chunks = create_chunks(documents)
    print(f"Created {len(chunks)} text chunks.")

    embedding_model = get_embedding_model()
    db = FAISS.from_documents(chunks, embedding_model)

    os.makedirs(os.path.dirname(DB_FAISS_PATH), exist_ok=True)
    db.save_local(DB_FAISS_PATH)
    print(f"Saved vector database to {DB_FAISS_PATH}")

if __name__ == "__main__":
    main()
