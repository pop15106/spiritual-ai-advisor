"""
Test py-iztro library
"""
from py_iztro import Astro

# 1991-07-02, 未時(7), 男性
astro = Astro()
result = astro.by_solar('1991-7-2', 7, '男', language='zh-TW')

print("=== py-iztro 計算結果 ===")
print(f"命主: {result.soul}")
print(f"身主: {result.body}")
print(f"五行局: {result.five_elements_class}")
print()
print("=== 十二宮位 ===")
for p in result.palaces:
    stars = [s.name for s in p.major_stars]
    print(f"{p.name}: {stars}")
