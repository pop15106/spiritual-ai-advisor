"""
Spiritual AI Advisor - 完整版 (含示範資料)
=========================================
塔羅 × 八字 × 人類圖 × 占星 × 紫微

啟動: streamlit run app.py
"""

import os
import random
from datetime import datetime, date
import streamlit as st
from dotenv import load_dotenv
import plotly.graph_objects as go

load_dotenv()

# ========== 頁面設定 ==========
st.set_page_config(page_title="🔮 AI 身心靈顧問", page_icon="🔮", layout="wide")

# ========== 預設假資料 (Demo Mode) ==========
DEMO_BAZI = {
    "success": True, "lunar": "庚午年十二月廿五",
    "year_gan": "庚", "year_zhi": "午", "month_gan": "己", "month_zhi": "丑",
    "day_gan": "甲", "day_zhi": "子", "hour_gan": "丙", "hour_zhi": "寅",
    "day_master": "甲",
    "liunian": [{"year": 2024, "ganzhi": "甲辰"}, {"year": 2025, "ganzhi": "乙巳"}, 
                {"year": 2026, "ganzhi": "丙午"}, {"year": 2027, "ganzhi": "丁未"},
                {"year": 2028, "ganzhi": "戊申"}, {"year": 2029, "ganzhi": "己酉"}]
}

DEMO_HD = {"type": "生產者", "profile": "3/5 烈士/異端", 
           "info": {"color": "#ff6b6b", "desc": "世界的建設者，擁有持久的生命力能量", "strategy": "等待回應", "icon": "⚡"}}

DEMO_ASTRO = {"sun": "♑ 摩羯座", "ascendant": "♌ 獅子座",
              "planets": {"☉ 太陽": "♑ 摩羯座", "☽ 月亮": "♋ 巨蟹座", "☿ 水星": "♐ 射手座",
                          "♀ 金星": "♒ 水瓶座", "♂ 火星": "♈ 牡羊座", "♃ 木星": "♎ 天秤座", "♄ 土星": "♑ 摩羯座"}}

DEMO_ZIWEI = {"main_star": "紫微", "mingzhu": "貪狼", "shenzhu": "天機",
              "palaces": {"命宮": "紫微", "兄弟宮": "天機", "夫妻宮": "太陽", "子女宮": "武曲",
                          "財帛宮": "天同", "疾厄宮": "廉貞", "遷移宮": "天府", "交友宮": "太陰",
                          "官祿宮": "貪狼", "田宅宮": "巨門", "福德宮": "天相", "父母宮": "天梁"}}

DEMO_TAROT = [{"name": "命運之輪", "reversed": False}, {"name": "星星", "reversed": False}, {"name": "戰車", "reversed": True}]

DEMO_AI_RESPONSE = """
## 🔮 核心訊息
從塔羅的「命運之輪」、八字的「甲木日主」、人類圖的「生產者」類型來看，您正處於人生的重要轉折點。命運之輪暗示變化即將來臨，而甲木日主代表您具有開拓進取的特質。

## ⚡ 各系統獨特觀點
- **塔羅**: 星星牌顯示希望與療癒，逆位戰車提醒需要調整方向
- **八字**: 甲木生於丑月，需要火來暖局，2026丙午年是好時機
- **人類圖**: 作為生產者，您需要等待正確的機會回應，而非主動出擊
- **占星**: 摩羯太陽+獅子上升，外表自信但內心務實
- **紫微**: 紫微坐命，天生具有領導格局

## 💎 綜合建議
1. 🎯 **把握 2026 年機會** - 丙火流年對您有利，適合展開新計畫
2. 🔄 **等待而非追求** - 符合生產者策略，讓機會來找您
3. 💪 **發揮領導特質** - 紫微命格適合帶領團隊，不要害怕承擔責任

---
*💜 以上為 AI 整合分析，結合東西方五大智慧系統*
"""

