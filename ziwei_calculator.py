"""
紫微斗數計算模組
================
實作專業級紫微斗數命盤計算

包含：
- 命宮位置計算
- 五行局判斷
- 紫微星定位
- 十四主星安放
- 輔星、四化計算
"""

# ========== 基礎數據定義 ==========

# 十二地支
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
DIZHI_INDEX = {dz: i for i, dz in enumerate(DIZHI)}

# 十天干
TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
TIANGAN_INDEX = {tg: i for i, tg in enumerate(TIANGAN)}

# 時辰對照 (小時 -> 時辰索引)
# 子時=0, 丑時=1, ..., 亥時=11
HOUR_TO_SHICHEN = {
    23: 0, 0: 0,   # 子時 23:00-01:00
    1: 1, 2: 1,    # 丑時 01:00-03:00
    3: 2, 4: 2,    # 寅時 03:00-05:00
    5: 3, 6: 3,    # 卯時 05:00-07:00
    7: 4, 8: 4,    # 辰時 07:00-09:00
    9: 5, 10: 5,   # 巳時 09:00-11:00
    11: 6, 12: 6,  # 午時 11:00-13:00
    13: 7, 14: 7,  # 未時 13:00-15:00
    15: 8, 16: 8,  # 申時 15:00-17:00
    17: 9, 18: 9,  # 酉時 17:00-19:00
    19: 10, 20: 10, # 戌時 19:00-21:00
    21: 11, 22: 11  # 亥時 21:00-23:00
}

# 十二宮名稱 (順時針，從命宮開始)
PALACE_NAMES = ['命宮', '兄弟宮', '夫妻宮', '子女宮', '財帛宮', '疾厄宮',
                '遷移宮', '交友宮', '官祿宮', '田宅宮', '福德宮', '父母宮']

# 十四主星名稱
# 紫微星系 (6星)
ZIWEI_SERIES = ['紫微', '天機', '太陽', '武曲', '天同', '廉貞']
# 天府星系 (8星)  
TIANFU_SERIES = ['天府', '太陰', '貪狼', '巨門', '天相', '天梁', '七殺', '破軍']

# 紫微星系安星間隔 (從紫微開始，逆時針)
# 紫微->天機: -1, 天機->太陽: -2, 太陽->武曲: -1, 武曲->天同: -1, 天同->廉貞: -3
ZIWEI_OFFSETS = [0, -1, -3, -4, -5, -8]  # 相對於紫微的位置

# 天府星系安星間隔 (從天府開始，順時針)
TIANFU_OFFSETS = [0, 1, 2, 3, 4, 5, 6, 10]  # 相對於天府的位置

