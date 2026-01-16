"""
Test Case 2: 1991-7-1 未時 (Lunar 5/20)
Compare with Wenmo Tianji professional software
"""
from ziwei_calculator import calculate_ziwei_chart, DIZHI

# 1991-7-1 = 農曆五月二十日
result = calculate_ziwei_chart(
    lunar_year=1991,
    lunar_month=5,
    lunar_day=20,  # Day 20, not 21!
    shichen=7,     # 未時
    year_tiangan='辛',
    year_dizhi='未'
)

print("=== 測試案例 2: 1991-7-1 未時 (農曆五月二十日) ===")
print(f"命宮: {result['ming_palace']}")
print(f"身宮: {result['shen_palace']}")
print(f"五行局: {result['wuxing_ju']}")
print(f"命主: {result['ming_zhu']}")
print(f"身主: {result['shen_zhu']}")
print(f"紫微位置: {result['ziwei_position']}")
print()

# 專業軟體資料
pro_data = {
    '亥': ('命宮', '廉貞, 貪狼, 文曲'),
    '戌': ('兄弟宮', '太陰'),
    '酉': ('夫妻宮', '天府'),
    '申': ('子女宮', '無主星(左輔)'),
    '未': ('財帛宮', '紫微, 破軍'),
    '午': ('疾厄宮', '天機, 右弼'),
    '巳': ('遷移宮', '無主星'),
    '辰': ('交友宮', '太陽'),
    '卯': ('官祿宮', '武曲, 七殺, 文昌'),
    '寅': ('田宅宮', '天同, 天梁'),
    '丑': ('福德宮[身宮]', '天相'),
    '子': ('父母宮', '巨門'),
}

print("=== 十二宮比對 ===")
print(f"{'地支':4s} | {'我們計算':12s} | {'我們主星':20s} | {'專業軟體'}")
print("-" * 70)

for name, data in result['palaces'].items():
    dz = data['dizhi']
    stars = ', '.join(data['stars']) if data['stars'] else '無主星'
    pro_palace, pro_stars = pro_data.get(dz, ('?', '?'))
    match = 'OK' if name.replace('宮', '') in pro_palace else 'XX'
    print(f"{dz:4s} | {name:10s} {match} | {stars:20s} | {pro_stars}")
