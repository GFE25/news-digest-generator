import feedparser
from datetime import datetime
import time
import random

# RSS ソースの定義
rss_sources = {
    "ソフトバンク": "https://news.google.com/rss/search?q=ソフトバンク&hl=ja&gl=JP&ceid=JP:ja",
    "大正製薬": "https://news.google.com/rss/search?q=大正製薬&hl=ja&gl=JP&ceid=JP:ja",
    "SBI証券": "https://news.google.com/rss/search?q=SBI証券&hl=ja&gl=JP&ceid=JP:ja",
    "電通": "https://news.google.com/rss/search?q=電通&hl=ja&gl=JP&ceid=JP:ja",
    "ガンホー": "https://news.google.com/rss/search?q=ガンホー&hl=ja&gl=JP&ceid=JP:ja",
    "GO": "https://news.google.com/rss/search?q=GO+タクシー&hl=ja&gl=JP&ceid=JP:ja",
    "森ビル": "https://news.google.com/rss/search?q=森ビル&hl=ja&gl=JP&ceid=JP:ja",
    "Spotify": "https://news.google.com/rss/search?q=スポティファイ&hl=ja&gl=JP&ceid=JP:ja",
    "Epic Games": "https://news.google.com/rss/search?q=フォートナイト&hl=ja&gl=JP&ceid=JP:ja",
    "富士電機": "https://news.google.com/rss/search?q=富士電機&hl=ja&gl=JP&ceid=JP:ja",
    "ZOZO": "https://news.google.com/rss/search?q=ZOZO&hl=ja&gl=JP&ceid=JP:ja",
    "えがお": "https://news.google.com/rss/search?q=えがお+株式会社&hl=ja&gl=JP&ceid=JP:ja",
    "芝浦機械": "https://news.google.com/rss/search?q=芝浦機械&hl=ja&gl=JP&ceid=JP:ja",
    "M&Aキャピタル": "https://news.google.com/rss/search?q=M%26A%E3%82%AD%E3%83%A3%E3%83%94%E3%82%BF%E3%83%AB%E3%83%91%E3%83%BC%E3%83%88%E3%83%8A%E3%83%BC%E3%82%BA&hl=ja&gl=JP&ceid=JP:ja",
    "エアウィーヴ": "https://news.google.com/rss/search?q=エアウィーヴ&hl=ja&gl=JP&ceid=JP:ja",
    "PayPay": "https://news.google.com/rss/search?q=PayPay&hl=ja&gl=JP&ceid=JP:ja",
    "アスクル": "https://news.google.com/rss/search?q=アスクル&hl=ja&gl=JP&ceid=JP:ja",
    "UCC上島珈琲": "https://news.google.com/rss/search?q=UCC%E4%B8%8A%E5%B3%B6%E7%8F%88%E7%90%B2&hl=ja&gl=JP&ceid=JP:ja",
    "TikTok": "https://news.google.com/rss/search?q=TikTok&hl=ja&gl=JP&ceid=JP:ja",
    "ispace": "https://news.google.com/rss/search?q=ispace&hl=ja&gl=JP&ceid=JP:ja",
    "プレミアグループ": "https://news.google.com/rss/search?q=プレミアグループ&hl=ja&gl=JP&ceid=JP:ja"
}


from datetime import datetime, timedelta

