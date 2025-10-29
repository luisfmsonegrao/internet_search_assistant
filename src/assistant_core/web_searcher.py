import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader
from ..config import WEBSEARCH_ENDPOINT

USER_AGENT = "internet-search-assistant"


def search_web(query, max_results):
    """
    Query DuckDuckGo HTML endpoint and return a list of search results.
    """
    headers = {"User-Agent": USER_AGENT}
    resp = requests.post(
        WEBSEARCH_ENDPOINT, data={"q": query}, headers=headers, timeout=10
    )  # Search Web
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for r in soup.select("div.result")[
        :max_results
    ]:  # Get title, snippet and URL of search hits. ToDo: Add error handling
        a = r.select_one("a.result__a")
        title = a.get_text(strip=True) if a else None
        url = a["href"] if a and a.has_attr("href") else None
        snippet_el = (
            r.select_one("a.result__snippet")
            or r.select_one("div.result__snippet")
            or r.select_one("div.result__content")
        )
        snippet = snippet_el.get_text(" ", strip=True) if snippet_el else ""
        if title and url:
            url = "https://ourbrand.asml.com/m/79d325b168e0fd7e/original/2024-Annual-Report-based-on-US-GAAP.pdf"  # just to avoid unreliability of search results for now
            if url.lower().endswith(".pdf"):
                title = url.split("/")[-1]

            text_content = fetch_page_text(url)  # Fetch text from HTML or PDF
            results.append(
                {
                    "title": title,
                    "snippet": snippet,
                    "url": url,
                    "text_content": text_content,
                }
            )

    # Fallback: if no results via class, try different selectors
    if not results:
        for a in soup.select("a.result__a")[:max_results]:
            title = a.get_text(strip=True)
            url = a.get("href")
            if url.lower().endswith(".pdf"):
                title = url.split("/")[-1]
            snippet = ""
            text_content = fetch_page_text(url)
            results.append(
                {
                    "title": title,
                    "snippet": snippet,
                    "url": url,
                    "text_content": text_content,
                }
            )

    return results


def extract_text_from_html(url):
    """
    Fetch an HTML page and extract readable text.
    """
    try:
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove unwanted tags like scripts, styles, navbars
        for tag in soup.find_all(
            ["script", "style", "noscript", "header", "footer", "nav"]
        ):
            tag.extract()
        text = soup.get_text(separator=" ", strip=True)
        return " ".join(text.split())
    except Exception as e:
        return f"[Error parsing HTML: {e}]"  # ToDo: Add proper error handling


def extract_text_from_pdf(url):  # PyPDF2 sometimes scrambles pdf content such as text in tables. LLM cannot correctly process this
    """
    Fetch and extract text from a PDF URL.
    """
    try:
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        pdf_data = BytesIO(resp.content)
        reader = PdfReader(pdf_data)
        text = " ".join(page.extract_text() or "" for page in reader.pages)
        return " ".join(text.split())
    except Exception as e:
        return f"[Error parsing PDF: {e}]"  # ToDo: Add proper error handling


def fetch_page_text(url):
    """
    Determine file type and extract text appropriately.
    """
    url_lower = url.lower()
    if ".pdf" in url_lower:
        return extract_text_from_pdf(url)
    else:
        return extract_text_from_html(url)
