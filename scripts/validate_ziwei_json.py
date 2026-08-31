import json
import os

def validate_ziwei_json(filepath):
    """
    驗證紫微斗數 14 主星定義 JSON 格式是否正確
    """
    if not os.path.exists(filepath):
        print(f"檔案不存在: {filepath}")
        return False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("錯誤：JSON 根元素必須是 list 包含 14 顆星")
            return False

        if len(data) != 14:
            print(f"錯誤：資料筆數不正確，預期 14 顆，實際 {len(data)} 顆")
            return False

        required_keys = ["starName", "category", "coreMeaning", "palaceEffects", "modernInterpretation", "source", "version"]
        palaces = ["命宮", "兄弟宮", "夫妻宮", "子女宮", "財帛宮", "疾厄宮",
                   "遷移宮", "交友宮", "官祿宮", "田宅宮", "福德宮", "父母宮"]

        for star_data in data:
            star_name = star_data.get("starName", "Unknown")
            # 檢查頂層 key
            for key in required_keys:
                if key not in star_data:
                    print(f"錯誤 ({star_name})：缺少必要的欄位 '{key}'")
                    return False

            # 檢查 palaceEffects 是否包含 12 宮
            for palace in palaces:
                if palace not in star_data["palaceEffects"]:
                    print(f"錯誤 ({star_name})：palaceEffects 缺少 '{palace}'")
                    return False

        print("✅ JSON 格式驗證通過！(包含完整的 14 顆主星與 12 宮位結構)")
        return True

    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失敗: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 發生未預期的錯誤: {str(e)}")
        return False

if __name__ == "__main__":
    target_file = os.path.join(os.path.dirname(__file__), "..", "data", "ziwei_stars_definition.json")
    validate_ziwei_json(target_file)