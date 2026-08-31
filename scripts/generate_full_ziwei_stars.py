import json
import os

def generate_full_ziwei_stars():
    """
    產生包含全部 14 顆主星的 JSON 骨架
    """
    target_file = os.path.join(os.path.dirname(__file__), "..", "data", "ziwei_stars_definition.json")

    stars = [
        "紫微", "天機", "太陽", "武曲", "天同", "廉貞", "天府",
        "太陰", "貪狼", "巨門", "天相", "天梁", "七殺", "破軍"
    ]

    palaces = [
        "命宮", "兄弟宮", "夫妻宮", "子女宮", "財帛宮", "疾厄宮",
        "遷移宮", "交友宮", "官祿宮", "田宅宮", "福德宮", "父母宮"
    ]

    # 建立 14 顆星的骨架
    star_list = []
    for star in stars:
        star_data = {
            "starName": star,
            "category": "major",
            "coreMeaning": f"{star}星的核心意義待填入...",
            "palaceEffects": {palace: "" for palace in palaces},
            "modernInterpretation": {
                "職場": "",
                "人際": "",
                "情感": ""
            },
            "source": "《慧心齋主談命宮》",
            "version": "1.0"
        }

        # 保留原有的紫微星範例內容
        if star == "紫微":
            star_data["coreMeaning"] = "帝王星，領導力、權威、尊貴"
            star_data["palaceEffects"]["命宮"] = "自尊心強，有領導才能，不喜受人約束"
            star_data["palaceEffects"]["兄弟宮"] = "兄弟中有成就較高者，或得兄弟助力"
            star_data["palaceEffects"]["夫妻宮"] = "配偶能力強，但需注意相處時的權力平衡"
            star_data["modernInterpretation"]["職場"] = "適合管理職、創業、決策型工作"
            star_data["modernInterpretation"]["人際"] = "需注意過度強勢，學習授權與傾聽"
            star_data["modernInterpretation"]["情感"] = "感情中需要主導權，宜找能配合的對象"

        star_list.append(star_data)

    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(star_list, f, ensure_ascii=False, indent=2)

    print(f"✅ 已成功建立包含 14 顆主星的 JSON，路徑: {target_file}")

if __name__ == "__main__":
    generate_full_ziwei_stars()