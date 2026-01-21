"""八字模板 (組合式)"""
import random
from datetime import datetime
from greetings_closings import get_greeting, get_closing

DAY_MASTER_BASE = {
    "甲": {
        "element":"木","nature":"陽","image":"參天大樹",
        "traits":["開拓進取","領導力強","正直堅毅"],
        "descriptions": [
            "從命盤來看，您的日主為甲木，這代表您天生擁有一股剛毅的特質。",
            "您的核心能量源自甲木，如同參天大樹般挺拔，有著開拓者的氣魄。",
            "甲木日主的人，通常給人意志堅定的印象，這在您的命盤中非常明顯。",
            "您的生命藍圖以甲木為核心，象徵著向上生長、不斷突破的能量。"
        ]
    },
    "乙": {
        "element":"木","nature":"陰","image":"花草藤蔓",
        "traits":["溫和細膩","善於協調","柔中帶剛"],
        "descriptions": [
            "您的日主為乙木，宛如花草藤蔓，展現出強大的韌性與適應力。",
            "核心能量源於乙木，您擁有細膩的感知力，善於以柔克剛。",
            "乙木日主象徵著溫和與靈活，您懂得在變動中找到生存之道。",
            "如同在大地蔓延的綠意，您的生命力內斂而持久，充滿生機。"
        ]
    },
    "丙": {
        "element":"火","nature":"陽","image":"太陽烈火",
        "traits":["熱情開朗","光明磊落","感染力強"],
        "descriptions": [
            "您的日主是丙火，如同普照大地的太陽，天生帶有溫暖他人的使命。",
            "核心能量燃燒著丙火的熱情，您的出現總能驅散周圍的陰霾。",
            "丙火日主代表著光明與希望，您擁有強大的感染力與群眾魅力。",
            "像太陽一樣無私地燃燒，您的生命充滿了活力與正向的能量。"
        ]
    },
    "丁": {
        "element":"火","nature":"陰","image":"燭火星光",
        "traits":["溫暖體貼","注重細節","專注內斂"],
        "descriptions": [
            "您的日主為丁火，像是夜空中指引方向的星光，溫柔而堅定。",
            "核心能量源自丁火，您心思細膩，總能在細節中發現美好。",
            "丁火日主擁有內斂的燃燒特質，您的溫暖是默默付出而不張揚的。",
            "如同燭光般搖曳卻不熄滅，您的內心擁有一股專注而持久的力量。"
        ]
    },
    "戊": {
        "element":"土","nature":"陽","image":"高山大地",
        "traits":["穩重踏實","包容力強","誠信可靠"],
        "descriptions": [
            "您的日主是戊土，宛如巍峨的高山，給人一種穩重可靠的安全感。",
            "核心能量源於戊土，您擁有寬廣的胸懷，能包容萬物的生長。",
            "戊土日主象徵著誠信與堅定，您是團隊中不可或缺的中流砥柱。",
            "如同大地般厚德載物，您的生命展現出沉穩與不動如山的特質。"
        ]
    },
    "己": {
        "element":"土","nature":"陰","image":"田園沃土",
        "traits":["細心謹慎","善於經營","內斂務實"],
        "descriptions": [
            "您的日主為己土，像是滋養萬物的田園沃土，充滿了孕育的能量。",
            "核心能量源自己土，您做事細心謹慎，善於在默默耕耘中收穫。",
            "己土日主具有極強的可塑性，您能將手中的資源轉化為豐碩的成果。",
            "如同溫潤的泥土，您的務實與內斂，是成就事業的堅實基礎。"
        ]
    },
    "庚": {
        "element":"金","nature":"陽","image":"鋼鐵寶劍",
        "traits":["剛毅果斷","重義氣","行動力強"],
        "descriptions": [
            "您的日主是庚金，如同千錘百鍊的寶劍，天生帶有一股革新的銳氣。",
            "核心能量源於庚金，您行事果斷，面對困難從不輕言退縮。",
            "庚金日主講義氣、重然諾，您身上有一種俠客般的豪爽氣質。",
            "像鋼鐵一樣堅硬不屈，您的生命力展現出強大的意志與執行力。"
        ]
    },
    "辛": {
        "element":"金","nature":"陰","image":"珠寶美玉",
        "traits":["細緻優雅","有品味","有原則"],
        "descriptions": [
            "您的日主為辛金，宛如經過雕琢的珠寶美玉，散發著獨特的光彩。",
            "核心能量源自辛金，您追求完美，對生活有著獨到的品味與堅持。",
            "辛金日主外表溫潤但內心剛強，您有著不可侵犯的原則與自尊。",
            "如同閃耀的金飾，您的才華需要被看見，注定要在人群中發光。"
        ]
    },
    "壬": {
        "element":"水","nature":"陽","image":"江河大海",
        "traits":["聰明靈活","適應力強","思維活躍"],
        "descriptions": [
            "您的日主是壬水，像是奔流不息的江河大海，充滿了智慧與動能。",
            "核心能量源於壬水，您思維靈活奔放，不喜歡受到傳統框架的束縛。",
            "壬水日主擁有多變的面貌，您的適應力極強，能駕馭各種複雜局勢。",
            "如同大海般深不可測，您的胸襟開闊，蘊藏著巨大的潛能與智慧。"
        ]
    },
    "癸": {
        "element":"水","nature":"陰","image":"雨露甘霖",
        "traits":["智慧敏銳","洞察力佳","心思細膩"],
        "descriptions": [
            "您的日主為癸水，宛如滋潤大地的雨露甘霖，溫柔卻無孔不入。",
            "核心能量源自癸水，您擁有敏銳的直覺與洞察力，能看透事物的本質。",
            "癸水日主善於以柔克剛，您的智慧如水般滲透，能默默影響周遭。",
            "如同晨間的露珠，您的心思細膩剔透，擁有一種靈動而神秘的氣質。"
        ]
    }
}