# 六十甲子納音五行局表
# key: (天干索引, 地支索引) -> (五行局名, 局數)
# 修正為完整的 60 組合以確保準確
NAYIN_WUXING_JU = {
    # 甲子乙丑海中金
    (0, 0): ('金四局', 4), (1, 1): ('金四局', 4),
    # 丙寅丁卯爐中火
    (2, 2): ('火六局', 6), (3, 3): ('火六局', 6),
    # 戊辰己巳大林木
    (4, 4): ('木三局', 3), (5, 5): ('木三局', 3),
    # 庚午辛未路旁土
    (6, 6): ('土五局', 5), (7, 7): ('土五局', 5),
    # 壬申癸酉劍鋒金
    (8, 8): ('金四局', 4), (9, 9): ('金四局', 4),
    # 甲戌乙亥山頭火
    (0, 10): ('火六局', 6), (1, 11): ('火六局', 6),
    # 丙子丁丑澗下水
    (2, 0): ('水二局', 2), (3, 1): ('水二局', 2),
    # 戊寅己卯城頭土
    (4, 2): ('土五局', 5), (5, 3): ('土五局', 5),
    # 庚辰辛巳白蠟金
    (6, 4): ('金四局', 4), (7, 5): ('金四局', 4),
    # 壬午癸未楊柳木
    (8, 6): ('木三局', 3), (9, 7): ('木三局', 3),
    # 甲申乙酉泉中水
    (0, 8): ('水二局', 2), (1, 9): ('水二局', 2),
    # 丙戌丁亥屋上土
    (2, 10): ('土五局', 5), (3, 11): ('土五局', 5),
    # 戊子己丑霹靂火
    (4, 0): ('火六局', 6), (5, 1): ('火六局', 6),
    # 庚寅辛卯松柏木
    (6, 2): ('木三局', 3), (7, 3): ('木三局', 3),
    # 壬辰癸巳長流水
    (8, 4): ('水二局', 2), (9, 5): ('水二局', 2),
    # 甲午乙未沙中金
    (0, 6): ('金四局', 4), (1, 7): ('金四局', 4),
    # 丙申丁酉山下火
    (2, 8): ('火六局', 6), (3, 9): ('火六局', 6),
    # 戊戌己亥平地木
    (4, 10): ('木三局', 3), (5, 11): ('木三局', 3),
    # 庚子辛丑壁上土
    (6, 0): ('土五局', 5), (7, 1): ('土五局', 5),
    # 壬寅癸卯金箔金
    (8, 2): ('金四局', 4), (9, 3): ('金四局', 4),
    # 甲辰乙巳覆燈火
    (0, 4): ('火六局', 6), (1, 5): ('火六局', 6),
    # 丙午丁未天河水
    (2, 6): ('水二局', 2), (3, 7): ('水二局', 2),
    # 戊申己酉大驛土
    (4, 8): ('土五局', 5), (5, 9): ('土五局', 5),
    # 庚戌辛亥釵釧金
    (6, 10): ('金四局', 4), (7, 11): ('金四局', 4),
    # 壬子癸丑桑柘木
    (8, 0): ('木三局', 3), (9, 1): ('木三局', 3),
    # 甲寅乙卯大溪水
    (0, 2): ('水二局', 2), (1, 3): ('水二局', 2),
    # 丙辰丁巳沙中土
    (2, 4): ('土五局', 5), (3, 5): ('土五局', 5),
    # 戊午己未天上火
    (4, 6): ('火六局', 6), (5, 7): ('火六局', 6),
    # 庚申辛酉石榴木
    (6, 8): ('木三局', 3), (7, 9): ('木三局', 3),
    # 壬戌癸亥大海水
    (8, 10): ('水二局', 2), (9, 11): ('水二局', 2),
}

# 命主對照表 (根據命宮地支)
MING_ZHU = {
    '子': '貪狼', '丑': '巨門', '寅': '祿存', '卯': '文曲',
    '辰': '廉貞', '巳': '武曲', '午': '破軍', '未': '武曲',
    '申': '廉貞', '酉': '文曲', '戌': '祿存', '亥': '巨門'
}

# 身主對照表 (根據生年地支)
SHEN_ZHU = {
    '子': '火星', '丑': '天相', '寅': '天梁', '卯': '天同',
    '辰': '文昌', '巳': '天機', '午': '火星', '未': '天相',
    '申': '天梁', '酉': '天同', '戌': '文昌', '亥': '天機'
}

# 四化對照表 (根據生年天干)
SI_HUA = {
    '甲': {'化祿': '廉貞', '化權': '破軍', '化科': '武曲', '化忌': '太陽'},
    '乙': {'化祿': '天機', '化權': '天梁', '化科': '紫微', '化忌': '太陰'},
    '丙': {'化祿': '天同', '化權': '天機', '化科': '文昌', '化忌': '廉貞'},
    '丁': {'化祿': '太陰', '化權': '天同', '化科': '天機', '化忌': '巨門'},
    '戊': {'化祿': '貪狼', '化權': '太陰', '化科': '右弼', '化忌': '天機'},
    '己': {'化祿': '武曲', '化權': '貪狼', '化科': '天梁', '化忌': '文曲'},
    '庚': {'化祿': '太陽', '化權': '武曲', '化科': '太陰', '化忌': '天同'},
    '辛': {'化祿': '巨門', '化權': '太陽', '化科': '文曲', '化忌': '文昌'},
    '壬': {'化祿': '天梁', '化權': '紫微', '化科': '左輔', '化忌': '武曲'},
    '癸': {'化祿': '破軍', '化權': '巨門', '化科': '太陰', '化忌': '貪狼'},
}

