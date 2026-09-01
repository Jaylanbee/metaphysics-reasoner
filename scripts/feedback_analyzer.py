import json
import os
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def analyze_feedback(feedback_path: str = "data/user_feedback.json"):
    if not os.path.exists(feedback_path):
        logger.warning("No feedback data found.")
        return

    with open(feedback_path, "r", encoding="utf-8") as f:
        feedbacks = json.load(f)

    total_rating = 0
    pattern_hits = defaultdict(int)

    for fb in feedbacks:
        total_rating += fb.get("user_rating", 3)
        res = fb.get("reasoning_result", {})
        if isinstance(res, list):
            for p in res:
                if "patternName" in p:
                    pattern_hits[p["patternName"]] += 1

    avg_rating = total_rating / len(feedbacks) if feedbacks else 0

    logger.info(f"Analyzed {len(feedbacks)} feedback records.")
    logger.info(f"Average System Rating: {avg_rating:.2f}/5.0")
    logger.info("Top Suggested Rule Optimizations based on low hits:")
    # Mocking suggestion logic
    logger.info("- Review threshold for `紫府同宮`")

if __name__ == "__main__":
    analyze_feedback()
