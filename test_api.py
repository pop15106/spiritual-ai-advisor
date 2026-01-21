"""
Spiritual AI Advisor - API 自動測試腳本
========================================
測試所有 API 端點的功能狀況
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

# 測試結果統計
results = {
    "passed": 0,
    "failed": 0,
    "errors": []
}

def log_result(test_name, success, message="", details=None):
    """記錄測試結果"""
    if success:
        results["passed"] += 1
        print(f"✅ PASS: {test_name}")
        if details:
            print(f"   詳情: {details}")
    else:
        results["failed"] += 1
        results["errors"].append({"test": test_name, "message": message})
        print(f"❌ FAIL: {test_name}")
        print(f"   錯誤: {message}")

def test_health_check():
    """測試健康檢查端點"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                log_result("健康檢查 (/api/health)", True, details="後端服務運行正常")
                return True
        log_result("健康檢查 (/api/health)", False, "API 未返回健康狀態")
        return False
    except requests.exceptions.ConnectionError:
        log_result("健康檢查 (/api/health)", False, "無法連接到後端服務，請確認已啟動 python api.py")
        return False
    except Exception as e:
        log_result("健康檢查 (/api/health)", False, str(e))
        return False

def test_tarot_draw():
    """測試塔羅抽牌"""
    try:
        # 需要設定 Content-Type
        headers = {"Content-Type": "application/json"}
        payload = {"count": 3}
        response = requests.post(f"{BASE_URL}/api/tarot/draw", json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            cards = data.get("cards", [])
            if len(cards) == 3:
                log_result("塔羅抽牌 (/api/tarot/draw)", True, 
                          details=f"抽到: {', '.join([c['name'] for c in cards])}")
                return True
            log_result("塔羅抽牌 (/api/tarot/draw)", False, f"應返回3張牌，實際返回 {len(cards)} 張")
            return False
        log_result("塔羅抽牌 (/api/tarot/draw)", False, f"HTTP {response.status_code}")
        return False
    except Exception as e:
        log_result("塔羅抽牌 (/api/tarot/draw)", False, str(e))
        return False

def test_tarot_cards():
    """測試取得全部塔羅牌"""
    try:
        response = requests.get(f"{BASE_URL}/api/tarot/cards", timeout=5)
        if response.status_code == 200:
            data = response.json()
            cards = data.get("cards", [])
            if len(cards) >= 22:  # 至少有22張大牌
                log_result("塔羅牌列表 (/api/tarot/cards)", True, details=f"共 {len(cards)} 張牌")
                return True
            log_result("塔羅牌列表 (/api/tarot/cards)", False, f"牌數不足: {len(cards)}")
            return False
        log_result("塔羅牌列表 (/api/tarot/cards)", False, f"HTTP {response.status_code}")
        return False
    except Exception as e:
        log_result("塔羅牌列表 (/api/tarot/cards)", False, str(e))
        return False

def test_bazi_calculate():
    """測試八字排盤"""
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "birthDate": "1990-05-15",
            "birthHour": 5,  # 辰時
            "gender": "male"
        }
        response = requests.post(f"{BASE_URL}/api/bazi/calculate", json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                day_gan = data.get("day_gan", "")
                log_result("八字排盤 (/api/bazi/calculate)", True, 
                          details=f"日主: {day_gan}, 農曆: {data.get('lunar', '')}")
                return True
            log_result("八字排盤 (/api/bazi/calculate)", False, data.get("error", "未知錯誤"))
            return False
        log_result("八字排盤 (/api/bazi/calculate)", False, f"HTTP {response.status_code}")
        return False
    except Exception as e:
        log_result("八字排盤 (/api/bazi/calculate)", False, str(e))
        return False

def test_human_design_info():
    """測試人類圖 Demo"""
    try:
        response = requests.get(f"{BASE_URL}/api/humandesign/info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("type"):
                log_result("人類圖Demo (/api/humandesign/info)", True, details=f"類型: {data.get('type')}")
                return True
            log_result("人類圖Demo (/api/humandesign/info)", False, "缺少類型數據")
            return False
        log_result("人類圖Demo (/api/humandesign/info)", False, f"HTTP {response.status_code}")
        return False
    except Exception as e:
        log_result("人類圖Demo (/api/humandesign/info)", False, str(e))
        return False

def test_human_design_calculate():
    """測試人類圖計算"""
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "birthDate": "1990-05-15",
            "birthTime": "10:30"
        }
        response = requests.post(f"{BASE_URL}/api/humandesign/calculate", json=payload, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            hd_data = data.get("hd_data", {})
            hd_type = hd_data.get("type", "")
            centers = hd_data.get("centers", {})
            if hd_type and centers:
                defined_count = sum(1 for c in centers.values() if c.get("defined"))
                log_result("人類圖計算 (/api/humandesign/calculate)", True, 
                          details=f"類型: {hd_type}, 定義中心: {defined_count}個")
                return True
            log_result("人類圖計算 (/api/humandesign/calculate)", False, "缺少類型或中心數據")
            return False
        log_result("人類圖計算 (/api/humandesign/calculate)", False, f"HTTP {response.status_code}")
        return False
    except Exception as e:
        log_result("人類圖計算 (/api/humandesign/calculate)", False, str(e))
        return False

def test_astrology_demo():
    """測試占星 Demo"""
    try:
        response = requests.get(f"{BASE_URL}/api/astrology/chart", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("sun"):
                log_result("占星Demo (/api/astrology/chart)", True, details=f"太陽: {data.get('sun')}")
                return True
            log_result("占星Demo (/api/astrology/chart)", False, "缺少太陽數據")
            return False
        log_result("占星Demo (/api/astrology/chart)", False, f"HTTP {response.status_code}")
        return False
    except Exception as e:
        log_result("占星Demo (/api/astrology)", False, str(e))
        return False

def test_astrology_calculate():
    """測試占星盤計算"""
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "birthDate": "1990-05-15",
            "birthTime": "10:30",
            "birthLat": 25.0169,
            "birthLon": 121.4628,
            "birthCity": "新北市"
        }
        response = requests.post(f"{BASE_URL}/api/astrology/calculate", json=payload, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                planets = data.get("planets", {})
                asc = data.get("ascendant", {})
                log_result("占星盤計算 (/api/astrology/calculate)", True, 
                          details=f"太陽: {planets.get('太陽', '')[:10]}..., 上升: {asc.get('name', '')}")
                return True
            log_result("占星盤計算 (/api/astrology/calculate)", False, data.get("error", "未知錯誤"))
            return False
        log_result("占星盤計算 (/api/astrology/calculate)", False, f"HTTP {response.status_code}")
        return False
    except Exception as e:
        log_result("占星盤計算 (/api/astrology/calculate)", False, str(e))
        return False

def test_ziwei_demo():
    """測試紫微 Demo"""
    try:
        response = requests.get(f"{BASE_URL}/api/ziwei/chart", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("main_star"):
                log_result("紫微Demo (/api/ziwei/chart)", True, details=f"主星: {data.get('main_star')}")
                return True
            log_result("紫微Demo (/api/ziwei/chart)", False, "缺少主星數據")
            return False
        log_result("紫微Demo (/api/ziwei/chart)", False, f"HTTP {response.status_code}")
        return False
    except Exception as e:
        log_result("紫微Demo (/api/ziwei)", False, str(e))
        return False

def test_ziwei_calculate():
    """測試紫微斗數計算"""
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "birthDate": "1990-05-15",
            "birthHour": 5,
            "gender": "male"
        }
        response = requests.post(f"{BASE_URL}/api/ziwei/calculate", json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            zw_data = data.get("zw_data", {})
            main_star = zw_data.get("main_star", "")
            palaces = zw_data.get("palaces", {})
            if main_star or palaces:
                log_result("紫微斗數計算 (/api/ziwei/calculate)", True, 
                          details=f"命主星: {main_star}")
                return True
            log_result("紫微斗數計算 (/api/ziwei/calculate)", False, "缺少主星或宮位數據")
            return False
        log_result("紫微斗數計算 (/api/ziwei/calculate)", False, f"HTTP {response.status_code}")
        return False
    except Exception as e:
        log_result("紫微斗數計算 (/api/ziwei/calculate)", False, str(e))
        return False

def test_integration():
    """測試多系統整合分析"""
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "systems": ["tarot", "bazi", "astrology"],
            "question": "我的事業發展如何？",
            "stream": False
        }
        response = requests.post(f"{BASE_URL}/api/integration/analyze", json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            data = response.json()
            analysis = data.get("analysis", "")
            if analysis:
                log_result("多系統整合 (/api/integration/analyze)", True, 
                          details=f"分析長度: {len(analysis)} 字元")
                return True
            log_result("多系統整合 (/api/integration/analyze)", False, "缺少分析結果")
            return False
        log_result("多系統整合 (/api/integration/analyze)", False, f"HTTP {response.status_code}")
        return False
    except Exception as e:
        log_result("多系統整合 (/api/integration/analyze)", False, str(e))
        return False

def print_summary():
    """打印測試摘要"""
    total = results["passed"] + results["failed"]
    print("\n" + "="*60)
    print("📊 測試摘要")
    print("="*60)
    print(f"總測試數: {total}")
    print(f"✅ 通過: {results['passed']}")
    print(f"❌ 失敗: {results['failed']}")
    
    if results["errors"]:
        print("\n📋 失敗的測試:")
        for err in results["errors"]:
            print(f"  • {err['test']}: {err['message']}")
    
    success_rate = (results['passed'] / total * 100) if total > 0 else 0
    print(f"\n🎯 成功率: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🎉 所有測試通過！")
    elif success_rate >= 80:
        print("⚠️ 大部分功能正常，部分需要檢查")
    else:
        print("🚨 多個功能異常，需要排查")

def run_all_tests():
    """執行所有測試"""
    print("🔮 AI 身心靈顧問 - API 自動測試")
    print("="*60)
    print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"後端地址: {BASE_URL}")
    print("="*60 + "\n")
    
    # 首先測試連接
    if not test_health_check():
        print("\n⚠️ 後端服務未啟動，跳過後續測試")
        print("請先執行: cd spiritual_ai_advisor && python api.py")
        print_summary()
        return
    
    print()
    
    # 塔羅測試
    print("🃏 塔羅占卜測試:")
    print("-"*40)
    test_tarot_draw()
    test_tarot_cards()
    print()
    
    # 八字測試
    print("☯️ 八字命理測試:")
    print("-"*40)
    test_bazi_calculate()
    print()
    
    # 人類圖測試
    print("🧬 人類圖測試:")
    print("-"*40)
    test_human_design_info()
    test_human_design_calculate()
    print()
    
    # 占星測試
    print("⭐ 西洋占星測試:")
    print("-"*40)
    test_astrology_demo()
    test_astrology_calculate()
    print()
    
    # 紫微測試
    print("💜 紫微斗數測試:")
    print("-"*40)
    test_ziwei_demo()
    test_ziwei_calculate()
    print()
    
    # 整合測試
    print("🌐 多系統整合測試:")
    print("-"*40)
    test_integration()
    
    print_summary()

if __name__ == "__main__":
    run_all_tests()
