import json
import os

def validate_bazi_foundations(filepath):
    """
    驗證八字基礎 JSON 格式是否正確
    """
    if not os.path.exists(filepath):
        print(f"檔案不存在: {filepath}")
        return False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        required_sections = ["version", "source", "wuxing", "tiangan", "shishen"]

        for section in required_sections:
            if section not in data:
                print(f"錯誤：缺少主要的 section '{section}'")
                return False

        # 驗證五行
        wuxing = data.get("wuxing", {})
        if len(wuxing) != 5:
            print(f"錯誤：五行數量應為 5，目前為 {len(wuxing)}")
            return False

        # 驗證十神
        shishen = data.get("shishen", {})
        if len(shishen) != 10:
            print(f"錯誤：十神數量應為 10，目前為 {len(shishen)}")
            return False

        # 驗證天干
        tiangan = data.get("tiangan", {})
        if len(tiangan) != 10:
            print(f"錯誤：天干數量應為 10，目前為 {len(tiangan)}")
            return False

        print("✅ 八字基礎知識 JSON 驗證通過！(包含五行、天干、十神結構)")
        return True

    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失敗: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 發生未預期的錯誤: {str(e)}")
        return False

if __name__ == "__main__":
    target_file = os.path.join(os.path.dirname(__file__), "..", "data", "bazi_foundations.json")
    validate_bazi_foundations(target_file)