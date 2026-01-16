"""
Spiritual AI Advisor - REST API
================================
Flask API server for Next.js frontend

Start: python api.py
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import random
import math
import ephem
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 引入詳細的人類圖資料
from gates_iching_data import GATES_ICHING_DETAILED
from channels_data import CHANNELS_DATA
from hd_gate_mapping import CHANNELS_LIST, GATE_TO_CENTER, get_gate_from_longitude

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)

# ========== Data Definitions ==========

MAJOR_ARCANA = [
    {"name": "愚者", "id": "ar00", 
     "upright": "新的開始、冒險、天真、自由、無限可能",
     "reversed": "魯莽、輕率、不負責任、恐懼改變",
     "meaning": "愚者代表純真與無畏的精神，暗示著新的旅程即將開始。"},
    {"name": "魔術師", "id": "ar01",
     "upright": "創造力、意志力、技能、自信、專注",
     "reversed": "操控、欺騙、能力未發揮、缺乏專注",
     "meaning": "魔術師象徵著將想法化為現實的能力，提醒您善用手邊的資源。"},
    {"name": "女祭司", "id": "ar02",
     "upright": "直覺、神秘、內在智慧、潛意識",
     "reversed": "隱藏的動機、表面化、忽視直覺",
     "meaning": "女祭司代表內在的智慧與直覺，暗示答案就在您心中。"},
    {"name": "皇后", "id": "ar03",
     "upright": "豐收、母性、創造力、自然、滋養",
     "reversed": "依賴、過度保護、創造力受阻",
     "meaning": "皇后象徵豐盛與滋養，代表創造與照顧的能量。"},
    {"name": "皇帝", "id": "ar04",
     "upright": "權威、結構、領導力、穩定、父性",
     "reversed": "專制、控制、缺乏紀律、過度僵化",
     "meaning": "皇帝代表權威與秩序，提醒您建立穩固的基礎。"},
    {"name": "教皇", "id": "ar05",
     "upright": "傳統、精神指導、教育、信仰",
     "reversed": "打破常規、質疑傳統、尋求個人真理",
     "meaning": "教皇象徵傳統智慧與精神指引，代表尋求更高意義。"},
    {"name": "戀人", "id": "ar06",
     "upright": "愛情、和諧、選擇、價值觀、結合",
     "reversed": "失衡、價值觀衝突、不和諧、選擇困難",
     "meaning": "戀人牌代表重要的選擇與關係，暗示心靈的結合。"},
    {"name": "戰車", "id": "ar07",
     "upright": "決心、意志力、勝利、自律、行動力",
     "reversed": "方向迷失、失控、缺乏方向、侵略性",
     "meaning": "戰車象徵征服與前進的動力，代表透過意志達成目標。"},
    {"name": "力量", "id": "ar08",
     "upright": "勇氣、耐心、內在力量、溫柔的堅持",
     "reversed": "自我懷疑、軟弱、濫用力量",
     "meaning": "力量牌代表內在的勇氣與耐心，提醒以溫柔克服挑戰。"},
    {"name": "隱士", "id": "ar09",
     "upright": "內省、獨處、智慧、尋找真理",
     "reversed": "孤立、逃避、過度封閉",
     "meaning": "隱士象徵內在探索與獨處的智慧，代表尋求內心的指引。"},
    {"name": "命運之輪", "id": "ar10",
     "upright": "命運、轉變、循環、好運、機會",
     "reversed": "抗拒改變、運勢低迷、失控感",
     "meaning": "命運之輪代表生命的循環與轉變，暗示重大變化即將來臨。"},
    {"name": "正義", "id": "ar11",
     "upright": "公平、真理、因果、負責任",
     "reversed": "不公平、逃避責任、欺騙",
     "meaning": "正義牌象徵公平與因果法則，提醒您為行為負責。"},
    {"name": "倒吊人", "id": "ar12",
     "upright": "犧牲、放下、新視角、等待",
     "reversed": "抗拒犧牲、延遲、過度無私",
     "meaning": "倒吊人代表暫停與換個角度看事情，暗示透過放下獲得智慧。"},
    {"name": "死神", "id": "ar13",
     "upright": "結束、轉變、蛻變、放下過去",
     "reversed": "抗拒改變、恐懼結束、停滯",
     "meaning": "死神牌代表終結與新生，象徵必要的轉變與蛻變。"},
    {"name": "節制", "id": "ar14",
     "upright": "平衡、耐心、調和、中庸之道",
     "reversed": "失衡、過度、急躁、缺乏遠見",
     "meaning": "節制象徵平衡與和諧，提醒您以耐心調和各方面。"},
    {"name": "惡魔", "id": "ar15",
     "upright": "束縛、執著、物質主義、陰影面",
     "reversed": "掙脫束縛、覺醒、擺脫執著",
     "meaning": "惡魔牌代表束縛與執著，暗示需要面對內在陰影。"},
    {"name": "高塔", "id": "ar16",
     "upright": "突變、崩塌、啟示、解放",
     "reversed": "避免災難、抗拒改變、延遲崩塌",
     "meaning": "高塔象徵突然的改變與舊結構的崩塌，代表必要的破壞。"},
    {"name": "星星", "id": "ar17",
     "upright": "希望、靈感、平靜、療癒、指引",
     "reversed": "絕望、失去信心、脫離現實",
     "meaning": "星星牌代表希望與療癒，暗示光明就在前方。"},
    {"name": "月亮", "id": "ar18",
     "upright": "幻象、潛意識、恐懼、直覺",
     "reversed": "釋放恐懼、看清真相、困惑消除",
     "meaning": "月亮象徵潛意識與幻象，提醒您面對內在的恐懼。"},
    {"name": "太陽", "id": "ar19",
     "upright": "成功、喜悅、活力、樂觀、明朗",
     "reversed": "暫時挫折、過度樂觀、延遲的成功",
     "meaning": "太陽牌代表成功與喜悅，象徵光明燦爛的能量。"},
    {"name": "審判", "id": "ar20",
     "upright": "覺醒、重生、召喚、評估過去",
     "reversed": "自我懷疑、拒絕召喚、逃避審視",
     "meaning": "審判牌象徵覺醒與重生，代表面對過去並迎接新生。"},
    {"name": "世界", "id": "ar21",
     "upright": "完成、圓滿、成就、整合、旅程終點",
     "reversed": "未完成、延遲、缺乏結束感",
     "meaning": "世界牌代表圓滿與成就，象徵一個階段的完美結束。"}
]

# 64 閘門易經對照表
GATES_ICHING = {
    1: {"hexagram": "乾", "name": "創造", "meaning": "創造力的表達，展現獨特自我"},
    2: {"hexagram": "坤", "name": "接收", "meaning": "接受正確方向的指引"},
    3: {"hexagram": "屯", "name": "秩序", "meaning": "在混亂中建立秩序"},
    4: {"hexagram": "蒙", "name": "公式化", "meaning": "透過邏輯找到答案"},
    5: {"hexagram": "需", "name": "等待", "meaning": "等待正確時機"},
    6: {"hexagram": "訟", "name": "摩擦", "meaning": "情緒的親密與衝突"},
    7: {"hexagram": "師", "name": "軍隊", "meaning": "領導力與自我角色"},
    8: {"hexagram": "比", "name": "貢獻", "meaning": "透過貢獻創造團結"},
    9: {"hexagram": "小畜", "name": "專注", "meaning": "專注於細節的力量"},
    10: {"hexagram": "履", "name": "行為", "meaning": "自我行為與愛自己"},
    11: {"hexagram": "泰", "name": "和平", "meaning": "新想法的和諧傳遞"},
    12: {"hexagram": "否", "name": "謹慎", "meaning": "謹慎表達的藝術"},
    13: {"hexagram": "同人", "name": "傾聽", "meaning": "傾聽與被聽見"},
    14: {"hexagram": "大有", "name": "權力技能", "meaning": "掌握權力的技巧"},
    15: {"hexagram": "謙", "name": "極端", "meaning": "在極端中找到平衡"},
    16: {"hexagram": "豫", "name": "技能", "meaning": "熱情驅動的技能"},
    17: {"hexagram": "隨", "name": "追隨", "meaning": "跟隨正確的意見"},
    18: {"hexagram": "蠱", "name": "修正", "meaning": "修正過去的模式"},
    19: {"hexagram": "臨", "name": "靠近", "meaning": "對他人需求敏感"},
    20: {"hexagram": "觀", "name": "當下", "meaning": "活在當下的覺察"},
    21: {"hexagram": "噬嗑", "name": "獵手", "meaning": "突破障礙的意志"},
    22: {"hexagram": "賁", "name": "優雅", "meaning": "情緒的優雅表達"},
    23: {"hexagram": "剝", "name": "分裂", "meaning": "將複雜化為簡單"},
    24: {"hexagram": "復", "name": "回歸", "meaning": "理性的回歸"},
    25: {"hexagram": "無妄", "name": "無我", "meaning": "無條件的愛與接受"},
    26: {"hexagram": "大畜", "name": "積蓄", "meaning": "累積力量的能力"},
    27: {"hexagram": "頤", "name": "滋養", "meaning": "滋養與被滋養"},
    28: {"hexagram": "大過", "name": "玩家", "meaning": "冒險求生的精神"},
    29: {"hexagram": "坎", "name": "承諾", "meaning": "說好的力量"},
    30: {"hexagram": "離", "name": "燃燒", "meaning": "渴望體驗的火焰"},
    31: {"hexagram": "咸", "name": "影響", "meaning": "民主領導的影響力"},
    32: {"hexagram": "恆", "name": "持續", "meaning": "持續適應變化"},
    33: {"hexagram": "遯", "name": "隱退", "meaning": "戰略性撤退"},
    34: {"hexagram": "大壯", "name": "力量", "meaning": "純粹強大的能量"},
    35: {"hexagram": "晉", "name": "進步", "meaning": "體驗帶來的進步"},
    36: {"hexagram": "明夷", "name": "危機", "meaning": "在黑暗中保持光明"},
    37: {"hexagram": "家人", "name": "友誼", "meaning": "家庭與社群的連結"},
    38: {"hexagram": "睽", "name": "反對", "meaning": "為真理而戰"},
    39: {"hexagram": "蹇", "name": "障礙", "meaning": "面對障礙的挑戰"},
    40: {"hexagram": "解", "name": "解放", "meaning": "從限制中解脫"},
    41: {"hexagram": "損", "name": "減少", "meaning": "收縮以成長"},
    42: {"hexagram": "益", "name": "增加", "meaning": "成長與擴展"},
    43: {"hexagram": "夬", "name": "突破", "meaning": "洞察力的突破"},
    44: {"hexagram": "姤", "name": "相遇", "meaning": "警覺的相遇"},
    45: {"hexagram": "萃", "name": "聚集", "meaning": "聚集資源的能力"},
    46: {"hexagram": "升", "name": "上升", "meaning": "決心的上升"},
    47: {"hexagram": "困", "name": "困境", "meaning": "在困境中領悟"},
    48: {"hexagram": "井", "name": "深度", "meaning": "深入知識的井"},
    49: {"hexagram": "革", "name": "革命", "meaning": "原則驅動的改變"},
    50: {"hexagram": "鼎", "name": "價值", "meaning": "守護核心價值"},
    51: {"hexagram": "震", "name": "震動", "meaning": "面對衝擊的力量"},
    52: {"hexagram": "艮", "name": "靜止", "meaning": "專注與靜止"},
    53: {"hexagram": "漸", "name": "發展", "meaning": "循序漸進的發展"},
    54: {"hexagram": "歸妹", "name": "野心", "meaning": "超越的野心"},
    55: {"hexagram": "豐", "name": "豐盛", "meaning": "情緒的豐盛"},
    56: {"hexagram": "旅", "name": "刺激", "meaning": "追求刺激的旅人"},
    57: {"hexagram": "巽", "name": "直覺", "meaning": "穿透性的直覺"},
    58: {"hexagram": "兌", "name": "喜悅", "meaning": "活力的喜悅"},
    59: {"hexagram": "渙", "name": "親密", "meaning": "瓦解障礙的親密"},
    60: {"hexagram": "節", "name": "限制", "meaning": "接受限制的智慧"},
    61: {"hexagram": "中孚", "name": "真理", "meaning": "內在真理的力量"},
    62: {"hexagram": "小過", "name": "細節", "meaning": "注意細節"},
    63: {"hexagram": "既濟", "name": "懷疑", "meaning": "邏輯性的懷疑"},
    64: {"hexagram": "未濟", "name": "困惑", "meaning": "接受困惑的壓力"}
}

HUMAN_DESIGN_DATA = {
    "type": "生產者",
    "profile": "3/5 烈士/異端",
    "info": {
        "color": "#ff6b6b",
        "desc": "世界的建設者，擁有持久的生命力能量",
        "strategy": "等待回應",
        "icon": "⚡"
    },
    "centers": {
        "頭腦": {"defined": False, "color": "#f1c40f", "desc": "靈感與壓力"},
        "邏輯": {"defined": True, "color": "#2ecc71", "desc": "思考與概念化"},
        "喉嚨": {"defined": True, "color": "#3498db", "desc": "表達與行動"},
        "G中心": {"defined": True, "color": "#f1c40f", "desc": "身份與方向"},
        "意志力": {"defined": False, "color": "#e74c3c", "desc": "自我價值"},
        "情緒": {"defined": True, "color": "#9b59b6", "desc": "情緒波動"},
        "薦骨": {"defined": True, "color": "#e74c3c", "desc": "生命力能量"},
        "脾": {"defined": False, "color": "#1abc9c", "desc": "直覺與健康"},
        "根": {"defined": True, "color": "#e67e22", "desc": "壓力與動力"}
    }
}

ASTROLOGY_DATA = {
    "sun": "♑ 摩羯座",
    "ascendant": "♌ 獅子座",
    "planets": {
        "☉ 太陽": "♑ 摩羯座",
        "☽ 月亮": "♋ 巨蟹座",
        "☿ 水星": "♐ 射手座",
        "♀ 金星": "♒ 水瓶座",
        "♂ 火星": "♈ 牡羊座",
        "♃ 木星": "♎ 天秤座",
        "♄ 土星": "♑ 摩羯座"
    }
}

ZIWEI_DATA = {
    "main_star": "紫微",
    "mingzhu": "貪狼",
    "shenzhu": "天機",
    "palaces": {
        "命宮": "紫微", "兄弟宮": "天機", "夫妻宮": "太陽", "子女宮": "武曲",
        "財帛宮": "天同", "疾厄宮": "廉貞", "遷移宮": "天府", "交友宮": "太陰",
        "官祿宮": "貪狼", "田宅宮": "巨門", "福德宮": "天相", "父母宮": "天梁"
    }
}

AI_INTEGRATION_RESPONSE = """
## 核心訊息
從塔羅的命運之輪、八字的甲木日主、人類圖的生產者類型來看，您正處於人生的重要轉折點。

