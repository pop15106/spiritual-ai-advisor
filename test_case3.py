"""
Test Case 3: 1992-8-15 申時 (壬申年七月十七日)
Verify new grid layout and algorithm accuracy
"""
from ziwei_calculator import calculate_ziwei_chart, DIZHI

# 1992-8-15 = 農曆七月十七日
result = calculate_ziwei_chart(
    lunar_year=1992,
    lunar_month=7,
    lunar_day=17,
    shichen=8,  # 申時
    year_tiangan='壬',
    year_dizhi='申'
)

print("=== 測試案例 3: 1992-8-15 申時 (壬申年七月十七日) ===")
print(f"命宮: {result['ming_palace']}")
print(f"身宮: {result['shen_palace']}")
print(f"五行局: {result['wuxing_ju']}")
print(f"命主: {result['ming_zhu']}")
print(f"身主: {result['shen_zhu']}")
print()

# 專業軟體資料
pro_data = {
    '子': ('命宮', '貪狼'),
    '丑': ('父母宮', '天同, 巨門'),
    '寅': ('福德宮', '武曲, 天相'),
    '卯': ('田宅宮', '太陽, 天梁'),
    '辰': ('官祿宮[身宮]', '七殺'),
    '巳': ('交友宮', '天機'),
    '午': ('遷移宮', '紫微'),
    '未': ('疾厄宮', '無主星'),
    '申': ('財帛宮', '破軍'),
    '酉': ('子女宮', '無主星'),
    '戌': ('夫妻宮', '廉貞, 天府'),
    '亥': ('兄弟宮', '太陰'),
}

print("=== 對比驗證 ===")
match_count = 0
for name, data in result['palaces'].items():
    dz = data['dizhi']
    stars = ', '.join(data['stars']) if data['stars'] else '無主星'
    pro_palace, pro_stars = pro_data.get(dz, ('?', '?'))
    
    # 簡化比對
    palace_match = name in pro_palace or pro_palace.startswith(name)
    status = 'OK' if palace_match else 'XX'
    if palace_match:
        match_count += 1
    print(f"{dz} | {name:6s} {status} | {stars[:20]:20s} | {pro_stars}")

print(f"\n匹配: {match_count}/12")
