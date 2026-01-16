"""
Test ziwei_calculator with comprehensive output
"""
from ziwei_calculator import calculate_ziwei_chart, DIZHI

result = calculate_ziwei_chart(
    lunar_year=1991,
    lunar_month=5,
    lunar_day=21,
    shichen=7,  # 未時
    year_tiangan='辛',
    year_dizhi='未'
)

print("=== 計算結果 ===")
print(f"命宮地支: {result['ming_palace']}")
print(f"身宮地支: {result['shen_palace']}")
print(f"五行局: {result['wuxing_ju']}")
print(f"命主: {result['ming_zhu']}")
print(f"身主: {result['shen_zhu']}")
print(f"紫微位置: {result['ziwei_position']}")
print()
print("=== 我們的十二宮 vs 專業軟體 ===")
print("地支 | 我們的宮位 | 我們的主星 | 專業軟體")
print("-" * 60)

# 專業軟體資料
pro_data = {
    '亥': ('命宮', '巨門, 文曲'),
    '戌': ('兄弟宮', '貪狼'),
    '酉': ('夫妻宮', '太陰'),
    '申': ('子女宮', '紫微, 天府, 左輔'),
    '未': ('財帛宮', '天機'),
    '午': ('疾厄宮', '破軍, 右弼'),
    '巳': ('遷移宮', '太陽'),
    '辰': ('交友宮', '武曲'),
    '卯': ('官祿宮', '天同, 文昌'),
    '寅': ('田宅宮', '七殺'),
    '丑': ('福德宮', '天梁'),
    '子': ('父母宮', '廉貞, 天相'),
}

for name, data in result['palaces'].items():
    dz = data['dizhi']
    stars = ', '.join(data['stars']) if data['stars'] else '無'
    pro_palace, pro_stars = pro_data.get(dz, ('?', '?'))
    match = 'OK' if name == pro_palace else 'XX'
    print(f"{dz}({DIZHI.index(dz):2d}) | {name:6s} {match} | {stars:20s} | {pro_stars}")