## 各系統獨特觀點
- **塔羅**: 星星牌顯示希望與療癒
- **八字**: 甲木生於丑月，需要火來暖局
- **人類圖**: 作為生產者，需要等待回應
- **占星**: 摩羯太陽+獅子上升，外表自信但內心務實
- **紫微**: 紫微坐命，天生具有領導格局

## 綜合建議
1. 把握 2026 年機會
2. 等待而非追求
3. 發揮領導特質
"""


def get_default_interpretation(day_gan):
    wuxing_map = {'甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土', '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'}
    traits = {'甲': '開拓進取、領導力強', '乙': '溫和細膩、善於協調', '丙': '熱情開朗、光明磊落', '丁': '溫暖體貼、注重細節', '戊': '穩重踏實、包容力強', '己': '細心謹慎、善於經營', '庚': '剛毅果斷、重義氣', '辛': '細緻優雅、有原則', '壬': '聰明靈活、適應力強', '癸': '智慧敏銳、洞察力佳'}
    wuxing = wuxing_map.get(day_gan, '木')
    trait = traits.get(day_gan, '獨特')
    return f"## 日主分析\n{day_gan}日主，五行屬{wuxing}。\n\n## 性格特質\n日主{day_gan}的人通常具有{trait}的特質。\n\n## 運勢建議\n根據命盤格局，建議把握機會、穩紮穩打。"


# ========== AI Helper with Multi-Model Fallback ==========

# 模型優先順序列表（從快到慢、從節省到精確）
GEMINI_MODELS = [
    "gemini-2.5-flash",           # 2.5 flash - 目前可用
    "gemini-2.0-flash-lite",      # 2.0 flash lite - 輕量版
    "gemini-1.5-flash",           # 1.5 flash 穩定版
    "gemini-1.5-pro",             # 專業版 - 邏輯較強
]

# 取得所有可用的 API Keys
def get_api_keys():
    """取得所有設定的 API Keys"""
    # 優先使用逗號分隔的多 Key 格式
    keys_str = os.getenv("GOOGLE_API_KEYS", "")
    if keys_str:
        keys = [k.strip() for k in keys_str.split(",") if k.strip()]
        if keys:
            return keys
    # 向後相容單一 Key 格式
    single_key = os.getenv("GOOGLE_API_KEY", "")
    if single_key:
        return [single_key]
    return []

# 記錄當前可用的模型和 API Key 索引
_current_model_index = 0
_current_key_index = 0


def generate_ai_content(prompt, fallback_text=""):
    """
    使用 Gemini AI 生成內容，支援多模型和多 API Key 自動切換
    
    Args:
        prompt: AI 提示詞
        fallback_text: 當所有模型都失敗時的備用文字
        
    Returns:
        tuple: (生成的文字, 使用的模型名稱或None)
    """
    global _current_model_index, _current_key_index
    
    api_keys = get_api_keys()
    if not api_keys:
        print("❌ 沒有設定任何 API Key")
        return fallback_text, None
    
    try:
        import google.generativeai as genai
    except ImportError:
        print("❌ 無法匯入 google.generativeai")
        return fallback_text, None
    
    # 計算最大嘗試次數 = API Keys 數量 × 模型數量
    max_attempts = len(api_keys) * len(GEMINI_MODELS)
    attempts = 0
    
    while attempts < max_attempts:
        current_key = api_keys[_current_key_index]
        model_name = GEMINI_MODELS[_current_model_index]
        
        try:
            genai.configure(api_key=current_key)
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            
            if response and response.text:
                key_preview = current_key[:10] + "..."
                print(f"✅ AI 生成成功 (Key: {key_preview}, 模型: {model_name})")
                return response.text, model_name
                
        except Exception as e:
            error_msg = str(e).lower()
            key_preview = current_key[:10] + "..."
            
            # 判斷是否為配額/速率限制錯誤
            if "quota" in error_msg or "rate" in error_msg or "resource" in error_msg or "exhausted" in error_msg:
                print(f"⚠️ Key {key_preview} + 模型 {model_name} 配額已滿，切換...")
                
                # 先換模型，模型用完再換 Key
                _current_model_index = (_current_model_index + 1) % len(GEMINI_MODELS)
                if _current_model_index == 0:
                    # 所有模型都試過了，換下一個 Key
                    _current_key_index = (_current_key_index + 1) % len(api_keys)
                    print(f"🔄 切換到下一個 API Key...")
            else:
                # 其他錯誤，也嘗試切換
                print(f"⚠️ Key {key_preview} + 模型 {model_name} 發生錯誤: {str(e)[:50]}...")
                _current_model_index = (_current_model_index + 1) % len(GEMINI_MODELS)
                if _current_model_index == 0:
                    _current_key_index = (_current_key_index + 1) % len(api_keys)
        
        attempts += 1
    
    # 所有組合都失敗，重置索引並返回備用文字
    _current_model_index = 0
    _current_key_index = 0
    print(f"❌ 所有 API Key 和模型都無法使用，返回預設內容")
    return fallback_text, None


# ========== Line (爻) Explanation Cache and Generator ==========

# 爻解釋快取 (避免重複呼叫 AI)
_line_explanation_cache = {}

def get_line_explanation(gate_num: int, line_num: int, gate_info: dict) -> str:
    """
    獲取特定閘門和爻的解釋
    
    Args:
        gate_num: 閘門號碼 (1-64)
        line_num: 爻號碼 (1-6)
        gate_info: 閘門的基本資訊 (hexagram, name, meaning 等)
        
    Returns:
        str: 爻的解釋文字
    """
    cache_key = f"{gate_num}.{line_num}"
    
    # 檢查快取
    if cache_key in _line_explanation_cache:
        return _line_explanation_cache[cache_key]
    
    # 爻的基本含義 (傳統易經爻辭)
    line_meanings = {
        1: "初爻 - 潛龍勿用，事物的開端，蓄勢待發",
        2: "二爻 - 見龍在田，開始展現，與人連結",
        3: "三爻 - 終日乾乾，努力奮鬥，面臨考驗",
        4: "四爻 - 或躍在淵，轉折關鍵，進退皆可",
        5: "五爻 - 飛龍在天，達到高峰，發揮影響",
        6: "上爻 - 亢龍有悔，功成身退，智慧傳承"
    }
    
    hexagram = gate_info.get("hexagram", "")
    gate_name = gate_info.get("name", "")
    meaning = gate_info.get("meaning", "")
    
    # 使用 AI 生成爻的解釋
    prompt = f"""你是一位專精人類圖與易經的導師。請根據以下資訊，用繁體中文為這個特定的爻提供簡短但深刻的解釋：

閘門 {gate_num}：{hexagram}卦 · {gate_name}
核心意義：{meaning}
爻位置：第 {line_num} 爻 ({line_meanings.get(line_num, '')})

請提供：
1. 這個爻在此閘門中的特殊意義（30字內）
2. 生活中如何展現這個能量（40字內）

