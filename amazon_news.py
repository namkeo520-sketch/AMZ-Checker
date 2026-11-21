
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

topics = [
    "Amazon Seller Central policy update",
    "Amazon FBA seller fees",
    "Amazon listing SEO advertising",
    "Amazon print on demand personalized gifts",
    "Amazon seller account compliance"
]

articles = []
seen = set()

for topic in topics:
    query = urllib.parse.quote(topic + " when:7d")
    url = (
        "https://news.google.com/rss/search?q="
        + query + "&hl=en-US&gl=US&ceid=US:en"
    )

    try:
        request = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            root = ET.fromstring(response.read())

        for item in root.findall(".//item")[:8]:
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            published = item.findtext("pubDate", "")

            if not title or not link or link in seen:
                continue

            seen.add(link)
            articles.append((topic, title, link, published))

    except Exception as error:
        print(f"Error fetching {topic}: {error}")

lines = [
    "# Amazon US News",
    "",
    "Updated: " + datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M UTC"
    ),
    "",
]

for topic in topics:
    lines.append(f"## {topic}")
    lines.append("")
    for category, title, link, published in articles:
        if category == topic:
            lines.append(f"- [{title}]({link})")
            lines.append(f"  - Published: {published}")
    lines.append("")

Path("amazon-news.md").write_text(
    "\n".join(lines), encoding="utf-8"
)
print(f"Saved {len(articles)} news items")

