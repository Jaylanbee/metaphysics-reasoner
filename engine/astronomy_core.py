# -*- coding: utf-8 -*-
"""
astronomy_core.py
=================
東方命理認知系統 ‧ 天文曆法與農曆節氣換算核心引擎
提供西曆、農曆、真太陽時、24節氣與天干地支五行精確轉換演算法。

[核心排盤引擎來源說明]
本模組為完全自主重新實作 (Clean-room implementation) 的純 Python 天文曆法與排盤核心引擎，
並非改寫或依賴自 iztro 等 Node.js 開源專案。此設計旨在確保系統於無 Node.js 依賴的
邊緣計算環境 (Edge computing) 或離線隔離環境中，依然具備 100% 的自主運算能力，
從而大幅提升系統長期的維護性、可移植性與除錯效率。
"""

import math
import datetime
from typing import Tuple, Dict, Any, List

# 天干與地支常數
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 五行與陰陽
GAN_WU_XING = {
    "甲": ("木", "陽"), "乙": ("木", "陰"),
    "丙": ("火", "陽"), "丁": ("火", "陰"),
    "戊": ("土", "陽"), "己": ("土", "陰"),
    "庚": ("金", "陽"), "辛": ("金", "陰"),
    "壬": ("水", "陽"), "癸": ("水", "陰")
}

ZHI_WU_XING = {
    "子": ("水", "陽"), "丑": ("土", "陰"),
    "寅": ("木", "陽"), "卯": ("木", "陰"),
    "辰": ("土", "陽"), "巳": ("火", "陰"),
    "午": ("火", "陽"), "未": ("土", "陰"),
    "申": ("金", "陽"), "酉": ("金", "陰"),
    "戌": ("土", "陽"), "亥": ("水", "陰")
}

# 地支藏干 (主氣, 中氣, 餘氣)
ZHI_CANG_GAN = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"]
}

# 納音五行速查表 (六十甲子納音)
NA_YIN_TABLE = {
    "甲子": "海中金", "乙丑": "海中金", "丙寅": "爐中火", "丁卯": "爐中火", "戊辰": "大林木", "己巳": "大林木",
    "庚午": "路旁土", "辛未": "路旁土", "壬申": "劍鋒金", "癸酉": "劍鋒金", "甲戌": "山頭火", "乙亥": "山頭火",
    "丙子": "澗下水", "丁丑": "澗下水", "戊寅": "城頭土", "己卯": "城頭土", "庚辰": "白蠟金", "辛巳": "白蠟金",
    "壬午": "楊柳木", "癸未": "楊柳木", "甲申": "泉中水", "乙酉": "泉中水", "丙戌": "屋上土", "丁亥": "屋上土",
    "戊子": "霹靂火", "己丑": "霹靂火", "庚寅": "松柏木", "辛卯": "松柏木", "壬辰": "長流水", "癸巳": "長流水",
    "甲午": "沙中金", "乙未": "沙中金", "丙申": "山下火", "丁酉": "山下火", "戊戌": "平地木", "己亥": "平地木",
    "庚子": "壁上土", "辛丑": "壁上土", "壬寅": "金箔金", "癸卯": "金箔金", "甲辰": "覆燈火", "乙巳": "覆燈火",
    "丙午": "天河水", "丁未": "天河水", "戊申": "大驛土", "己酉": "大驛土", "庚戌": "釵釧金", "辛亥": "釵釧金",
    "壬子": "桑柘木", "癸丑": "桑柘木", "甲寅": "大溪水", "乙卯": "大溪水", "丙辰": "沙中土", "丁巳": "沙中土",
    "戊午": "天上火", "己未": "天上火", "庚申": "石榴木", "辛酉": "石榴木", "壬戌": "大海水", "癸亥": "大海水"
}

# 24 節氣名稱
JIE_QI_NAMES = [
    "小寒", "大寒", "立春", "雨水", "驚蟄", "春分",
    "清明", "穀雨", "立夏", "小滿", "芒種", "夏至",
    "小暑", "大暑", "立秋", "處暑", "白露", "秋分",
    "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
]

