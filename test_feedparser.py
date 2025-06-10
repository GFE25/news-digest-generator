import feedparser

url = "https://news.google.com/rss/search?q=ソフトバンク&hl=ja&gl=JP&ceid=JP:ja"

print("🔍 RSS フィード読み込み中:", url)

feed = feedparser.parse(url)

print("✅ パース成功か:", not feed.bozo)
print("🔢 ニュース件数:", len(feed.entries))

for entry in feed.entries[:5]:
    print("📰", entry.title)