MONTH_MODIFIERS = {
    "子":{"season":"冬","advice":"宜靜養蓄力"},"丑":{"season":"冬末","advice":"宜穩健前行"},
    "寅":{"season":"初春","advice":"宜積極開拓"},"卯":{"season":"仲春","advice":"宜把握機會"},
    "辰":{"season":"暮春","advice":"宜調整方向"},"巳":{"season":"初夏","advice":"宜展現自我"},
    "午":{"season":"盛夏","advice":"宜大展宏圖"},"未":{"season":"暮夏","advice":"宜沉澱思考"},
    "申":{"season":"初秋","advice":"宜收穫成果"},"酉":{"season":"仲秋","advice":"宜精進專業"},
    "戌":{"season":"暮秋","advice":"宜總結經驗"},"亥":{"season":"初冬","advice":"宜規劃未來"}
}

TEN_GODS = {
    "比肩": {"meaning": "與我相同", "strength": "獨立自主", "career": "創業/自由業", "advice": "注意過於固執"},
    "劫財": {"meaning": "競爭能量", "strength": "積極進取", "career": "銷售/競技", "advice": "防止衝動破財"},
    "食神": {"meaning": "創作才華", "strength": "藝術天分", "career": "文創/餐飲", "advice": "享受生活的美好"},
    "傷官": {"meaning": "表現慾望", "strength": "口才辯才", "career": "律師/演說家", "advice": "避免過度批判"},
    "正財": {"meaning": "穩定收入", "strength": "理財守成", "career": "會計/金融穩定職", "advice": "腳踏實地最可靠"},
    "偏財": {"meaning": "意外之財", "strength": "投資眼光", "career": "投資/業務", "advice": "高報酬伴隨高風險"},
    "正官": {"meaning": "正當權威", "strength": "責任感強", "career": "公職/管理", "advice": "適合體制內發展"},
    "七殺": {"meaning": "魄力威嚴", "strength": "執行力強", "career": "軍警/開創型", "advice": "剛柔並濟更成功"},
    "正印": {"meaning": "學習庇蔭", "strength": "學術能力", "career": "教育/研究", "advice": "善用貴人運"},
    "偏印": {"meaning": "獨特思維", "strength": "創新思考", "career": "技術/研發", "advice": "避免想太多不行動"}
}

CAREER = {"木":["教育","醫療","環保"],"火":["銷售","演藝","科技"],"土":["金融","地產","管理"],"金":["法律","財務","製造"],"水":["貿易","傳媒","旅遊"]}
RELATIONSHIP = {"陽":["傾向主導，建議多傾聽","熱情擔當是魅力，也要給空間"],"陰":["細膩體貼但有時被動","溫柔包容是特質，也要表達需求"]}

def generate_bazi_interpretation(chart):
    dm = chart.get('day_master','甲')
    pillars = chart.get('pillars', {})
    month_data = pillars.get('month', {}) if isinstance(pillars, dict) else {}
    mz = month_data.get('zhi', '子') if isinstance(month_data, dict) else '子'
    ten_gods = chart.get('ten_gods', []) # Expecting a list of strings if available

    d = DAY_MASTER_BASE.get(dm, DAY_MASTER_BASE['甲'])
    m = MONTH_MODIFIERS.get(mz, MONTH_MODIFIERS['子'])
    year = datetime.now().year
    careers = random.sample(CAREER.get(d['element'],CAREER['木']),2)
    rel = random.choice(RELATIONSHIP.get(d['nature'],RELATIONSHIP['陽']))
    
    # 隨機選擇描述
    desc = random.choice(d.get('descriptions', [f"您是{dm}日主"]))

    out = [f"{get_greeting('bazi')}\n"]
    out.append(f"\n## 🎋 日主性格")
    out.append(f"\n{desc}")
    out.append(f"\n核心特質：**{d['traits'][0]}**、**{d['traits'][1]}**、**{d['traits'][2]}**。")

    out.append(f"\n\n## 🌙 月令影響")
    out.append(f"\n生於{m['season']}，{m['advice']}。")

    # 十神格局分析 (如果有)
    if ten_gods:
        out.append("\n\n## 🔮 格局解析")
        if isinstance(ten_gods, list):
             # 取前兩個主要格局
            for tg in ten_gods[:2]:
                if tg in TEN_GODS:
                    god = TEN_GODS[tg]
                    out.append(f"\n**{tg}格**：{god['meaning']}。")
                    out.append(f"\n優勢：{god['strength']}。建議：{god['advice']}。")
    
    out.append(f"\n\n## 💼 事業方向")
    out.append(f"\n適合：{'/'.join(careers)}等行業。")

    out.append(f"\n\n## 💕 感情特質")
    out.append(f"\n{rel}")

    out.append(f"\n\n## 📅 {year}年運勢")
    out.append(f"\n今年{m['advice']}，穩步前行。")
    
    out.append(get_closing('bazi'))
    
    return "".join(out)
