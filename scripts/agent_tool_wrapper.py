import json
import os
from chart_parser import ChartParser
from destiny_reasoner import DestinyReasoner

class MetaphysicsAgentWrapper:
    """
    這是一個封裝層，將後端的解析邏輯包裝為可以給 LLM 直接 Tool Call 的規格。
    """
    def __init__(self):
        self.parser = ChartParser()
        self.reasoner = DestinyReasoner()

    @staticmethod
    def get_tool_schema():
        """返回符合 OpenAI/Claude JSON-Schema 的 Tool 宣告"""
        return {
            "type": "function",
            "function": {
                "name": "analyze_metaphysics_chart",
                "description": "根據給定的出生年月日時，進行紫微斗數與八字的雙軌排盤，並執行玄學天時與氣運合參分析，產出命理決策報告。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "year": {
                            "type": "integer",
                            "description": "西元出生年份，例如 1985"
                        },
                        "month": {
                            "type": "integer",
                            "description": "出生月份 (1-12)"
                        },
                        "day": {
                            "type": "integer",
                            "description": "出生日期 (1-31)"
                        },
                        "time_str": {
                            "type": "string",
                            "description": "出生時辰，輸入單一中文字，如 '子', '丑', '寅', '卯'"
                        },
                        "gender": {
                            "type": "string",
                            "enum": ["M", "F"],
                            "description": "性別，'M' 代表男，'F' 代表女"
                        }
                    },
                    "required": ["year", "month", "day", "time_str", "gender"]
                }
            }
        }

    def execute_tool(self, kwargs_json_str):
        """
        接收 LLM 傳入的 JSON 字串參數，執行完整 workflow，回傳最終 JSON 字串結果
        """
        try:
            params = json.loads(kwargs_json_str)
            year = params["year"]
            month = params["month"]
            day = params["day"]
            time_str = params["time_str"]
            gender = params["gender"]

            # Step 1: 呼叫外部前導程式排盤
            ziwei_data, bazi_data = self.parser.generate_chart_payload(year, month, day, time_str, gender)
            if not ziwei_data or not bazi_data:
                return json.dumps({"error": "排盤失敗，請檢查輸入參數或排盤引擎狀態。"}, ensure_ascii=False)

            # Step 2: 呼叫推理大腦進行合參
            combined_report = self.reasoner.analyze_combined_chart(ziwei_data, bazi_data)

            return json.dumps(combined_report, ensure_ascii=False, indent=2)

        except json.JSONDecodeError:
            return json.dumps({"error": "參數非有效的 JSON 格式。"}, ensure_ascii=False)
        except KeyError as e:
            return json.dumps({"error": f"缺少必要參數: {str(e)}"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": f"執行過程發生未預期錯誤: {str(e)}"}, ensure_ascii=False)

if __name__ == "__main__":
    # 測試 Wrapper Schema
    print("=== Agent Tool Schema ===")
    print(json.dumps(MetaphysicsAgentWrapper.get_tool_schema(), ensure_ascii=False, indent=2))