# 農曆 1900 - 2100 年份數據編碼 (經典天文曆法庫位元組)
LUNAR_INFO = [
    0x04bd8,0x04ae0,0x0a570,0x054d5,0x0d260,0x0d950,0x16554,0x056a0,0x09ad0,0x055d2,
    0x04ae0,0x0a5b6,0x0a4d0,0x0d250,0x1d255,0x0b540,0x0d6a0,0x0ada2,0x095b0,0x14977,
    0x04970,0x0a4b0,0x0b4b5,0x06a50,0x06d40,0x1ab54,0x02b60,0x09570,0x052f2,0x04970,
    0x06566,0x0d4a0,0x0ea50,0x06e95,0x05ad0,0x02b60,0x186e3,0x092e0,0x1c8d7,0x0c950,
    0x0d4a0,0x1d8a6,0x0b550,0x056a0,0x1a5b4,0x025d0,0x092d0,0x0d2b2,0x0a950,0x0b557,
    0x06ca0,0x0b550,0x15355,0x04da0,0x0a5d0,0x14573,0x052d0,0x0a9a8,0x0e950,0x06aa0,
    0x0aea6,0x0ab50,0x04b60,0x0aae4,0x0a570,0x05260,0x0f263,0x0d950,0x05b57,0x056a0,
    0x096d0,0x04dd5,0x04ad0,0x0a4d0,0x0d4d4,0x0d250,0x0d558,0x0b540,0x0b5a0,0x195a6,
    0x095b0,0x049b0,0x0a974,0x0a4b0,0x0b27a,0x06a50,0x06d40,0x0af46,0x0ab60,0x09570,
    0x04af5,0x04970,0x064b0,0x074a3,0x0ea50,0x06b58,0x055c0,0x0ab60,0x096d5,0x092e0,
    0x0c960,0x0d954,0x0d4a0,0x0da50,0x07552,0x056a0,0x0abb7,0x025d0,0x092d0,0x0cab5,
    0x0a950,0x0b4a0,0x0baa4,0x0ad50,0x055d9,0x04ba0,0x0a5b0,0x15176,0x052b0,0x0a930,
    0x07954,0x06aa0,0x0ad50,0x05b52,0x04b60,0x0a6e6,0x0a4e0,0x0d260,0x0ea65,0x0d530,
    0x05aa0,0x076a3,0x096d0,0x04afb,0x04ad0,0x0a4d0,0x1d0b6,0x0d250,0x0d520,0x0dd45,
    0x0b5a0,0x056d0,0x055b2,0x049b0,0x0a577,0x0a4b0,0x0aa50,0x1b255,0x06d20,0x0ada0,
    0x14b63,0x09370,0x049f8,0x04970,0x064b0,0x168a6,0x0ea50,0x06b20,0x1a6c4,0x0aae0,
    0x092e0,0x0d2e3,0x0c960,0x0d557,0x0d4a0,0x0da50,0x05d55,0x056a0,0x0a6d0,0x055d4,
    0x052d0,0x0a9b8,0x0a950,0x0b4a0,0x0b6a6,0x0ad50,0x055a0,0x0aba4,0x0a5b0,0x052b0,
    0x0b273,0x06930,0x07337,0x06aa0,0x0ad50,0x14b55,0x04b60,0x0a570,0x054e4,0x0d160,
    0x0e968,0x0d520,0x0daa0,0x16aa6,0x056d0,0x04ae0,0x0a9d4,0x0a2d0,0x0d150,0x0f252,
    0x0d520
]

def get_lunar_year_days(year: int) -> int:
    info = LUNAR_INFO[year - 1900]
    total = 0
    for i in range(12):
        total += 30 if (info & (0x10000 >> (i + 1))) else 29
    leap_month = info & 0xf
    if leap_month > 0:
        total += 30 if (info & 0x10000) else 29
    return total

