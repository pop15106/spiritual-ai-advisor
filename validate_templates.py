
import sys
import os

# 加至 path
sys.path.append(os.getcwd())

from template_engine import (
    get_bazi_text, get_tarot_text, get_tarot_spread,
    get_astrology_text, get_ziwei_text, get_hd_text
)

def test_bazi():
    print("\n[測試八字]")
    chart = {'day_master': '甲', 'pillars': {'month': {'zhi': '寅'}}}
    res, src = get_bazi_text(chart)
    print(f"來源: {src}")
    print(f"內容長度: {len(res)}")
    print(f"預覽: {res[:50]}...")

def test_tarot():
    print("\n[測試塔羅]")
    q = "我的事業發展？"
    spread, pos = get_tarot_spread(q)
    print(f"牌陣: {spread}, 位置: {pos}")
    
    cards = [{"name": "愚者", "reversed": False}, {"name": "魔術師", "reversed": True}]
    res, src = get_tarot_text(q, cards, pos[:2])
    print(f"來源: {src}")
    print(f"內容長度: {len(res)}")
    print(f"預覽: {res[:50]}...")

def test_astrology():
    print("\n[測試占星]")
    res, src = get_astrology_text("獅子座", "巨蟹座", "天蠍座")
    print(f"來源: {src}")
    print(f"內容長度: {len(res)}")
    print(f"預覽: {res[:50]}...")

def test_ziwei():
    print("\n[測試紫微]")
    res, src = get_ziwei_text("紫微", {"命宮": "紫微", "財帛宮": "武曲"})
    print(f"來源: {src}")
    print(f"內容長度: {len(res)}")
    print(f"預覽: {res[:50]}...")

def test_hd():
    print("\n[測試人類圖]")
    res, src = get_hd_text("生產者", "3/5", "薦骨權威")
    print(f"來源: {src}")
    print(f"內容長度: {len(res)}")
    print(f"預覽: {res[:50]}...")

if __name__ == "__main__":
    test_bazi()
    test_tarot()
    test_astrology()
    test_ziwei()
    test_hd()
    print("\n✅ 所有模組測試完成！")
