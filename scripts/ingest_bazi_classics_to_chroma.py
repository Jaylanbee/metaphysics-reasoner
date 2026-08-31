import json
import os
import sys

def ingest_bazi_classics():
    """
    將八字古籍真實全文切塊並匯入 ChromaDB 向量庫 (供 RAG 檢索使用)
    若系統環境不支援持久化 ChromaDB (如 CI/CD 或輕量化容器)，
    可將其轉存為靜態索引檔案，此腳本主要用於本地知識庫的生成與更新。
    """
    try:
        import chromadb
        from chromadb.utils import embedding_functions
    except ImportError:
        print("未安裝 chromadb。請執行 pip install chromadb")
        return False

    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "..", "data")
    classics_dir = os.path.join(data_dir, "classics")
    chroma_db_dir = os.path.join(data_dir, "chroma_db")

    # 確保資料庫目錄存在
    os.makedirs(chroma_db_dir, exist_ok=True)

    print("初始化 ChromaDB...")
    client = chromadb.PersistentClient(path=chroma_db_dir)
    collection = client.get_or_create_collection(
        name="bazi_knowledge",
        embedding_function=embedding_functions.DefaultEmbeddingFunction()
    )

    # 讀取剛剛用爬蟲下載的真實古籍
    books = [
        "yuanhaiziping_cleaned.json",
        "sanmingtonghui_cleaned.json",
        "ditiansui_cleaned.json",
        "zipingzhenquan_cleaned.json",
        "qiongtongbaojian_cleaned.json"
    ]

    ids = []
    documents = []
    metadatas = []
    count = 0

    for book_file in books:
        filepath = os.path.join(classics_dir, book_file)
        if not os.path.exists(filepath):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            text = data.get("originalText", "")
            book_name = data.get("book", "")

            # 使用句號來進行大約的 Chunking 切塊
            chunks = [t.strip() for t in text.replace("\n", "。").split("。") if len(t.strip()) > 10]

            for chunk in chunks:
                count += 1
                ids.append(f"{book_name}_{count}")
                documents.append(chunk)
                metadatas.append({"source": book_name, "chapter": data.get("chapter", "")})

    if documents:
        print(f"準備匯入 {len(documents)} 筆八字古籍文獻真實語料切塊...")
        # 為了避免一次匯入過多造成 memory issue，分批匯入
        batch_size = 5000
        for i in range(0, len(documents), batch_size):
            end_idx = min(i + batch_size, len(documents))
            collection.upsert(
                ids=ids[i:end_idx],
                documents=documents[i:end_idx],
                metadatas=metadatas[i:end_idx]
            )
            print(f"  已匯入 {end_idx}/{len(documents)} 筆...")

        print(f"✅ 成功匯入 ChromaDB！目前 bazi_knowledge 庫共有 {collection.count()} 筆真實古籍紀錄。")
    else:
        print("找不到任何可匯入的文獻。")

    return True

if __name__ == "__main__":
    ingest_bazi_classics()
