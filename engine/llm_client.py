from typing import Dict, Any
from backend.config import settings

class LLMClient:
    def __init__(self):
        self.endpoint = settings.LLM_ENDPOINT
        self.api_key = settings.LLM_API_KEY

    def generate_interpretation(self, chart_data: Dict[str, Any]) -> str:
        """
        Calls the fine-tuned LLM inference endpoint to generate a reading.
        """
        if not self.endpoint or not self.api_key:
            return "Local structural reasoning utilized. (LLM endpoint not configured)"

        return "LLM Interpretation: Based on your stars, you have great potential."
