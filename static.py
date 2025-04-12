# static.py：靜態網頁爬蟲，將 Yahoo 新聞首頁文章標題與網址存入 static.csv

import requests
from bs4 import BeautifulSoup
import csv

# 網頁目標
url = "https://tw.news.yahoo.com/"
headers = {"User-Agent": "Mozilla/5.0"}

# 發送請求
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# 擷取標題與網址
news_list = []
for item in soup.select("a[href^='https://tw.news.yahoo.com']"):
    title = item.get_text().strip()
    link = item["href"]
    if title and len(title) > 10 and link not in [x[1] for x in news_list]:
        news_list.append([title, link])
    if len(news_list) >= 10:  # 最多取前10則
        break

# 寫入 CSV
with open("static.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["標題", "網址"])
    writer.writerows(news_list)

print("新聞已寫入 static.csv")
