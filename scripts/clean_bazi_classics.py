import json
import os

def create_bazi_classics_skeleton():
    """
    建立八字五大名著的 JSON 骨架與部分模擬原文，供 RAG 檢索使用
    """
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "..", "data", "classics")
    os.makedirs(data_dir, exist_ok=True)

    bazi_books = [
        {
            "file": "yuanhaiziping_cleaned.json",
            "book": "淵海子平",
            "chapter": "論十干",
            "text": "甲木天上貴，乙木人間生。丙火猛烈，欺霜侮雪。丁火柔中，內性昭融。正印乃生我之母，主文雅、學術與庇護。正官乃治國之本，主權力與法度。"
        },
        {
            "file": "sanmingtonghui_cleaned.json",
            "book": "三命通會",
            "chapter": "論十神",
            "text": "傷官見官，為禍百端。食神生財，富貴自天排。七殺化印，乃將相之才。偏財透出，慷慨孟嘗。日主身弱遇印，如枯苗得雨。"
        },
        {
            "file": "ditiansui_cleaned.json",
            "book": "滴天髓",
            "chapter": "通神論",
            "text": "欲知其人富，財氣通門戶。欲知其人貴，官星有理會。木盛逢者，必見其傷。火炎土燥，必用水潤。五行和者，一世無災。"
        },
        {
            "file": "zipingzhenquan_cleaned.json",
            "book": "子平真詮",
            "chapter": "論用神",
            "text": "八字用神，專求月令。以日干配月令地支，而生剋不同，格局分焉。財官印食，此用神之善而順用之者也；殺傷劫刃，用神之不善而逆用之者也。"
        },
        {
            "file": "qiongtongbaojian_cleaned.json",
            "book": "窮通寶鑑",
            "chapter": "論木",
            "text": "春月之木，猶有餘寒，得火溫之，乃無盤屈之患。秋月之木，氣漸淒涼，形漸凋敗。夏木枝葉繁盛，用水潤之。冬木枯槁，得火暖之乃吉。"
        }
    ]

    for info in bazi_books:
        output_data = {
            "book": info["book"],
            "chapter": info["chapter"],
            "originalText": info["text"] + "\n\n... (截取片段，供 RAG 檢索骨架測試使用)",
            "annotations": {},
            "source": f"manual_extraction/{info['file']}"
        }

        output_path = os.path.join(data_dir, info["file"])
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"已輸出八字古籍骨架至：{output_path}")

    print("八字古籍骨架清洗作業完成！")
    return True

if __name__ == "__main__":
    create_bazi_classics_skeleton()