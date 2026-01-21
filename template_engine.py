"""混合模板引擎：模板優先 + AI 備援"""
import logging
import json

logger = logging.getLogger(__name__)

# 導入模板
from bazi_templates import generate_bazi_interpretation
from tarot_templates import generate_tarot_interpretation, select_spread
from astrology_templates import generate_astrology_interpretation
from ziwei_templates import generate_ziwei_interpretation
from humandesign_templates import generate_hd_interpretation

# 我們不能直接在此導入 api.generate_ai_content，因為 api.py 可能會導入這檔案，造成循環依賴。
# 所以採用延遲導入 (lazy import) 或是在 api.py 中注入函數。
# 但為了簡單起見，我們這裡使用延遲導入。

def _ai_fallback(prompt, fallback_text):
    """內部 AI 備援函數"""
    try:
        # 延遲導入以避免循環依賴
        from api import generate_ai_content, AI_INTEGRATION_RESPONSE
        
        # 如果 prompt 是多系統整合，可能比較複雜，直接回傳預設回應作為 fallback
        if "整合分析" in prompt:
             return AI_INTEGRATION_RESPONSE, "ai_fallback"

        logger.info(f"🔄 觸發 AI 備援: {prompt[:30]}...")
        content, _ = generate_ai_content(prompt, fallback_text)
        return content, "ai"
    except ImportError:
        logger.error("無法導入 api 模組，回傳純 fallback 文字")
        return fallback_text, "fallback_static"
    except Exception as e:
        logger.error(f"AI 備援失敗: {e}")
        return fallback_text, "fallback_static"

def get_bazi_text(chart):
    """取得八字解讀 (模板優先)"""
    try:
        return generate_bazi_interpretation(chart), "template"
    except Exception as e:
        logger.warning(f"八字模板失敗: {e}")
        dm = chart.get('day_master', '甲')
        prompt = f"作為八字大師，分析日主{dm}的命盤特質。"
        return _ai_fallback(prompt, f"{dm}日主具有獨特特質。")

def get_tarot_text(question, cards, positions):
    """取得塔羅解讀 (模板優先)"""
    try:
        # 如果是單張牌抽牌 (有的 API 呼叫可能只有一張)，這裡也能處理
        return generate_tarot_interpretation(question, cards, positions), "template"
    except Exception as e:
        logger.warning(f"塔羅模板失敗: {e}")
        card_names = [c.get('name','') for c in cards]
        prompt = f"解讀塔羅牌組合：{card_names}，問題：{question}"
        return _ai_fallback(prompt, "這組牌象徵著轉變與機會。")

def get_tarot_spread(question):
    """選擇牌陣 (純規則)"""
    # 牌陣選擇是簡單規則，不需要 AI 備援
    return select_spread(question)

def get_astrology_text(sun, moon=None, asc=None):
    """取得占星解讀 (模板優先)"""
    try:
        return generate_astrology_interpretation(sun, moon, asc), "template"
    except Exception as e:
        logger.warning(f"占星模板失敗: {e}")
        prompt = f"分析太陽{sun}、月亮{moon}、上升{asc}的星盤特質。"
        return _ai_fallback(prompt, "您的星盤顯示獨特潛能。")

def get_ziwei_text(main_star, palaces=None):
    """取得紫微解讀 (模板優先)"""
    try:
        return generate_ziwei_interpretation(main_star, palaces), "template"
    except Exception as e:
        logger.warning(f"紫微模板失敗: {e}")
        prompt = f"分析{main_star}坐命的紫微命盤特質。"
        return _ai_fallback(prompt, f"{main_star}星帶來獨特格局。")

def get_hd_text(hd_type, profile=None, authority=None, centers=None):
    """取得人類圖解讀 (模板優先)"""
    try:
        return generate_hd_interpretation(hd_type, profile, authority, centers), "template"
    except Exception as e:
        logger.warning(f"人類圖模板失敗: {e}")
        prompt = f"分析{hd_type}類型、{profile}人生角色的人類圖特質。"
        return _ai_fallback(prompt, f"您是{hd_type}類型，擁有獨特設計。")