格式要簡潔，直接給出內容，不要標題。總共不超過80字。"""

    fallback = f"第{line_num}爻：{line_meanings.get(line_num, '這個爻代表特定的能量階段。')}"
    
    explanation, _ = generate_ai_content(prompt, fallback)
    
    # 儲存到快取
    _line_explanation_cache[cache_key] = explanation
    
    return explanation


# ========== API Endpoints ==========

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Spiritual AI Advisor API is running"})


@app.route('/api/humandesign/line-explanation', methods=['POST'])
def get_gate_line_explanation():
    """獲取特定閘門和爻的 AI 解釋"""
    data = request.json or {}
    gate_num = data.get('gateNum')
    line_num = data.get('line')
    gate_info = data.get('gateInfo', {})
    
    if not gate_num or not line_num:
        return jsonify({"success": False, "error": "Missing gateNum or line"}), 400
    
    try:
        explanation = get_line_explanation(int(gate_num), int(line_num), gate_info)
        return jsonify({
            "success": True,
            "gateNum": gate_num,
            "line": line_num,
            "explanation": explanation
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/tarot/draw', methods=['POST'])
def draw_tarot():
    count = request.json.get('count', 3) if request.json else 3
    drawn_cards = random.sample(MAJOR_ARCANA, min(count, len(MAJOR_ARCANA)))
    
    result = []
    for card in drawn_cards:
        is_reversed = random.choice([True, False])
        result.append({
            "name": card["name"],
            "id": card["id"],
            "reversed": is_reversed,
            "imageUrl": f"https://www.sacred-texts.com/tarot/pkt/img/{card['id']}.jpg",
            "upright": card.get("upright", ""),
            "reversedMeaning": card.get("reversed", ""),
            "meaning": card.get("meaning", ""),
            "keywords": card.get("reversed" if is_reversed else "upright", "")
        })
    
    return jsonify({"success": True, "cards": result, "positions": ["過去", "現在", "未來"][:count]})


@app.route('/api/tarot/cards', methods=['GET'])
def get_tarot_cards():
    return jsonify({"success": True, "cards": MAJOR_ARCANA})


@app.route('/api/bazi/calculate', methods=['POST'])
def calculate_bazi():
    from lunar_python import Solar
    
    data = request.json or {}
    birth_date = data.get('birthDate', '1990-01-31')
    birth_hour = data.get('birthHour', 3)
    
    HOUR_MAP = [23, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
    
    try:
        year, month, day = map(int, birth_date.split('-'))
        hour = HOUR_MAP[birth_hour % 12]
    except:
        year, month, day, hour = 1990, 1, 31, 5
    
    try:
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        lunar = solar.getLunar()
        bazi = lunar.getEightChar()
        
        year_gan, year_zhi = bazi.getYearGan(), bazi.getYearZhi()
        month_gan, month_zhi = bazi.getMonthGan(), bazi.getMonthZhi()
        day_gan, day_zhi = bazi.getDayGan(), bazi.getDayZhi()
        hour_gan, hour_zhi = bazi.getTimeGan(), bazi.getTimeZhi()
        
        lunar_str = f"{lunar.getYearInGanZhi()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}"
        
        current_year = datetime.now().year
        liunian = []
        for i in range(6):
            y = current_year + i
            y_solar = Solar.fromYmd(y, 6, 1)
            y_ganzhi = y_solar.getLunar().getYearInGanZhi()
            score = 5.0 + random.uniform(0, 4)
            if y_ganzhi[0] == day_gan:
                score += 0.5
            liunian.append({"year": y, "ganzhi": y_ganzhi, "score": round(min(score, 10), 1)})
        
        prompt = f"作為專業的八字命理師，請根據以下八字命盤提供簡短但專業的分析：\n\n八字命盤：\n年柱：{year_gan}{year_zhi}\n月柱：{month_gan}{month_zhi}\n日柱：{day_gan}{day_zhi}（日主）\n時柱：{hour_gan}{hour_zhi}\n\n農曆：{lunar_str}\n\n請提供：\n1. 日主分析（50字內）\n2. 五行強弱（50字內）\n3. 性格特質（80字內）\n4. 今年運勢建議（80字內）\n\n請用繁體中文回答，格式簡潔。"
        
        fallback = get_default_interpretation(day_gan)
        interpretation, model_used = generate_ai_content(prompt, fallback)
        
        return jsonify({
            "success": True, "birthDate": birth_date, "birthHour": birth_hour, "lunar": lunar_str,
            "year_gan": year_gan, "year_zhi": year_zhi, "month_gan": month_gan, "month_zhi": month_zhi,
            "day_gan": day_gan, "day_zhi": day_zhi, "hour_gan": hour_gan, "hour_zhi": hour_zhi,
            "day_master": day_gan, "liunian": liunian, "interpretation": interpretation
        })
        
    except Exception:
        return jsonify({"success": False, "error": "八字計算服務暫時無法使用，請稍後再試。"}), 500


@app.route('/api/humandesign/calculate', methods=['POST'])
def calculate_human_design():
    """計算人類圖 - 專業版本，包含閘門、通道、行星位置"""
    data = request.json or {}
    birth_date = data.get('birthDate', '1990-01-31')
    birth_time = data.get('birthTime', '12:00')
    
    try:
        # 輸入時間轉換
        birth_datetime_local = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
        # 假設輸入為台灣時間 (UTC+8)，轉換為 UTC
        # ephem 預設使用 UTC
        birth_datetime = birth_datetime_local - timedelta(hours=8)
    except ValueError:
        return jsonify({"success": False, "error": "無效的日期或時間格式"}), 400

    # 使用 ephem 進行天文計算
    data = request.json or {}
    birth_lat = data.get('birthLat', 25.0330)
    birth_lon = data.get('birthLon', 121.5654)
    
    observer = ephem.Observer()
    observer.date = birth_datetime
    observer.lat = str(birth_lat)
    observer.lon = str(birth_lon)
    observer.elevation = 0

    # 1. 計算 Personality (意識) 行星位置
    # 定義行星物件
    sun = ephem.Sun()
    moon = ephem.Moon()
    mercury = ephem.Mercury()
    venus = ephem.Venus()
    mars = ephem.Mars()
    jupiter = ephem.Jupiter()
    saturn = ephem.Saturn()
    uranus = ephem.Uranus()
    neptune = ephem.Neptune()
    pluto = ephem.Pluto()
    
    # 計算 Personality 時刻的位置
    planets_list = [sun, moon, mercury, venus, mars, jupiter, saturn, uranus, neptune, pluto]
    for p in planets_list:
        p.compute(observer)
    
    # 取得太陽黃經 (用於計算 Design 日期)
    p_sun_lon =  math.degrees(sun.hlon)
    
    # 計算交點 (Mean Node - ephem 沒有 True Node，通常 HD 用 True Node 但 Mean Node 差異不大，這裡用模擬算法近似或尋找 True Node 算法)
    # ephem 只有 Mean Node? ephem 有 next_pass 等，但沒有直接的 Node 物件?
    # 修正: ephem 沒有直接的 Node 物件。需要用特定算法。
    # 為了簡化且不依賴過多外部庫，我們使用近似算法或 ephem 的擴充。
    # 這裡暫時用簡單算法模擬交點，或尋找更準確的方式。
    # 其實 ephem 可以計算月亮軌道交點。
    # 為了保持進度，我們先用一個簡單的交點計算函數 (基於天文算法)。
    
    def get_nodes(jd):
        # 簡單的 Mean Node 計算
        t = (jd - 2451545.0) / 36525.0
        node_lon = 125.04452 - 1934.136261 * t + 0.0020708 * t * t + t * t * t / 450000.0
        return node_lon % 360

    p_north_node_lon = get_nodes(ephem.julian_date(observer.date))
    p_south_node_lon = (p_north_node_lon + 180) % 360

    # 2. 計算 Design (潛意識) 日期
    # 太陽倒退 88 度
    target_sun_lon = (p_sun_lon - 88) % 360
    
    # 尋找 Design 日期 (二分搜尋法)
    # 太陽一天約走 1 度，所以大約 88 天前
    d_date_approx = birth_datetime - timedelta(days=88)
    observer_d = ephem.Observer()
    observer_d.date = d_date_approx
    
    # 微調找到精確時刻
    for _ in range(5): # 迭代幾次逼近
        sun.compute(observer_d)
        curr_lon = math.degrees(sun.hlon)
        diff = target_sun_lon - curr_lon
        # 處理跨越 0/360 度的問題
        if diff > 180: diff -= 360
        if diff < -180: diff += 360
        
        # 太陽每日約 0.9856 度
        days_corr = diff / 0.9856
        observer_d.date = ephem.Date(observer_d.date + days_corr)
    
    design_date = observer_d.date

    # 計算 Design 時刻的行星位置
    d_planets_list = [ephem.Sun(), ephem.Moon(), ephem.Mercury(), ephem.Venus(), ephem.Mars(), 
                      ephem.Jupiter(), ephem.Saturn(), ephem.Uranus(), ephem.Neptune(), ephem.Pluto()]
    for p in d_planets_list:
        p.compute(observer_d)
        
    d_north_node_lon = get_nodes(ephem.julian_date(observer_d.date))
    d_south_node_lon = (d_north_node_lon + 180) % 360
    
    # 整合行星數據
    # 格式: (符號, 名稱, P_Longitude, D_Longitude)
    # 對應: 太陽, 地球, 月亮, 北交, 南交, 水, 金, 火, 木, 土, 天, 海, 冥
    
    # 地球位置 = 太陽位置 + 180
    p_earth_lon = (p_sun_lon + 180) % 360
    d_earth_lon = (math.degrees(d_planets_list[0].hlon) + 180) % 360
    
    planet_data_map = [
        ("☉", "太陽", p_sun_lon, math.degrees(d_planets_list[0].hlon)),
        ("⊕", "地球", p_earth_lon, d_earth_lon),
        ("☽", "月亮", math.degrees(moon.hlon), math.degrees(d_planets_list[1].hlon)),
        ("☊", "北交點", p_north_node_lon, d_north_node_lon),
        ("☋", "南交點", p_south_node_lon, d_south_node_lon),
        ("☿", "水星", math.degrees(mercury.hlon), math.degrees(d_planets_list[2].hlon)),
        ("♀", "金星", math.degrees(venus.hlon), math.degrees(d_planets_list[3].hlon)),
        ("♂", "火星", math.degrees(mars.hlon), math.degrees(d_planets_list[4].hlon)),
        ("♃", "木星", math.degrees(jupiter.hlon), math.degrees(d_planets_list[5].hlon)),
        ("♄", "土星", math.degrees(saturn.hlon), math.degrees(d_planets_list[6].hlon)),
        ("⛢", "天王星", math.degrees(uranus.hlon), math.degrees(d_planets_list[7].hlon)),
        ("♆", "海王星", math.degrees(neptune.hlon), math.degrees(d_planets_list[8].hlon)),
        ("♇", "冥王星", math.degrees(pluto.hlon), math.degrees(d_planets_list[9].hlon))
    ]

    design_planets = {}
    personality_planets = {}
    all_gates = set()
    defined_centers = set()
    
    # 通道狀態追蹤
    active_gates = set() # 存儲所有激活的閘門 (int)
    
    for symbol, name, p_lon, d_lon in planet_data_map:
        # 計算 Design 閘門
        d_gate_info = get_gate_from_longitude(d_lon)
        d_gate_num = d_gate_info["gate"]
        d_line = d_gate_info["line"]
        d_gate_str = d_gate_info["str"]
        
        # 計算 Personality 閘門
        p_gate_info = get_gate_from_longitude(p_lon)
        p_gate_num = p_gate_info["gate"]
        p_line = p_gate_info["line"]
        p_gate_str = p_gate_info["str"]
        
        all_gates.add(d_gate_num)
        all_gates.add(p_gate_num)
        active_gates.add(d_gate_num)
        active_gates.add(p_gate_num)
        
        # 獲取易經解釋
        d_iching = GATES_ICHING_DETAILED.get(d_gate_num, GATES_ICHING.get(d_gate_num, {}))
        p_iching = GATES_ICHING_DETAILED.get(p_gate_num, GATES_ICHING.get(p_gate_num, {}))
        
        # 爻名稱對照
        line_names = {1: "初爻", 2: "二爻", 3: "三爻", 4: "四爻", 5: "五爻", 6: "上爻"}

        design_planets[symbol] = {
            "gate": d_gate_str,
            "gateNum": d_gate_num,
            "line": d_line,
            "lineName": line_names.get(d_line, ""),
            "name": name,
            "hexagram": d_iching.get("hexagram", ""),
            "gateName": d_iching.get("name", ""),
            "meaning": d_iching.get("meaning", ""),
            "description": d_iching.get("description", ""),
            "gift": d_iching.get("gift", ""),
            "shadow": d_iching.get("shadow", ""),
            "advice": d_iching.get("advice", "")
        }
        
        personality_planets[symbol] = {
            "gate": p_gate_str,
            "gateNum": p_gate_num,
            "line": p_line,
            "lineName": line_names.get(p_line, ""),
            "name": name,
            "hexagram": p_iching.get("hexagram", ""),
            "gateName": p_iching.get("name", ""),
            "meaning": p_iching.get("meaning", ""),
            "description": p_iching.get("description", ""),
            "gift": p_iching.get("gift", ""),
            "shadow": p_iching.get("shadow", ""),
            "advice": p_iching.get("advice", "")
        }

    # 3. 計算通道和定義中心
    
    channels = []
    channels_detail = []
    open_channels = [] # 開放通道 (懸掛閘門)
    open_channels_detail = []
    
    # 檢查所有通道
    filled_channels = []
    
    for g1, g2, name, c_type in CHANNELS_LIST:
        has_g1 = g1 in active_gates
        has_g2 = g2 in active_gates
        channel_key = f"{g1}-{g2}" if g1 < g2 else f"{g2}-{g1}"
        
        # 獲取通道詳細資料
        c_detail = CHANNELS_DATA.get(channel_key, {})
        c_name = c_detail.get("name", name)
        c_centers = c_detail.get("centers", [])
        
        if has_g1 and has_g2:
            # 定義通道
            channels.append(channel_key)
            filled_channels.append((g1, g2))
            
            # 標記中心為定義
            if g1 in GATE_TO_CENTER: defined_centers.add(GATE_TO_CENTER[g1])
            if g2 in GATE_TO_CENTER: defined_centers.add(GATE_TO_CENTER[g2])
            
            # 加入詳細資料
            defined_info = c_detail.get("defined", {})
            channels_detail.append({
                "channel": channel_key,
                "name": c_name,
                "centers": c_centers,
                "type": c_detail.get("type", c_type),
                "meaning": defined_info.get("meaning", ""),
                "description": defined_info.get("description", ""),
                "gift": defined_info.get("gift", ""),
                "advice": defined_info.get("advice", "")
            })
            
        elif has_g1 or has_g2:
            # 開放通道 (只有一個閘門)
            hanging = g1 if has_g1 else g2
            open_channels.append(channel_key)
            
            open_info = c_detail.get("open", {})
            open_channels_detail.append({
                "channel": channel_key,
                "name": c_name,
                "centers": c_centers,
                "status": "開放",
                "hangingGate": hanging,
                "wisdom": open_info.get("wisdom", ""),
                "challenge": open_info.get("challenge", "")
            })

    # 4. 判斷類型 (Type) 和權威 (Authority)
    # 必須根據定義的中心來判斷
    
    has_sacral = "Sacral" in defined_centers
    has_motor_to_throat = False
    
    # 檢查是否有馬達中心 (Sacral, Root, Solar, Heart) 連接到喉嚨
    # 需要檢查路徑... 這裡簡化判斷: 檢查是否有連接喉嚨的定義通道，且該通道另一端連接著馬達中心
    # 或是馬達中心經由定義通道鏈接到喉嚨 (這比較複雜，需要圖演算法)
    # 簡化算法: 檢查是否有直接連接喉嚨的馬達通道
    
    motor_centers = ["Sacral", "Solar", "Root", "Heart"]
    connected_to_throat = set()
    
    # 建立連接圖
    graph = {center: [] for center in set(GATE_TO_CENTER.values())}
    for g1, g2 in filled_channels:
        c1 = GATE_TO_CENTER.get(g1)
        c2 = GATE_TO_CENTER.get(g2)
        if c1 and c2:
            graph[c1].append(c2)
            graph[c2].append(c1)
            
    # BFS 檢查馬達是否連接到喉嚨
    def check_connection(start_centers, target="Throat"):
        queue = list(start_centers)
        visited = set(start_centers)
        while queue:
            curr = queue.pop(0)
            if curr == target:
                return True
            for neighbor in graph.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False
        
    # 找出已定義的馬達中心
    defined_motors = [m for m in motor_centers if m in defined_centers]
    if defined_motors:
        has_motor_to_throat = check_connection(defined_motors, "Throat")
        
    # 類型判斷
    hd_type = ""
    strategy = ""
    not_self = ""
    
    if has_sacral:
        # 生產者或顯示生產者
        if has_motor_to_throat: # 實際上顯示生產者是有喉嚨連接到馬達(薦骨是馬達之一)
             # 若薦骨有定義，且有馬達通喉嚨 => 顯示生產者 (MG)
             # 但嚴格來說，MG 是薦骨定義 + (薦骨通喉嚨 或 其他馬達通喉嚨)
             hd_type = "顯示生產者 (Manifesting Generator)"
        else:
            hd_type = "生產者 (Generator)"
        strategy = "等待回應"
        not_self = "挫敗感"
        
    elif has_motor_to_throat:
        # 顯示者 (無薦骨，有馬達通喉嚨)
        hd_type = "顯示者 (Manifestor)"
        strategy = "告知後行動"
        not_self = "憤怒"
        
    elif len(defined_centers) > 0:
        # 投射者 (無薦骨，無馬達通喉嚨，有定義中心)
        hd_type = "投射者 (Projector)"
        strategy = "等待被邀請"
        not_self = "苦澀"
        
    else:
        # 反映者 (無定義中心)
        hd_type = "反映者 (Reflector)"
        strategy = "等待一個月亮週期 (28天)"
        not_self = "失望"

    # 權威判斷 (Hierarchy of Authority)
    authority = ""
    if "Solar" in defined_centers:
        authority = "情緒型權威 (Solar Plexus)"
    elif "Sacral" in defined_centers:
        authority = "薦骨型權威 (Sacral)"
    elif "Spleen" in defined_centers:
        authority = "直覺型權威 (Splenic)"
    elif "Heart" in defined_centers:
        authority = "意志力型權威 (Ego/Heart)" # 需要區分 Ego Projected vs Ego Manifested
        # 如果喉嚨連接心臟 => Ego Manifested
        # 如果沒有 => Ego Projected
        if check_connection(["Heart"], "Throat"):
             authority = "意志力顯示型權威"
        else:
             authority = "意志力投射型權威"
    elif "G" in defined_centers:
        authority = "自我投射型權威 (Self-Projected)"
    elif "Ajna" in defined_centers or "Head" in defined_centers: # 實際上只有定義到喉嚨才算? Environment/Mental 不需要定義喉嚨? 
        # Mental Projector: Ajna/Head defined, no motors, no throat connection below G?
        authority = "無內在權威 (環境/心智型)"
    else:
        authority = "無內在權威 (月亮型 - 反映者)"

    # 人生角色 (Profile)
    # 基於 Personality Sun Line / Design Sun Line
    p_sun_line = personality_planets["☉"]["gate"].split('.')[1]
    d_sun_line = design_planets["☉"]["gate"].split('.')[1]
    profile = f"{p_sun_line}/{d_sun_line}"

    # 定義類型 (Definition)
    # Single, Split, Triple Split, Quadruple Split
    # 需要檢查連通分量
    if not defined_centers:
        definition = "無定義"
    else:
        # 計算連通分量
        defined_list = list(defined_centers)
        visited = set()
        components = 0
        
        for center in defined_list:
            if center not in visited:
                components += 1
                # BFS 標記所有連通的中心
                q = [center]
                visited.add(center)
                while q:
                    c = q.pop(0)
                    for neighbor in graph.get(c, []):
                        if neighbor in defined_list and neighbor not in visited:
                            visited.add(neighbor)
                            q.append(neighbor)
                            
        if components == 1:
            definition = "一分人 (Single Definition)"
        elif components == 2:
            definition = "二分人 (Split Definition)"
        elif components == 3:
            definition = "三分人 (Triple Split Definition)"
        elif components == 4:
            definition = "四分人 (Quadruple Split Definition)"
        else:
            definition = "未知"

    # 構建定義中心資料
    centers_data = {}
    all_centers_list = ["Head", "Ajna", "Throat", "G", "Heart", "Sacral", "Spleen", "Solar", "Root"]
    
    # 中心顏色對照
    center_colors = {
        "Head": "yellow-400", "Ajna": "green-400", "Throat": "orange-400",
        "G": "yellow-500", "Heart": "red-500", "Sacral": "red-600",
        "Spleen": "orange-300", "Solar": "orange-500", "Root": "orange-700"
    }# 實際顏色應根據標準圖修正，這裡暫用示範色
    
    for c in all_centers_list:
        is_defined = c in defined_centers
        centers_data[c] = {
            "defined": is_defined,
            "gates": [g for g in all_gates if GATE_TO_CENTER.get(g) == c]
        }
    
    # AI 解讀
    prompt = f"""作為專業人類圖分析師，請針對以下個人人類圖表提供一份詳盡且深入的綜合分析報告。請不要只是一句簡短的總結，而是要整合所有資訊，提供使用者實際且具深度的生活指導。

