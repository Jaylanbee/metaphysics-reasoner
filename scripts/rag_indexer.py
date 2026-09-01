import os
import json
import logging
import chromadb

logger = logging.getLogger(__name__)

class ClassicsIndexer:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection(name="classics_collection")
        self.texts = {
            "滴天髓": "身強印旺，必主文章之貴。財輕劫重，宜求技術之能。...",
            "子平真詮": "八字用神，專求月令。有殺先論殺，無殺方論用。...",
            "三命通會": "夫命之理，幽微奧妙，非通神者不能究其源。...",
            "淵海子平": "年看祖業，月看父母，日看己身及配偶，時看子息。...",
            "窮通寶鑑": "甲木生於寅月，陽氣漸生，木旺火相。...",
            "骨髓賦": "紫微辰戌遇破軍，富而不貴有虛名。...",
            "全集": "天機太陰在寅申，必定因才顯大名。...",
            "全書": "太陽巨門同宮，主為人直爽但多口舌。...",
            "太微賦": "七殺朝斗，爵祿榮昌。...",
            "斗數彀率": "祿存厚重，入財帛而主豐饒。...",
            "斗數發微論": "化科化權照命，一躍龍門。..."
        }

    def populate(self):
        logger.info("Initializing ChromaDB connection...")
        docs = []
        metadatas = []
        ids = []

        for idx, (title, content) in enumerate(self.texts.items()):
            docs.append(content)
            metadatas.append({"title": f"《{title}》"})
            ids.append(f"classic_{idx}")

        self.collection.add(
            documents=docs,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Successfully updated ChromaDB with {len(self.texts)} ancient texts.")

if __name__ == "__main__":
    indexer = ClassicsIndexer()
    indexer.populate()
