# -*- coding: utf-8 -*-
"""
cli.py
======
Metaphysics Reasoner 命令列與一鍵執行入口 (CLI Interface)
支援輸入西曆出生年月日、時辰、性別，一鍵完成自動排盤、合參推理與生成 HTML 報告。
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.chart_parser import ChartParser
from scripts.destiny_reasoner import DestinyReasoner
from renderers.visual_chart_renderer import VisualChartRenderer

def main():
    parser = argparse.ArgumentParser(description="東方命理認知系統 (Metaphysics Reasoner CLI)")
    parser.add_argument("--year", type=int, default=1985, help="西元出生年份，如 1985")
    parser.add_argument("--month", type=int, default=2, help="出生月份 (1-12)")
    parser.add_argument("--day", type=int, default=28, help="出生日期 (1-31)")
    parser.add_argument("--time", type=str, default="卯", help="出生時辰 (子丑寅卯辰巳午未申酉戌亥)")
    parser.add_argument("--gender", type=str, default="M", choices=["M", "F"], help="性別 (M=男, F=女)")
    parser.add_argument("--html", type=str, default="metaphysics_report.html", help="輸出 HTML 報告路徑")

    args = parser.parse_args()

    print("================================================================================")
    print("🔮 東方命理認知系統 (Metaphysics Reasoner Engine)")
    print(f"👉 正在為出生資料 [{args.year}年{args.month}月{args.day}日 {args.time}時 (性別: {args.gender})] 執行自動排盤與合參推論...")
    print("================================================================================")

    # 1. 自動排盤
    chart_parser = ChartParser()
    z_data, b_data = chart_parser.generate_chart_payload(args.year, args.month, args.day, args.time, args.gender)

    if not z_data:
        print("❌ 排盤失敗，請檢查 Node.js 與 iztro 套件依賴。")
        sys.exit(1)

    chart_payload = {
        "ziwei_data": z_data,
        "bazi_data": b_data
    }

    # 2. 執行合參推理
    reasoner = DestinyReasoner()
    report = reasoner.analyze_combined_chart(z_data, b_data)

    print("\n✅ 推理完成！合參結論概要：")
    print(report.get("cross_reasoning_synthesis", ""))

    # 3. 渲染 HTML 報告
    renderer = VisualChartRenderer()
    out_path = Path(args.html)
    renderer.render_html_report(chart_payload, report, str(out_path))
    print(f"📄 典藏級視覺報告已生成至: {out_path.resolve()}")
    print("================================================================================")

if __name__ == "__main__":
    main()