"""
Spiritual AI Advisor - 八字命理 Agent
======================================
AI 八字命理師，使用 lunar-python 進行八字排盤與 AI 解讀。
"""

from lunar_python import Lunar, Solar
from datetime import datetime


def get_bazi_from_datetime(year: int, month: int, day: int, hour: int) -> dict:
    """
    根據陽曆生日計算八字
    
    Args:
        year: 出生年 (陽曆)
        month: 出生月 (陽曆)
        day: 出生日 (陽曆)
        hour: 出生時辰 (0-23)
    
    Returns:
        dict: 包含八字資訊的字典
    """
    # 從陽曆轉農曆
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lunar = solar.getLunar()
    
    # 取得八字
    bazi = lunar.getEightChar()
    
    # 年柱、月柱、日柱、時柱
    year_pillar = bazi.getYear()      # 年柱
    month_pillar = bazi.getMonth()    # 月柱
    day_pillar = bazi.getDay()        # 日柱
    hour_pillar = bazi.getTime()      # 時柱
    
    # 日主 (日柱天干)
    day_master = bazi.getDayGan()
    
    # 五行統計
    wuxing = bazi.getWuXing()
    
    # 十神
    year_shishen = bazi.getYearShiShenGan()
    month_shishen = bazi.getMonthShiShenGan()
    hour_shishen = bazi.getTimeShiShenGan()
    
    # 大運
    yun = bazi.getYun(1 if lunar.getYearGanByLiChun().find('陽') >= 0 else 0)  # 1=男, 0=女 (暫時預設男)
    
    # 大運列表
    dayun_list = []
    for dayun in yun.getDaYun():
        dayun_list.append({
            "start_age": dayun.getStartAge(),
            "end_age": dayun.getEndAge(),
            "ganzhi": dayun.getGanZhi()
        })
    
    return {
        "solar_date": f"{year}年{month}月{day}日 {hour}時",
        "lunar_date": lunar.toString(),
        "year_pillar": year_pillar,
        "month_pillar": month_pillar,
        "day_pillar": day_pillar,
        "hour_pillar": hour_pillar,
        "day_master": day_master,
        "four_pillars_display": f"{year_pillar}  {month_pillar}  {day_pillar}  {hour_pillar}",
        "wuxing": wuxing,
        "shishen": {
            "year": year_shishen,
            "month": month_shishen,
            "hour": hour_shishen
        },
        "dayun": dayun_list[:5]  # 取前5個大運
    }


def get_wuxing_analysis(bazi_result: dict) -> str:
    """分析五行喜用"""
    # 簡化版五行分析說明
    analysis = f"""
### 🔥 五行分析

**日主**: {bazi_result['day_master']}

**四柱**:
| 年柱 | 月柱 | 日柱 | 時柱 |
|------|------|------|------|
| {bazi_result['year_pillar']} | {bazi_result['month_pillar']} | {bazi_result['day_pillar']} | {bazi_result['hour_pillar']} |

**十神**:
- 年柱: {bazi_result['shishen']['year']}
- 月柱: {bazi_result['shishen']['month']}
- 時柱: {bazi_result['shishen']['hour']}

**大運行運** (前5個):
"""
    for dy in bazi_result['dayun']:
        analysis += f"- {dy['start_age']}~{dy['end_age']}歲: {dy['ganzhi']}\n"
    
    return analysis


# 天干地支元素說明 (給 AI 解讀用)
TIANGAN_ELEMENTS = {
    "甲": "陽木，如大樹，代表仁德、進取、直率",
    "乙": "陰木，如花草，代表柔韌、適應、溫和",
    "丙": "陽火，如太陽，代表熱情、光明、外向",
    "丁": "陰火，如燭光，代表細膩、內斂、聰明",
    "戊": "陽土，如高山，代表穩重、信用、包容",
    "己": "陰土，如田園，代表務實、中庸、謹慎",
    "庚": "陽金，如刀劍，代表剛毅、果斷、義氣",
    "辛": "陰金，如珠玉，代表精緻、敏感、完美",
    "壬": "陽水，如大海，代表智慧、包容、靈活",
    "癸": "陰水，如雨露，代表滋潤、敏銳、多思"
}

DIZHI_ELEMENTS = {
    "子": "陽水，鼠，代表智慧、機敏",
    "丑": "陰土，牛，代表勤勞、穩重",
    "寅": "陽木，虎，代表勇敢、進取",
    "卯": "陰木，兔，代表溫和、機敏",
    "辰": "陽土，龍，代表變化、權威",
    "巳": "陰火，蛇，代表智慧、神秘",
    "午": "陽火，馬，代表熱情、積極",
    "未": "陰土，羊，代表溫順、藝術",
    "申": "陽金，猴，代表機靈、變通",
    "酉": "陰金，雞，代表精確、完美",
    "戌": "陽土，狗，代表忠誠、正直",
    "亥": "陰水，豬，代表淳厚、享受"
}
