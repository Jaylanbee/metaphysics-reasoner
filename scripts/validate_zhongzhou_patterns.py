import json
import os

def validate_zhongzhou_patterns(filepath):
    """
    驗證中州學派格局規則 JSON 格式是否正確
    """
    if not os.path.exists(filepath):
        print(f"檔案不存在: {filepath}")
        return False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("錯誤：JSON 根元素必須是 list")
            return False

        required_keys = ["patternId", "patternName", "category", "condition", "interpretation", "source", "version"]

        for idx, pattern in enumerate(data):
            for key in required_keys:
                if key not in pattern:
                    print(f"錯誤 (index {idx})：缺少必要的欄位 '{key}'")
                    return False

            condition = pattern.get("condition", {})
            if "description" not in condition or "rules" not in condition:
                 print(f"錯誤 ({pattern.get('patternName')})：condition 結構不正確")
                 return False

            interpretation = pattern.get("interpretation", {})
            if "classic" not in interpretation or "modern" not in interpretation or "exception" not in interpretation:
                 print(f"錯誤 ({pattern.get('patternName')})：interpretation 結構不正確，需包含 classic, modern, exception")
                 return False

        print(f"✅ 中州學派格局規則驗證通過！(共 {len(data)} 條格局)")
        return True

    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失敗: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 發生未預期的錯誤: {str(e)}")
        return False

if __name__ == "__main__":
    target_file = os.path.join(os.path.dirname(__file__), "..", "data", "zhongzhou_patterns_v2.json")
    validate_zhongzhou_patterns(target_file)