"""
Spiritual AI Advisor - Tarot Agent (完整版)
============================================
AI 塔羅牌解讀師，支援多種牌陣。

使用方式:
    python tarot_agent.py

支援牌陣:
    1. 單牌 - 快速指引
    2. 三牌陣 - 過去/現在/未來
    3. 五牌陣 - 感情專用
    4. 凱爾特十字 - 深度解析
"""

import os
import sys
import random
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("❌ 請在 .env 檔案中設定 GOOGLE_API_KEY")
    sys.exit(1)

import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')


# ========== 塔羅牌資料庫 (78張標準塔羅) ==========
MAJOR_ARCANA = [
    "愚者 (The Fool)", "魔術師 (The Magician)", "女祭司 (The High Priestess)",
    "皇后 (The Empress)", "皇帝 (The Emperor)", "教皇 (The Hierophant)",
    "戀人 (The Lovers)", "戰車 (The Chariot)", "力量 (Strength)",
    "隱士 (The Hermit)", "命運之輪 (Wheel of Fortune)", "正義 (Justice)",
    "倒吊人 (The Hanged Man)", "死神 (Death)", "節制 (Temperance)",
    "惡魔 (The Devil)", "高塔 (The Tower)", "星星 (The Star)",
    "月亮 (The Moon)", "太陽 (The Sun)", "審判 (Judgement)", "世界 (The World)"
]

MINOR_ARCANA_SUITS = ["權杖 (Wands)", "聖杯 (Cups)", "寶劍 (Swords)", "錢幣 (Pentacles)"]
MINOR_ARCANA_RANKS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "侍者 (Page)", "騎士 (Knight)", "王后 (Queen)", "國王 (King)"]


# ========== 牌陣定義 ==========
SPREADS = {
    "1": {
        "name": "單牌占卜",
        "description": "快速指引，適合簡單問題",
        "positions": ["指引"],
        "count": 1
    },
    "2": {
        "name": "三牌陣 (時間線)",
        "description": "過去、現在、未來的發展脈絡",
        "positions": ["過去", "現在", "未來"],
        "count": 3
    },
    "3": {
        "name": "五牌陣 (感情專用)",
        "description": "深入分析感情狀況",
        "positions": ["你的狀態", "對方的狀態", "關係現況", "阻礙/挑戰", "未來發展"],
        "count": 5
    },
    "4": {
        "name": "凱爾特十字 (深度解析)",
        "description": "最完整的牌陣，適合複雜問題",
        "positions": [
            "1. 現況 (核心問題)",
            "2. 阻礙 (橫跨的挑戰)",
            "3. 意識層面 (你知道的)",
            "4. 潛意識 (你不知道的)",
            "5. 過去",
            "6. 近期未來",
            "7. 你的態度",
            "8. 外部環境",
            "9. 希望與恐懼",
            "10. 最終結果"
        ],
        "count": 10
    }
}


def get_all_cards():
    """生成完整的 78 張塔羅牌"""
    cards = MAJOR_ARCANA.copy()
    for suit in MINOR_ARCANA_SUITS:
        for rank in MINOR_ARCANA_RANKS:
            cards.append(f"{rank} of {suit}")
    return cards


def draw_cards(num: int) -> list:
    """抽取指定數量的牌，並決定正逆位"""
    all_cards = get_all_cards()
    drawn = random.sample(all_cards, num)
    result = []
    for card in drawn:
        orientation = random.choice(["正位", "逆位"])
        result.append(f"{orientation} - {card}")
    return result


def interpret_cards(question: str, spread_name: str, positions: list, cards: list) -> str:
    """使用 Gemini 解讀塔羅牌"""
    cards_str = "\n".join([f"  {positions[i]}: {cards[i]}" for i in range(len(cards))])
    
    prompt = f"""
你是一位擁有 20 年經驗的專業塔羅牌解讀師。
你的風格溫暖、有洞察力，能給予實用的人生建議。

【牌陣類型】
{spread_name}

【用戶問題】
{question}

【抽到的牌】
{cards_str}

請提供完整的塔羅解讀：

## 🃏 各位置牌義解析
（請依序解讀每個位置的牌義，並說明與問題的關聯）

## 🔮 整體解讀
（綜合所有牌，回答用戶的問題，分析整體趨勢）

## 💡 行動建議
（給用戶具體可執行的 3 條建議）

---
⚠️ 免責聲明：塔羅牌僅供娛樂與自我反思參考，不構成任何專業建議。

請使用繁體中文回答，格式為 Markdown。
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ API 錯誤: {e}"


def select_spread() -> dict:
    """讓用戶選擇牌陣"""
    print("\n【請選擇牌陣】")
    for key, spread in SPREADS.items():
        print(f"  {key}. {spread['name']} - {spread['description']}")
    
    while True:
        choice = input("\n請輸入數字 (1-4): ").strip()
        if choice in SPREADS:
            return SPREADS[choice]
        print("❌ 請輸入有效的選項 (1-4)")


def main():
    print("\n" + "="*50)
    print("🔮 AI 塔羅牌解讀師 (完整版)")
    print("="*50)
    
    # 選擇牌陣
    spread = select_spread()
    print(f"\n✅ 已選擇: {spread['name']}")
    
    # 獲取用戶問題
    print("\n請輸入您想問的問題：")
    question = input("❓ 您的問題: ").strip()
    
    if not question:
        print("請輸入有效的問題！")
        return
    
    # 抽牌
    print(f"\n🎴 正在為您抽取 {spread['count']} 張牌...")
    cards = draw_cards(spread['count'])
    
    print("\n" + "="*50)
    print(f"【{spread['name']}】抽牌結果")
    print("="*50)
    for i, card in enumerate(cards):
        print(f"  {spread['positions'][i]}: {card}")
    
    # AI 解讀
    print("\n🧙 塔羅師正在解讀中...\n")
    interpretation = interpret_cards(question, spread['name'], spread['positions'], cards)
    
    print(interpretation)
    
    # 儲存結果
    output_file = "tarot_reading.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# 🔮 塔羅牌解讀報告\n\n")
        f.write(f"**牌陣**: {spread['name']}\n\n")
        f.write(f"**問題**: {question}\n\n")
        f.write(f"**抽到的牌**:\n")
        for i, card in enumerate(cards):
            f.write(f"- {spread['positions'][i]}: {card}\n")
        f.write(f"\n---\n\n")
        f.write(interpretation)
    
    print(f"\n✅ 解讀已儲存至 {output_file}")


if __name__ == "__main__":
    main()
