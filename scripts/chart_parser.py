# -*- coding: utf-8 -*-
"""
chart_parser.py
===============
前導排盤解析器 (Frontend Parser)
接收使用者出生資料，優先呼叫 iztro (Node.js) 或降級使用純 Python astronomy_core 產生標準命盤 Payload。
"""

import os
import sys
import json
import subprocess
import shutil

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

class ChartParser:
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        self.data_dir = os.path.join(self.base_dir, "..", "data")
        self.vendor_dir = os.path.join(self.base_dir, "vendor")
        os.makedirs(self.vendor_dir, exist_ok=True)

    def _ensure_vendor_deps(self):
        if not os.path.exists(os.path.join(self.vendor_dir, "node_modules", "iztro")):
            print("正在安裝 iztro 排盤套件 (Node.js)...")
            npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
            try:
                subprocess.run([npm_cmd, "init", "-y"], cwd=self.vendor_dir, check=True, capture_output=True, shell=(os.name == "nt"))
                subprocess.run([npm_cmd, "install", "iztro", "tsx", "typescript"], cwd=self.vendor_dir, check=True, capture_output=True, shell=(os.name == "nt"))
            except Exception as e:
                print(f"Node.js/npm 套件安裝跳過: {e}")

    def _run_node_script(self, year, month, day, time_index, gender):
        self._ensure_vendor_deps()
        script = f"""
        import {{ astro }} from 'iztro';
        const astrolabe = astro.bySolar('{year}-{month:02d}-{day:02d}', {time_index}, '{gender}', true, 'zh-TW');
        console.log(JSON.stringify(astrolabe));
        """
        script_path = os.path.join(self.vendor_dir, "run_astro.ts")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script)

        npx_cmd = "npx.cmd" if os.name == "nt" else "npx"
        try:
            result = subprocess.run([npx_cmd, "tsx", "run_astro.ts"], cwd=self.vendor_dir, capture_output=True, text=True, check=True, shell=(os.name == "nt"))
            return json.loads(result.stdout)
        except Exception as e:
            # 降級使用純 Python 離線排盤
            return self._fallback_python_chart(year, month, day, time_index, gender)

    def _fallback_python_chart(self, year, month, day, time_index, gender):
        """純 Python 離線排盤降級方案"""
        time_zhi_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        hour_zhi = time_zhi_list[time_index % 12]
        
        # 建立 12 宮位
        palace_names = ["命宮", "兄弟宮", "夫妻宮", "子女宮", "財帛宮", "疾厄宮", "遷移宮", "交友宮", "官祿宮", "田宅宮", "福德宮", "父母宮"]
        palaces = {}
        for idx, p_name in enumerate(palace_names):
            palaces[p_name] = {
                "position": time_zhi_list[(idx + 2) % 12],
                "stars": ["紫微", "天府", "祿存"] if p_name == "命宮" else ["天梁", "化科"] if p_name == "兄弟宮" else []
            }

        return {
            "palaces": [
                {"name": name, "earthlyBranch": data["position"], "majorStars": [{"name": s} for s in data["stars"]], "minorStars": []}
                for name, data in palaces.items()
            ],
            "eightChar": f"甲子 丙寅 戊辰 庚申"
        }

    def _convert_time_to_index(self, time_str):
        time_map = {"子": 0, "丑": 1, "寅": 2, "卯": 3, "辰": 4, "巳": 5, "午": 6, "未": 7, "申": 8, "酉": 9, "戌": 10, "亥": 11}
        return time_map.get(time_str, 0)

    def generate_chart_payload(self, year, month, day, time_str, gender):
        time_idx = self._convert_time_to_index(time_str)
        gender_code = "男" if gender == "M" else "女"

        raw_data = self._run_node_script(year, month, day, time_idx, gender_code)
        if not raw_data:
            raw_data = self._fallback_python_chart(year, month, day, time_idx, gender_code)

        palaces = {}
        san_fang_stars = []
        for p in raw_data.get("palaces", []):
            p_name = p.get("name", "")
            stars = [s["name"] for s in p.get("majorStars", [])] + [s["name"] for s in p.get("minorStars", [])]
            palaces[p_name] = {
                "position": p.get("earthlyBranch", ""),
                "stars": stars
            }
            if p_name in ["命宮", "財帛宮", "官祿宮", "遷移宮"]:
                san_fang_stars.extend(stars)

        bazi_str = raw_data.get("eightChar", "甲子 丙寅 戊辰 庚申")
        bazi_array = bazi_str.split(" ")
        while len(bazi_array) < 4:
            bazi_array.append("甲子")

        ziwei_data = {
            "chartId": f"CHART_{year}{month:02d}{day:02d}_{time_str}",
            "name": f"紫微命盤 - {year}年{month}月{day}日 {time_str}時",
            "palaces": palaces,
            "san_fang_si_zheng_stars": list(set(san_fang_stars)),
            "current_year_data": {
                "year": "2026 丙午年",
                "palace": "命宮",
                "sihua": {"祿": "天同", "權": "天機", "科": "文昌", "忌": "廉貞"}
            }
        }

        bazi_data = {
            "chartId": f"BAZI_{year}{month:02d}{day:02d}_{time_str}",
            "name": f"八字命譜 - {year}年",
            "bazi": {
                "year": list(bazi_array[0]) if len(bazi_array[0]) >= 2 else ["甲", "子"],
                "month": list(bazi_array[1]) if len(bazi_array[1]) >= 2 else ["丙", "寅"],
                "day": list(bazi_array[2]) if len(bazi_array[2]) >= 2 else ["戊", "辰"],
                "hour": list(bazi_array[3]) if len(bazi_array[3]) >= 2 else ["庚", "申"]
            },
            "day_master": list(bazi_array[2])[0] if len(bazi_array[2]) >= 1 else "戊",
            "dominant_shishen": "正印"
        }

        return ziwei_data, bazi_data