import requests
from bs4 import BeautifulSoup
import csv
import sys

def getStock(code):
    #使用這輸入的股票網址
    url = f'https://tw.stock.yahoo.com/quote/{code}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    web = requests.get(url, headers=headers)
    soup = BeautifulSoup(web.text, "html.parser")

    try:
        title = soup.select_one('h1.C\\(\\$c-link-text\\)').get_text() #股票名稱
        price = soup.select_one('.Fz\\(32px\\)').get_text() #股票現價
        change = soup.select_one('.Fz\\(20px\\)').get_text() #股票漲幅
        trend = ''
        #判斷漲跌
        if soup.select_one('#main-0-QuoteHeader-Proxy .C\\(\\$c-trend-down\\)'):
            trend = '-'
        elif soup.select_one('#main-0-QuoteHeader-Proxy .C\\(\\$c-trend-up\\)'):
            trend = '+'

        return [title, code, price, f'{trend}{change}']

    except Exception as e:
        print(f"抓取失敗: {url}，錯誤訊息：{e}")
        return [f"錯誤：{code}", "", "", ""]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # command line 模式：從 sys.argv[1:] 取得代碼
        stock_codes = sys.argv[1:]
    else:
        # 互動模式
        user_input = input("請輸入股票代碼（用空格分隔）：")
        stock_codes = [code.strip() for code in user_input.split() if code.strip()]

    results = [getStock(code) for code in stock_codes]

    with open("api.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["名稱", "代碼", "現價", "漲跌"])
        writer.writerows(results)

    print("股票查詢完成，api.csv 已寫入")