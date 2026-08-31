import argparse
import os
import sqlite3
import gzip
import json
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_schema(cursor):
    """
    建立 SQLite 資料表與索引
    """
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS samples (
        chart_id TEXT PRIMARY KEY,
        solar_year INTEGER,
        solar_month INTEGER,
        solar_day INTEGER,
        solar_hour INTEGER,
        lunar_year INTEGER,
        lunar_month INTEGER,
        lunar_day INTEGER,
        is_leap_month BOOLEAN,
        time_period TEXT,
        gender TEXT,
        wuxing_ju TEXT,
        main_stars TEXT,
        palaces_json TEXT,
        topics_json TEXT,
        detected_patterns TEXT,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_lunar_year ON samples(lunar_year)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_main_stars ON samples(main_stars)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_gender ON samples(gender)')

def extract_main_stars(chart_data):
    """
    從命盤資料提取命宮主星，以逗號分隔
    """
    palaces = chart_data.get('palaces', [])
    for palace in palaces:
        if palace.get('name') == '命宮' or palace.get('name') == '命宫':
            major_stars = [star.get('name', '') for star in palace.get('majorStars', [])]
            return ",".join(major_stars)
    return ""

def process_file(file_path):
    """
    處理單一 JSONL 檔案並回傳解析後的資料列
    """
    rows = []
    try:
        open_func = gzip.open if file_path.endswith('.gz') else open
        with open_func(file_path, 'rt', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    birth_info = data.get('birthInfo', {})
                    chart_data = data.get('chart', {})
                    topics_data = data.get('topics', {})
                    lunar_info = chart_data.get('lunarInfo', {})

                    # Solar / Birth Info
                    s_year = birth_info.get('year') or birth_info.get('solar', {}).get('year')
                    s_month = birth_info.get('month') or birth_info.get('solar', {}).get('month')
                    s_day = birth_info.get('day') or birth_info.get('solar', {}).get('day')
                    s_hour = birth_info.get('hour', 0)
                    gender = birth_info.get('gender', '')
                    time_branch = birth_info.get('timeBranch', '')

                    # Lunar Info
                    l_year = lunar_info.get('lunarYear') or birth_info.get('lunar', {}).get('year')
                    l_month = lunar_info.get('lunarMonth') or birth_info.get('lunar', {}).get('month')
                    l_day = lunar_info.get('lunarDay') or birth_info.get('lunar', {}).get('day')
                    is_leap = lunar_info.get('isLeapMonth') or birth_info.get('lunar', {}).get('isLeap', False)

                    # Chart ID
                    chart_id = data.get('chartId') or f"{s_year}_{s_month}_{s_day}_{s_hour}_{gender}"

                    wuxing_ju = chart_data.get('wuxingJuName', '')
                    main_stars = extract_main_stars(chart_data)

                    row = (
                        chart_id,
                        s_year,
                        s_month,
                        s_day,
                        s_hour,
                        l_year,
                        l_month,
                        l_day,
                        is_leap,
                        time_branch,
                        gender,
                        wuxing_ju,
                        main_stars,
                        json.dumps(chart_data.get('palaces', []), ensure_ascii=False),
                        json.dumps(topics_data, ensure_ascii=False),
                        None
                    )
                    rows.append(row)
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse JSON line in {file_path}")
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
    return rows

def batch_ingest(folder_path: str, db_path: str, batch_size: int = 2000):
    """
    從指定資料夾讀取所有 .jsonl.gz 檔案，批次匯入 SQLite
    """
    if not os.path.exists(folder_path):
        logger.error(f"資料夾不存在: {folder_path}")
        return

    # 連線至 SQLite 資料庫
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 建立 Schema
    create_schema(cursor)
    conn.commit()

    # 取得所有 .jsonl / .jsonl.gz 檔案
    files = []
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.jsonl') or filename.endswith('.jsonl.gz'):
                files.append(os.path.join(root, filename))

    if not files:
        logger.info(f"在 {folder_path} 找不到任何 jsonl 檔案。")
        return

    logger.info(f"找到 {len(files)} 個檔案，準備匯入...")

    insert_sql = '''
    INSERT OR REPLACE INTO samples (
        chart_id, solar_year, solar_month, solar_day, solar_hour,
        lunar_year, lunar_month, lunar_day, is_leap_month,
        time_period, gender, wuxing_ju, main_stars, palaces_json, topics_json, detected_patterns
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    total_inserted = 0
    batch = []

    for file_path in tqdm(files, desc="Processing Files"):
        rows = process_file(file_path)
        for row in rows:
            batch.append(row)
            if len(batch) >= batch_size:
                cursor.executemany(insert_sql, batch)
                conn.commit()
                total_inserted += len(batch)
                batch = []

    if batch:
        cursor.executemany(insert_sql, batch)
        conn.commit()
        total_inserted += len(batch)

    conn.close()
    logger.info(f"匯入完成！總共插入/更新 {total_inserted} 筆資料至 {db_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest JSONL data to SQLite.")
    parser.add_argument("--folder", required=True, help="Path to the folder containing .jsonl or .jsonl.gz files.")
    parser.add_argument("--db-path", required=True, help="Path to the output SQLite database file.")
    parser.add_argument("--batch-size", type=int, default=2000, help="Number of rows per batch insert.")

    args = parser.parse_args()
    batch_ingest(args.folder, args.db_path, args.batch_size)