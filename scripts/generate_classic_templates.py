import os

def generate_classic_templates():
    """
    產生紫微古籍三本文本清洗與標註的骨架 (JSON 格式範例)
    """
    classics_dir = os.path.join(os.path.dirname(__file__), "..", "data", "classics")

    # 古籍清單
    books = [
        {"filename": "gusuifu_cleaned.json", "book": "紫微斗數骨髓賦"},
        {"filename": "quanji_cleaned.json", "book": "紫微斗數全集"},
        {"filename": "quanshu_cleaned.json", "book": "紫微斗數全書"}
    ]

    template = """{
  "book": "%s",
  "chapter": "第一章 (範例)",
  "originalText": "（待填入清洗後的純文字...）",
  "annotations": {
    "關鍵詞1": "解釋1"
  },
  "source": "ziwei-doushu-skill/lib/classics/"
}"""

    for book in books:
        filepath = os.path.join(classics_dir, book["filename"])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template % book["book"])
        print(f"已建立古籍標註骨架: {filepath}")

if __name__ == "__main__":
    generate_classic_templates()