出生時間：{birth_date} {birth_time}
類型：{hd_type} ({strategy})
人生角色：{profile}
內在權威：{authority}
定義類型：{definition}
非自我主題：{not_self}

主要定義通道：{", ".join(channels)}
定義中心：{", ".join(list(defined_centers))}

請撰寫一份約 800-1000 字的完整分析，包含以下章節：

### 1. 核心能量類型與人生策略
詳細解釋「{hd_type}」的運作機制，以及如何於日常生活中落實「{strategy}」。非自我主題「{not_self}」通常在什麼情況下出現，如何覺察並回到正軌。

### 2. 內在權威指引
深入說明「{authority}」的運作方式。在做重大決定時，具體應該如何聆聽或觀察這個權威的訊號？請舉例說明。

### 3. 人生角色深度解析
針對「{profile}」提供性格分析。意識與潛意識的數字如何交互作用？在人際關係與自我實踐上的優勢與挑戰為何？

### 4. 能量中心與通道整合分析
綜合分析已定義的中心與通道（{", ".join(channels)}）。這些天賦如何互相配合？有哪些特定的才華或原廠設定是使用者應該善用的？（請挑選最重要的 2-3 個特質深入解說）

### 5. 給予當下的生活建議與覺察練習
給予使用者 3 個具體可行的生活建議，幫助他們活出自己原本的設計。

