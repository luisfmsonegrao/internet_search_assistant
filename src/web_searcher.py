import requests
from bs4 import BeautifulSoup

DUCKDUCKGO_HTML = "https://html.duckduckgo.com/html/"
USER_AGENT = "internet-search-assistant"
MAX_RESULTS = 2

def search_web(query, max_results):
    """
    Query DuckDuckGo HTML endpoint and return a list of search results:
    [{title, snippet, url, source}...]
    """
    headers = {"User-Agent": USER_AGENT}
    # Use the HTML endpoint which is easier to parse in scripts
    resp = requests.post(DUCKDUCKGO_HTML, data={"q": query}, headers=headers, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    results = []
    # ddg HTML structure: result containers have class "result" or "result__body" (inspect)
    for r in soup.select("div.result")[:max_results]:
        a = r.select_one("a.result__a")
        title = a.get_text(strip=True) if a else None
        url = a["href"] if a and a.has_attr("href") else None
        snippet_el = r.select_one("a.result__snippet") or r.select_one("div.result__snippet") or r.select_one("div.result__content")
        snippet = snippet_el.get_text(" ", strip=True) if snippet_el else ""
        if title and url:
            results.append({"title": title, "snippet": snippet, "url": url})
    # Fallback: if no results via class, try different selectors
    if not results:
        for a in soup.select("a.result__a")[:max_results]:
            title = a.get_text(strip=True)
            url = a.get("href")
            snippet = ""
            results.append({"title": title, "snippet": snippet, "url": url})
    return results