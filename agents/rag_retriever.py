from typing import List, Dict

class ClassicsRAGRetriever:
    def retrieve_classics(self, query: str, limit: int = 3) -> List[Dict[str, str]]:
        return [{"source": "《骨髓賦》", "chapter": "星曜篇", "quote": "紫微辰戌遇破軍，富而不貴有虛名。"}]
