import json
import os

def fill_patterns():
    filepath = os.path.join(os.path.dirname(__file__), "..", "data", "zhongzhou_patterns_v2.json")
    with open(filepath, 'r', encoding='utf-8') as f:
        patterns = json.load(f)

    # 新增幾條常見的中州派格局，以達到「填補齊全」的目標
    new_patterns = [
        {
            "patternId": "P_YUE_LANG_TIAN_MEN",
            "patternName": "月朗天門格",
            "category": "富貴",
            "condition": {
                "description": "太陰在亥宮守命",
                "rules": [
                    {"target": "命宮", "stars": ["太陰"], "operator": "IN_SAME_PALACE"},
                    {"target": "命宮", "positions": ["亥"], "operator": "IN_POSITION"}
                ]
            },
            "interpretation": {
                "classic": "月朗天門，進爵封侯",
                "modern": "太陰在亥宮最為明亮，主財源廣進、房地產豐厚，性格溫和但內在堅定。適合從事金融、房地產、設計或企劃。",
                "exception": "若見地空、地劫，則容易變為華而不實，或為宗教命理之士。"
            },
            "source": "中州學派經典",
            "version": "2.0"
        },
        {
            "patternId": "P_JU_RI_TONG_GONG",
            "patternName": "巨日同宮格",
            "category": "競爭/名聲",
            "condition": {
                "description": "太陽、巨門同在寅宮守命",
                "rules": [
                    {"target": "命宮", "stars": ["太陽", "巨門"], "operator": "IN_SAME_PALACE"},
                    {"target": "命宮", "positions": ["寅"], "operator": "IN_POSITION"}
                ]
            },
            "interpretation": {
                "classic": "巨日同宮，官封三代",
                "modern": "太陽驅散巨門的暗曜，主能言善道、具備強大的說服力與影響力。適合從事律師、跨國企業代表、教師或自媒體。但競爭激烈。",
                "exception": "若在申宮則太陽偏暗，格局大打折扣，容易多口舌是非而少實質成就。"
            },
            "source": "中州學派經典",
            "version": "2.0"
        },
        {
            "patternId": "P_YANG_TUO_JIA_JI",
            "patternName": "羊陀夾忌格",
            "category": "凶局/破格",
            "condition": {
                "description": "命宮化忌，且前後兩宮被擎羊、陀羅夾制（必定同時有祿存同宮化忌）",
                "rules": [
                    {"target": "命宮", "stars": ["化忌", "祿存"], "operator": "IN_SAME_PALACE"}
                ] # 簡化邏輯：祿存必定被羊陀夾，若祿存與化忌同宮，即構成羊陀夾忌。
            },
            "interpretation": {
                "classic": "羊陀夾忌為敗局",
                "modern": "代表人生常面臨被前後包夾、進退維谷的困境，或是看似有財（祿存）卻無法動用（化忌），甚至因財惹禍。需學習放下執念與退讓。",
                "exception": "如果三方四正有強力的吉星（如紫微化權），可以轉為危機處理專家，但也極其辛苦。"
            },
            "source": "中州學派經典",
            "version": "2.0"
        }
    ]

    # 合併現有與新的格局
    # 避免重複添加 (使用 patternId 作為檢查基準)
    existing_ids = {p["patternId"] for p in patterns}
    for np in new_patterns:
        if np["patternId"] not in existing_ids:
            patterns.append(np)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(patterns, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fill_patterns()
    print("✅ 中州學派常見核心格局已填補擴充。")