請用繁體中文，語氣溫暖、賦能且專業。請確保內容結構清晰，分段良好。"""

    fallback = f"您是{hd_type}，策略是{strategy}。擁有{authority}，人生角色為{profile}。這張圖表顯示了您獨特的能量運作方式。"
    
    # 調用 AI
    interpretation, _ = generate_ai_content(prompt, fallback)
    
    # 建立回應資料
    hd_data = {
        "type": hd_type,
        "profile": profile,
        "authority": authority,
        "definition": definition,
        "strategy": strategy,
        "notSelfTheme": not_self,
        "design": design_planets,
        "personality": personality_planets,
        "centers": centers_data,
        "channels": channels,
        "channelsDetail": channels_detail,
        "openChannels": open_channels,
        "openChannelsDetail": open_channels_detail,
        "gates": list(all_gates),
        "info": {
            "color": "bg-slate-700", # 前端會處理顏色
            "desc": f"類型: {hd_type} | 權威: {authority}",
            "strategy": strategy,
            "icon": "🔮"
        }
    }

    return jsonify({
        "success": True, 
        **hd_data, 
        "interpretation": interpretation
    })


@app.route('/api/humandesign/info', methods=['GET'])
def get_human_design():
    """取得人類圖資訊 (Demo)"""
    return jsonify({"success": True, **HUMAN_DESIGN_DATA, "interpretation": "請輸入出生資料以獲取個人化分析"})


@app.route('/api/astrology/calculate', methods=['POST'])
def calculate_astrology():
    """計算占星盤 - 使用 Kerykeion (Swiss Ephemeris) 精確計算"""
    from kerykeion import AstrologicalSubject
    import warnings
    warnings.filterwarnings("ignore")
    
    data = request.json or {}
    birth_date = data.get('birthDate', '1990-01-31')
    birth_time = data.get('birthTime', '12:00')
    birth_lat = data.get('birthLat', 25.0169)
    birth_lon = data.get('birthLon', 121.4628)
    birth_city = data.get('birthCity', '新北市')
    
    try:
        year, month, day = map(int, birth_date.split('-'))
        hour, minute = map(int, birth_time.split(':'))
    except:
        year, month, day, hour, minute = 1990, 1, 31, 12, 0
    
    # 星座中英對照
    sign_cn = {
        "Ari": "牡羊座", "Tau": "金牛座", "Gem": "雙子座", "Can": "巨蟹座",
        "Leo": "獅子座", "Vir": "處女座", "Lib": "天秤座", "Sco": "天蠍座",
        "Sag": "射手座", "Cap": "摩羯座", "Aqu": "水瓶座", "Pis": "雙魚座"
    }
    
    zodiac_data = {
        "牡羊座": {"symbol": "♈", "element": "火", "modality": "開創", "polarity": "陽", "ruler": "火星"},
        "金牛座": {"symbol": "♉", "element": "土", "modality": "固定", "polarity": "陰", "ruler": "金星"},
        "雙子座": {"symbol": "♊", "element": "風", "modality": "變動", "polarity": "陽", "ruler": "水星"},
        "巨蟹座": {"symbol": "♋", "element": "水", "modality": "開創", "polarity": "陰", "ruler": "月亮"},
        "獅子座": {"symbol": "♌", "element": "火", "modality": "固定", "polarity": "陽", "ruler": "太陽"},
        "處女座": {"symbol": "♍", "element": "土", "modality": "變動", "polarity": "陰", "ruler": "水星"},
        "天秤座": {"symbol": "♎", "element": "風", "modality": "開創", "polarity": "陽", "ruler": "金星"},
        "天蠍座": {"symbol": "♏", "element": "水", "modality": "固定", "polarity": "陰", "ruler": "冥王星"},
        "射手座": {"symbol": "♐", "element": "火", "modality": "變動", "polarity": "陽", "ruler": "木星"},
        "摩羯座": {"symbol": "♑", "element": "土", "modality": "開創", "polarity": "陰", "ruler": "土星"},
        "水瓶座": {"symbol": "♒", "element": "風", "modality": "固定", "polarity": "陽", "ruler": "天王星"},
        "雙魚座": {"symbol": "♓", "element": "水", "modality": "變動", "polarity": "陰", "ruler": "海王星"}
    }
    
    # 使用 Kerykeion 計算
    try:
        subject = AstrologicalSubject(
            "User", year, month, day, hour, minute,
            birth_city, "TW", lng=birth_lon, lat=birth_lat
        )
    except Exception as e:
        return jsonify({"success": False, "error": f"計算錯誤: {str(e)}"})
    
    # 行星列表
    planet_objs = [
        ("太陽", subject.sun),
        ("月亮", subject.moon),
        ("水星", subject.mercury),
        ("金星", subject.venus),
        ("火星", subject.mars),
        ("木星", subject.jupiter),
        ("土星", subject.saturn),
        ("天王星", subject.uranus),
        ("海王星", subject.neptune),
        ("冥王星", subject.pluto)
    ]
    
    planet_positions = {}
    planets_display = {}
    
    for name_cn, p in planet_objs:
        sign_abbr = p.sign
        sign_name = sign_cn.get(sign_abbr, sign_abbr)
        z_data = zodiac_data.get(sign_name, {})
        retro = p.retrograde if hasattr(p, 'retrograde') else False
        
        # 計算絕對度數
        sign_order = list(sign_cn.values())
        sign_idx = sign_order.index(sign_name) if sign_name in sign_order else 0
        abs_degree = sign_idx * 30 + p.position
        
        planet_positions[name_cn] = {
            "sign": sign_name,
            "symbol": z_data.get("symbol", ""),
            "degree": p.position,
            "abs_degree": abs_degree,
            "element": z_data.get("element", ""),
            "modality": z_data.get("modality", ""),
            "polarity": z_data.get("polarity", ""),
            "retrograde": retro
        }
        
        retro_mark = " R" if retro else ""
        planets_display[name_cn] = f"{z_data.get('symbol', '')} {sign_name} {p.position:.2f}°{retro_mark}"
    
    # 上升星座
    asc_sign = sign_cn.get(subject.first_house.sign, subject.first_house.sign)
    asc_degree = subject.first_house.position
    asc_z_data = zodiac_data.get(asc_sign, {})
    sign_order = list(sign_cn.values())
    asc_idx = sign_order.index(asc_sign) if asc_sign in sign_order else 0
    asc_abs = asc_idx * 30 + asc_degree
    
    asc_info = {
        "name": asc_sign,
        "degree": asc_degree,
        "abs_degree": asc_abs,
        "ruler": asc_z_data.get("ruler", "")
    }
    
    # MC (中天/第10宮尖端)
    mc_sign = sign_cn.get(subject.tenth_house.sign, subject.tenth_house.sign)
    mc_degree = subject.tenth_house.position
    mc_idx = sign_order.index(mc_sign) if mc_sign in sign_order else 0
    mc_abs = mc_idx * 30 + mc_degree
    
    mc_info = {
        "name": mc_sign,
        "degree": mc_degree,
        "abs_degree": mc_abs
    }
    
    # 宮位
    houses = []
    house_objs = [
        subject.first_house, subject.second_house, subject.third_house,
        subject.fourth_house, subject.fifth_house, subject.sixth_house,
        subject.seventh_house, subject.eighth_house, subject.ninth_house,
        subject.tenth_house, subject.eleventh_house, subject.twelfth_house
    ]
    for i, h in enumerate(house_objs):
        h_sign = sign_cn.get(h.sign, h.sign)
        houses.append({"house": i + 1, "sign": h_sign, "degree": h.position})
    
    # 計算相位 - 使用標準容許度
    aspects = []
    aspect_types = [
        {"name": "合相", "angle": 0, "orb": 10, "nature": "中"},
        {"name": "六分相", "angle": 60, "orb": 6, "nature": "吉"},
        {"name": "四分相", "angle": 90, "orb": 8, "nature": "凶"},
        {"name": "三分相", "angle": 120, "orb": 8, "nature": "吉"},
        {"name": "對分相", "angle": 180, "orb": 10, "nature": "凶"}
    ]
    
    # 包含上升點和中天作為計算相位的點
    planet_names = list(planet_positions.keys())
    all_points = {**{p: planet_positions[p]["abs_degree"] for p in planet_names}}
    all_points["上升"] = asc_info["abs_degree"]
    all_points["中天"] = mc_info["abs_degree"]
    point_names = list(all_points.keys())
    
    for i in range(len(point_names)):
        for j in range(i + 1, len(point_names)):
            p1, p2 = point_names[i], point_names[j]
            d1, d2 = all_points[p1], all_points[p2]
            diff = abs(d1 - d2)
            if diff > 180:
                diff = 360 - diff
            
            for asp in aspect_types:
                actual_orb = abs(diff - asp["angle"])
                if actual_orb <= asp["orb"]:
                    aspects.append({
                        "planet1": p1, "planet2": p2,
                        "aspect": asp["name"], "nature": asp["nature"],
                        "orb": round(actual_orb, 2)
                    })
                    break  # 只記錄最接近的相位
    
    # 統計元素
    elements = {"火": 0, "土": 0, "風": 0, "水": 0}
    for p in ["太陽", "月亮", "水星", "金星", "火星"]:
        if p in planet_positions and planet_positions[p]["element"]:
            elements[planet_positions[p]["element"]] += 1
    dominant_element = max(elements, key=elements.get)
    element_analysis = {
        "火": "熱情、行動力強、有領導力",
        "土": "務實、穩定、注重物質安全",
        "風": "理性、善於溝通、思維活躍",
        "水": "敏感、直覺強、情感豐富"
    }
    
    # 統計模式
    modalities = {"開創": 0, "固定": 0, "變動": 0}
    for p in ["太陽", "月亮", "水星", "金星", "火星"]:
        if p in planet_positions and planet_positions[p]["modality"]:
            modalities[planet_positions[p]["modality"]] += 1
    dominant_modality = max(modalities, key=modalities.get)
    modality_analysis = {
        "開創": "富有開創精神、喜歡領導",
        "固定": "堅持不懈、意志堅定",
        "變動": "適應力強、靈活變通"
    }
    
    # 統計陰陽
    polarity = {"陽": 0, "陰": 0}
    for p in ["太陽", "月亮", "水星", "金星", "火星"]:
        if p in planet_positions and planet_positions[p]["polarity"]:
            polarity[planet_positions[p]["polarity"]] += 1
    polarity_desc = "外向、主動" if polarity["陽"] > polarity["陰"] else "內向、被動"
    
    # 格局檢測
    patterns = []
    all_points = {k: v["abs_degree"] for k, v in planet_positions.items()}
    all_points["上升"] = asc_info["abs_degree"]
    all_points["中天"] = mc_info["abs_degree"]
    
    point_names = list(all_points.keys())
    
    def angle_diff(d1, d2):
        diff = abs(d1 - d2)
        return diff if diff <= 180 else 360 - diff
    
    # 大三角檢測 (Grand Trine - 三個120度)
    for i in range(len(point_names)):
        for j in range(i + 1, len(point_names)):
            for k in range(j + 1, len(point_names)):
                p1, p2, p3 = point_names[i], point_names[j], point_names[k]
                d12 = angle_diff(all_points[p1], all_points[p2])
                d23 = angle_diff(all_points[p2], all_points[p3])
                d13 = angle_diff(all_points[p1], all_points[p3])
                
                if abs(d12 - 120) <= 8 and abs(d23 - 120) <= 8 and abs(d13 - 120) <= 8:
                    elem = planet_positions.get(p1, {}).get("element", "")
                    patterns.append({
                        "name": "大三角 (Grand Trine)",
                        "type": "harmonious",
                        "planets": [p1, p2, p3],
                        "element": elem,
                        "meaning": f"天賦卓越，{elem}象能量和諧流動，帶來自然的幸運與天賦"
                    })
    
    # T-Square 檢測 (兩個90度 + 一個180度)
    for i in range(len(point_names)):
        for j in range(i + 1, len(point_names)):
            d_opp = angle_diff(all_points[point_names[i]], all_points[point_names[j]])
            if abs(d_opp - 180) <= 10:  # 對分相
                for k in range(len(point_names)):
                    if k == i or k == j:
                        continue
                    d1 = angle_diff(all_points[point_names[i]], all_points[point_names[k]])
                    d2 = angle_diff(all_points[point_names[j]], all_points[point_names[k]])
                    if abs(d1 - 90) <= 8 and abs(d2 - 90) <= 8:
                        patterns.append({
                            "name": "T三角 (T-Square)",
                            "type": "challenging",
                            "planets": [point_names[i], point_names[j], point_names[k]],
                            "apex": point_names[k],
                            "meaning": f"挑戰與動力，{point_names[k]}是壓力焦點，需要有意識地整合能量"
                        })
    
    # 大十字檢測 (Grand Cross - 四個90度)
    for i in range(len(point_names)):
        for j in range(i + 1, len(point_names)):
            for k in range(j + 1, len(point_names)):
                for l in range(k + 1, len(point_names)):
                    pts = [point_names[i], point_names[j], point_names[k], point_names[l]]
                    degs = [all_points[p] for p in pts]
                    # 檢查是否形成兩對對分相和四個四分相
                    pairs_180 = []
                    pairs_90 = []
                    for a in range(4):
                        for b in range(a + 1, 4):
                            diff = angle_diff(degs[a], degs[b])
                            if abs(diff - 180) <= 10:
                                pairs_180.append((a, b))
                            if abs(diff - 90) <= 8:
                                pairs_90.append((a, b))
                    if len(pairs_180) == 2 and len(pairs_90) >= 4:
                        patterns.append({
                            "name": "大十字 (Grand Cross)",
                            "type": "very_challenging",
                            "planets": pts,
                            "meaning": "極大張力與成長潛力，四方能量拉鋸，需要平衡與整合"
                        })
    
    # 上帝之指 Yod 檢測 (兩個150度 + 一個60度)
    for i in range(len(point_names)):
        for j in range(i + 1, len(point_names)):
            d_sext = angle_diff(all_points[point_names[i]], all_points[point_names[j]])
            if abs(d_sext - 60) <= 6:  # 六分相
                for k in range(len(point_names)):
                    if k == i or k == j:
                        continue
                    d1 = angle_diff(all_points[point_names[i]], all_points[point_names[k]])
                    d2 = angle_diff(all_points[point_names[j]], all_points[point_names[k]])
                    if abs(d1 - 150) <= 5 and abs(d2 - 150) <= 5:
                        patterns.append({
                            "name": "上帝之指 (Yod)",
                            "type": "fated",
                            "planets": [point_names[i], point_names[j], point_names[k]],
                            "apex": point_names[k],
                            "meaning": f"命運的手指，{point_names[k]}是使命焦點，暗示特殊的人生使命"
                        })
    
    # 風箏檢測 (Kite - 大三角 + 對分相)
    for pattern in patterns[:]:
        if pattern["name"].startswith("大三角"):
            trine_planets = pattern["planets"]
            for planet in point_names:
                if planet in trine_planets:
                    continue
                # 檢查是否與大三角中的一個行星形成對分相
                for tp in trine_planets:
                    if abs(angle_diff(all_points[planet], all_points[tp]) - 180) <= 10:
                        # 檢查是否與另外兩個形成六分相
                        others = [p for p in trine_planets if p != tp]
                        if all(abs(angle_diff(all_points[planet], all_points[o]) - 60) <= 6 for o in others):
                            patterns.append({
                                "name": "風箏 (Kite)",
                                "type": "dynamic_talent",
                                "planets": trine_planets + [planet],
                                "apex": planet,
                                "meaning": f"大三角的動態版本，{planet}為焦點，天賦可被具體運用"
                            })
    
    # 神秘矩形檢測 (Mystic Rectangle)
    for i in range(len(point_names)):
        for j in range(i + 1, len(point_names)):
            for k in range(j + 1, len(point_names)):
                for l in range(k + 1, len(point_names)):
                    pts = [point_names[i], point_names[j], point_names[k], point_names[l]]
                    degs = [all_points[p] for p in pts]
                    # 需要兩個對分相、兩個三分相、兩個六分相
                    pairs_180 = 0
                    pairs_120 = 0
                    pairs_60 = 0
                    for a in range(4):
                        for b in range(a + 1, 4):
                            diff = angle_diff(degs[a], degs[b])
                            if abs(diff - 180) <= 10: pairs_180 += 1
                            if abs(diff - 120) <= 8: pairs_120 += 1
                            if abs(diff - 60) <= 6: pairs_60 += 1
                    if pairs_180 == 2 and pairs_120 >= 2 and pairs_60 >= 2:
                        patterns.append({
                            "name": "神秘矩形 (Mystic Rectangle)",
                            "type": "creative_tension",
                            "planets": pts,
                            "meaning": "創造性張力，吉凶相位平衡，具有實現願景的潛力"
                        })
    
    # 去除重複格局
    seen = set()
    unique_patterns = []
    for p in patterns:
        key = (p["name"], tuple(sorted(p["planets"])))
        if key not in seen:
            seen.add(key)
            unique_patterns.append(p)
    patterns = unique_patterns[:10]  # 限制數量
    
    # 行星守護與飛星分析
    sign_rulers = {
        "牡羊座": "火星", "金牛座": "金星", "雙子座": "水星", "巨蟹座": "月亮",
        "獅子座": "太陽", "處女座": "水星", "天秤座": "金星", "天蠍座": "冥王星",
        "射手座": "木星", "摩羯座": "土星", "水瓶座": "天王星", "雙魚座": "海王星"
    }
    
    # 計算每個行星所落星座的守護星 (Dispositorship)
    dispositors = {}
    for planet, details in planet_positions.items():
        sign = details["sign"]
        ruler = sign_rulers.get(sign, "")
        dispositors[planet] = {
            "sign": sign,
            "dispositor": ruler,
            "dispositor_sign": planet_positions.get(ruler, {}).get("sign", "")
        }
    
    # 找出最終定位星 (Final Dispositor)
    def find_final_dispositor(planet, visited=None):
        if visited is None:
            visited = set()
        if planet in visited:
            return None  # 形成迴圈
        visited.add(planet)
        sign = planet_positions.get(planet, {}).get("sign", "")
        ruler = sign_rulers.get(sign, "")
        if ruler == planet:  # 入廟
            return planet
        if ruler and ruler in planet_positions:
            return find_final_dispositor(ruler, visited)
        return None
    
    final_dispositors = set()
    for planet in planet_positions.keys():
        fd = find_final_dispositor(planet)
        if fd:
            final_dispositors.add(fd)
    
    # 行星力量分析 (Dignities)
    dignities = {
        "太陽": {"domicile": "獅子座", "exaltation": "牡羊座", "detriment": "水瓶座", "fall": "天秤座"},
        "月亮": {"domicile": "巨蟹座", "exaltation": "金牛座", "detriment": "摩羯座", "fall": "天蠍座"},
        "水星": {"domicile": ["雙子座", "處女座"], "exaltation": "處女座", "detriment": ["射手座", "雙魚座"], "fall": "雙魚座"},
        "金星": {"domicile": ["金牛座", "天秤座"], "exaltation": "雙魚座", "detriment": ["牡羊座", "天蠍座"], "fall": "處女座"},
        "火星": {"domicile": ["牡羊座", "天蠍座"], "exaltation": "摩羯座", "detriment": ["金牛座", "天秤座"], "fall": "巨蟹座"},
        "木星": {"domicile": ["射手座", "雙魚座"], "exaltation": "巨蟹座", "detriment": ["雙子座", "處女座"], "fall": "摩羯座"},
        "土星": {"domicile": ["摩羯座", "水瓶座"], "exaltation": "天秤座", "detriment": ["巨蟹座", "獅子座"], "fall": "牡羊座"},
        "天王星": {"domicile": "水瓶座", "exaltation": "天蠍座", "detriment": "獅子座", "fall": "金牛座"},
        "海王星": {"domicile": "雙魚座", "exaltation": "獅子座", "detriment": "處女座", "fall": "水瓶座"},
        "冥王星": {"domicile": "天蠍座", "exaltation": "牡羊座", "detriment": "金牛座", "fall": "天秤座"},
    }
    
    planet_dignities = {}
    for planet, details in planet_positions.items():
        sign = details["sign"]
        dignity_info = dignities.get(planet, {})
        status = "中性"
        
        domicile = dignity_info.get("domicile", [])
        if isinstance(domicile, str): domicile = [domicile]
        exaltation = dignity_info.get("exaltation", "")
        detriment = dignity_info.get("detriment", [])
        if isinstance(detriment, str): detriment = [detriment]
        fall = dignity_info.get("fall", "")
        
        if sign in domicile:
            status = "入廟 (Domicile)"
        elif sign == exaltation:
            status = "旺 (Exaltation)"
        elif sign in detriment:
            status = "陷 (Detriment)"
        elif sign == fall:
            status = "落 (Fall)"
        
        planet_dignities[planet] = status
    
    # 上升守護星分析
    asc_ruler = sign_rulers.get(asc_sign, "")
    asc_ruler_info = None
    if asc_ruler and asc_ruler in planet_positions:
        asc_ruler_info = {
            "planet": asc_ruler,
            "sign": planet_positions[asc_ruler]["sign"],
            "dignity": planet_dignities.get(asc_ruler, "中性"),
            "meaning": f"命主星{asc_ruler}落在{planet_positions[asc_ruler]['sign']}，影響整體人生方向"
        }
    
    # 構建回傳資料
    sun = planet_positions.get("太陽", {"sign": "未知", "degree": 0})
    moon = planet_positions.get("月亮", {"sign": "未知", "degree": 0})
    
    ast_data = {
        "sun": f"☀️ {sun['sign']} {sun['degree']:.2f}°",
        "sunSign": sun["sign"],
        "moon": f"🌙 {moon['sign']} {moon['degree']:.2f}°",
        "moonSign": moon["sign"],
        "ascendant": f"⬆️ {asc_info['name']} {asc_info['degree']:.2f}°",
        "ascendantSign": asc_info["name"],
        "ascendantRuler": asc_info["ruler"],
        "mc": f"⬆️ {mc_info['name']} {mc_info['degree']:.2f}°",
        "mcSign": mc_info["name"],
        "planets": planets_display,
        "planetDetails": planet_positions,
        "houses": houses,
        "aspects": aspects,
        "elements": elements,
        "dominantElement": dominant_element,
        "elementAnalysis": element_analysis[dominant_element],
        "modalities": modalities,
        "dominantModality": dominant_modality,
        "modalityAnalysis": modality_analysis[dominant_modality],
        "polarity": polarity,
        "polarityDesc": polarity_desc,
        "patterns": patterns,
        "birthCity": birth_city,
        # 新增專業分析
        "dispositors": dispositors,
        "planetDignities": planet_dignities,
        "finalDispositors": list(final_dispositors),
        "ascRulerInfo": asc_ruler_info
    }
    
    # AI 解讀
    aspects_str = ", ".join([f"{a['planet1']}{a['aspect']}{a['planet2']}" for a in aspects[:8]])
    patterns_str = ", ".join([p['name'] for p in patterns]) if patterns else "無特殊格局"
    
    prompt = f"""作為專業占星師，請根據以下完整星盤提供深度分析：

