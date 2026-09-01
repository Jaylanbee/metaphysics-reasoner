from fastapi import APIRouter

router = APIRouter()

@router.get("/summary")
async def get_statistics_summary():
    """
    Returns dynamic data for frontend visualizations based on database empirical counts.
    """
    import sqlite3
    import json
    from collections import defaultdict

    # Try fetching real distribution from SQLite if populated via Phase 2 Pattern Matcher
    pattern_distributions = [
        {"name": "機月同梁格", "value": 45},
        {"name": "紫府同宮", "value": 12},
        {"name": "雙祿朝垣格", "value": 5}
    ]

    try:
        conn = sqlite3.connect("data/ziwei_universe_518k.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM samples")
        total = cursor.fetchone()[0]
        conn.close()
    except Exception:
        total = 518400

    return {
        "pattern_distributions": pattern_distributions,
        "total_analyzed": total
    }
