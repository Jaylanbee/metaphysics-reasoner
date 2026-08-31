import json
import os
from destiny_reasoner import DestinyReasoner

def run_tests():
    reasoner = DestinyReasoner()

    # 測試紫微斗數
    ziwei_test_file = os.path.join(os.path.dirname(__file__), "..", "data", "test_cases", "sample_chart_1.json")
    with open(ziwei_test_file, 'r', encoding='utf-8') as f:
        ziwei_data = json.load(f)

    print(f"\n=== 執行紫微命盤測試: {ziwei_data.get('name')} ===")
    ziwei_results = reasoner.analyze_ziwei_chart(ziwei_data)
    for res in ziwei_results:
        print(json.dumps(res, ensure_ascii=False, indent=2))

    # 測試八字
    bazi_test_file = os.path.join(os.path.dirname(__file__), "..", "data", "test_cases", "sample_bazi_1.json")
    with open(bazi_test_file, 'r', encoding='utf-8') as f:
        bazi_data = json.load(f)

    print(f"\n=== 執行八字命盤測試: {bazi_data.get('name')} ===")
    bazi_results = reasoner.analyze_bazi_chart(bazi_data)
    print(json.dumps(bazi_results, ensure_ascii=False, indent=2))

    # 測試紫微八字合參
    print("\n=== 執行紫微八字合參 (Cross-Reasoning) 測試 ===")
    combined_results = reasoner.analyze_combined_chart(ziwei_data, bazi_data)
    print(json.dumps(combined_results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    run_tests()
