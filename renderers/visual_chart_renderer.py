# -*- coding: utf-8 -*-
"""
visual_chart_renderer.py
========================
東方命理認知系統 ‧ 典藏級視覺排盤渲染器 (Apple-Grade HTML/SVG Renderer)
生成高雅、極簡、全響應式的紫微斗數十二宮命盤與八字能量分析報表。
"""

import json
import html

class VisualChartRenderer:
    """Apple 風格極簡命盤與診斷報告 HTML 渲染器"""

    def __init__(self):
        pass

    def render_html_report(self, chart_payload: dict, reasoning_report: dict, output_path: str = None) -> str:
        """渲染高解析度典藏級 HTML 診斷報告"""
        ziwei_data = chart_payload.get("ziwei_data", {})
        bazi_data = chart_payload.get("bazi_data", {})
        palaces = ziwei_data.get("palaces", {})
        
        # 12宮位標準位置矩陣 (4x4 迴環網格：頂部巳午未申，右側酉戌，底部亥子丑寅，左側卯辰)
        grid_order = [
            ["巳", "午", "未", "申"],
            ["辰", "CENTER", "CENTER", "酉"],
            ["卯", "CENTER", "CENTER", "戌"],
            ["寅", "丑", "子", "亥"]
        ]
        
        # 建立地支對應宮位數據
        pos_to_palace = {}
        for p_name, p_val in palaces.items():
            pos = p_val.get("position", "")
            pos_to_palace[pos] = {
                "name": p_name,
                "stars": p_val.get("stars", [])
            }

        # 組合 HTML
        cards_html = ""
        for row in grid_order:
            for cell in row:
                if cell == "CENTER":
                    continue
                p_info = pos_to_palace.get(cell, {"name": "未知宮", "stars": []})
                stars_span = "".join([f"<span class='star-badge {'major' if s in ['紫微','天府','太陽','太陰','武曲','天同','廉貞','貪狼','巨門','天相','天梁','七殺','破軍','天機'] else 'minor'}'>{s}</span>" for s in p_info["stars"]])
                cards_html += f"""
                <div class="palace-card pos-{cell}">
                    <div class="palace-header">
                        <span class="palace-name">{p_info['name']}</span>
                        <span class="palace-pos">{cell}</span>
                    </div>
                    <div class="stars-container">{stars_span or '<span class="empty-star">無主星</span>'}</div>
                </div>
                """

        patterns_html = ""
        for p in reasoning_report.get("ziwei_summary", []):
            patterns_html += f"""
            <div class="pattern-box">
                <div class="pattern-title">✨ {p.get('patternName', '')} <span class="pattern-tag">{p.get('category', '')}</span></div>
                <div class="pattern-desc">{p.get('analysis', '')}</div>
                <div class="pattern-quote">{p.get('classic_quote', '')}</div>
                {f"<div class='pattern-warn'>⚠️ {p.get('warning')}</div>" if 'warning' in p else ""}
            </div>
            """

        bazi_res = reasoning_report.get("bazi_summary", {})
        dm = bazi_res.get("day_master_analysis", {})
        career = bazi_res.get("career_analysis", {})
        cross_synthesis = reasoning_report.get("cross_reasoning_synthesis", "")

        html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>東方命理認知診斷報告 ‧ {ziwei_data.get('name', '紫微八字合參')}</title>
    <style>
        :root {{
            --bg-primary: #0a0e17;
            --bg-card: rgba(26, 34, 52, 0.75);
            --border-color: rgba(255, 255, 255, 0.12);
            --accent-cyan: #38bdf8;
            --accent-purple: #c084fc;
            --accent-amber: #fbbf24;
            --text-main: #f1f5f9;
            --text-sub: #94a3b8;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", sans-serif; }}
        body {{ background: var(--bg-primary); color: var(--text-main); padding: 40px 20px; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 28px; font-weight: 700; background: linear-gradient(135deg, #38bdf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; }}
        .header p {{ color: var(--text-sub); font-size: 14px; }}
        
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-template-rows: repeat(4, 140px);
            gap: 12px;
            margin-bottom: 30px;
        }}
        .palace-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            backdrop-filter: blur(8px);
        }}
        .palace-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 4px; }}
        .palace-name {{ font-weight: 700; font-size: 15px; color: var(--accent-cyan); }}
        .palace-pos {{ font-size: 12px; color: var(--text-sub); }}
        .stars-container {{ display: flex; flex-wrap: wrap; gap: 4px; margin-top: 6px; }}
        .star-badge {{ font-size: 11px; padding: 2px 6px; border-radius: 4px; }}
        .star-badge.major {{ background: rgba(192, 132, 252, 0.2); color: #e9d5ff; border: 1px solid rgba(192, 132, 252, 0.4); font-weight: 600; }}
        .star-badge.minor {{ background: rgba(56, 189, 248, 0.15); color: #bae6fd; }}
        .empty-star {{ font-size: 11px; color: #64748b; }}

        .center-dashboard {{
            grid-column: 2 / 4;
            grid-row: 2 / 4;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 12px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }}
        .center-dashboard h2 {{ font-size: 20px; color: var(--accent-amber); margin-bottom: 10px; }}
        .center-dashboard .bazi-summary {{ font-size: 14px; color: var(--text-sub); }}
        
        .section-title {{ font-size: 20px; font-weight: 700; margin: 30px 0 15px 0; color: var(--accent-cyan); border-left: 4px solid var(--accent-cyan); padding-left: 10px; }}
        .synthesis-card {{ background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px; padding: 20px; margin-bottom: 25px; }}
        .pattern-box {{ background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 15px; margin-bottom: 12px; }}
        .pattern-title {{ font-weight: 700; font-size: 16px; color: var(--accent-amber); margin-bottom: 6px; display: flex; align-items: center; justify-content: space-between; }}
        .pattern-tag {{ font-size: 12px; background: rgba(251, 191, 36, 0.2); color: var(--accent-amber); padding: 2px 8px; border-radius: 12px; }}
        .pattern-desc {{ font-size: 14px; margin-bottom: 6px; }}
        .pattern-quote {{ font-size: 13px; color: #a78bfa; font-style: italic; background: rgba(167, 139, 250, 0.1); padding: 6px 10px; border-radius: 6px; }}
        .pattern-warn {{ font-size: 13px; color: #f87171; margin-top: 6px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔮 東方命理認知診斷與決策報告</h1>
            <p>命盤標識：{ziwei_data.get('chartId', '')} | 產生時間：2026-08-31</p>
        </div>

        <div class="section-title">🏛️ 紫微斗數十二宮命盤佈局</div>
        <div class="chart-grid">
            {cards_html}
            <div class="center-dashboard">
                <h2>☯️ 八字 ✕ 紫微中樞</h2>
                <div class="bazi-summary">
                    <p><strong>日主天干</strong>：{dm.get('day_master', '未知')} ({dm.get('element', '')} / {dm.get('image', '')})</p>
                    <p><strong>主導十神</strong>：{career.get('dominant_shishen', '未知')} ({career.get('core_meaning', '')})</p>
                    <p><strong>適配領域</strong>：{career.get('career_suggestion', '')}</p>
                </div>
            </div>
        </div>

        <div class="section-title">⚡ 紫微八字合參決策總論 (Cross-Reasoning Synthesis)</div>
        <div class="synthesis-card">
            <p style="font-size: 15px; line-height: 1.8;">{cross_synthesis}</p>
        </div>

        <div class="section-title">📜 中州學派格局深度解析與古籍印證</div>
        {patterns_html}
    </div>
</body>
</html>"""
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"HTML 診斷報告已生成：{output_path}")

        return html_content