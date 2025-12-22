import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def scrape_price():
    # 你的目标网址
    url = "https://ochem.sci99.com/info/1_40696_43585356_1.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            # 这里先用模拟数据确保流程能跑通。
            # 如果要抓取真实标签，需要根据页面源码修改这里的 soup.find 逻辑
            price = 12000 + (datetime.now().day * 5) 
            
            new_entry = {
                "date": datetime.now().strftime("%m-%d"),
                "price": price
            }
            return new_entry
    except Exception as e:
        print(f"抓取失败: {e}")
    return None

def update_json(new_entry):
    file_path = 'data.json'
    data = []
    
    # 如果文件已存在，先读取旧数据
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    # 防止同一天重复记录
    if new_entry and (not data or data[-1]['date'] != new_entry['date']):
        data.append(new_entry)
    
    # 只保留最近 30 天的数据
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data[-30:], f, indent=4)

if __name__ == "__main__":
    entry = scrape_price()
    if entry:
        update_json(entry)
        print(f"✅ 成功更新数据: {entry}")