# ========== 樣式 ==========
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #faf0e6 0%, #f5e6d3 50%, #ede0d4 100%); }
    h1 { color: #6b4c9a !important; text-align: center; }
    h2 { color: #4a3070 !important; }
    .bazi-pillar { display: inline-block; margin: 5px; padding: 15px 20px; background: linear-gradient(145deg, #6b4c9a, #4a3070); color: white; border-radius: 15px; text-align: center; min-width: 80px; }
    .bazi-pillar .gan { font-size: 28px; font-weight: bold; }
    .bazi-pillar .zhi { font-size: 28px; margin-top: 5px; }
    .bazi-pillar .label { font-size: 12px; color: #ddd; margin-top: 8px; }
    .tip-box { background: linear-gradient(145deg, #fff3e0, #ffe0b2); border-left: 4px solid #ff9800; padding: 15px; margin: 10px 0; border-radius: 0 10px 10px 0; }
    .warning-box { background: linear-gradient(145deg, #ffebee, #ffcdd2); border-left: 4px solid #f44336; padding: 15px; margin: 10px 0; border-radius: 0 10px 10px 0; }
    .good-box { background: linear-gradient(145deg, #e8f5e9, #c8e6c9); border-left: 4px solid #4caf50; padding: 15px; margin: 10px 0; border-radius: 0 10px 10px 0; }
    .stButton > button { background: linear-gradient(90deg, #9b7ec9, #7c5bad); color: white; border: none; padding: 12px 25px; border-radius: 25px; font-size: 16px; font-weight: bold; }
    .planet-card { background: linear-gradient(145deg, #2d3436, #636e72); color: white; border-radius: 15px; padding: 15px; margin: 8px; text-align: center; }
    .ziwei-palace { background: linear-gradient(145deg, #6c5ce7, #a29bfe); color: white; border-radius: 12px; padding: 12px; margin: 5px; text-align: center; font-size: 14px; }
    .tarot-card { text-align: center; padding: 10px; }
    .tarot-card img { border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
</style>
""", unsafe_allow_html=True)


# ========== 初始化 Demo 資料 ==========
if 'demo_loaded' not in st.session_state:
    st.session_state['bazi_data'] = DEMO_BAZI
    st.session_state['hd_data'] = DEMO_HD
    st.session_state['astro_data'] = DEMO_ASTRO
    st.session_state['ziwei_data'] = DEMO_ZIWEI
    st.session_state['demo_loaded'] = True


# ========== Gemini (with fallback) ==========
def get_model():
    key = os.getenv("GOOGLE_API_KEY")
    if not key: return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        return genai.GenerativeModel('gemini-2.0-flash')
    except:
        return None


def ai_or_demo(prompt, demo_text):
    """嘗試 AI，失敗則用假資料"""
    model = get_model()
    if model:
        try:
            return model.generate_content(prompt).text
        except:
            pass
    return demo_text


# ========== 流年圖表 ==========
def create_fortune_chart(liunian_list):
    years = [ln["year"] for ln in liunian_list]
    scores = [6.5 + random.uniform(-2, 2.5) for _ in liunian_list]  # 模擬分數
    
    fig = go.Figure()
    colors = ['#f44336' if s < 5 else '#ff9800' if s < 6.5 else '#4caf50' for s in scores]
    fig.add_trace(go.Scatter(x=years, y=scores, mode='lines+markers', line=dict(color='#6b4c9a', width=3),
                             marker=dict(size=12, color=colors, line=dict(width=2, color='white')),
                             hovertemplate='%{x}年: %{y:.1f}分<extra></extra>'))
    fig.add_hrect(y0=0, y1=5, fillcolor="rgba(244,67,54,0.1)", line_width=0)
    fig.add_hrect(y0=5, y1=6.5, fillcolor="rgba(255,152,0,0.1)", line_width=0)
    fig.add_hrect(y0=6.5, y1=10, fillcolor="rgba(76,175,80,0.1)", line_width=0)
    fig.add_annotation(x=years[-1]+0.5, y=3, text="⚠️ 低迷", showarrow=False, font=dict(color="#f44336", size=10))
    fig.add_annotation(x=years[-1]+0.5, y=5.75, text="🔄 平穩", showarrow=False, font=dict(color="#ff9800", size=10))
    fig.add_annotation(x=years[-1]+0.5, y=8, text="🚀 旺盛", showarrow=False, font=dict(color="#4caf50", size=10))
    fig.update_layout(title="📈 流年運勢走勢圖", xaxis_title="年份", yaxis_title="運勢指數",
                      yaxis=dict(range=[0, 10]), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=280)
    return fig


# ========== 塔羅圖片 ==========
CARD_IMAGE_BASE = "https://www.sacred-texts.com/tarot/pkt/img"
MAJOR_ARCANA = {"愚者": "ar00", "魔術師": "ar01", "女祭司": "ar02", "皇后": "ar03", "皇帝": "ar04", "教皇": "ar05",
                "戀人": "ar06", "戰車": "ar07", "力量": "ar08", "隱士": "ar09", "命運之輪": "ar10", "正義": "ar11",
                "倒吊人": "ar12", "死神": "ar13", "節制": "ar14", "惡魔": "ar15", "高塔": "ar16", "星星": "ar17",
                "月亮": "ar18", "太陽": "ar19", "審判": "ar20", "世界": "ar21"}


# ==================== 主介面 ====================
st.title("🔮 AI 身心靈顧問")
st.markdown("<p style='text-align:center; color:#6b4c9a;'>融合東西方五大系統的智慧平台 | 🎭 <b>Demo Mode</b></p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🃏 塔羅", "☯️ 八字", "🧬 人類圖", "⭐ 占星", "💜 紫微", "🌐 整合分析"])

# ========== Tab 1: 塔羅 ==========
with tab1:
    st.header("🃏 塔羅占卜")
    st.info("📌 **Demo**: 已預設抽出三張牌")
    
    cols = st.columns(3)
    positions = ["過去", "現在", "未來"]
    for i, card in enumerate(DEMO_TAROT):
        with cols[i]:
            url = f"{CARD_IMAGE_BASE}/{MAJOR_ARCANA[card['name']]}.jpg"
            if card["reversed"]:
                st.markdown(f"<div class='tarot-card'><img src='{url}' style='transform:rotate(180deg); max-height:200px;'></div>", unsafe_allow_html=True)
            else:
                st.image(url, use_container_width=True)
            st.markdown(f"<p style='text-align:center;'><b>{positions[i]}</b><br>{'逆位' if card['reversed'] else '正位'} {card['name']}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
## 🔮 塔羅解讀

### 命運之輪 (正位) - 過去
您過去經歷了人生的起伏，命運之輪象徵著變化與循環。這段經歷讓您學會了順應天命。

### 星星 (正位) - 現在
星星牌帶來希望與療癒的能量！✨ 現在是一個充滿可能性的時刻，宇宙正在支持您。

### 戰車 (逆位) - 未來
逆位的戰車提醒您：不要太急躁！⚠️ 前進的方向可能需要調整，先停下來確認目標。

### 💡 行動建議
1. 接受過去的變化，不要執著
2. 把握現在的希望能量，許下願望
3. 未來行動前，先確認方向是否正確
""")

# ========== Tab 2: 八字 ==========
with tab2:
    st.header("☯️ 八字命理")
    st.info("📌 **Demo**: 1990年1月31日寅時出生")
    
    bazi = st.session_state['bazi_data']
    st.success(f"農曆: {bazi['lunar']}")
    
    st.markdown(f"""
    <div style="text-align:center; margin: 20px 0;">
        <div class="bazi-pillar"><div class="gan">{bazi['year_gan']}</div><div class="zhi">{bazi['year_zhi']}</div><div class="label">年柱</div></div>
        <div class="bazi-pillar"><div class="gan">{bazi['month_gan']}</div><div class="zhi">{bazi['month_zhi']}</div><div class="label">月柱</div></div>
        <div class="bazi-pillar" style="background:linear-gradient(145deg,#e94560,#c13584);"><div class="gan">{bazi['day_gan']}</div><div class="zhi">{bazi['day_zhi']}</div><div class="label">日柱</div></div>
        <div class="bazi-pillar"><div class="gan">{bazi['hour_gan']}</div><div class="zhi">{bazi['hour_zhi']}</div><div class="label">時柱</div></div>
    </div>""", unsafe_allow_html=True)
    
    fig = create_fortune_chart(bazi["liunian"])
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="good-box">🌟 <b>2026 丙午年</b> 運勢旺盛！適合展開新計畫</div>', unsafe_allow_html=True)
    st.markdown('<div class="tip-box">💡 <b>2027 丁未年</b> 財運上升，可考慮投資</div>', unsafe_allow_html=True)
    st.markdown('<div class="warning-box">⚠️ <b>2028 戊申年</b> 注意健康，避免過度勞累</div>', unsafe_allow_html=True)
    
    st.markdown("""
---
## 🔥 日主分析: 甲木

**甲木就像一棵參天大樹** 🌲

您的日主是「甲木」，代表您是一個正直、有抱負、渴望成長的人。就像大樹一樣，您追求向上發展，不喜歡被約束。

### 🌊 命格特點
- ✅ **優點**: 正直、有領導力、有遠見
- ⚠️ **缺點**: 有時過於固執、不夠靈活

### 💎 開運建議
1. 多接觸火元素 (紅色、南方)
2. 2026 是您的好年份，抓住機會！
3. 培養變通能力，不要太堅持己見
""")

# ========== Tab 3: 人類圖 ==========
with tab3:
    st.header("🧬 人類圖")
    st.info("📌 **Demo**: 生產者 3/5 人生角色")
    
    hd = st.session_state['hd_data']
    info = hd['info']
    
    col_chart, col_info = st.columns([1.2, 1])
    
    with col_chart:
        st.markdown("### 🔮 人體圖 Bodygraph")
        # 9 個能量中心的定義狀態 (Demo: 生產者通常薦骨是 defined)
        centers = {
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
        
        # 預先計算顏色
        head_fill = centers['頭腦']['color'] if centers['頭腦']['defined'] else 'white'
        head_text = 'white' if centers['頭腦']['defined'] else '#333'
        ajna_fill = centers['邏輯']['color'] if centers['邏輯']['defined'] else 'white'
        ajna_text = 'white' if centers['邏輯']['defined'] else '#333'
        throat_fill = centers['喉嚨']['color'] if centers['喉嚨']['defined'] else 'white'
        throat_text = 'white' if centers['喉嚨']['defined'] else '#333'
        g_fill = centers['G中心']['color'] if centers['G中心']['defined'] else 'white'
        g_text = 'white' if centers['G中心']['defined'] else '#333'
        ego_fill = centers['意志力']['color'] if centers['意志力']['defined'] else 'white'
        spleen_fill = centers['脾']['color'] if centers['脾']['defined'] else 'white'
        solar_fill = centers['情緒']['color'] if centers['情緒']['defined'] else 'white'
        solar_text = 'white' if centers['情緒']['defined'] else '#333'
        sacral_fill = centers['薦骨']['color'] if centers['薦骨']['defined'] else 'white'
        sacral_text = 'white' if centers['薦骨']['defined'] else '#333'
        root_fill = centers['根']['color'] if centers['根']['defined'] else 'white'
        root_text = 'white' if centers['根']['defined'] else '#333'
        
        # 使用 st.components.v1.html 繪製 SVG
        import streamlit.components.v1 as components
        
        svg_html = f'''
        <div style="text-align:center; padding:20px; background:#fff; border-radius:15px; box-shadow:0 4px 15px rgba(0,0,0,0.1);">
            <svg width="280" height="380" viewBox="0 0 280 380" xmlns="http://www.w3.org/2000/svg">
                <polygon points="140,10 170,50 110,50" fill="{head_fill}" stroke="#f1c40f" stroke-width="3"/>
                <text x="140" y="38" text-anchor="middle" fill="{head_text}" font-size="10" font-weight="bold">頭腦</text>
                <polygon points="140,55 170,95 110,95" fill="{ajna_fill}" stroke="#2ecc71" stroke-width="3"/>
                <text x="140" y="82" text-anchor="middle" fill="{ajna_text}" font-size="10" font-weight="bold">邏輯</text>
                <rect x="105" y="100" width="70" height="35" rx="5" fill="{throat_fill}" stroke="#3498db" stroke-width="3"/>
                <text x="140" y="123" text-anchor="middle" fill="{throat_text}" font-size="10" font-weight="bold">喉嚨</text>
                <polygon points="140,145 180,185 140,225 100,185" fill="{g_fill}" stroke="#f1c40f" stroke-width="3"/>
                <text x="140" y="190" text-anchor="middle" fill="{g_text}" font-size="10" font-weight="bold">G中心</text>
                <polygon points="65,165 90,185 65,205" fill="{ego_fill}" stroke="#e74c3c" stroke-width="3"/>
                <text x="52" y="189" text-anchor="middle" fill="#333" font-size="7">意志力</text>
                <polygon points="215,165 190,185 215,205" fill="{spleen_fill}" stroke="#1abc9c" stroke-width="3"/>
                <text x="228" y="189" text-anchor="middle" fill="#333" font-size="7">脾</text>
                <polygon points="180,235 215,275 180,315 145,275" fill="{solar_fill}" stroke="#9b59b6" stroke-width="3"/>
                <text x="180" y="280" text-anchor="middle" fill="{solar_text}" font-size="9" font-weight="bold">情緒</text>
                <rect x="100" y="235" width="75" height="50" rx="5" fill="{sacral_fill}" stroke="#e74c3c" stroke-width="3"/>
                <text x="138" y="265" text-anchor="middle" fill="{sacral_text}" font-size="10" font-weight="bold">薦骨</text>
                <rect x="100" y="300" width="75" height="35" rx="5" fill="{root_fill}" stroke="#e67e22" stroke-width="3"/>
                <text x="138" y="323" text-anchor="middle" fill="{root_text}" font-size="10" font-weight="bold">根</text>
                <line x1="140" y1="50" x2="140" y2="55" stroke="#2ecc71" stroke-width="4"/>
                <line x1="140" y1="95" x2="140" y2="100" stroke="#3498db" stroke-width="4"/>
                <line x1="140" y1="135" x2="140" y2="145" stroke="#3498db" stroke-width="4"/>
                <line x1="140" y1="225" x2="138" y2="235" stroke="#f1c40f" stroke-width="4"/>
                <line x1="138" y1="285" x2="138" y2="300" stroke="#e74c3c" stroke-width="4"/>
                <line x1="175" y1="265" x2="180" y2="255" stroke="#9b59b6" stroke-width="4"/>
            </svg>
            <p style="color:#888; font-size:12px; margin-top:10px;">■ 有顏色 = 被定義 | □ 白色 = 未定義</p>
        </div>
        '''
        components.html(svg_html, height=450)


    
    with col_info:
        st.markdown(f"""
        <div style="background:linear-gradient(145deg,{info['color']}33,{info['color']}11); border:3px solid {info['color']}; border-radius:20px; padding:25px; text-align:center;">
            <div style="font-size:50px;">{info['icon']}</div>
            <h2 style="color:{info['color']}; margin:10px 0;">{hd['type']}</h2>
            <p style="color:#666;">{info['desc']}</p>
            <div style="background:{info['color']}; color:white; display:inline-block; padding:8px 20px; border-radius:15px; margin:10px 0;">策略: {info['strategy']}</div>
            <p style="color:#6b4c9a;"><b>人生角色: {hd['profile']}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 能量中心狀態")
        for name, data in centers.items():
            status = "🟢 已定義" if data['defined'] else "⚪ 未定義"
            st.markdown(f"**{name}** {status} - {data['desc']}")
    
    st.markdown("""
---
## ✨ 你的天生設計

作為**生產者**，你擁有地球上約 70% 人口的能量類型！你的**薦骨中心**是被定義的（紅色方塊），這意味著你有源源不絕的生命力能量。

### � 已定義的中心 (你的固定特質)
- **薦骨** 🔴 - 你有強大的工作能量，可以持續工作很長時間
- **情緒** 🟣 - 你是情緒型權威，重大決定需要等情緒清明
- **根** 🟠 - 你有內在動力和壓力驅動力

### ⚪ 未定義的中心 (你的學習領域)
- **頭腦** - 容易被他人的想法影響，需要辨別真正的靈感
- **意志力** - 不需要證明自己的價值
- **脾** - 對環境敏感，需要注意健康訊號
""")


# ========== Tab 4: 占星 ==========
with tab4:
    st.header("⭐ 西洋占星")
    st.info("📌 **Demo**: 摩羯座太陽 + 獅子座上升")
    
    astro = st.session_state['astro_data']
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h2 style='text-align:center;'>☀️ 太陽星座<br><span style='color:#6b4c9a;'>{astro['sun']}</span></h2>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h2 style='text-align:center;'>⬆️ 上升星座<br><span style='color:#e94560;'>{astro['ascendant']}</span></h2>", unsafe_allow_html=True)
    
    st.markdown("### 🌌 行星位置")
    cols = st.columns(4)
    for i, (planet, sign) in enumerate(astro['planets'].items()):
        with cols[i % 4]:
            st.markdown(f"<div class='planet-card'><b>{planet}</b><br>{sign}</div>", unsafe_allow_html=True)
    
    st.markdown("""
---
## 🌟 星盤解讀

### 摩羯座太陽 ♑
您的核心是務實、有野心、追求成就的摩羯能量。您做事有計畫、有耐心，願意為長遠目標付出努力。

### 獅子座上升 ♌
您給人的第一印象是**自信、大方、有領導氣質**的！即使內心是務實的摩羯，外表卻散發著獅子的王者風範。

### 🎭 這個組合意味著...
- 外表看起來自信有魄力
- 內心其實很謹慎務實
- 適合擔任領導者角色
- 事業上容易有成就
""")

# ========== Tab 5: 紫微 ==========
with tab5:
    st.header("💜 紫微斗數")
    st.info("📌 **Demo**: 紫微坐命宮")
    
    ziwei = st.session_state['ziwei_data']
    
    st.markdown(f"### ⭐ 命宮主星: <span style='color:#6c5ce7; font-size:28px;'>{ziwei['main_star']}</span>", unsafe_allow_html=True)
    st.write(f"**命主**: {ziwei['mingzhu']} | **身主**: {ziwei['shenzhu']}")
    
    st.markdown("### 🏛️ 十二宮")
    cols = st.columns(4)
    for i, (palace, star) in enumerate(ziwei['palaces'].items()):
        with cols[i % 4]:
            st.markdown(f"<div class='ziwei-palace'><b>{palace}</b><br>{star}</div>", unsafe_allow_html=True)
    
    st.markdown("""
---
## 💜 命格解析

### 紫微坐命
**紫微星** 是斗數中的帝王星！紫微坐命的人天生具有**領導格局**，氣質高貴，有主見有魄力。

### 🌟 性格特質
- 👑 天生的領導者氣質
- 🎯 有主見、有決斷力
- 💼 適合擔任管理職位
- ⚠️ 注意不要太過高傲

### 💰 財運分析
天同在財帛宮，代表財運平穩，適合穩定收入的工作。不建議高風險投資！

### 💕 感情分析
太陽在夫妻宮，代表另一半可能是陽光、開朗的類型。感情運勢正面！
""")

# ========== Tab 6: 整合分析 ==========
with tab6:
    st.header("🌐 多系統整合分析")
    st.info("📌 **Demo**: 顯示預設的整合分析結果")
    
    st.markdown("### 📋 已載入的系統資料")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.success("🃏 塔羅 ✓")
    with col2: st.success("☯️ 八字 ✓")
    with col3: st.success("🧬 人類圖 ✓")
    with col4: st.success("⭐ 占星 ✓")
    with col5: st.success("💜 紫微 ✓")
    
    st.markdown("### ❓ 問題: 今年適合換工作嗎？")
    
    st.markdown("---")
    st.markdown(DEMO_AI_RESPONSE)

st.markdown("---")
st.markdown("<p style='text-align:center; color:#888;'>🔮 AI 身心靈顧問 | 🎭 Demo Mode | 僅供娛樂參考</p>", unsafe_allow_html=True)
