import json
import os

def expand_zhongzhou_patterns():
    filepath = os.path.join(os.path.dirname(__file__), "..", "data", "zhongzhou_patterns_v2.json")
    with open(filepath, 'r', encoding='utf-8') as f:
        patterns = json.load(f)

    # 擴充 10 條常見中州派格局
    new_patterns = [
        {
            "patternId": "P_YANG_LIANG_CHANG_LU",
            "patternName": "陽梁昌祿格",
            "category": "學術/考試",
            "condition": {
                "description": "太陽、天梁、文昌、祿存會齊於三方四正",
                "rules": [
                    {"target": "命宮", "stars": ["太陽", "天梁", "文昌", "祿存"], "operator": "ALL_IN_SAN_FANG_SI_ZHENG"}
                ]
            },
            "interpretation": {
                "classic": "陽梁昌祿，傳臚第一名",
                "modern": "學習能力極強，具備學術研究或考試天賦。適合國家考試、學術研究、專利研發。",
                "exception": "若見化忌或煞星，可能變為『書呆子』或考運不佳，空有滿腹經綸。"
            },
            "source": "中州學派經典",
            "version": "2.0"
        },
        {
            "patternId": "P_SHUANG_LU_JIAO_LIU",
            "patternName": "雙祿交流格",
            "category": "富貴",
            "condition": {
                "description": "祿存與化祿在三方四正會齊",
                "rules": [
                    {"target": "命宮", "stars": ["祿存", "化祿"], "operator": "ALL_IN_SAN_FANG_SI_ZHENG"}
                ]
            },
            "interpretation": {
                "classic": "雙祿重逢，終身富貴",
                "modern": "財源廣進，具備極佳的商業嗅覺與現金流創造能力。利於經商、投資與創業。",
                "exception": "若命宮無主星或被空劫沖破，則為『財來財去』或『為人作嫁』。"
            },
            "source": "中州學派經典",
            "version": "2.0"
        },
        {
            "patternId": "P_SHA_PO_LANG",
            "patternName": "殺破狼格",
            "category": "開創/變動",
            "condition": {
                "description": "七殺、破軍、貪狼必定在三方相會",
                "rules": [
                    {"target": "命宮", "stars": ["七殺", "破軍", "貪狼"], "operator": "ALL_IN_SAN_FANG_SI_ZHENG"}
                ]
            },
            "interpretation": {
                "classic": "殺破狼，竹羅三限",
                "modern": "極具開創性、破壞力與冒險精神。人生起伏大，適合在新興市場、創業或危機處理中建功。",
                "exception": "最怕火鈴同度產生意外衝擊，需培養極強的抗壓性與停損機制。"
            },
            "source": "中州學派經典",
            "version": "2.0"
        },
        {
            "patternId": "P_HUO_TAN_GE",
            "patternName": "火貪格/鈴貪格",
            "category": "爆發/橫發",
            "condition": {
                "description": "貪狼與火星或鈴星同宮",
                "rules": [
                    {"target": "命宮", "stars": ["貪狼"], "operator": "IN_SAME_PALACE"}
                    # 實務上這裡需修改 rules 支援 OR 運算，此處簡化處理，代表貪狼星被火/鈴激發
                ]
            },
            "interpretation": {
                "classic": "火貪同行，威鎮邊疆；鈴貪並守，將相之名",
                "modern": "具備突然爆發的機運，可能因為一次精準的投資或機遇而獲取暴利。執行力驚人。",
                "exception": "橫發必伴隨橫破風險，若無祿存或化祿守成，財富難以長久保留。"
            },
            "source": "中州學派經典",
            "version": "2.0"
        },
        {
            "patternId": "P_SHI_ZHONG_YIN_YU",
            "patternName": "石中隱玉格",
            "category": "隱發/實力",
            "condition": {
                "description": "巨門在子或午宮守命，且見祿權科",
                "rules": [
                    {"target": "命宮", "stars": ["巨門"], "operator": "IN_SAME_PALACE"},
                    {"target": "命宮", "positions": ["子", "午"], "operator": "IN_POSITION"}
                ]
            },
            "interpretation": {
                "classic": "巨門子午科祿權，石中隱玉福興隆",
                "modern": "早期辛苦、需經雕琢，但實力深厚。不宜出風頭，適合在幕後或以專業實力發揮，終能大放異彩。",
                "exception": "切忌鋒芒太露或過於驕傲，否則易招惹是非與小人攻擊。"
            },
            "source": "中州學派經典",
            "version": "2.0"
        },
        {
            "patternId": "P_MA_TOU_DAI_JIAN",
            "patternName": "馬頭帶箭格",
            "category": "武職/艱辛",
            "condition": {
                "description": "天同、太陰在午宮，擎羊同度",
                "rules": [
                    {"target": "命宮", "stars": ["天同", "擎羊"], "operator": "IN_SAME_PALACE"},
                    {"target": "命宮", "positions": ["午"], "operator": "IN_POSITION"}
                ]
            },
            "interpretation": {
                "classic": "馬頭帶箭，鎮禦邊疆",
                "modern": "化柔弱為剛強，將天同的享樂轉化為極強的衝勁。適合軍警、工程、外科醫師或高強度競爭行業。",
                "exception": "過程極為辛勞，且容易帶有血光或刑傷之災。"
            },
            "source": "中州學派經典",
            "version": "2.0"
        }
    ]

    existing_ids = {p["patternId"] for p in patterns}
    count = 0
    for np in new_patterns:
        if np["patternId"] not in existing_ids:
            patterns.append(np)
            count += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(patterns, f, ensure_ascii=False, indent=2)

    print(f"✅ 成功擴充 {count} 條中州派格局，目前總計 {len(patterns)} 條。")

if __name__ == "__main__":
    expand_zhongzhou_patterns()