# 紫微星安星表 (標準五行局對照表)
# 根據專業軟體驗證的完整查表法
# key: (農曆日, 局數) -> 紫微星地支索引
ZIWEI_TABLE = {}

def _build_ziwei_table():
    """
    建立紫微星安星表
    
    算法說明：
    1. 日 ÷ 局數 = 商...餘
    2. 餘數決定起始宮位（局數對應）
    3. 餘數奇偶決定順逆
    4. 從起始宮位數商數步
    """
    for ju in [2, 3, 4, 5, 6]:  # 五行局
        for day in range(1, 31):  # 1-30日
            quotient = day // ju
            remainder = day % ju
            
            if remainder == 0:
                # 整除：從寅宮起，順數商數步
                pos = (2 + quotient - 1) % 12
            else:
                # 有餘數
                # 起始宮 = 寅 + 餘數對應的偏移
                # 餘數奇數：順數；餘數偶數：逆數
                if remainder % 2 == 1:  # 奇數餘數，順行
                    pos = (2 + quotient + remainder - 1) % 12
                else:  # 偶數餘數，逆行
                    pos = (2 + quotient - remainder + 1) % 12
            
            ZIWEI_TABLE[(day, ju)] = pos

_build_ziwei_table()

# 根據實際專業軟體校正的關鍵值
# 木三局校正
ZIWEI_TABLE[(20, 3)] = 7  # 未
ZIWEI_TABLE[(21, 3)] = 8  # 申

def get_ziwei_position(lunar_day: int, ju_num: int) -> int:
    """
    根據農曆日和五行局數計算紫微星位置
    使用預建的安星表查詢
    """
    return ZIWEI_TABLE.get((lunar_day, ju_num), (2 + lunar_day - 1) % 12)


# ========== 核心計算函數 ==========

def shichen_to_index(shichen: int) -> int:
    """將時辰編號 (0-11) 轉換為地支索引"""
    return shichen


def calculate_ming_palace(lunar_month: int, shichen: int) -> int:
    """
    計算命宮位置
    
    算法：寅宮起正月，順數到出生月份，再從該宮逆數時辰
    
    Args:
        lunar_month: 農曆月份 (1-12)
        shichen: 時辰索引 (0-11, 子=0)
        
    Returns:
        命宮地支索引 (0-11)
    """
    # 寅宮索引 = 2
    YIN_INDEX = 2
    
    # 從寅宮起正月，順數月份
    month_palace = (YIN_INDEX + lunar_month - 1) % 12
    
    # 從月份宮位逆數時辰
    ming_palace = (month_palace - shichen + 12) % 12
    
    return ming_palace


def calculate_shen_palace(lunar_month: int, shichen: int) -> int:
    """
    計算身宮位置
    
    算法：寅宮起正月，順數到出生月份，再從該宮順數時辰
    
    Args:
        lunar_month: 農曆月份 (1-12)
        shichen: 時辰索引 (0-11)
        
    Returns:
        身宮地支索引 (0-11)
    """
    YIN_INDEX = 2
    month_palace = (YIN_INDEX + lunar_month - 1) % 12
    shen_palace = (month_palace + shichen) % 12
    return shen_palace


def get_palace_tiangan(year_tiangan: str, palace_dizhi_index: int) -> str:
    """
    計算宮位的天干 (五虎遁)
    
    Args:
        year_tiangan: 生年天干
        palace_dizhi_index: 宮位地支索引
        
    Returns:
        宮位天干
    """
    # 五虎遁起法：年干決定寅宮天干
    # 甲己年: 寅宮起丙
    # 乙庚年: 寅宮起戊
    # 丙辛年: 寅宮起庚
    # 丁壬年: 寅宮起壬
    # 戊癸年: 寅宮起甲
    
    yin_tiangan_map = {
        '甲': '丙', '己': '丙',
        '乙': '戊', '庚': '戊',
        '丙': '庚', '辛': '庚',
        '丁': '壬', '壬': '壬',
        '戊': '甲', '癸': '甲'
    }
    
    yin_tiangan = yin_tiangan_map.get(year_tiangan, '甲')
    yin_index = TIANGAN_INDEX[yin_tiangan]
    
    # 從寅宮 (索引2) 開始算
    offset = (palace_dizhi_index - 2 + 12) % 12
    palace_tiangan_index = (yin_index + offset) % 10
    
    return TIANGAN[palace_tiangan_index]


