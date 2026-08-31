import json
import os

class DestinyReasoner:
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        self.data_dir = os.path.join(self.base_dir, "..", "data")
        self.exact_map_file = os.path.join(self.data_dir, "pattern_to_classics_map.json")
        self.exact_map = {}
        if os.path.exists(self.exact_map_file):
            try:
                with open(self.exact_map_file, "r", encoding="utf-8") as ef:
                    self.exact_map = json.load(ef)
            except Exception:
                pass
        self.zhongzhou_patterns = self._load_json("zhongzhou_patterns_v2.json")
        self.bazi_foundations = self._load_json("bazi_foundations.json")
        self.classics_corpus = self._load_classics()

        # 初始化 ChromaDB 客戶端供八字 RAG 檢索使用
        self.chroma_client = None
        self.bazi_collection = None
        self._init_chromadb()

        # 12 地支順序，用於推算三方四正
        self.dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    def _get_san_fang_si_zheng(self, current_zhi):
        """
        根據目前地支，推算三方（相合）與四正（對沖）的地支
        三方：間隔 4 個地支 (120度)
        四正(對沖)：間隔 6 個地支 (180度)
        """
        if current_zhi not in self.dizhi:
            return []

        idx = self.dizhi.index(current_zhi)
        san_fang_1 = self.dizhi[(idx + 4) % 12]
        san_fang_2 = self.dizhi[(idx + 8) % 12]
        si_zheng = self.dizhi[(idx + 6) % 12]

        return [current_zhi, san_fang_1, san_fang_2, si_zheng]

    def _get_stars_in_positions(self, chart_data, positions):
        """獲取指定多個地支宮位內的所有星曜"""
        stars = []
        for palace_name, data in chart_data.get("palaces", {}).items():
            if data.get("position") in positions:
                stars.extend(data.get("stars", []))
        return list(set(stars)) # 確保不重複

    def _load_json(self, filename):
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            print(f"Warning: {filename} not found.")
            return {}
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_classics(self):
        """載入古籍文本作為簡單的 RAG 語料庫"""
        corpus = []
        classics_dir = os.path.join(self.data_dir, "classics")
        if os.path.exists(classics_dir):
            for filename in os.listdir(classics_dir):
                if filename.endswith("_cleaned.json"):
                    with open(os.path.join(classics_dir, filename), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if "originalText" in data:
                            corpus.append(data["originalText"])
        return "\n".join(corpus)

    def _init_chromadb(self):
        try:
            import chromadb
            from chromadb.utils import embedding_functions
            chroma_db_dir = os.path.join(self.data_dir, "chroma_db")
            if os.path.exists(chroma_db_dir):
                self.chroma_client = chromadb.PersistentClient(path=chroma_db_dir)
                self.bazi_collection = self.chroma_client.get_collection(
                    name="bazi_knowledge",
                    embedding_function=embedding_functions.DefaultEmbeddingFunction()
                )
        except Exception as e:
            # 若無安裝套件或資料庫不存在，則靜默略過
            pass

    def _retrieve_bazi_quote(self, query_text):
        """真實 RAG 檢索：向 ChromaDB 查詢八字古籍文獻"""
        if not self.bazi_collection:
            return None
        try:
            results = self.bazi_collection.query(
                query_texts=[query_text],
                n_results=1
            )
            docs = results.get("documents", [[]])[0]
            metas = results.get("metadatas", [[]])[0]
            if docs and metas:
                return f"《{metas[0].get('source', '古籍')}》: 「{docs[0]}」"
        except Exception:
            pass
        return None

    def _retrieve_classic_quote(self, pattern_name):
        """簡單的關鍵字檢索，模擬 RAG 的 Retrieve 過程"""
        if not self.classics_corpus:
            return None

        # 以格局名稱的前兩個字作為關鍵字去古籍中尋找
        keyword = pattern_name[:2]
        lines = self.classics_corpus.split('\n')
        for line in lines:
            if keyword in line and len(line) > 10:
                return line.strip()
        return None

    def analyze_ziwei_chart(self, chart_data):
        """
        分析紫微命盤，回傳符合的格局與解析
        """
        results = []

        if not isinstance(self.zhongzhou_patterns, list):
            print("Error: zhongzhou_patterns is not loaded correctly.")
            return results

        # 1. 靜態本命格局分析
        for pattern in self.zhongzhou_patterns:
            condition = pattern.get("condition", {})
            rules = condition.get("rules", [])

            is_match = True
            for rule in rules:
                target_palace = rule.get("target")
                operator = rule.get("operator")

                # 獲取命盤中該宮位的星星與地支
                palace_data = chart_data.get("palaces", {}).get(target_palace, {})
                stars_in_palace = palace_data.get("stars", [])
                position = palace_data.get("position", "")

                if operator == "IN_SAME_PALACE":
                    required_stars = rule.get("stars", [])
                    # 檢查 required_stars 是否全部都在 stars_in_palace 中
                    if not all(star in stars_in_palace for star in required_stars):
                        is_match = False
                        break

                elif operator == "IN_SAME_PALACE_ANY":
                    required_stars = rule.get("stars", [])
                    # 檢查 required_stars 是否至少有一個在 stars_in_palace 中
                    if not any(star in stars_in_palace for star in required_stars):
                        is_match = False
                        break

                elif operator == "IN_POSITION":
                    required_positions = rule.get("positions", [])
                    if position not in required_positions:
                        is_match = False
                        break

                elif operator == "ALL_IN_SAN_FANG_SI_ZHENG":
                    required_stars = rule.get("stars", [])
                    # 真實三方四正演算法推演
                    if not position:
                        is_match = False
                        break

                    target_positions = self._get_san_fang_si_zheng(position)
                    san_fang_stars = self._get_stars_in_positions(chart_data, target_positions)

                    if not all(star in san_fang_stars for star in required_stars):
                        is_match = False
                        break

            if is_match:
                # 檢查三方四正煞星例外情況
                shaxing = ["擎羊", "陀羅", "火星", "鈴星", "地空", "地劫"]
                if condition.get("rules") and condition["rules"][0].get("target"):
                    main_pos = chart_data.get("palaces", {}).get(condition["rules"][0]["target"], {}).get("position")
                    if main_pos:
                        sf_positions = self._get_san_fang_si_zheng(main_pos)
                        sf_stars = self._get_stars_in_positions(chart_data, sf_positions)
                        shaxing_count = sum(1 for star in sf_stars if star in shaxing)
                    else:
                        shaxing_count = 0
                else:
                    shaxing_count = 0

                response = {
                    "patternName": pattern.get("patternName"),
                    "category": pattern.get("category"),
                    "analysis": pattern.get("interpretation", {}).get("modern")
                }

                # 結合 RAG 檢索古籍引言
                quote = self._retrieve_classic_quote(pattern.get("patternName"))
                if quote:
                    response["classic_quote"] = f"古籍印證: 「...{quote}...」"
                else:
                    response["classic_quote"] = f"古籍印證: {pattern.get('interpretation', {}).get('classic')}"

                if shaxing_count > 1:
                    response["warning"] = pattern.get("interpretation", {}).get("exception")

                results.append(response)

        # 2. 動態流年分析 (若有提供 current_year_data)
        current_year_data = chart_data.get("current_year_data", {})
        if current_year_data:
            year_name = current_year_data.get("year", "未知年份")
            year_palace = current_year_data.get("palace", "")
            sihua = current_year_data.get("sihua", {})

            # 獲取流年命宮的本命星曜
            palace_data = chart_data.get("palaces", {}).get(year_palace, {})
            year_position = palace_data.get("position", "")
            stars_in_year_palace = palace_data.get("stars", [])

            # 取流年三方四正
            sf_positions = self._get_san_fang_si_zheng(year_position)
            sf_stars = self._get_stars_in_positions(chart_data, sf_positions)

            # 複雜流年吉凶判斷邏輯
            # 檢查流年四化是否引動本宮或三方四正
            hua_ji_star = sihua.get("忌", "")
            hua_lu_star = sihua.get("祿", "")

            year_analysis = {
                "year": year_name,
                "palace_position": year_palace,
                "stars_in_palace": stars_in_year_palace,
                "timing_synthesis": ""
            }

            if hua_ji_star in stars_in_year_palace:
                year_analysis["timing_synthesis"] = f"【流年本宮重災】本年流年命宮正逢化忌星（{hua_ji_star}）正沖！諸事不宜躁進，重大投資應極度保守。"
                year_analysis["risk_level"] = "HIGH"
            elif hua_ji_star in sf_stars:
                year_analysis["timing_synthesis"] = f"【流年三方見忌】本年流年三方四正見化忌星（{hua_ji_star}）干擾。雖非本宮正沖，但暗流湧動，需防外來阻力與意外波折。"
                year_analysis["risk_level"] = "MEDIUM-HIGH"
            elif hua_lu_star in stars_in_year_palace:
                year_analysis["timing_synthesis"] = f"【流年本宮大吉】本年流年命宮得化祿星（{hua_lu_star}）照拂！氣運流暢，利於開創、投資與擴張。"
                year_analysis["risk_level"] = "LOW"
            elif hua_lu_star in sf_stars:
                year_analysis["timing_synthesis"] = f"【流年三方迎祿】本年流年三方四正見化祿星（{hua_lu_star}）拱照。得外力協助，投資與事業可穩健推進。"
                year_analysis["risk_level"] = "LOW"
            else:
                year_analysis["timing_synthesis"] = f"【流年平穩過渡】本年流年命宮（{year_palace}）及三方四正氣場平穩，未受重大四化引動。宜按部就班。"
                year_analysis["risk_level"] = "MEDIUM"

            # 將流年分析附加於結果中
            results.append({
                "patternName": f"{year_name} 流年氣運",
                "category": "動態流年",
                "analysis": year_analysis["timing_synthesis"],
                "classic_quote": "古籍印證: 「大限流年，凶星化忌不可當，吉星化祿反呈祥。」"
            })

        return results

    def _calculate_bazi_elements(self, bazi_data, day_master_element):
        """
        計算八字中的五行分數，並初步判斷身強身弱
        這裡做為展示，採用簡化版計分法：
        同黨 (印、比) 得正分，異黨 (官、殺、財、食、傷) 得負分
        """
        # 天干地支五行對照表 (簡化版，無藏干)
        element_map = {
            "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
            "寅": "木", "卯": "木", "巳": "火", "午": "火", "辰": "土", "戌": "土", "丑": "土", "未": "土", "申": "金", "酉": "金", "亥": "水", "子": "水"
        }

        # 生剋關係映射 (生我者為印，同我者為比)
        support_map = {
            "木": ["水", "木"],
            "火": ["木", "火"],
            "土": ["火", "土"],
            "金": ["土", "金"],
            "水": ["金", "水"]
        }

        score = 0
        element_counts = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        supporters = support_map.get(day_master_element, [])

        bazi_pillars = bazi_data.get("bazi", {})
        for pillar, chars in bazi_pillars.items():
            for char in chars:
                element = element_map.get(char)
                if element:
                    element_counts[element] += 1
                    # 簡化計分：同黨+1，異黨-1 (月令通常權重更高，此處暫不展開)
                    if element in supporters:
                        score += 1
                    else:
                        score -= 1

        # 扣除日主本身的一分 (因為日主算同黨，但不列入支持力計算)
        score -= 1

        strength = "身弱" if score < 0 else "身強"

        return {
            "element_counts": element_counts,
            "score": score,
            "strength": strength,
            "advice": "宜用印星(學習/貴人)與比劫(合夥)來幫身" if strength == "身弱" else "宜用食傷(發揮才華)與財官(創業/管理)來洩秀"
        }

    def analyze_bazi_chart(self, bazi_data):
        """
        分析八字命盤，回傳性格、職涯推論與身強身弱判定
        """
        results = {}

        if not self.bazi_foundations:
            print("Error: bazi_foundations is not loaded correctly.")
            return results

        day_master = bazi_data.get("day_master", "")
        dominant_shishen = bazi_data.get("dominant_shishen", "")

        # 日主天干推演
        day_master_element = ""
        tiangan_dict = self.bazi_foundations.get("tiangan", {})
        if day_master in tiangan_dict:
            tg_info = tiangan_dict[day_master]
            day_master_element = tg_info.get("element")
            results["day_master_analysis"] = {
                "day_master": day_master,
                "element": day_master_element,
                "image": tg_info.get("image"),
                "personality": tg_info.get("modern_trait")
            }

        # 五行計分與身強身弱推演
        if day_master_element and bazi_data.get("bazi"):
            element_analysis = self._calculate_bazi_elements(bazi_data, day_master_element)
            results["elemental_analysis"] = element_analysis

        # 主要十神推演
        shishen_dict = self.bazi_foundations.get("shishen", {})
        if dominant_shishen in shishen_dict:
            ss_info = shishen_dict[dominant_shishen]
            results["career_analysis"] = {
                "dominant_shishen": dominant_shishen,
                "core_meaning": ss_info.get("core_meaning"),
                "career_suggestion": ss_info.get("modern_career")
            }

            # 使用 RAG 查詢十神的古籍引言
            bazi_quote = self._retrieve_bazi_quote(dominant_shishen)
            if bazi_quote:
                results["career_analysis"]["classic_quote"] = bazi_quote

        return results

    def analyze_combined_chart(self, ziwei_data, bazi_data):
        """
        紫微八字合參邏輯 (Cross-Reasoning)
        """
        ziwei_results = self.analyze_ziwei_chart(ziwei_data)
        bazi_results = self.analyze_bazi_chart(bazi_data)

        combined_report = {
            "ziwei_summary": ziwei_results,
            "bazi_summary": bazi_results,
            "cross_reasoning_synthesis": ""
        }

        # [合參機制透明度說明]
        # 此處的「紫微 ✕ 八字交叉合參仲裁」採用明確的規則引擎 (Rule-based engine) 進行推論。
        # 目的是為了確保決策的「可追溯性」(Traceability) 與穩健性，
        # 並非依賴不可解釋的統計或機器學習 (ML/Black-box) 模型。
        # 現階段規則：根據紫微星象的靜態破格(煞星)特徵與八字十神(動態/穩健)進行交叉比對仲裁。

        # 明確的合參規則仲裁邏輯 (Rule-based Arbitration Logic)
        zw_has_warning = any("warning" in res for res in ziwei_results)
        bz_career = bazi_results.get("career_analysis", {}).get("dominant_shishen", "")

        if zw_has_warning and bz_career in ["七殺", "傷官", "劫財"]:
            combined_report["cross_reasoning_synthesis"] = (
                "【高度風險警告】紫微星象顯示煞星破格（潛藏波動與挫折），"
                "同時八字由動態/破壞性十神（如七殺、傷官）主導。這種組合極易因衝動或過度自信導致重大破敗。"
                "建議採取極度保守策略，暫緩重大投資或創業，以退為進。"
            )
        elif not zw_has_warning and bz_career in ["正官", "正印", "正財"]:
            combined_report["cross_reasoning_synthesis"] = (
                "【平穩發展契機】紫微星象呈現吉格且無嚴重煞星破壞，"
                "搭配八字由穩定型十神（如正官、正印）主導。這是一段極佳的積累期，"
                "適合按部就班在現有體系內晉升，或進行長線穩健的資產配置。"
            )
        else:
            combined_report["cross_reasoning_synthesis"] = (
                "【中性發展/動態平衡】紫微與八字的氣場呈現互補狀態。"
                "請依據紫微的具體格局建議，搭配八字的本性特質進行靈活調整。"
            )

        return combined_report

if __name__ == "__main__":
    # 簡單的單元測試
    reasoner = DestinyReasoner()

    # 模擬一個命盤：紫微天府在寅宮
    mock_chart = {
        "palaces": {
            "命宮": {
                "position": "寅",
                "stars": ["紫微", "天府", "祿存"]
            }
        },
        "san_fang_si_zheng_stars": ["紫微", "天府", "祿存", "左輔", "文昌"]
    }

    print("=== 紫微命盤推論測試 ===")
    results = reasoner.analyze_ziwei_chart(mock_chart)
    for res in results:
        print(json.dumps(res, ensure_ascii=False, indent=2))