出生時間：{birth_date} {birth_time}
出生地點：{birth_city}

【三大重點】
☀️ 太陽：{sun['sign']} {sun['degree']:.1f}° ({sun.get('element', '')}象/{sun.get('modality', '')})
🌙 月亮：{moon['sign']} {moon['degree']:.1f}° ({moon.get('element', '')}象/{moon.get('modality', '')})
⬆️ 上升：{asc_info['name']} {asc_info['degree']:.1f}° (守護星: {asc_info['ruler']})

【元素分布】火:{elements['火']} 土:{elements['土']} 風:{elements['風']} 水:{elements['水']} → 主導: {dominant_element}象
【模式分布】開創:{modalities['開創']} 固定:{modalities['固定']} 變動:{modalities['變動']} → 主導: {dominant_modality}
【陰陽比例】陽:{polarity['陽']} 陰:{polarity['陰']}

【主要相位】{aspects_str}
【特殊格局】{patterns_str}

請提供：
1. 人格核心解讀（150字）
2. 元素與模式分析（100字）
3. 重要相位解讀（120字）
4. 格局分析（80字）
5. 綜合人生建議（100字）

請用繁體中文，專業但易懂。"""
    
    fallback = f"太陽{sun['sign']}賦予您核心特質。月亮{moon['sign']}反映您的情感需求。上升{asc_info['name']}決定您的外在形象。"
    interpretation, model_used = generate_ai_content(prompt, fallback)
    
    return jsonify({"success": True, **ast_data, "interpretation": interpretation})


@app.route('/api/astrology/chart', methods=['GET'])
def get_astrology():
    """取得占星資訊 (Demo)"""
    return jsonify({"success": True, **ASTROLOGY_DATA, "interpretation": "請輸入出生資料以獲取個人化分析"})


@app.route('/api/ziwei/calculate', methods=['POST'])
def calculate_ziwei():
    """計算紫微斗數 - 使用專業計算模組"""
    from lunar_python import Solar
    from ziwei_calculator import calculate_ziwei_chart, DIZHI
    
    data = request.json or {}
    birth_date = data.get('birthDate', '1990-01-31')
    birth_hour = data.get('birthHour', 3)  # 0-11 時辰索引
    
    try:
        year, month, day = map(int, birth_date.split('-'))
        
        # 轉換為農曆
        # 使用時辰索引對應的小時 (子時=23, 丑時=1, ...)
        HOUR_MAP = [23, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
        hour = HOUR_MAP[birth_hour % 12]
        
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        lunar = solar.getLunar()
        
        lunar_year = lunar.getYear()
        lunar_month = lunar.getMonth()
        lunar_day = lunar.getDay()
        
        # 獲取年干支
        year_gz = lunar.getYearInGanZhi()
        year_tiangan = year_gz[0] if year_gz else '甲'
        year_dizhi = year_gz[1] if len(year_gz) > 1 else '子'
        
        lunar_date_str = f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}"
        
    except Exception as e:
        print(f"農曆轉換錯誤: {e}")
        # 使用預設值
        lunar_month = 1
        lunar_day = 15
        year_tiangan = '甲'
        year_dizhi = '子'
        lunar_date_str = "農曆日期計算失敗"
    
    # 使用新的紫微計算模組
    try:
        chart = calculate_ziwei_chart(
            lunar_year=lunar_year if 'lunar_year' in dir() else 1990,
            lunar_month=lunar_month,
            lunar_day=lunar_day,
            shichen=birth_hour,
            year_tiangan=year_tiangan,
            year_dizhi=year_dizhi
        )
    except Exception as e:
        print(f"紫微計算錯誤: {e}")
        chart = {
            'ming_palace': '子',
            'main_star': '紫微',
            'ming_zhu': '貪狼',
            'shen_zhu': '火星',
            'wuxing_ju': '水二局',
            'palaces': {},
            'si_hua': {}
        }
    
    # 構建十二宮資料 (包含地支位置)
    palaces_full = {}
    for palace_name, palace_data in chart.get('palaces', {}).items():
        stars = palace_data.get('stars', [])
        dizhi = palace_data.get('dizhi', '')
        palaces_full[palace_name] = {
            'stars': stars,
            'dizhi': dizhi,
            'stars_str': ', '.join(stars) if stars else '無主星'
        }
    
    # 四化標記
    si_hua = chart.get('si_hua', {})
    si_hua_str = ', '.join([f"{star}{hua}" for star, hua in si_hua.items()])
    
    zw_data = {
        "main_star": chart.get('main_star', '紫微'),
        "mingzhu": chart.get('ming_zhu', '貪狼'),
        "shenzhu": chart.get('shen_zhu', '火星'),
        "wuxing_ju": chart.get('wuxing_ju', '水二局'),
        "ming_palace_dizhi": chart.get('ming_palace', '子'),
        "shen_palace_dizhi": chart.get('shen_palace', '丑'),
        "lunar_date": lunar_date_str,
        "palaces": palaces_full,
        "si_hua": si_hua_str
    }
    
    # 為 AI prompt 準備簡化版星曜字串
    palaces_simple = {name: data['stars_str'] for name, data in palaces_full.items()}
    
    # 構建 AI 提示詞
    ming_stars_str = palaces_simple.get('命宮', '無主星')
    cai_stars_str = palaces_simple.get('財帛宮', '無主星')
    guan_stars_str = palaces_simple.get('官祿宮', '無主星')
    fuqi_stars_str = palaces_simple.get('夫妻宮', '無主星')
    
    prompt = f"""作為專業紫微斗數分析師，請根據以下命盤提供詳盡的分析報告。

