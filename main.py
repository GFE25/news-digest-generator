import feedparser
from datetime import datetime

# RSSフィードURL（好きなニュースサイトのRSSに変えてOK）
RSS_URL = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"

# RSSをパース
feed = feedparser.parse(RSS_URL)

# 最新ニュースタイトル（存在しない場合はエラーメッセージ）
latest_title = feed.entries[0].title if feed.entries else "ニュースが取得できませんでした。"

today = datetime.now().strftime('%Y年%m月%d日')

html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>11BP 生成AI勉強会 NEWS DIGEST</title>
</head>
<body>
    <h1>11BP 生成AI勉強会 NEWS DIGEST</h1>
    <p><strong>日付:</strong> {today}</p>
    <div style="background:#f5f5f5;padding:1em;border-radius:8px;">
        <h2>最新ニュースタイトル</h2>
        <p>{latest_title}</p>
    </div>
</body>
</html>
"""

# index.htmlを書き出す
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ index.html を生成しました。")
