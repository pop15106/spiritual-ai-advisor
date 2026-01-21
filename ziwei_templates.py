"""紫微模板 (組合式強化版)"""
import random
from greetings_closings import get_greeting, get_closing

STARS = {
    "紫微":{"type":"帝星","traits":["領導格局","氣質高貴"],"career":"管理/政治","love":"需被尊重"},
    "天機":{"type":"智星","traits":["思維敏捷","善謀劃"],"career":"策劃/研究","love":"需智性交流"},
    "太陽":{"type":"光明星","traits":["正直熱心","助人為樂"],"career":"公職/教育","love":"坦誠直接"},
    "武曲":{"type":"財星","traits":["剛毅果斷","理財能手"],"career":"金融/商業","love":"務實理性"},
    "天同":{"type":"福星","traits":["溫和善良","知足常樂"],"career":"服務/社工","love":"隨和包容"},
    "廉貞":{"type":"囚星","traits":["聰明幹練","感情豐富"],"career":"藝術/法務","love":"熱烈但易妒"},
    "天府":{"type":"財庫星","traits":["穩重大方","守成之才"],"career":"金融/地產","love":"穩定可靠"},
    "太陰":{"type":"富星","traits":["細膩敏感","藝術天分"],"career":"設計/藝術","love":"溫柔體貼"},
    "貪狼":{"type":"桃花星","traits":["多才多藝","社交能手"],"career":"演藝/銷售","love":"魅力四射"},
    "巨門":{"type":"暗星","traits":["口才極佳","愛辯論"],"career":"律師/教師","love":"需多溝通"},
    "天相":{"type":"印星","traits":["正義感強","輔佐之才"],"career":"秘書/幕僚","love":"忠誠可靠"},
    "天梁":{"type":"蔭星","traits":["慈悲為懷","長輩緣好"],"career":"醫療/公益","love":"年長緣佳"},
    "七殺":{"type":"將星","traits":["剛強獨立","開創力強"],"career":"創業/軍警","love":"個性強烈"},
    "破軍":{"type":"耗星","traits":["勇於變革","不安現狀"],"career":"開拓/改革","love":"變動較多"}
}

# 宮位影響
PALACE_INFLUENCE = {
    "命宮":"決定您的核心性格","財帛宮":"影響財富運勢","事業宮":"決定職業發展方向",
    "夫妻宮":"影響感情婚姻","遷移宮":"關係外出與貴人運","福德宮":"反映精神狀態與享受"
}

# 星曜組合
STAR_COMBOS = {
    # 原有組合
    ("紫微","天府"):"紫府同宮，富貴雙全之格",
    ("紫微","貪狼"):"桃花旺盛但需節制慾望",
    ("太陽","太陰"):"日月同輝，陰陽調和之格",
    ("武曲","天府"):"財星入庫，理財能力極佳",
    ("天機","太陰"):"機月同梁格，適合文職",
    ("七殺","破軍"):"殺破狼格局，開創力強但波動大",
    
    # 新增組合
    ("紫微","七殺"): "紫殺同宮，威權震懾，適合領導但需防獨斷",
    ("紫微","破軍"): "紫破同宮，大開大合，人生起伏較大",
    ("天機","巨門"): "機巨同宮，口才極佳，適合教學或法律",
    ("太陽","巨門"): "巨日同宮，光明化解是非，貴人運佳",
    ("武曲","貪狼"): "武貪同宮，財星遇桃花，事業與感情皆精彩",
    ("武曲","七殺"): "武殺同宮，剛毅果斷，軍警或開創事業佳",
    ("廉貞","七殺"): "廉殺同宮，聰明幹練但感情波折",
    ("廉貞","貪狼"): "廉貞貪狼，桃花極旺，藝術或演藝天分",
    ("天府","廉貞"): "府廉同宮，穩中求進，財運不錯",
    ("天同","太陰"): "同陰同宮，溫和善良，福澤深厚",
    ("天同","天梁"): "同梁同宮，福星蔭星，長輩緣極佳",
    ("天梁","太陽"): "陽梁同宮，正直無私，公職運佳"
}

def generate_ziwei_interpretation(main_star, palace_data=None):
    star = STARS.get(main_star, STARS["紫微"])
    out = [f"{get_greeting('ziwei')}\n"]
    out.append(f"## ⭐ 命宮主星：{main_star}（{star['type']}）")
    out.append(f"\n性格：{'/'.join(star['traits'])}")
    out.append(f"\n事業傾向：{star['career']}")
    out.append(f"\n感情特質：{star['love']}")
    
    if palace_data:
        out.append("\n\n## 🏛️ 重要宮位分析")
        # 只取前幾個重要宮位或隨機幾個
        items = list(palace_data.items())
        # 簡單過濾，只顯示有定義主星的宮位
        valid_items = [(p, s) for p, s in items if s in STARS and p in PALACE_INFLUENCE]
        
        for palace, star_name in valid_items[:4]:
            s = STARS[star_name]
            out.append(f"\n**{palace}**（{PALACE_INFLUENCE[palace]}）：{star_name}")
            out.append(f"\n→ {s['traits'][0]}的能量在此發揮")
            
            # 檢查組合
            combo_key = tuple(sorted([main_star, star_name]))
            if combo_key in STAR_COMBOS:
                out.append(f"\n💫 特殊格局：{STAR_COMBOS[combo_key]}")
    
    out.append(get_closing('ziwei'))
    return "".join(out)
