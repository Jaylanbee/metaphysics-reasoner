import os
import json
import re

def clean_classics_text():
    """
    從 ziwei-doushu-skill/lib/classics/data 中提取並清洗古籍文本
    """
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "..", "data", "classics")
    source_dir = os.path.join(data_dir, "ziwei-doushu-skill", "lib", "classics", "data")

    if not os.path.exists(source_dir):
        print(f"錯誤：找不到原文目錄 {source_dir}。請確認已 clone 該專案。")
        return False

    books = {
        "gusuifu.ts": {"file": "gusuifu_cleaned.json", "name": "紫微斗數骨髓賦", "chapter": "骨髓賦原文"},
        "quanji.ts": {"file": "quanji_cleaned.json", "name": "紫微斗數全集", "chapter": "全集節錄"},
        "quanshu.ts": {"file": "quanshu_cleaned.json", "name": "紫微斗數全書", "chapter": "全書節錄"}
    }

    for ts_file, info in books.items():
        source_path = os.path.join(source_dir, ts_file)
        if not os.path.exists(source_path):
            print(f"警告：找不到原文檔案 {ts_file}，略過。")
            continue

        print(f"正在處理 {ts_file} ...")

        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取 export const xxx = `...` 中的內容
            matches = re.findall(r'`(.*?)`', content, re.DOTALL)

            cleaned_text = ""
            if matches:
                cleaned_text = "\n".join(matches)
            else:
                # 若無 backticks，就粗略清理 (實務應寫正規 parser)
                cleaned_text = re.sub(r'[a-zA-Z\{\}\(\)\[\]=;:/\'\"]', '', content).strip()

            # 去除多餘空行與空白，保持純文本乾淨
            cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text).strip()

            output_data = {
                "book": info["name"],
                "chapter": info["chapter"],
                "originalText": cleaned_text[:2000] + ("\n\n... (截取前2000字，完整內容請見原始檔案)" if len(cleaned_text) > 2000 else ""),
                "annotations": {},
                "source": f"ziwei-doushu-skill/lib/classics/data/{ts_file}"
            }

            output_path = os.path.join(data_dir, info["file"])
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)

            print(f"已輸出清洗後檔案至：{output_path}")

        except Exception as e:
            print(f"處理 {ts_file} 時發生錯誤: {e}")

    print("古籍清洗作業完成！")
    return True

if __name__ == "__main__":
    clean_classics_text()