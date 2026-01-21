"""塔羅模板 (組合式)"""
import random
from greetings_closings import get_greeting, get_closing

SPREAD_RULES = [
    (["愛情","感情","戀愛","婚姻"],"愛情十字",["現況","障礙","建議","對方心態","結果"]),
    (["工作","事業","升遷","職場"],"事業指引",["現況","挑戰","建議","結果"]),
    (["財運","金錢","投資"],"財富路徑",["財務現況","機會","風險","建議"]),
]
def select_spread(q):
    for kws,name,pos in SPREAD_RULES:
        if any(k in q for k in kws): return name,pos
    return "時間之流",["過去","現在","未來"]

CARDS = {
    "愚者": {
        "theme": "新開始",
        "up": ["冒險", "自由", "可能"],
        "rev": ["魯莽", "輕率", "恐懼"],
        "contexts": {
            "love": {
                "up": "一段無拘無束的新戀情即將展開，享受單純的心動吧。",
                "rev": "感情上可能還沒準備好承諾，或對關係有些逃避。"
            },
            "career": {
                "up": "適合嘗試新工作領域，不要怕沒經驗，勇敢跳脫舒適圈。",
                "rev": "工作上可能過於冒進，建議三思而後行。"
            },
            "general": {
                "up": "新的開始就在眼前，保持開放心態迎接可能性。",
                "rev": "提醒您不要因恐懼而裹足不前，也不要魯莽行事。"
            }
        }
    },
    "魔術師": {
        "theme": "創造",
        "up": ["意志力", "技能", "專注"],
        "rev": ["操控", "欺騙", "未發揮"],
        "contexts": {
            "love": {
                "up": "在這個關係中您擁有主動權，積極溝通能帶來好結果。",
                "rev": "可能存在溝通不良或不真承的情況，需留意對方的真實意圖。"
            },
            "career": {
                "up": "展現才華的好時機，您擁有完成任務所需的所有資源。",
                "rev": "可能感到懷才不遇，或執行力不足，建議重新盤點資源。"
            },
            "general": {
                "up": "您擁有創造現實的能力，專注目標並付諸行動吧。",
                "rev": "注意是否被表象迷惑，或者在計畫上不夠周全。"
            }
        }
    },
    "女祭司": {
        "theme": "直覺",
        "up": ["智慧", "神秘", "潛意識"],
        "rev": ["忽視直覺", "表面化"],
        "contexts": {
            "love": {
                "up": "一段柏拉圖式的精神連結，或需要多傾聽內在的聲音。",
                "rev": "感情中可能過於冷淡或封閉，建議多表達真實感受。"
            },
            "career": {
                "up": "適合從事研究或需要洞察力的工作，相信您的直覺判斷。",
                "rev": "職場人際可能較為疏離，或忽視了重要的潛在訊息。"
            },
            "general": {
                "up": "靜下心來，答案就在您的內在智慧中。",
                "rev": "不要只看表面，深入挖掘背後的真相。"
            }
        }
    },
    "皇后": {
        "theme": "豐盛",
        "up": ["創造力", "滋養", "母性"],
        "rev": ["依賴", "創造力受阻"],
        "contexts": {
            "love": {
                "up": "感情豐收，充滿愛與關懷的關係，甚至有懷孕的可能。",
                "rev": "可能在關係中過於依賴，或過度溺愛導致失衡。"
            },
            "career": {
                "up": "創業或專案將有豐碩成果，適合發揮創意與美感。",
                "rev": "工作上可能缺乏動力，或資源分配不均。"
            },
            "general": {
                "up": "享受生活的美好與豐盛，大自然會帶給您力量。",
                "rev": "注意不要過度揮霍，或忽視了內在的匱乏感。"
            }
        }
    },
    "皇帝": {
        "theme": "權威",
        "up": ["領導力", "結構", "穩定"],
        "rev": ["專制", "控制", "僵化"],
        "contexts": {
            "love": {
                "up": "一段穩定且具責任感的關係，對方可能是成熟可靠的伴侶。",
                "rev": "關係中可能存在過強的控制欲，或缺乏情感交流。"
            },
            "career": {
                "up": "適合展現領導力，建立制度與規範，事業穩步上升。",
                "rev": "職場上可能遇到頑固的主管，或制度僵化難以發揮。"
            },
            "general": {
                "up": "建立秩序與自律是成功的關鍵。",
                "rev": "避免過於固執己見，適度彈性會更好。"
            }
        }
    },
    "戀人": {
        "theme": "選擇",
        "up": ["愛情", "和諧", "結合"],
        "rev": ["失衡", "價值衝突"],
        "contexts": {
            "love": {
                "up": "兩人情投意合，甜蜜的熱戀期，或面臨重要的關係抉擇。",
                "rev": "可能面臨價值觀不合，或誘惑導致的關係不穩。"
            },
            "career": {
                "up": "良好的合作夥伴關係，簽約順利。",
                "rev": "合作可能破局，或面臨職場上的兩難選擇。"
            },
            "general": {
                "up": "聽從內心的呼喚，做出符合真實自我的選擇。",
                "rev": "不要因為衝動而做出錯誤的決定。"
            }
        }
    },
    "高塔": {
        "theme": "突變",
        "up": ["啟示", "解放", "突破"],
        "rev": ["崩塌", "災難"],
        "contexts": {
            "love": {
                "up": "關係面臨劇變，可能是突然的分手或真相大白。",
                "rev": "勉強維持一段已經崩壞的關係，不願面對現實。"
            },
            "career": {
                "up": "組織改組或突發狀況，雖然衝擊但也是重建的機會。",
                "rev": "工作上可能遭遇重大挫折，需提防突發危機。"
            },
            "general": {
                "up": "舊的不去新的不來，接受改變才能重生。",
                "rev": "抗拒改變只會延長痛苦，不如坦然接受。"
            }
        }
    }
}

