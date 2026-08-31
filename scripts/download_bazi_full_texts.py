import json
import os
import requests
import re
from bs4 import BeautifulSoup

def fetch_bazi_classic_texts():
    """
    從公有領域百科/維基百科下載真實完整的八字古籍文獻，並清洗儲存為 RAG 所需的 JSON
    此處以維基文庫 (Wikisource) 作為可信的開放來源進行爬取
    """
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "..", "data", "classics")
    os.makedirs(data_dir, exist_ok=True)

    # 維基文庫的八字古籍來源
    sources = [
        {
            "file": "yuanhaiziping_cleaned.json",
            "book": "淵海子平",
            "chapter": "淵海子平全文",
            # 淵海子平
            "url": "https://zh.wikisource.org/zh-hant/%E6%B7%B5%E6%B5%B7%E5%AD%90%E5%B9%B3"
        },
        {
            "file": "sanmingtonghui_cleaned.json",
            "book": "三命通會",
            "chapter": "卷一至卷十二精選",
            # 三命通會第一卷
            "url": "https://zh.wikisource.org/zh-hant/%E4%B8%89%E5%91%BD%E9%80%9A%E6%9C%83_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%8D%B701"
        }
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print("開始下載真實八字古籍全文...")

    for source in sources:
        print(f"正在擷取《{source['book']}》全文...")
        try:
            response = requests.get(source['url'], headers=headers)
            response.raise_for_status()

            # 使用 BeautifulSoup 清洗 HTML，只取內文段落
            soup = BeautifulSoup(response.text, 'html.parser')
            content_div = soup.find('div', class_='mw-parser-output')

            if content_div:
                paragraphs = content_div.find_all('p')
                full_text = "\n".join([p.get_text() for p in paragraphs if len(p.get_text().strip()) > 10])

                # 清除引用標籤 [1] 等
                full_text = re.sub(r'\[\d+\]', '', full_text)

                if len(full_text) > 100:
                    output_data = {
                        "book": source["book"],
                        "chapter": source["chapter"],
                        "originalText": full_text,
                        "annotations": {},
                        "source": source["url"]
                    }

                    output_path = os.path.join(data_dir, source["file"])
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(output_data, f, ensure_ascii=False, indent=2)

                    print(f"✅ 《{source['book']}》下載與清洗完成！字數: {len(full_text)}")
                else:
                    print(f"❌ 擷取失敗或內文過短: {source['book']}")
            else:
                 print(f"❌ 找不到內文標籤: {source['book']}")

        except Exception as e:
            print(f"下載失敗 {source['book']}: {e}")

if __name__ == "__main__":
    fetch_bazi_classic_texts()
