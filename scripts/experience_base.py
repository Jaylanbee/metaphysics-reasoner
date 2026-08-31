# -*- coding: utf-8 -*-
"""
experience_base.py
==================
東方命理認知系統 ‧ 經驗庫模組 (Experience Base)

此模組作為系統從「優秀引擎」邁向「可進化平台」的關鍵組件。
負責整合 51.8 萬筆命盤樣本數據集，提供 A/B 基線對比功能，
並包含用戶反饋閉環機制，以持續驗證並優化排盤引擎與合參推理的準確度。
"""

import os
import json
import time
import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExperienceBase:
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            self.base_dir = os.path.dirname(__file__)
            self.data_dir = os.path.join(self.base_dir, "..", "data")
        else:
            self.data_dir = data_dir

        self.dataset_path = os.path.join(self.data_dir, "dataset_518k.json")
        self.feedback_path = os.path.join(self.data_dir, "user_feedback.json")
        self.dataset: List[Dict[str, Any]] = []

    def load_dataset(self) -> int:
        """
        整合 51.8 萬筆命盤樣本數據集

        Returns:
            載入的樣本數量
        """
        if not os.path.exists(self.dataset_path):
            logger.warning(f"數據集檔案不存在: {self.dataset_path}。將建立空列表以供未來整合。")
            self.dataset = []
            return 0

        try:
            with open(self.dataset_path, "r", encoding="utf-8") as f:
                self.dataset = json.load(f)
                logger.info(f"成功載入數據集，共 {len(self.dataset)} 筆樣本。")
                return len(self.dataset)
        except Exception as e:
            logger.error(f"載入數據集失敗: {e}")
            self.dataset = []
            return 0

    def ab_baseline_compare(self, model_a_results: List[Dict[str, Any]], model_b_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        A/B 基線對比
        對比兩個模型或兩個版本的推理結果，評估準確率或特定指標的差異。

        Args:
            model_a_results: 模型 A 的推理結果
            model_b_results: 模型 B 的推理結果

        Returns:
            對比分析報告
        """
        logger.info("執行 A/B 基線對比...")

        # 簡單的對比邏輯示範 (未來可擴展為更複雜的統計分析)
        total_samples = max(len(model_a_results), len(model_b_results))
        match_count = 0

        for a, b in zip(model_a_results, model_b_results):
            # 這裡的對比條件應依據實際資料結構調整
            if a.get("risk_level") == b.get("risk_level"):
                match_count += 1

        match_rate = (match_count / total_samples) if total_samples > 0 else 0

        report = {
            "total_samples_compared": total_samples,
            "match_count": match_count,
            "match_rate": match_rate,
            "conclusion": "一致性高" if match_rate > 0.8 else "存在顯著差異，需進一步分析"
        }
        return report

    def record_user_feedback(self, chart_id: str, reasoning_result: Dict[str, Any], user_rating: int, comments: str) -> bool:
        """
        用戶反饋閉環機制
        記錄用戶對推理結果的評價與反饋，用於未來模型的微調與優化。

        Args:
            chart_id: 命盤 ID
            reasoning_result: 系統給出的推理結果
            user_rating: 用戶評分 (1-5)
            comments: 用戶具體反饋意見

        Returns:
            是否成功記錄
        """
        feedback_entry = {
            "chart_id": chart_id,
            "reasoning_result": reasoning_result,
            "user_rating": user_rating,
            "comments": comments,
            "timestamp": time.time()
        }

        feedbacks = []
        if os.path.exists(self.feedback_path):
            try:
                with open(self.feedback_path, "r", encoding="utf-8") as f:
                    feedbacks = json.load(f)
            except Exception as e:
                logger.error(f"讀取既有反饋失敗: {e}")
                return False

        feedbacks.append(feedback_entry)

        try:
            with open(self.feedback_path, "w", encoding="utf-8") as f:
                json.dump(feedbacks, f, ensure_ascii=False, indent=2)
            logger.info(f"成功記錄用戶反饋，Chart ID: {chart_id}")
            return True
        except Exception as e:
            logger.error(f"寫入反饋失敗: {e}")
            return False


    def integrate_feedback_to_baseline(self, baseline_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        結合用戶反饋調整基線對比結果
        """
        feedbacks = []
        if os.path.exists(self.feedback_path):
            try:
                with open(self.feedback_path, "r", encoding="utf-8") as f:
                    feedbacks = json.load(f)
            except Exception as e:
                logger.error(f"讀取反饋失敗: {e}")

        if not feedbacks:
            baseline_report["adjusted_match_rate"] = baseline_report.get("match_rate", 0)
            baseline_report["feedback_impact"] = "No feedback data available."
            return baseline_report

        total_rating = sum(f.get("user_rating", 3) for f in feedbacks)
        avg_rating = total_rating / len(feedbacks)

        # Adjust match rate based on average user rating (assuming 3 is neutral, 5 is perfect)
        # We define an adjustment factor, e.g. rating 5 increases match rate, rating 1 decreases it.
        rating_factor = (avg_rating - 3) * 0.05

        original_match_rate = baseline_report.get("match_rate", 0)
        adjusted_match_rate = min(1.0, max(0.0, original_match_rate + rating_factor))

        baseline_report["adjusted_match_rate"] = adjusted_match_rate
        baseline_report["average_user_rating"] = avg_rating
        baseline_report["feedback_impact"] = f"Adjusted match rate by {rating_factor:+.2f} based on {len(feedbacks)} feedbacks."

        return baseline_report