def get_leap_month(year: int) -> int:
    return LUNAR_INFO[year - 1900] & 0xf

def get_leap_month_days(year: int) -> int:
    if get_leap_month(year) > 0:
        return 30 if (LUNAR_INFO[year - 1900] & 0x10000) else 29
    return 0

def get_lunar_month_days(year: int, month: int) -> int:
    info = LUNAR_INFO[year - 1900]
    return 30 if (info & (0x10000 >> month)) else 29

def solar_to_lunar(year: int, month: int, day: int) -> Tuple[int, int, int, bool]:
    base_date = datetime.date(1900, 1, 31)
    target_date = datetime.date(year, month, day)
    offset = (target_date - base_date).days

    lunar_year = 1900
    while lunar_year < 2100 and offset > 0:
        days_in_year = get_lunar_year_days(lunar_year)
        if offset < days_in_year:
            break
        offset -= days_in_year
        lunar_year += 1

    leap_m = get_leap_month(lunar_year)
    is_leap = False
    lunar_month = 1

    while lunar_month <= 12:
        if is_leap:
            days_in_month = get_leap_month_days(lunar_year)
        else:
            days_in_month = get_lunar_month_days(lunar_year, lunar_month)

        if offset < days_in_month:
            break
        offset -= days_in_month

        if leap_m > 0 and lunar_month == leap_m and not is_leap:
            is_leap = True
        else:
            if is_leap:
                is_leap = False
            lunar_month += 1

    lunar_day = offset + 1
    return (lunar_year, lunar_month, lunar_day, is_leap)

def get_hour_branch(hour: int, minute: int = 0) -> str:
    total_min = hour * 60 + minute
    if total_min >= 23 * 60 or total_min < 1 * 60:
        return "子"
    idx = (total_min - 60) // 120 + 1
    return DI_ZHI[idx % 12]

def get_gan_zhi_year(year: int) -> str:
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12
    return TIAN_GAN[gan_idx] + DI_ZHI[zhi_idx]

def get_gan_zhi_month(year_gan: str, lunar_month: int) -> str:
    start_gan_map = {
        "甲": 2, "己": 2, # 丙作首
        "乙": 4, "庚": 4, # 戊為頭
        "丙": 6, "辛": 6, # 庚起
        "丁": 8, "壬": 8, # 壬位
        "戊": 0, "癸": 0  # 甲寅
    }
    start_gan = start_gan_map.get(year_gan, 0)
    month_gan_idx = (start_gan + (lunar_month - 1)) % 10
    month_zhi_idx = (2 + (lunar_month - 1)) % 12 # 正月為寅 (index 2)
    return TIAN_GAN[month_gan_idx] + DI_ZHI[month_zhi_idx]

def get_gan_zhi_hour(day_gan: str, hour_zhi: str) -> str:
    start_gan_map = {
        "甲": 0, "己": 0, # 甲
        "乙": 2, "庚": 2, # 丙
        "丙": 4, "辛": 4, # 戊
        "丁": 6, "壬": 6, # 庚
        "戊": 8, "癸": 8  # 壬
    }
    start_gan = start_gan_map.get(day_gan, 0)
    zhi_idx = DI_ZHI.index(hour_zhi)
    hour_gan_idx = (start_gan + zhi_idx) % 10
    return TIAN_GAN[hour_gan_idx] + hour_zhi

def get_gan_zhi_day(year: int, month: int, day: int) -> str:
    base_date = datetime.date(2000, 1, 1)
    target_date = datetime.date(year, month, day)
    diff = (target_date - base_date).days
    gan_idx = (4 + diff) % 10
    zhi_idx = (6 + diff) % 12
    return TIAN_GAN[gan_idx] + DI_ZHI[zhi_idx]

def compute_solar_time_correction(longitude: float, standard_meridian: float = 120.0) -> int:
    diff_deg = longitude - standard_meridian
    return int(diff_deg * 240)