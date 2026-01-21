"""占星模板 (組合式強化版)"""
import random
from greetings_closings import get_greeting, get_closing

SIGNS = {
    "牡羊座":{"e":"火","m":"開創","traits":["熱情","衝動","勇敢"],"ruler":"火星","compatible":["獅子座","射手座"]},
    "金牛座":{"e":"土","m":"固定","traits":["穩重","務實","品味"],"ruler":"金星","compatible":["處女座","摩羯座"]},
    "雙子座":{"e":"風","m":"變動","traits":["機智","多變","好奇"],"ruler":"水星","compatible":["天秤座","水瓶座"]},
    "巨蟹座":{"e":"水","m":"開創","traits":["敏感","顧家","直覺"],"ruler":"月亮","compatible":["天蠍座","雙魚座"]},
    "獅子座":{"e":"火","m":"固定","traits":["自信","大方","領袖"],"ruler":"太陽","compatible":["牡羊座","射手座"]},
    "處女座":{"e":"土","m":"變動","traits":["細心","分析","完美"],"ruler":"水星","compatible":["金牛座","摩羯座"]},
    "天秤座":{"e":"風","m":"開創","traits":["和諧","優雅","公平"],"ruler":"金星","compatible":["雙子座","水瓶座"]},
    "天蠍座":{"e":"水","m":"固定","traits":["神秘","深沉","堅定"],"ruler":"冥王星","compatible":["巨蟹座","雙魚座"]},
    "射手座":{"e":"火","m":"變動","traits":["樂觀","冒險","自由"],"ruler":"木星","compatible":["牡羊座","獅子座"]},
    "摩羯座":{"e":"土","m":"開創","traits":["務實","野心","責任"],"ruler":"土星","compatible":["金牛座","處女座"]},
    "水瓶座":{"e":"風","m":"固定","traits":["獨立","創新","人道"],"ruler":"天王星","compatible":["雙子座","天秤座"]},
    "雙魚座":{"e":"水","m":"變動","traits":["浪漫","敏感","直覺"],"ruler":"海王星","compatible":["巨蟹座","天蠍座"]}
}

PLANETS = {
    "太陽": {"symbol": "☀️", "meaning": "核心自我", "domain": "意志力、生命力、父親"},
    "月亮": {"symbol": "🌙", "meaning": "情緒本能", "domain": "情感、母親、安全感"},
    "水星": {"symbol": "☿", "meaning": "溝通思維", "domain": "學習、表達、手足"},
    "金星": {"symbol": "♀", "meaning": "愛與美", "domain": "愛情、金錢、審美"},
    "火星": {"symbol": "♂", "meaning": "行動力", "domain": "勇氣、性慾、競爭"},
    "木星": {"symbol": "♃", "meaning": "擴張幸運", "domain": "機會、信仰、高等教育"},
    "土星": {"symbol": "♄", "meaning": "限制成長", "domain": "責任、考驗、時間"},
    "天王星": {"symbol": "♅", "meaning": "突破革新", "domain": "自由、科技、意外"},
    "海王星": {"symbol": "♆", "meaning": "夢幻迷惑", "domain": "靈性、藝術、逃避"},
    "冥王星": {"symbol": "♇", "meaning": "死亡重生", "domain": "轉化、權力、深層心理"}
}

HOUSES = {
    1: {"name": "命宮", "domain": "自我形象、外表、人生態度"},
    2: {"name": "財帛宮", "domain": "金錢、物質、價值觀"},
    3: {"name": "溝通宮", "domain": "學習、短途旅行、兄弟姐妹"},
    4: {"name": "家庭宮", "domain": "家庭、根源、內心安全感"},
    5: {"name": "創造宮", "domain": "戀愛、子女、創作、娛樂"},
    6: {"name": "工作宮", "domain": "日常工作、健康、服務"},
    7: {"name": "伴侶宮", "domain": "婚姻、合作關係、公開敵人"},
    8: {"name": "資源宮", "domain": "他人資源、性、死亡與重生"},
    9: {"name": "遠行宮", "domain": "遠行、高等教育、哲學信仰"},
    10: {"name": "事業宮", "domain": "事業、社會地位、公眾形象"},
    11: {"name": "社群宮", "domain": "朋友、團體、願望"},
    12: {"name": "秘密宮", "domain": "潛意識、隱藏敵人、犧牲"}
}

ELEMENT_COMBOS = {
    ("火","火"):"雙火組合，熱情爆發但需注意衝動",
    ("火","土"):"火土組合，熱情與務實並存",
    ("火","風"):"火風組合，想法與行動力俱佳",
    ("火","水"):"火水組合，矛盾中尋求平衡",
    ("土","土"):"雙土組合，穩定務實但需增加彈性",
    ("土","風"):"土風組合，實際與理想間找平衡",
    ("土","水"):"土水組合，感性與務實兼備",
    ("風","風"):"雙風組合，思維活躍但需落地執行",
    ("風","水"):"風水組合，理性與感性交織",
    ("水","水"):"雙水組合，情感豐富但需增加理性"
}

MOON_NEEDS = {"火":"需要被認可和表現空間","土":"需要安全感和穩定","風":"需要溝通和智性刺激","水":"需要情感連結和理解"}
ASC_IMPRESSION = {"火":"積極主動、充滿活力","土":"穩重可靠、腳踏實地","風":"機智靈活、善於社交","水":"溫柔敏感、富有同理心"}

def generate_astrology_interpretation(sun_sign, moon_sign=None, asc_sign=None):
    clean_sun = sun_sign.split(' ')[-1] if sun_sign else "牡羊座"
    sun = SIGNS.get(clean_sun, SIGNS["牡羊座"])
    
    # 獲取守護星資訊
    ruler_name = sun['ruler']
    ruler_info = PLANETS.get(ruler_name, {})
    ruler_desc = f"{ruler_name}（{ruler_info.get('meaning','')}）" if ruler_info else ruler_name

    out = [f"{get_greeting('astrology')}\n"]
    out.append(f"## ☀️ 太陽{clean_sun}\n**元素**：{sun['e']} | **模式**：{sun['m']} | **守護星**：{ruler_desc}")
    out.append(f"\n核心特質：{'/'.join(sun['traits'])}")
    out.append(f"\n最佳拍檔：{'/'.join(sun['compatible'])}")
    
    if moon_sign:
        clean_moon = moon_sign.split(' ')[-1]
        if clean_moon in SIGNS:
            moon = SIGNS[clean_moon]
            combo_key = tuple(sorted([sun['e'], moon['e']]))
            combo_desc = ELEMENT_COMBOS.get(combo_key, "獨特的元素組合")
            out.append(f"\n\n## 🌙 月亮{clean_moon}\n情緒需求：{MOON_NEEDS.get(moon['e'],'情感豐富')}")
            out.append(f"\n**日月組合**：{combo_desc}")
    
    if asc_sign:
        clean_asc = asc_sign.split(' ')[-1]
        if clean_asc in SIGNS:
            asc = SIGNS[clean_asc]
            asc_ruler = asc['ruler']
            # Ascendant ruler info
            # asc_ruler_info = PLANETS.get(asc_ruler, {})
            out.append(f"\n\n## ⬆️ 上升{clean_asc}\n第一印象：{ASC_IMPRESSION.get(asc['e'],'獨特魅力')}")
            out.append(f"\n人生方向受{asc_ruler}影響")
    
    out.append(get_closing('astrology'))
    return "".join(out)