def get_news_for_company(company, url, max_retries=3):
    """特定の会社のニュースを取得する関数（1か月以内、最大10件まで）"""
    one_month_ago = datetime.now() - timedelta(days=30)

    for attempt in range(max_retries):
        try:
            print(f"🔍 {company} ニュース取得中 (試行 {attempt + 1}/{max_retries}): {url}")
            
            # フィードを取得
            feed = feedparser.parse(url)
            
            # ステータスコードをチェック
            if hasattr(feed, 'status') and feed.status != 200:
                print(f"⚠️  {company}: HTTP ステータス {feed.status}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
            
            # エントリが存在するかチェック
            if not hasattr(feed, 'entries') or len(feed.entries) == 0:
                print(f"⚠️  {company}: エントリが見つかりません")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return []

            # 一か月以内のニュースだけにフィルタ
            filtered_entries = []
            for entry in feed.entries:
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                    if pub_date >= one_month_ago:
                        filtered_entries.append(entry)

            # 最大10件まで
            filtered_entries = filtered_entries[:10]

            print(f"✅ {company} 件数: {len(filtered_entries)}（1か月以内）")
            return filtered_entries
            
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
        excluded_keywords = ["ホークス", "野球", "選手", "打者", "投手", "試合", "連勝", "連敗", "引き分け", "猛打賞", "復帰", "離脱", "捕手", "安打", "監督", "球場", "打点", "ヒット", "二塁打", "三塁打", "巨人", "ホームラン", "１軍", "城島", "失点", "打球", "先発", "最下位", "起用", "退場", "守護神", "球団"]
        return [entry for entry in entries if not any(kw in entry.title for kw in excluded_keywords)]
    elif company == "SBI証券":
        excluded_keywords = ["投資判断", "中立", "買い", "売り"]
        return [entry for entry in entries if not any(kw in entry.title for kw in excluded_keywords)]
    return entries


def get_company_icon(company):
    icon_map = {
        "ソフトバンク": "SB",
        "大正製薬": "大",
        "SBI証券": "SBI",
        "電通": "電",
        "ガンホー": "GH",
        "GO": "GO",
        "森ビル": "森",
        "Spotify": "♪",
        "Epic Games": "🎮",
        "富士電機": "富",
        "ZOZO": "ZZ",
        "えがお": "笑",
        "芝浦機械": "芝",
        "M&Aキャピタル": "M&A",
        "エアウィーヴ": "Air",
        "PayPay": "PP",
        "アスクル": "AS",
        "UCC上島珈琲": "☕",
        "TikTok": "TT",
        "ispace": "🚀",
        "プレミアグループ": "PG"
    }
    return icon_map.get(company, company[:2])

def get_tab_id(company):
    tab_map = {
        "ソフトバンク": "softbank",
        "大正製薬": "taisho", 
        "SBI証券": "sbi",
        "電通": "dentsu",
        "ガンホー": "gungho",
        "GO": "go",
        "森ビル": "mori",
        "Spotify": "spotify",
        "Epic Games": "epic",
        "富士電機": "fuji",
        "ZOZO": "zozo",
        "えがお": "egao",
        "芝浦機械": "shibaura",
        "M&Aキャピタル": "macapital",
        "エアウィーヴ": "airweave",
        "PayPay": "paypay",
        "アスクル": "askul",
        "UCC上島珈琲": "ucc",
        "TikTok": "tiktok",
        "ispace": "ispace",
        "プレミアグループ": "premier"
    }
    return tab_map.get(company, company.lower())


def generate_news_items(entries):
    """ニュースアイテムのHTMLを生成"""
    if not entries:
        return "<li class='news-item'><div style='color: #e74c3c; font-style: italic;'>現在ニュースを取得できません。後ほど再度お試しください。</div></li>"

    # 日付でソート（新しい順）
    entries.sort(key=lambda e: getattr(e, 'published_parsed', time.gmtime(0)), reverse=True)
    
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
                    pub_date = f"<div class='news-date'>{date_obj.strftime('%m/%d %H:%M')}</div>"
                except:
                    pass
            
            # HTMLエスケープ（簡易版）
            title = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            items += f"""
            <li class="news-item">
                <a href='{link}' target='_blank'>{title}</a>
                {pub_date}
            </li>
            """
            
        except Exception as e:
            print(f"⚠️  エントリ処理エラー: {e}")
            continue
    
    return items

def generate_news_section(company, entries, section_class="news-section scroll-fade"):
    """ニュースセクションのHTMLを生成（タブ対応）"""
    icon = get_company_icon(company)
    news_items = generate_news_items(entries)
    
    return f"""
    <div class="{section_class}">
        <h2><div class="company-icon">{icon}</div>{company} 最新ニュース</h2>
        <ul class="news-list">
            {news_items}
        </ul>
    </div>
    """

def generate_all_news_tab(companies_data):
    """すべてのニュースタブのコンテンツを生成"""
    content = ""
    for company, entries in companies_data.items():
        content += generate_news_section(company, entries)
    return content

def generate_individual_tabs(companies_data):
    """個別企業タブのコンテンツを生成"""
    tabs_content = ""
    for company, entries in companies_data.items():
        tab_id = get_tab_id(company)
        section_content = generate_news_section(company, entries)
        tabs_content += f"""
        <div class="tab-content" id="{tab_id}">
            {section_content}
        </div>
        """
    return tabs_content

def generate_quote_tab(quote):
    """格言タブのコンテンツを生成"""
    return f"""
    <div class="tab-content" id="quote">
        <div class="special-section quote-section">
            <h2>💡 今日の格言</h2>
            <div class="quote-text">{quote}</div>
        </div>
    </div>
    """

def generate_story_tab(story):
    """ストーリータブのコンテンツを生成"""
    return f"""
    <div class="tab-content" id="story">
        <div class="special-section story-section">
            <h2>📘 今日のショートストーリー</h2>
            <div class="story-text">{story}</div>
        </div>
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
    
    # ニュースデータを収集
    companies_data = {}
    total_articles = 0
    
    for company, url in rss_sources.items():
        entries = get_news_for_company(company, url)
        filtered_entries = filter_entries(company, entries)
        companies_data[company] = filtered_entries
        total_articles += len(filtered_entries)
        
        # レート制限対策：各リクエスト間に少し待機
        time.sleep(1)
    
    print(f"📊 合計記事数: {total_articles}")
    
    # タブコンテンツ生成
    all_news_content = generate_all_news_tab(companies_data)
    individual_tabs_content = generate_individual_tabs(companies_data)
    quote_tab_content = generate_quote_tab(quote)
    story_tab_content = generate_story_tab(story)
    
    # HTMLテンプレート（タブ機能拡張版）
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>11BP 生成AI勉強会 NEWS DIGEST</title>
    <style>
        :root {{
            --primary-color: #3498db;
            --secondary-color: #2c3e50;
            --accent-color: #e74c3c;
            --success-color: #27ae60;
            --warning-color: #f39c12;
            --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --card-shadow: 0 10px 30px rgba(0,0,0,0.1);
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Hiragino Sans', sans-serif; 
            background: var(--background-gradient);
            padding: 1em;
            line-height: 1.6;
            min-height: 100vh;
            animation: fadeIn 0.8s ease-out;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes slideInUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        /* ヘッダー */
        .header {{
            text-align: center;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 2em;
            border-radius: 20px;
            box-shadow: var(--card-shadow);
            margin-bottom: 2em;
            animation: slideInUp 0.6s ease-out;
        }}

        .header h1 {{
            color: var(--secondary-color);
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 0.5em;
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .header-info {{
            background: var(--secondary-color);
            color: white;
            padding: 1em 2em;
            border-radius: 50px;
            margin-top: 1em;
            display: inline-block;
            font-weight: 500;
        }}

        /* タブナビゲーション */
        .tab-container {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1em;
            margin-bottom: 2em;
            box-shadow: var(--card-shadow);
            animation: slideInUp 0.7s ease-out;
        }}

        .tab-nav {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 0.5em;
            margin-bottom: 1em;
        }}

        .tab-button {{
            background: transparent;
            border: 2px solid var(--primary-color);
            color: var(--primary-color);
            padding: 0.8em 1.5em;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            transition: var(--transition);
            position: relative;
            overflow: hidden;
            font-size: 0.9em;
        }}

        .tab-button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: var(--primary-color);
            transition: var(--transition);
            z-index: -1;
        }}

        .tab-button:hover::before,
        .tab-button.active::before {{
            left: 0;
        }}

        .tab-button:hover,
        .tab-button.active {{
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }}

        /* 特殊タブボタンのスタイル */
        .tab-button[data-tab="quote"] {{
            border-color: var(--success-color);
            color: var(--success-color);
        }}

        .tab-button[data-tab="quote"]::before {{
            background: var(--success-color);
        }}

        .tab-button[data-tab="story"] {{
            border-color: var(--accent-color);
            color: var(--accent-color);
        }}

        .tab-button[data-tab="story"]::before {{
            background: var(--accent-color);
        }}

        /* ニュースセクション */
        .tab-content {{
            display: none;
            animation: slideInUp 0.5s ease-out;
        }}

        .tab-content.active {{
            display: block;
        }}

        .news-section {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 2em;
            margin-bottom: 1.5em;
            border-radius: 20px;
            box-shadow: var(--card-shadow);
            border-left: 5px solid var(--primary-color);
            transition: var(--transition);
            animation: slideInUp 0.8s ease-out;
        }}

        .news-section:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }}

        .news-section h2 {{
            color: var(--secondary-color);
            margin-bottom: 1em;
            font-size: 1.5em;
            display: flex;
            align-items: center;
            gap: 0.5em;
        }}

        .company-icon {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--primary-color);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
        }}

        .news-list {{
            list-style: none;
        }}

        .news-item {{
            padding: 1em 0;
            border-bottom: 1px solid rgba(0,0,0,0.1);
            transition: var(--transition);
            position: relative;
        }}

        .news-item:last-child {{
            border-bottom: none;
        }}

        .news-item:hover {{
            padding-left: 1em;
            background: rgba(52, 152, 219, 0.05);
            border-radius: 10px;
        }}

        .news-item::before {{
            content: '📰';
            position: absolute;
            left: -30px;
            opacity: 0;
            transition: var(--transition);
        }}

        .news-item:hover::before {{
            opacity: 1;
            left: 0;
        }}

        .news-item a {{
            text-decoration: none;
            color: var(--secondary-color);
            font-weight: 500;
            transition: var(--transition);
            display: block;
        }}

        .news-item a:hover {{
            color: var(--primary-color);
            padding-left: 0.5em;
        }}

        .news-date {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 0.3em;
        }}

        /* 特別セクション */
        .special-section {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 2em;
            border-radius: 20px;
            box-shadow: var(--card-shadow);
            transition: var(--transition);
            animation: slideInUp 0.9s ease-out;
            margin-bottom: 1.5em;
        }}

        .special-section:hover {{
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }}

        .special-section h2 {{
            color: var(--secondary-color);
            margin-bottom: 1em;
            font-size: 1.5em;
        }}

        .quote-section {{
            border-left: 5px solid var(--success-color);
        }}

        .story-section {{
            border-left: 5px solid var(--accent-color);
        }}

        .quote-text {{
            font-size: 1.2em;
            font-style: italic;
            color: var(--secondary-color);
            position: relative;
            padding: 1.5em;
            background: rgba(39, 174, 96, 0.1);
            border-radius: 15px;
            line-height: 1.8;
            text-align: center;
        }}

        .quote-text::before {{
            content: '"';
            font-size: 3em;
            color: var(--success-color);
            position: absolute;
            top: -10px;
            left: 20px;
            font-family: serif;
        }}

        .quote-text::after {{
            content: '"';
            font-size: 3em;
            color: var(--success-color);
            position: absolute;
            bottom: -20px;
            right: 20px;
            font-family: serif;
        }}

        .story-text {{
            color: #34495e;
            line-height: 1.8;
            position: relative;
            padding: 1.5em;
            background: rgba(231, 76, 60, 0.1);
            border-radius: 15px;
            font-size: 1.1em;
        }}

        .story-text::before {{
            content: '📖';
            font-size: 2em;
            position: absolute;
            top: 10px;
            left: 15px;
            opacity: 0.3;
        }}

        /* フッター */
        .footer {{
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 3em;
            padding: 2em;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            animation: slideInUp 1s ease-out;
        }}

        /* レスポンシブ */
        @media (max-width: 768px) {{
            body {{ padding: 0.5em; }}
            .header h1 {{ font-size: 2em; }}
            .tab-nav {{ 
                flex-direction: column;
                align-items: center;
            }}
            .tab-button {{
                width: 200px;
                text-align: center;
            }}
            .news-section, .special-section {{ padding: 1.5em; }}
        }}

        @media (max-width: 480px) {{
            .tab-button {{
                width: 100%;
                padding: 1em;
                font-size: 0.85em;
            }}
        }}

        /* スクロールアニメーション */
        .scroll-fade {{
            opacity: 0;
            transform: translateY(30px);
            transition: var(--transition);
        }}

        .scroll-fade.visible {{
            opacity: 1;
            transform: translateY(0);
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- ヘッダー -->
        <div class="header">
            <h1>11BP 生成AI勉強会 NEWS DIGEST</h1>
            <div class="header-info">
                📅 {today} | 🕐 {current_time} | 📊 {total_articles}件
            </div>
        </div>

        <!-- タブナビゲーション -->
        <div class="tab-container">
            <div class="tab-nav">
                <button class="tab-button active" data-tab="all">🌟 すべて</button>
                <button class="tab-button" data-tab="softbank">📱 ソフトバンク</button>
                <button class="tab-button" data-tab="taisho">💊 大正製薬</button>
                <button class="tab-button" data-tab="sbi">💰 SBI証券</button>
                <button class="tab-button" data-tab="dentsu">📺 電通</button>
                <button class="tab-button" data-tab="gungho">🎮 ガンホー</button>
                <button class="tab-button" data-tab="go">🚕 GO</button>
                <button class="tab-button" data-tab="mori">🏢 森ビル</button>
                <button class="tab-button" data-tab="spotify">♪ Spotify</button>
                <button class="tab-button" data-tab="epic">🎮 Epic Games</button>
                <button class="tab-button" data-tab="fuji">⚡ 富士電機</button>
                <button class="tab-button" data-tab="zozo">👕 ZOZO</button>
                <button class="tab-button" data-tab="egao">😊 えがお</button>
                <button class="tab-button" data-tab="shibaura">🔧 芝浦機械</button>
                <button class="tab-button" data-tab="macapital">📈 M&Aキャピタル</button>
                <button class="tab-button" data-tab="airweave">🛏️ エアウィーヴ</button>
                <button class="tab-button" data-tab="paypay">💳 PayPay</button>
                <button class="tab-button" data-tab="askul">📦 アスクル</button>
                <button class="tab-button" data-tab="ucc">☕ UCC上島珈琲</button>
                <button class="tab-button" data-tab="tiktok">📱 TikTok</button>
                <button class="tab-button" data-tab="ispace">🚀 ispace</button>
                <button class="tab-button" data-tab="premier">🏆 プレミアグループ</button>
                <button class="tab-button" data-tab="quote">💡 今日の格言</button>
                <button class="tab-button" data-tab="story">📘 ショートストーリー</button>
            </div>

            <!-- すべてのニュース -->
            <div class="tab-content active" id="all">
                {all_news_content}
            </div>

            <!-- 個別企業タブ -->
            {individual_tabs_content}

            <!-- 格言タブ -->
            {quote_tab_content}

            <!-- ストーリータブ -->
            {story_tab_content}
        </div>

        <!-- フッター -->
        <div class="footer">
            最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} JST<br>　
           Enjoy Daily Life with the Latest News
        </div>
    </div>
    
    <script>
        // タブ切り替え機能
        document.addEventListener('DOMContentLoaded', function() {{
            const tabButtons = document.querySelectorAll('.tab-button');
            const tabContents = document.querySelectorAll('.tab-content');

            tabButtons.forEach(button => {{
                button.addEventListener('click', function() {{
                    const targetTab = this.getAttribute('data-tab');

                    // アクティブ状態をリセット
                    tabButtons.forEach(btn => btn.classList.remove('active'));
                    tabContents.forEach(content => content.classList.remove('active'));

                    // 新しいアクティブ状態を設定
                    this.classList.add('active');
                    document.getElementById(targetTab).classList.add('active');
                }});
            }});

            // スクロールアニメーション
            const observerOptions = {{
                threshold: 0.1,
                rootMargin: '0px 0px -100px 0px'
            }};

            const observer = new IntersectionObserver(function(entries) {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.classList.add('visible');
                    }}
                }});
            }}, observerOptions);

            // スクロールフェード要素を監視
            document.querySelectorAll('.scroll-fade').forEach(el => {{
                observer.observe(el);
            }});

            // ニュースアイテムにホバーエフェクト
            document.querySelectorAll('.news-item').forEach(item => {{
                item.addEventListener('mouseenter', function() {{
                    this.style.transform = 'translateX(10px)';
                }});

                item.addEventListener('mouseleave', function() {{
                    this.style.transform = 'translateX(0)';
                }});
            }});

            // キーボードショートカット
            document.addEventListener('keydown', function(e) {{
                if (e.altKey) {{
                    switch(e.key) {{
                        case '1':
                            e.preventDefault();
                            document.querySelector('[data-tab="all"]').click();
                            break;
                        case '2':
                            e.preventDefault();
                            document.querySelector('[data-tab="softbank"]').click();
                            break;
                        case '3':
                            e.preventDefault();
                            document.querySelector('[data-tab="taisho"]').click();
                            break;
                        case '4':
                            e.preventDefault();
                            document.querySelector('[data-tab="sbi"]').click();
                            break;
                        case '5':
                            e.preventDefault();
                            document.querySelector('[data-tab="quote"]').click();
                            break;
                        case '6':
                            e.preventDefault();
                            document.querySelector('[data-tab="story"]').click();
                            break;
                    }}
                }}
            }});
        }});
    </script>
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
