import os
from datetime import datetime

# --- ① シークレットからAPIキーを取得（環境変数）
API_KEY = os.getenv("MY_API_KEY")

# --- ② ニュースや格言などのデータを取得（ここは仮データ）
quote = "「全盛期？これからだよ」 - 三浦知良"
story = "電車で出会った彼女との何気ない5分間の会話が、ずっと心に残っている。"
today = datetime.now().strftime('%Y年%m月%d日')

# --- ③ HTMLテンプレート
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
        <h2>今日の格言</h2>
        <p>{quote}</p>
    </div>
    <div style="background:#f0f8ff;padding:1em;border-radius:8px;margin-top:1em;">
        <h2>今日のショートストーリー</h2>
        <p>{story}</p>
    </div>
</body>
</html>
"""

# --- ④ 出力ファイル名（GitHub Pages用に index.html）
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ HTMLファイルを生成しました（index.html）")
