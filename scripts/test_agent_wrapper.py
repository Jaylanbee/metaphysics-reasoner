# -*- coding: utf-8 -*-
import json
import sys
import os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.agent_tool_wrapper import MetaphysicsAgentWrapper

def run_integration_test():
    print("=== 啟動 Agent UI Wrapper 整合測試 ===")
    wrapper = MetaphysicsAgentWrapper()
    mock_llm_args = json.dumps({
        "year": 1990,
        "month": 5,
        "day": 5,
        "time_str": "辰",
        "gender": "M"
    })
    
    print(f"模擬 LLM 呼叫 Tool 傳入參數: {mock_llm_args}")
    response_str = wrapper.execute_tool(mock_llm_args)
    print("\n=== Agent Tool 回傳結果 ===")
    print(response_str)
    
    try:
        data = json.loads(response_str)
        if "ziwei_summary" in data and "bazi_summary" in data and "cross_reasoning_synthesis" in data:
            print("\n[PASS] 整合測試成功！回傳符合預期架構。")
        else:
            print("\n[FAIL] 回傳格式缺少必要區塊。")
    except Exception as e:
        print(f"[FAIL] 回傳非預期 JSON: {e}")

if __name__ == "__main__":
    run_integration_test()