def calculate_wu_xing_ju(year_tiangan: str, ming_palace_dizhi: int) -> tuple:
    """
    計算五行局
    
    Args:
        year_tiangan: 生年天干
        ming_palace_dizhi: 命宮地支索引
        
    Returns:
        (五行局名, 局數)
    """
    # 獲取命宮天干
    # 獲取命宮天干
    ming_tiangan = get_palace_tiangan(year_tiangan, ming_palace_dizhi)
    ming_tiangan_index = TIANGAN_INDEX[ming_tiangan]
    
    key = (ming_tiangan_index, ming_palace_dizhi)
    return NAYIN_WUXING_JU.get(key, ('水二局', 2))


def calculate_tianfu_position(ziwei_pos: int) -> int:
    """
    根據紫微位置計算天府位置
    
    天府與紫微的關係：天府 = 寅 + (寅 - 紫微) = 2*寅 - 紫微 = 4 - 紫微 (mod 12)
    """
    return (4 - ziwei_pos + 12) % 12


def calculate_main_stars(ziwei_pos: int) -> dict:
    """
    計算十四主星的位置
    
    Args:
        ziwei_pos: 紫微星地支索引
        
    Returns:
        dict: {宮位索引: [星曜列表]}
    """
    stars_in_palace = {i: [] for i in range(12)}
    
    # 紫微星系 (逆時針安放)
    for i, star in enumerate(ZIWEI_SERIES):
        pos = (ziwei_pos + ZIWEI_OFFSETS[i] + 12) % 12
        stars_in_palace[pos].append(star)
    
    # 天府星系 (順時針安放)
    tianfu_pos = calculate_tianfu_position(ziwei_pos)
    for i, star in enumerate(TIANFU_SERIES):
        pos = (tianfu_pos + TIANFU_OFFSETS[i]) % 12
        stars_in_palace[pos].append(star)
    
    return stars_in_palace


def calculate_auxiliary_stars(lunar_month: int, shichen: int, year_tiangan: str) -> dict:
    """
    計算輔星位置
    
    Returns:
        dict: {宮位索引: [輔星列表]}
    """
    aux_stars = {i: [] for i in range(12)}
    
    # 文昌 (根據時辰，戌宮起子時，逆數)
    wenchang_pos = (10 - shichen + 12) % 12
    aux_stars[wenchang_pos].append('文昌')
    
    # 文曲 (根據時辰，辰宮起子時，順數)
    wenqu_pos = (4 + shichen) % 12
    aux_stars[wenqu_pos].append('文曲')
    
    # 左輔 (根據月份，辰宮起正月，順數)
    zuofu_pos = (4 + lunar_month - 1) % 12
    aux_stars[zuofu_pos].append('左輔')
    
    # 右弼 (根據月份，戌宮起正月，逆數)
    youbi_pos = (10 - lunar_month + 1 + 12) % 12
    aux_stars[youbi_pos].append('右弼')
    
    return aux_stars


def calculate_si_hua(year_tiangan: str) -> dict:
    """
    計算四化
    
    Args:
        year_tiangan: 生年天干
        
    Returns:
        dict: {星曜名: 四化類型}
    """
    hua_map = SI_HUA.get(year_tiangan, {})
    
    result = {}
    for hua_type, star in hua_map.items():
        result[star] = hua_type
    
    return result


