import feedparser
from datetime import datetime
import time
import random

# RSS ソースの定義
rss_sources = {
    "ソフトバンク": "https://news.google.com/rss/search?q=ソフトバンク&hl=ja&gl=JP&ceid=JP:ja",
    "大正製薬": "https://news.google.com/rss/search?q=大正製薬&hl=ja&gl=JP&ceid=JP:ja",
    "SBI証券": "https://news.google.com/rss/search?q=SBI証券&hl=ja&gl=JP&ceid=JP:ja"
}

def get_news_for_company(company, url, max_retries=3):
    """特定の会社のニュースを取得する関数"""
    for attempt in range(max_retries):
        try:
            print(f"🔍 {company} ニュース取得中 (試行 {attempt + 1}/{max_retries}): {url}")
            
            # フィードを取得
            feed = feedparser.parse(url)
            
            # ステータスコードをチェック
            if hasattr(feed, 'status') and feed.status != 200:
                print(f"⚠️  {company}: HTTP ステータス {feed.status}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # 2秒待機してリトライ
                    continue
            
            # エントリが存在するかチェック
            if not hasattr(feed, 'entries') or len(feed.entries) == 0:
                print(f"⚠️  {company}: エントリが見つかりません")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return []
            
            print(f"✅ {company} 件数: {len(feed.entries)}")
            return feed.entries[:10]  # 最大10件
            
        except Exception as e:
            print(f"❌ {company} エラー (試行 {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                print(f"❌ {company}: 最大試行回数に達しました")
                return []
    
    return []
    
def filter_entries(company, entries):
    """会社ごとにニュースをフィルタリング（例：ソフトバンクのホークス除外）"""
    if company == "ソフトバンク":
        return [entry for entry in entries if "ホークス" not in entry.title]
    return entries

def generate_news_section(company, entries):
    """ニュースセクションのHTMLを生成"""
    if not entries:
        return f"""
<div class="section">
    <h2>📰 {company} の最新ニュース</h2>
    <p class="no-news">現在ニュースを取得できません。後ほど再度お試しください。</p>
</div>
"""
    
    items = ""
    for entry in entries:
        try:
            title = entry.title if hasattr(entry, 'title') else 'タイトルなし'
            link = entry.link if hasattr(entry, 'link') else '#'
            
            # 日付があれば表示
            pub_date = ""
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    date_obj = datetime(*entry.published_parsed[:6])
                    pub_date = f" <span class='date'>({date_obj.strftime('%m/%d %H:%M')})</span>"
                except:
                    pass
            
            # HTMLエスケープ（簡易版）
            title = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            items += f"<li><a href='{link}' target='_blank'>{title}</a>{pub_date}</li>\n"
            
        except Exception as e:
            print(f"⚠️  エントリ処理エラー: {e}")
            continue
    
    return f"""
<div class="section">
    <h2>📰 {company} の最新ニュース</h2>
    <ul class="news-list">{items}</ul>
</div>
"""

def main():
    """メイン処理"""
    print("=" * 50)
    print("📰 NEWS DIGEST 生成開始")
    print("=" * 50)
    
    # 現在の日時
    today = datetime.now().strftime('%Y年%m月%d日')
    current_time = datetime.now().strftime('%H:%M')
    
    # 名言リスト
    quotes = [
        "「全盛期？これからだよ」 - 三浦知良",
        "「成功する秘訣は、成功するまで諦めないことだ」 - アルベルト・アインシュタイン",
        "「未来を予測する最良の方法は、それを創ることだ」 - ピーター・ドラッカー",
        "「壁というのは、できないことを他人に証明するためにあるのではない」 - イチロー",
        "「迷ったら前へ」 - 羽生善治"
    ]

    # ストーリーリスト
    stories = [
        "電車で出会った彼女との何気ない5分間の会話が、ずっと心に残っている。",
        "ふとしたきっかけで始めた習慣が、人生を変える第一歩だった。",
        "子供が描いた絵に、人生で一番大切なものが詰まっていた。",
        "雨の日に傘を貸してくれたあの人の優しさが、ずっと記憶に残っている。",
        "小さなカフェで見かけた、老夫婦の静かな時間に心を打たれた。"
    ]

    # ランダム選択
    quote = random.choice(quotes)
    story = random.choice(stories)

    # 以下、残りの処理は元のコードと同様


    
    # ニュースセクションを生成
    news_sections = ""
    total_articles = 0
    
    for company, url in rss_sources.items():
        entries = get_news_for_company(company, url)
        news_sections += generate_news_section(company, entries)
        entries = filter_entries(company, entries) 
        total_articles += len(entries)
        
        # レート制限対策：各リクエスト間に少し待機
        time.sleep(1)
    
    print(f"📊 合計記事数: {total_articles}")
    
    # HTMLテンプレート（改良版）
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>11BP 生成AI勉強会 NEWS DIGEST</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Hiragino Sans', sans-serif; 
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 1em;
            margin: 0;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        
        h1 {{ 
            color: #2c3e50; 
            text-align: center;
            background: white;
            padding: 1.5em;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 1.5em;
        }}
        
        .header-info {{
            text-align: center;
            background: #34495e;
            color: white;
            padding: 1em;
            border-radius: 8px;
            margin-bottom: 2em;
        }}
        
        .section {{ 
            background: white; 
            padding: 2em; 
            margin-bottom: 1.5em; 
            border-radius: 12px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 4px solid #3498db;
        }}
        
        .section h2 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 0.5em;
        }}
        
        .news-list li {{ 
            margin-bottom: 0.8em;
            padding: 0.5em 0;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        .news-list li:last-child {{
            border-bottom: none;
        }}
        
        a {{ 
            text-decoration: none; 
            color: #2980b9;
            font-weight: 500;
        }}
        
        a:hover {{
            color: #3498db;
            text-decoration: underline;
        }}
        
        .date {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        .no-news {{
            color: #e74c3c;
            font-style: italic;
        }}
        
        .footer {{
            text-align: center;
            color: #7f8c8d;
            margin-top: 2em;
            padding: 1em;
            background: white;
            border-radius: 8px;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 0.5em; }}
            .section {{ padding: 1.5em; }}
            h1 {{ font-size: 1.5em; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>11BP 生成AI勉強会 NEWS DIGEST</h1>
        
        <div class="header-info">
            <p><strong>📅 日付:</strong> {today} | <strong>🕐 更新時刻:</strong> {current_time}</p>
            <p><strong>📊 総記事数:</strong> {total_articles}件</p>
        </div>
        
        {news_sections}
        
        <div class="section">
            <h2>💡 今日の格言</h2>
            <p style="font-size: 1.1em; font-style: italic; color: #2c3e50;">{quote}</p>
        </div>
        
        <div class="section">
            <h2>📘 今日のショートストーリー</h2>
            <p style="color: #34495e;">{story}</p>
        </div>
        
        <div class="footer">
            最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} JST<br>
            自動生成システムにより作成
        </div>
    </div>
</body>
</html>
"""

    # HTMLファイル出力
    try:
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("✅ index.html を正常に生成しました")
        
        # ファイルサイズを確認
        import os
        file_size = os.path.getsize("index.html")
        print(f"📁 ファイルサイズ: {file_size:,} bytes")
        
    except Exception as e:
        print(f"❌ ファイル書き込みエラー: {e}")
        raise
    
    print("=" * 50)
    print("🎉 NEWS DIGEST 生成完了")
    print("=" * 50)

if __name__ == "__main__":
    main()
