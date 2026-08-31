import json
import os

def create_bazi_foundations():
    """
    建立八字命理（天干地支、五行、十神）的 JSON 骨架
    """
    target_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "bazi_foundations.json")

    # 定義八字基礎骨架
    foundations = {
        "version": "1.0",
        "source": "《現代八字命理學綱要》及經典子平法",
        "wuxing": {
            "木": {"attribute": "生發、條達", "color": "綠", "direction": "東"},
            "火": {"attribute": "炎上、熱烈", "color": "紅", "direction": "南"},
            "土": {"attribute": "稼穡、包容", "color": "黃", "direction": "中"},
            "金": {"attribute": "從革、肅殺", "color": "白", "direction": "西"},
            "水": {"attribute": "潤下、流動", "color": "黑", "direction": "北"}
        },
        "tiangan": {
            "甲": {"element": "木", "polarity": "陽", "image": "參天大樹", "modern_trait": "具備領導力、直來直往、仁慈但固執"},
            "乙": {"element": "木", "polarity": "陰", "image": "花草藤蔓", "modern_trait": "適應力強、善於交際、身段柔軟"},
            "丙": {"element": "火", "polarity": "陽", "image": "太陽之火", "modern_trait": "熱情奔放、樂於助人、性急"},
            "丁": {"element": "火", "polarity": "陰", "image": "燈燭之火", "modern_trait": "細膩敏感、外柔內剛、具洞察力"},
            "戊": {"element": "土", "polarity": "陽", "image": "城牆之土", "modern_trait": "穩重固執、包容力強、重視信用"},
            "己": {"element": "土", "polarity": "陰", "image": "田園之土", "modern_trait": "溫和內斂、注重細節、包容性強"},
            "庚": {"element": "金", "polarity": "陽", "image": "刀劍之金", "modern_trait": "果斷剛毅、重義氣、具破壞力"},
            "辛": {"element": "金", "polarity": "陰", "image": "珠寶之金", "modern_trait": "精緻完美主義、愛面子、溫潤秀氣"},
            "壬": {"element": "水", "polarity": "陽", "image": "江河之水", "modern_trait": "聰明活躍、心胸寬廣、變化多端"},
            "癸": {"element": "水", "polarity": "陰", "image": "雨露之水", "modern_trait": "細膩聰慧、心思深沉、重視精神面"}
        },
        "shishen": {
            "正官": {"relation": "剋我者，陰陽異性", "core_meaning": "法規、權力、理性", "modern_career": "公職、大企業管理、法務"},
            "七殺": {"relation": "剋我者，陰陽同性", "core_meaning": "權威、破壞、冒險", "modern_career": "軍警、創業者、業務、外科"},
            "正印": {"relation": "生我者，陰陽異性", "core_meaning": "庇護、學術、傳統", "modern_career": "教育、研究、宗教、行政"},
            "偏印": {"relation": "生我者，陰陽同性", "core_meaning": "非主流學術、直覺、孤僻", "modern_career": "設計、占星命理、藝術、偏門研究"},
            "比肩": {"relation": "同我者，陰陽同性", "core_meaning": "自我、競爭、朋友", "modern_career": "自由業、合夥、獨立作業"},
            "劫財": {"relation": "同我者，陰陽異性", "core_meaning": "奪取、行動力、投機", "modern_career": "業務、公關、競技、冒險性行業"},
            "食神": {"relation": "我生者，陰陽同性", "core_meaning": "才華、享受、溫和", "modern_career": "餐飲、文學、服務業、教育"},
            "傷官": {"relation": "我生者，陰陽異性", "core_meaning": "才華外露、反叛、創新", "modern_career": "演藝、創意、律師、行銷"},
            "正財": {"relation": "我剋者，陰陽異性", "core_meaning": "固定資產、勞動所得、妻", "modern_career": "金融、會計、穩定受薪階級"},
            "偏財": {"relation": "我剋者，陰陽同性", "core_meaning": "流動資產、投機、交際", "modern_career": "貿易、投資、業務、企業家"}
        }
    }

    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(foundations, f, ensure_ascii=False, indent=2)

    print(f"已建立八字基礎 JSON 骨架: {target_file}")

if __name__ == "__main__":
    create_bazi_foundations()