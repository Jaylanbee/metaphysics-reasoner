# 🔮 Metaphysics-Reasoner (東方命理認知與天時推理引擎)

> **版本**：v2.0.0  
> **架構**：獨立解耦微服務倉庫 (Decoupled Micro-Repository)  
> **定位**：去迷信化的東方高維度心智特徵、時間能量向量與命理決策推論引擎。

---

## 🏛️ 系統核心特性

1. **雙軌自動排盤**：支援西曆/農曆生日輸入，自動排定紫微斗數十二宮（十四主星、六吉、六煞、四化）與八字四柱十神；
2. **中州學派格局智慧識別**：包含 11 組經典中州格局（紫府同宮、月朗天門、巨日同宮、羊陀夾忌等）及三方四正煞曜破格演算法；
3. **紫微 ✕ 八字交叉合參仲裁**：結合星象空間格局與十神能量向量，發布高風險防禦警告或平穩長線契機；
4. **八大古籍 RAG 自動印證**：整合《滴天髓》《子平真詮》《三命通會》《淵海子平》《窮通寶鑑》《骨髓賦》《全集》《全書》等 2,200+ 段經典文獻；
5. **典藏級 Apple 風格視覺排盤**：全響應式 HTML/SVG 命盤渲染器；
6. **標準 Antigravity Agent Skill 接口**：可作為獨立 AI Agent 技能隨選調用。

---

## 🚀 快速開始 (Quickstart)

```bash
# 安裝 Python 依賴
pip install -r requirements.txt

# 一鍵執行排盤、合參推理與生成 HTML 報告
python scripts/cli.py --year 1985 --month 2 --day 28 --time 卯 --gender M --html my_chart.html
```

---

## 📂 目錄結構

```plaintext
Metaphysics-Reasoner/
├── data/
│   ├── bazi_foundations.json          # 八字天干五行十神定義庫
│   ├── zhongzhou_patterns_v2.json     # 中州學派格局規則庫
│   ├── ziwei_stars_definition.json    # 紫微 14 主星心智定義庫
│   └── classics/                      # 8 本古籍清洗 JSON
├── engine/                            # 核心計算與天文引擎
│   ├── astronomy_core.py
│   └── destiny_reasoner.py
├── renderers/                         # 視覺與報表渲染器
│   └── visual_chart_renderer.py
├── scripts/                           # 工具腳本與 CLI
│   ├── cli.py
│   ├── chart_parser.py
│   ├── agent_tool_wrapper.py
│   └── run_test_cases.py
└── tests/
```
### Phase 1: SQLite Data Ingestion

The repository now contains `scripts/ingest_to_sqlite.py`, which is capable of parsing and batch ingesting `.jsonl` or `.jsonl.gz` dataset files containing Zi Wei chart data.

**Example Usage**:
```bash
python scripts/ingest_to_sqlite.py \
    --folder ./data/ziwei_samples_v3/ \
    --db-path ./data/ziwei_universe_518k.db \
    --batch-size 1000
```
Run `python scripts/ingest_to_sqlite.py --help` for full usage documentation.
