import pytest
import sqlite3
import os
import json
import gzip
from scripts.ingest_to_sqlite import batch_ingest

DB_PATH = "test_ingestion.db"
MOCK_FOLDER = "test_mock_data"

@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup
    os.makedirs(MOCK_FOLDER, exist_ok=True)
    mock_file = os.path.join(MOCK_FOLDER, "test.jsonl.gz")
    with gzip.open(mock_file, "wt", encoding="utf-8") as f:
        sample = {
            "chartId": "test_chart_1",
            "birthInfo": {
                "solar": {"year": 1990, "month": 5, "day": 10},
                "lunar": {"year": 1990, "month": 4, "day": 16, "isLeap": False},
                "timeBranch": "寅",
                "gender": "F"
            },
            "chart": {
                "palaces": [
                    {
                        "name": "命宮",
                        "earthlyBranch": "子",
                        "majorStars": [{"name": "紫微"}, {"name": "天府"}]
                    }
                ]
            },
            "topics": {"topic_1": "test topic"}
        }
        f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    yield

    # Teardown
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    if os.path.exists(MOCK_FOLDER):
        for file in os.listdir(MOCK_FOLDER):
            os.remove(os.path.join(MOCK_FOLDER, file))
        os.rmdir(MOCK_FOLDER)

def test_ingestion():
    batch_ingest(MOCK_FOLDER, DB_PATH, batch_size=10)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM samples")
    count = cursor.fetchone()[0]
    assert count == 1

    cursor.execute("SELECT chart_id, gender, main_stars FROM samples")
    row = cursor.fetchone()
    assert row[0] == "test_chart_1"
    assert row[1] == "F"
    assert row[2] == "紫微,天府"

    conn.close()