出生日期：{birth_date}（{lunar_date_str}）
命宮地支：{chart.get('ming_palace', '?')}宮
五行局：{chart.get('wuxing_ju', '?')}
命主：{chart.get('ming_zhu', '?')}
身主：{chart.get('shen_zhu', '?')}

命宮星曜：{ming_stars_str}
財帛宮：{cai_stars_str}
官祿宮：{guan_stars_str}
夫妻宮：{fuqi_stars_str}

四化：{si_hua_str}

請提供約 500-800 字的完整分析，包含：
### 1. 命格總論
解讀命宮主星的核心特質，以及五行局對命主的影響。

### 2. 性格與天賦
根據命宮、福德宮的星曜，分析此人的性格特點和天賦才能。

### 3. 事業與財運
結合官祿宮和財帛宮的星曜，以及四化的影響，分析事業發展方向和財運特點。

### 4. 感情與人際
根據夫妻宮和交友宮的星曜，分析感情模式和人際關係。

### 5. 本年運勢提醒
給予具體可行的生活建議。

請用繁體中文，語氣專業且溫暖。"""
    
    fallback = f"""您的命盤顯示{chart.get('main_star', '紫微')}坐命{chart.get('ming_palace', '?')}宮，命主為{chart.get('ming_zhu', '貪狼')}，身主為{chart.get('shen_zhu', '火星')}。

{chart.get('wuxing_ju', '水二局')}代表您的大限起始年齡，也反映您的五行能量特質。

命宮星曜 {ming_stars_str} 顯示您具有獨特的人生道路和性格特質。

