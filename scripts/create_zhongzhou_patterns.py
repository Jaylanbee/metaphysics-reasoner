import json
import os

def create_zhongzhou_patterns():
    """
    建立《中州學派》格局判定規則的 JSON 骨架
    """
    target_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "zhongzhou_patterns_v2.json")

    # 定義基本的格局骨架
    patterns = [
        {
            "patternId": "P_JI_YUE_TONG_LIANG",
            "patternName": "機月同梁格",
            "category": "富貴/穩定",
            "condition": {
                "description": "命宮在寅申，三方四正會齊天機、太陰、天同、天梁",
                "rules": [
                    {"target": "命宮", "stars": ["天機", "太陰", "天同", "天梁"], "operator": "ALL_IN_SAN_FANG_SI_ZHENG"}
                ]
            },
            "interpretation": {
                "classic": "寅申機月同梁會，公吏職居",
                "modern": "適合公職、大企業幕僚、教育或醫療體系。性格穩重保守，適合穩定累積。",
                "exception": "若會照煞星過多（擎羊、陀羅、火星、鈴星），則主懷才不遇或需以特殊技藝安身。"
            },
            "source": "中州學派經典",
            "version": "2.0"
        },
        {
            "patternId": "P_ZI_FU_TONG_GONG",
            "patternName": "紫府同宮格",
            "category": "貴氣",
            "condition": {
                "description": "紫微與天府同在命宮（必定在寅或申宮）",
                "rules": [
                    {"target": "命宮", "stars": ["紫微", "天府"], "operator": "IN_SAME_PALACE"},
                    {"target": "命宮", "positions": ["寅", "申"], "operator": "IN_POSITION"}
                ]
            },
            "interpretation": {
                "classic": "紫府同宮，終身福厚",
                "modern": "自尊心極強，具備統御能力，但有時會陷入『孤高』或『優柔寡斷』（兩顆帝星相抗）。適合大平臺發揮。",
                "exception": "若無左輔右弼同宮或會照，則為『孤君』，徒有虛名而無實權。"
            },
            "source": "中州學派經典",
            "version": "2.0"
        }
    ]

    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(patterns, f, ensure_ascii=False, indent=2)

    print(f"已建立中州學派格局規則骨架: {target_file}")

if __name__ == "__main__":
    create_zhongzhou_patterns()