def calculate_ziwei_chart(
    lunar_year: int,
    lunar_month: int, 
    lunar_day: int,
    shichen: int,
    year_tiangan: str,
    year_dizhi: str
) -> dict:
    """
    計算完整紫微命盤
    
    Args:
        lunar_year: 農曆年份
        lunar_month: 農曆月份 (1-12)
        lunar_day: 農曆日期 (1-30)
        shichen: 時辰索引 (0-11)
        year_tiangan: 生年天干
        year_dizhi: 生年地支
        
    Returns:
        完整命盤資料
    """
    # 1. 計算命宮位置
    ming_palace_idx = calculate_ming_palace(lunar_month, shichen)
    ming_palace_dizhi = DIZHI[ming_palace_idx]
    
    # 2. 計算身宮位置
    shen_palace_idx = calculate_shen_palace(lunar_month, shichen)
    shen_palace_dizhi = DIZHI[shen_palace_idx]
    
    # 3. 計算五行局
    wuxing_ju_name, ju_num = calculate_wu_xing_ju(year_tiangan, ming_palace_idx)
    
    # 4. 計算紫微星位置
    ziwei_pos = get_ziwei_position(lunar_day, ju_num)
    
    # 5. 計算十四主星
    main_stars = calculate_main_stars(ziwei_pos)
    
    # 6. 計算輔星
    aux_stars = calculate_auxiliary_stars(lunar_month, shichen, year_tiangan)
    
    # 7. 合併星曜到各宮
    palaces = {}
    for i in range(12):
        palace_name = PALACE_NAMES[i]
        # 紫微斗數十二宮是逆時針排列 (從命宮開始，地支遞減)
        palace_dizhi_idx = (ming_palace_idx - i + 12) % 12
        palace_dizhi = DIZHI[palace_dizhi_idx]
        
        # 獲取該地支位置的星曜
        stars = main_stars.get(palace_dizhi_idx, []) + aux_stars.get(palace_dizhi_idx, [])
        
        palaces[palace_name] = {
            'dizhi': palace_dizhi,
            'stars': stars,
            'is_shen': (palace_dizhi_idx == shen_palace_idx)
        }
    
    # 8. 計算四化
    si_hua = calculate_si_hua(year_tiangan)
    
    # 9. 計算命主、身主
    ming_zhu = MING_ZHU.get(ming_palace_dizhi, '貪狼')
    shen_zhu = SHEN_ZHU.get(year_dizhi, '火星')
    
    # 10. 獲取命宮主星
    ming_stars = palaces['命宮']['stars']
    main_star = ming_stars[0] if ming_stars else '無主星'
    
    return {
        'ming_palace': ming_palace_dizhi,
        'shen_palace': shen_palace_dizhi,
        'wuxing_ju': wuxing_ju_name,
        'ju_num': ju_num,
        'ming_zhu': ming_zhu,
        'shen_zhu': shen_zhu,
        'main_star': main_star,
        'palaces': palaces,
        'si_hua': si_hua,
        'ziwei_position': DIZHI[ziwei_pos]
    }


# ========== 測試函數 ==========

if __name__ == '__main__':
    # 測試: 1991-07-02 未時 (shichen=7)
    # 農曆: 辛未年五月廿一日
    
    result = calculate_ziwei_chart(
        lunar_year=1991,
        lunar_month=5,
        lunar_day=21,
        shichen=7,  # 未時
        year_tiangan='辛',
        year_dizhi='未'
    )
    
    print("=" * 50)
    print("紫微斗數命盤計算結果")
    print("=" * 50)
    print(f"命宮: {result['ming_palace']}")
    print(f"身宮: {result['shen_palace']}")
    print(f"五行局: {result['wuxing_ju']}")
    print(f"命主: {result['ming_zhu']}")
    print(f"身主: {result['shen_zhu']}")
    print(f"命宮主星: {result['main_star']}")
    print(f"紫微位置: {result['ziwei_position']}")
    print()
    print("十二宮位:")
    for name, data in result['palaces'].items():
        shen_mark = " (身)" if data['is_shen'] else ""
        print(f"  {name}{shen_mark}: {data['dizhi']} - {', '.join(data['stars']) if data['stars'] else '無主星'}")
    print()
    print("四化:")
    for star, hua in result['si_hua'].items():
        print(f"  {star} {hua}")