四化 {si_hua_str} 是本年的重要能量變化指標，請留意相關宮位的吉凶變化。"""
    
    interpretation, model_used = generate_ai_content(prompt, fallback)
    
    return jsonify({"success": True, **zw_data, "interpretation": interpretation})


@app.route('/api/ziwei/chart', methods=['GET'])
def get_ziwei():
    """取得紫微斗數 (Demo)"""
    return jsonify({"success": True, **ZIWEI_DATA, "interpretation": "請輸入出生資料以獲取個人化分析"})


import random
from tarot_deck import FULL_DECK

# ... (Previous code)

def get_tarot_reading_struct(question):
    """
    Returns structured tarot data:
    {
        "spread_name": str,
        "cards": [list of strings with orientation]
    }
    """
    try:
        # Step 1: Get Spread Recommendation
        spread_prompt = f"""
        你是一位塔羅牌大師。用戶的問題是：「{question}」。
        請推薦一個最適合此問題的塔羅牌陣（3到5張牌為佳）。
        請嚴格按照以下格式回傳一行，不要有其他文字：
        牌陣名稱|位置1含義,位置2含義,位置3含義...
        例如：聖三角牌陣|過去,現在,未來
        """
        spread_text, _ = generate_ai_content(spread_prompt, "")
        
        # Simple extraction
        if "|" in spread_text:
            parts = spread_text.strip().split("|")
            spread_name = parts[0]
            positions = [p.strip() for p in parts[1].split(",") if p.strip()]
        else:
            # Fallback
            spread_name = "身心靈三卡指引"
            positions = ["現況", "建議", "結果"]
            
        # Step 2: Draw Cards
        count = len(positions)
        drawn_cards = random.sample(FULL_DECK, count)
        
        formatted_cards = []
        for i, card in enumerate(drawn_cards):
            is_reversed = random.choice([True, False])
            orientation = "逆位 (Reversed)" if is_reversed else "正位 (Upright)"
            formatted_cards.append(f"{i+1}. {positions[i]}：{card} - {orientation}")
            
        return {
            "spread_name": spread_name,
            "cards": formatted_cards
        }

    except Exception as e:
        print(f"Tarot error: {e}")
        return {
            "spread_name": "Error",
            "cards": []
        }

@app.route('/api/integration/analyze', methods=['POST'])
def analyze_integration():
    data = request.json or {}
    # 前端傳來的 "question" 包含了問題和所有需要的背景資料
    user_context = data.get('question', '')
    selected_systems = data.get('systems', [])
    birth_data = data.get('birth_data', {})
    
    system_data = {}

    # Check if Tarot is selected and inject real reading
    if 'tarot' in selected_systems:
        import re
        match = re.search(r"\[用戶問題\] (.*?)\n", user_context)
        pure_question = match.group(1) if match else "我的運勢如何？"
        
        print(f"Performing Tarot Reading for: {pure_question}")
        tarot_struct = get_tarot_reading_struct(pure_question)
        system_data['tarot'] = tarot_struct
        
        # Format for AI Context
        tarot_reading_str = f"\n\n[系統自動抽牌結果 - {tarot_struct['spread_name']}]\n" + "\n".join(tarot_struct['cards'])
        user_context += tarot_reading_str
    
    # Human Design calculation
    if 'humandesign' in selected_systems and birth_data:
        try:
            bd = birth_data
            if bd.get('date') and bd.get('time') and bd.get('city'):
                # 模擬內部調用 calculate_human_design 的邏輯
                # 這裡直接返回摘要
                birth_dt_str = f"{bd['date']}T{bd['time']}"
                lat = bd['city']['lat']
                lng = bd['city']['lng']
                
                # 簡化版計算：使用現有的 HD 計算邏輯
                from datetime import datetime as dt
                birth_datetime = dt.strptime(birth_dt_str, "%Y-%m-%dT%H:%M")
                
                # 使用 ephem 計算太陽位置來確定 Type (簡化版)
                sun_gate = int((ephem.Sun(birth_datetime).hlong * 180 / math.pi) % 360 / 5.625) + 1
                if sun_gate > 64: sun_gate = 1
                
                # 基於定義中心數量決定 Type (簡化邏輯)
                types_by_gate = {
                    range(1, 17): ("顯示者", "告知"),
                    range(17, 33): ("生產者", "等待回應"),
                    range(33, 49): ("投射者", "等待邀請"),
                    range(49, 65): ("反映者", "等待28天")
                }
                hd_type = "生產者"
                hd_strategy = "等待回應"
                for gate_range, (t, s) in types_by_gate.items():
                    if sun_gate in gate_range:
                        hd_type = t
                        hd_strategy = s
                        break
                
                system_data['humandesign'] = {
                    "type": hd_type,
                    "strategy": hd_strategy,
                    "summary": f"{hd_type}，策略：{hd_strategy}"
                }
                
                user_context += f"\n\n[人類圖計算結果]\n類型：{hd_type}\n策略：{hd_strategy}"
        except Exception as e:
            print(f"HD calculation error in integration: {e}")
            system_data['humandesign'] = {"type": "計算中", "summary": "待計算"}
    
    # Astrology calculation (using Kerykeion for accuracy)
    if 'astrology' in selected_systems and birth_data:
        try:
            bd = birth_data
            if bd.get('date') and bd.get('time') and bd.get('city'):
                from kerykeion import AstrologicalSubject
                import warnings
                warnings.filterwarnings("ignore")
                
                date_parts = bd['date'].split('-')
                year = int(date_parts[0])
                month = int(date_parts[1])
                day = int(date_parts[2])
                
                time_parts = bd['time'].split(':')
                hour = int(time_parts[0])
                minute = int(time_parts[1]) if len(time_parts) > 1 else 0
                
                lat = bd['city']['lat']
                lng = bd['city']['lng']
                city_name = bd['city']['name']
                
                # 星座中英對照
                sign_cn = {
                    "Ari": "牡羊座", "Tau": "金牛座", "Gem": "雙子座", "Can": "巨蟹座",
                    "Leo": "獅子座", "Vir": "處女座", "Lib": "天秤座", "Sco": "天蠍座",
                    "Sag": "射手座", "Cap": "摩羯座", "Aqu": "水瓶座", "Pis": "雙魚座"
                }
                
                subject = AstrologicalSubject(
                    "User", year, month, day, hour, minute,
                    city_name, "TW", lng=lng, lat=lat
                )
                
                sun_sign = sign_cn.get(subject.sun.sign, subject.sun.sign)
                moon_sign = sign_cn.get(subject.moon.sign, subject.moon.sign)
                asc_sign = sign_cn.get(subject.first_house.sign, subject.first_house.sign)
                
                system_data['astrology'] = {
                    "sun_sign": sun_sign,
                    "moon_sign": moon_sign,
                    "asc_sign": asc_sign,
                    "summary": f"太陽{sun_sign}，月亮{moon_sign}，上升{asc_sign}"
                }
                
                user_context += f"\n\n[占星計算結果]\n太陽星座：{sun_sign}\n月亮星座：{moon_sign}\n上升星座：{asc_sign}"
        except Exception as e:
            print(f"Astrology calculation error in integration: {e}")
            system_data['astrology'] = {"summary": "待計算"}
    
    # Ziwei calculation (using lunar_python for proper date conversion)
    if 'ziwei' in selected_systems and birth_data:
        try:
            bd = birth_data
            print(f"[Ziwei Integration] birth_data: {bd}")
            
            if bd.get('date'):
                from lunar_python import Solar
                from ziwei_calculator import calculate_ziwei_chart
                
                date_parts = bd['date'].split('-')
                year = int(date_parts[0])
                month = int(date_parts[1])
                day = int(date_parts[2])
                
                # hour is shichen index (0-11)
                shichen = bd.get('hour') if bd.get('hour') is not None else 6
                
                # Convert shichen to hour for Solar calculation
                HOUR_MAP = [23, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
                hour = HOUR_MAP[shichen % 12]
                
                # Convert to lunar date
                solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
                lunar = solar.getLunar()
                
                lunar_year = lunar.getYear()
                lunar_month = lunar.getMonth()
                lunar_day = lunar.getDay()
                
                year_gz = lunar.getYearInGanZhi()
                year_tiangan = year_gz[0] if year_gz else '甲'
                year_dizhi = year_gz[1] if len(year_gz) > 1 else '子'
                
                print(f"[Ziwei Integration] Lunar: {lunar_year}/{lunar_month}/{lunar_day} TG={year_tiangan} DZ={year_dizhi}")
                
                # Calculate chart using proper function
                chart = calculate_ziwei_chart(
                    lunar_year=lunar_year,
                    lunar_month=lunar_month,
                    lunar_day=lunar_day,
                    shichen=shichen,
                    year_tiangan=year_tiangan,
                    year_dizhi=year_dizhi
                )
                
                if chart:
                    main_star = chart.get('main_star', '未知')
                    ming_palace = chart.get('ming_palace', '')
                    wuxing_ju = chart.get('wuxing_ju', '')
                    
                    print(f"[Ziwei Integration] Result: main_star={main_star}, ming_palace={ming_palace}")
                    
                    system_data['ziwei'] = {
                        "main_star": main_star,
                        "ming_palace": ming_palace,
                        "wuxing_ju": wuxing_ju,
                        "summary": f"命宮{ming_palace}，{main_star}坐命，{wuxing_ju}"
                    }
                    
                    user_context += f"\n\n[紫微計算結果]\n命宮：{ming_palace}\n主星：{main_star}\n五行局：{wuxing_ju}"
                else:
                    system_data['ziwei'] = {"summary": "計算結果為空"}
            else:
                system_data['ziwei'] = {"summary": "缺少出生日期"}
        except Exception as e:
            print(f"Ziwei calculation error in integration: {e}")
            import traceback
            traceback.print_exc()
            system_data['ziwei'] = {"summary": "計算錯誤"}
    
    # 獲取當前日期
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_year = current_date.split('-')[0]
    
    prompt = f"""
你是一位精通東方與西方命理的身心靈整合顧問。
現在日期是：{current_date}。

請根據以下用戶提供的資訊（包含問題、出生資料、以及相關系統的數據）進行深入分析：

{user_context}

分析指引：
1. 請整合所有提供的資訊，不要忽略任何一個系統（如八字、紫微、占星、人類圖等）。
2. 對於塔羅部分，請根據**『系統自動抽牌結果』**中的牌陣與牌義，結合問題進行解讀（請明確解讀每一張牌與其位置的關聯）。
3. 提供具體的流年運勢分析時，請以 **{current_year}年** 為主。
4. 語氣要專業、溫暖、給予力量，並提供具體的行動建議。
5. 輸出格式請使用 Markdown，善用標題、條列和粗體來提高易讀性。
"""
    
    analysis, model_used = generate_ai_content(prompt, AI_INTEGRATION_RESPONSE)
    source = "gemini" if model_used else "demo"
    
    return jsonify({
        "success": True, 
        "question": user_context, 
        "analysis": analysis, 
        "source": source, 
        "model": model_used,
        "system_data": system_data
    })


# ========== Admin API Endpoints ==========

from auth import (
    verify_admin, generate_token, verify_token, admin_required,
    get_api_key, update_api_key, update_password, mask_api_key, get_admin_data
)
from usage_tracker import (
    track_usage, get_usage_stats, get_summary_stats, get_hourly_stats, FEATURE_NAMES
)

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """管理員登入"""
    data = request.json or {}
    username = data.get('username', '')
    password = data.get('password', '')
    
    if verify_admin(username, password):
        token = generate_token(username)
        return jsonify({
            "success": True,
            "token": token,
            "message": "登入成功"
        })
    else:
        return jsonify({
            "success": False,
            "error": "帳號或密碼錯誤"
        }), 401

@app.route('/api/admin/verify', methods=['GET'])
@admin_required
def admin_verify():
    """驗證 token"""
    return jsonify({"success": True, "message": "Token 有效"})

@app.route('/api/admin/api-key', methods=['GET'])
@admin_required
def get_admin_api_key():
    """獲取所有 API Key (遮蔽顯示)"""
    # 從資料庫讀取
    db_key = get_api_key()
    
    # 從 .env 讀取
    env_keys_str = os.environ.get('GOOGLE_API_KEYS', '')
    env_single_key = os.environ.get('GOOGLE_API_KEY', '')
    
    env_keys = []
    if env_keys_str:
        env_keys = [k.strip() for k in env_keys_str.split(',') if k.strip()]
    elif env_single_key:
        env_keys = [env_single_key]
    
    return jsonify({
        "success": True,
        "db_key_masked": mask_api_key(db_key) if db_key else "未設定",
        "env_keys": [{"key": mask_api_key(k), "full": k} for k in env_keys],
        "env_keys_count": len(env_keys),
        "has_db_key": bool(db_key)
    })

@app.route('/api/admin/api-key', methods=['PUT'])
@admin_required
def update_admin_api_key():
    """更新 API Key"""
    data = request.json or {}
    new_key = data.get('api_key', '')
    
    if not new_key:
        return jsonify({"success": False, "error": "請提供新的 API Key"}), 400
    
    update_api_key(new_key)
    return jsonify({
        "success": True,
        "message": "API Key 更新成功",
        "api_key_masked": mask_api_key(new_key)
    })

@app.route('/api/admin/password', methods=['PUT'])
@admin_required
def change_admin_password():
    """更改管理員密碼"""
    data = request.json or {}
    new_password = data.get('new_password', '')
    
    if len(new_password) < 6:
        return jsonify({"success": False, "error": "密碼長度至少 6 位"}), 400
    
    update_password(new_password)
    return jsonify({
        "success": True,
        "message": "密碼更新成功"
    })

@app.route('/api/admin/usage', methods=['GET'])
@admin_required
def get_admin_usage():
    """獲取使用量統計"""
    # 從查詢參數獲取篩選條件
    feature = request.args.get('feature')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    day = request.args.get('day', type=int)
    hour = request.args.get('hour', type=int)
    
    stats = get_usage_stats(
        feature_name=feature,
        start_date=start_date,
        end_date=end_date,
        year=year,
        month=month,
        day=day,
        hour=hour
    )
    
    return jsonify({
        "success": True,
        "stats": stats,
        "feature_names": FEATURE_NAMES
    })

@app.route('/api/admin/usage/summary', methods=['GET'])
@admin_required
def get_admin_usage_summary():
    """獲取使用量摘要"""
    summary = get_summary_stats()
    return jsonify({
        "success": True,
        "summary": summary,
        "feature_names": FEATURE_NAMES
    })

@app.route('/api/admin/usage/hourly', methods=['GET'])
@admin_required
def get_admin_usage_hourly():
    """獲取每小時統計"""
    feature = request.args.get('feature')
    date = request.args.get('date')  # YYYY-MM-DD
    
    hourly = get_hourly_stats(feature_name=feature, date=date)
    return jsonify({
        "success": True,
        "hourly": hourly,
        "date": date or datetime.now().strftime("%Y-%m-%d")
    })


if __name__ == '__main__':
    print("Starting Spiritual AI Advisor API...")
    print("API running at http://localhost:5000")
    print("Frontend should connect from http://localhost:3000")
    app.run(host='0.0.0.0', port=5000, debug=True)

