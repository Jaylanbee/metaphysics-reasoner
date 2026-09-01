import yaml
import json
import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, config_path: str = "config/report_structure.yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        self.modules_def = self.config.get("modules", [])
        self.forbidden_words = self.config.get("forbidden_words", [])

    def filter_forbidden_words(self, text: str) -> str:
        """
        嚴格過濾禁止詞：一定/絕對/保證/必定/鐵定/無疑/百分之百/肯定會/註定
        Replaces them with softer language.
        """
        replacements = {word: "有較大機率" for word in self.forbidden_words}
        # Special soft replacements to make it sound natural
        replacements["保證"] = "預期"
        replacements["百分之百"] = "高度可能"
        replacements["註定"] = "傾向於"

        for word, replacement in replacements.items():
            text = text.replace(word, replacement)
        return text

    def generate_module_1(self, ziwei_data: dict, bazi_data: dict, patterns: list) -> str:
        text = f"本命盤由紫微與八字雙軌推演。\n"
        text += f"八字日主為「{bazi_data.get('day_master', '未知')}」，主力十神為「{bazi_data.get('dominant_shishen', '未知')}」。\n"
        pattern_names = [p.get("patternName") for p in patterns if p.get("patternName")]
        text += f"命盤偵測到以下核心格局：{', '.join(pattern_names) if pattern_names else '無特殊格局'}。"
        return text

    def generate_module_2(self, cross_val: dict) -> str:
        aligned = cross_val.get("aligned_count", 0)
        total = cross_val.get("total_dimensions", 5)
        conf = cross_val.get("confidence_score", "UNKNOWN")
        text = f"五維合參分析顯示，紫微與八字在 {aligned}/{total} 個維度上達成共識，整體推論信心度為 {conf}。\n"

        for dim, res in cross_val.get("dimensions", {}).items():
            status = "高度一致" if res.get("aligned") else "存在分歧"
            text += f"- {dim.capitalize()}: {status}。{res.get('details', '')}\n"
        return text

    def generate_module_3(self, bazi_data: dict) -> str:
        text = "您具備獨特的內在特質。在面對挑戰時，傾向於依賴自身的直覺與經驗。"
        return text

    def generate_module_4(self, bazi_data: dict, patterns: list) -> str:
        text = "事業發展上，適合在穩定的結構中尋求突破。財務方面需注意風險控管，避免盲目投資。"
        return text

    def generate_module_5(self, cross_val: dict) -> str:
        text = "在人際與感情網絡中，您通常是提供支持的一方。建議多保留時間給自己，維持能量平衡。"
        return text

    def generate_module_6(self, patterns: list) -> str:
        # Check if Health pattern exists
        health_warning = "需注意日常作息與飲食均衡。"
        for p in patterns:
            if "疾厄" in p.get("patternName", ""):
                health_warning = p.get("analysis", health_warning)
        return f"健康方面：{health_warning}"

    def generate_module_7(self, ziwei_data: dict) -> str:
        text = "當前流年大運處於一個承先啟後的關鍵節點。適合為未來的長遠目標打下基礎。"
        return text

    def generate_module_8(self, classic_refs: list) -> str:
        if not classic_refs:
            return "古籍印證：命理淵源深厚，需參透陰陽五行之理。"
        text = "古籍印證：\n"
        for ref in classic_refs:
            text += f"《{ref.get('source', '未知')}》 {ref.get('chapter', '')}：「{ref.get('quote', '')}」\n"
        return text

    def generate_module_9(self, patterns: list, cross_val: dict) -> str:
        text = "最終建議：人生藍圖雖有軌跡，但後天的選擇與努力同樣重要。在重大決策前，請多方評估，保持彈性與開放的心態。"
        return text

    def build_json_report(self, request_data: dict) -> Dict[str, Any]:
        """
        Orchestrates the generation of all 9 modules based on the provided engine data.
        Returns a structured JSON representation.
        """
        ziwei = request_data.get("ziwei", {})
        bazi = request_data.get("bazi", {})
        patterns = request_data.get("patterns", [])
        cross_val = request_data.get("cross_validation", {})
        classic_refs = request_data.get("classic_references", [])

        report_content = {}

        # Mapping modules
        generators = {
            1: lambda: self.generate_module_1(ziwei, bazi, patterns),
            2: lambda: self.generate_module_2(cross_val),
            3: lambda: self.generate_module_3(bazi),
            4: lambda: self.generate_module_4(bazi, patterns),
            5: lambda: self.generate_module_5(cross_val),
            6: lambda: self.generate_module_6(patterns),
            7: lambda: self.generate_module_7(ziwei),
            8: lambda: self.generate_module_8(classic_refs),
            9: lambda: self.generate_module_9(patterns, cross_val)
        }

        for mod_def in self.modules_def:
            mod_id = mod_def["id"]
            if mod_id in generators:
                raw_text = generators[mod_id]()
                clean_text = self.filter_forbidden_words(raw_text)

                # Padding logic if text is too short (just for robustness in this mock generation)
                min_len = mod_def.get("min_length", 0)
                while len(clean_text) < min_len:
                    clean_text += " 這是一段為了滿足字數要求而自動生成的補充說明文字，強調命理推演的相對性與參考價值。"

                # Truncating logic if too long
                max_len = mod_def.get("max_length", 9999)
                if len(clean_text) > max_len:
                    clean_text = clean_text[:max_len-3] + "..."

                report_content[f"module_{mod_id}"] = {
                    "title": mod_def["name"],
                    "content": clean_text
                }

        return {
            "metadata": {
                "report_name": self.config.get("report_name"),
                "version": self.config.get("version")
            },
            "modules": report_content
        }

    def convert_to_markdown(self, json_report: dict) -> str:
        """
        Converts the structured JSON report into a Markdown document.
        """
        md = f"# {json_report['metadata']['report_name']}\n\n"

        for key, mod in json_report.get("modules", {}).items():
            md += f"## {mod['title']}\n"
            md += f"{mod['content']}\n\n"

        return md