BASIC_CARDS = {
    "教皇":{"theme":"傳統","up":["指導","教育","信仰"],"rev":["教條","限制"]},
    "戰車":{"theme":"行動","up":["決心","勝利","自律"],"rev":["方向迷失","失控"]},
    "力量":{"theme":"勇氣","up":["耐心","內在力量"],"rev":["自我懷疑","軟弱"]},
    "隱士":{"theme":"內省","up":["智慧","獨處","真理"],"rev":["孤立","逃避"]},
    "命運之輪":{"theme":"轉變","up":["好運","機會","循環"],"rev":["運勢低迷","抗拒改變"]},
    "正義":{"theme":"公平","up":["真理","因果","負責"],"rev":["不公平","逃避責任"]},
    "倒吊人":{"theme":"放下","up":["新視角","犧牲","等待"],"rev":["抗拒犧牲","延遲"]},
    "死神":{"theme":"結束","up":["轉變","蛻變","放下"],"rev":["抗拒改變","停滯"]},
    "節制":{"theme":"平衡","up":["調和","耐心","中庸"],"rev":["失衡","過度","急躁"]},
    "惡魔":{"theme":"束縛","up":["面對陰影","覺察"],"rev":["束縛","成癮"]},
    "星星":{"theme":"希望","up":["靈感","療癒","指引"],"rev":["絕望","失去信心"]},
    "月亮":{"theme":"幻象","up":["直覺","潛意識"],"rev":["幻象","恐懼","困惑"]},
    "太陽":{"theme":"成功","up":["喜悅","活力","樂觀"],"rev":["暫時挫折","延遲"]},
    "審判":{"theme":"覺醒","up":["重生","召喚"],"rev":["自我懷疑","逃避"]},
    "世界":{"theme":"圓滿","up":["完成","成就","整合"],"rev":["未完成","延遲"]}
}

# Merge BASIC_CARDS into CARDS if they are not there
for k, v in BASIC_CARDS.items():
    if k not in CARDS:
        CARDS[k] = v

POS = {"過去":"過去顯示","現在":"目前是","未來":"未來指向","建議":"建議您","結果":"結果是","現況":"現況是","障礙":"障礙是","對方心態":"對方心態是","挑戰":"挑戰是","機會":"機會是","風險":"風險是","財務現況":"財務狀況"}

def detect_context(question):
    """根據問題內容判斷情境類型"""
    love_keywords = ["愛情", "感情", "戀愛", "婚姻", "對象", "喜歡", "分手", "復合", "他"]
    career_keywords = ["工作", "事業", "升遷", "職場", "跳槽", "面試", "老闆", "創業", "離職"]
    
    # 簡單的關鍵字匹配
    q_lower = question.lower()
    for kw in love_keywords:
        if kw in q_lower:
            return "love"
    for kw in career_keywords:
        if kw in q_lower:
            return "career"
    return "general"

def generate_tarot_interpretation(q,cards,positions):
    context = detect_context(q)
    out = [f"{get_greeting('tarot')}\n"]
    out.append(f"🔮 **問題**：{q}\n")
    
    for i,(c,p) in enumerate(zip(cards,positions),1):
        name = c.get("name","愚者")
        rev = c.get("reversed",False)
        ori = "逆位" if rev else "正位"
        
        data = CARDS.get(name,CARDS["愚者"])
        
        # 嘗試獲取情境描述
        context_data = data.get("contexts", {}).get(context, {})
        if context_data:
            desc = context_data.get("rev" if rev else "up", "")
        else:
            # Fallback 到舊邏輯
            kw = data.get("rev" if rev else "up", ["無關鍵字"]) 
            # 確保 kw 是 list (兼容舊結構)
            if isinstance(kw, str): kw = [kw]
            desc = f"關鍵字：{random.choice(kw)}"

        # 主題
        theme = data.get('theme', '未知')
        
        pos_desc = POS.get(p, f"在{p}位置")
        out.append(f"\n### {i}. {p}—**{name}**({ori})\n主題：{theme}｜{pos_desc}：{desc}")
        
    out.append(get_closing('tarot'))
    return "".join(out)
