
import twstock
import csv
import sys

def fetch_twstock_info(codes):
    results = []
    for code in codes:
        data = twstock.realtime.get(code)
        if data['success']:
            results.append([
                data['info']['name'],
                code,
                data['realtime']['latest_trade_price'],
                data['realtime']['open'],
                data['realtime']['high'],
                data['realtime']['low'],
            ])
        else:
            print(f"無法查詢 {code}")
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        stock_codes = sys.argv[1:]
    else:
        user_input = input("請輸入股票代號（例如 2330 2317）：")
        stock_codes = user_input.strip().split()

    results = fetch_twstock_info(stock_codes)

    with open("api.csv", "w", newline='', encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["公司名稱", "代碼", "現價", "開盤", "最高", "最低"])
        writer.writerows(results)

    print("已寫入 api.csv")
    for row in results:
        print("｜".join(map(str, row)))
