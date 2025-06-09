import feedparser
from datetime import datetime

# --- 検索対象とRSS URLのマッピング
rss_sources = {
    "ソフトバンク": "https://news.google.com/rss/search?q=ソフトバンク",
    "大正製薬": "https://news.google.com/rss/search?q=大正製薬",
    "SBI証券": "https://news.google.com/rss/search?q=SBI証券"
}

# --- 今日の情報
today = datetime.now().strftime('%Y年%m月%d日')
quote = "「全盛期？これからだよ」 - 三浦知良"
story = "電車で出会った彼女との何気ない5分間の会話が、ずっと心に残っている。"

# --- 各社のニュースをHTML化
news_sections = ""
for company, url in rss_sources.items():
    feed = feedparser.parse(url)
    items = ""
    for entry in feed.entries[:10]:  # 各10件
        title = entry.title
        link = entry.link
        items += f"<li><a href='{link}' target='_blank'>{title}</a></li>\n"
    news_sections += f"""
    <div class="section">
        <h2>📰 {company} の最新ニュース</h2>
        <ul>{items}</ul>
    </div>
    """

# --- HTML全体テンプレート
html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>11BP 生成AI勉強会 NEWS DIGEST</title>
    <style>
        body {{ font-family: sans-serif; background: #f9f9f9; padding: 2em; }}
        h1 {{ color: #2c3e50; }}
        .section {{ background: white; padding: 1.5em; margin-bottom: 1.5em; border-radius: 8px; box-shadow: 0 0 8px #ddd; }}
        li {{ margin-bottom: 0.5em; }}
        a {{ text-decoration: none; color: #2980b9; }}
    </style>
</head>
<body>
    <h1>11BP 生成AI勉強会 NEWS DIGEST</h1>
    <p><strong>日付:</strong> {today}</p>

    {news_sections}

    <div class="section">
        <h2>💡 今日の格言</h2>
        <p>{quote}</p>
    </div>

    <div class="section">
        <h2>📘 今日のショートストーリー</h2>
        <p>{story}</p>
    </div>
</body>
</html>
"""

# --- HTMLファイル出力
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ index.html を生成しました。")
