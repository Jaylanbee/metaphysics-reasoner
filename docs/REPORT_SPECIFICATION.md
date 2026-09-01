# Professional Report Generator Specification

## Overview
The `ReportGenerator` dynamically compiles comprehensive astrological readings spanning Zi Wei and Bazi 5D validations into structured JSON or Markdown.

## Quality Gates (G1-G10)
Processed through `QualityGates` interceptors:
1. **Module Completion**: Ensures all 9 defined modules exist.
2. **Length Validation**: Checks content sizes against boundaries defined in `config/report_structure.yaml`. Auto-repairs short segments.
3. **Forbidden Word Filtering**: Strips deterministic guarantees replacing them with probabilistically sound phrasing.
  * *Filtered*: "保證", "必定", "百分之百"
  * *Replaced With*: "預期", "有較大機率", "高度可能"

## Modules
1. **基本命盤與格局總覽**: Chart & Patterns Overview
2. **五維合參分析**: 5D Cross-Validation Analysis
3. **核心性格與潛力**: Core Personality
4. **事業與財富發展**: Career & Wealth
5. **感情與人際關係**: Relationships
6. **健康與疾厄風險**: Health Risks
7. **流年大運解析**: Current Decade
8. **古籍印證與引言**: Classic Texts Citations
9. **最終行動建議與避險**: Final Actionable Advice

## Output Formats
Supports both raw structural JSON parsing natively or conversion into pre-formatted Markdown blocks available natively via the `/api/v1/report` endpoint.
