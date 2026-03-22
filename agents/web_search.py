# agents/web_search.py

import requests
from bs4 import BeautifulSoup
from ddgs import DDGS


MAX_RESULTS = 3        # number of search results to fetch
MAX_CHARS = 500        # max chars to scrape per page


def _search_duckduckgo(query: str) -> list[dict]:
    """
    Searches DuckDuckGo and returns top results with title, url, body snippet.
    """
    print(f"[web_search] Searching DuckDuckGo for: '{query}'")

    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=MAX_RESULTS):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
            })

    print(f"[web_search] Found {len(results)} results.")
    return results


def _scrape_page(url: str) -> str:
    """
    Fetches a webpage and extracts clean text using BeautifulSoup.
    Returns empty string on any failure.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts and styles
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        # Trim to MAX_CHARS to avoid flooding the LLM context
        return text[:MAX_CHARS]

    except Exception as e:
        print(f"[web_search] Failed to scrape {url}: {e}")
        return ""


def search_web(state: dict) -> dict:
    """
    Agent 3 — Web Search
    Searches DuckDuckGo, scrapes top results, builds context string.
    Updates state with 'search_results' key.
    """
    query = state.get("transcript", "").strip()

    results = _search_duckduckgo(query)

    # Build a structured string combining snippet + scraped content
    combined = []
    for i, r in enumerate(results, 1):
        scraped = _scrape_page(r["url"])
        content = scraped if scraped else r["snippet"]
        combined.append(
            f"[{i}] {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Content: {content}"
        )

    search_results = "\n\n".join(combined)

    print(f"[web_search] Context built, total chars: {len(search_results)}")

    return {
        **state,
        "search_results": search_results,
    }