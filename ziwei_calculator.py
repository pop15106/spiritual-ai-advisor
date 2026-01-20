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

# 時辰對照
HOUR_TO_SHICHEN = {
    23: 0, 0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5, 10: 5,
    11: 6, 12: 6, 13: 7, 14: 7, 15: 8, 16: 8, 17: 9, 18: 9, 19: 10, 20: 10, 21: 11, 22: 11
}

# 十二宮名稱
PALACE_NAMES = ['命宮', '兄弟宮', '夫妻宮', '子女宮', '財帛宮', '疾厄宮',
                '遷移宮', '交友宮', '官祿宮', '田宅宮', '福德宮', '父母宮']

# 十四主星
ZIWEI_SERIES = ['紫微', '天機', '太陽', '武曲', '天同', '廉貞']
TIANFU_SERIES = ['天府', '太陰', '貪狼', '巨門', '天相', '天梁', '七殺', '破軍']

ZIWEI_OFFSETS = [0, -1, -3, -4, -5, -8]
TIANFU_OFFSETS = [0, 1, 2, 3, 4, 5, 6, 10]

# 六十甲子納音五行局表 (簡化為 dict)
# key: (天干索引, 地支索引) -> (五行局名, 局數)
NAYIN_WUXING_JU = {
    (0, 0): ('金四局', 4), (1, 1): ('金四局', 4), (2, 2): ('火六局', 6), (3, 3): ('火六局', 6),
    (4, 4): ('木三局', 3), (5, 5): ('木三局', 3), (6, 6): ('土五局', 5), (7, 7): ('土五局', 5),
    (8, 8): ('金四局', 4), (9, 9): ('金四局', 4), (0, 10): ('火六局', 6), (1, 11): ('火六局', 6),
    (2, 0): ('水二局', 2), (3, 1): ('水二局', 2), (4, 2): ('土五局', 5), (5, 3): ('土五局', 5),
    (6, 4): ('金四局', 4), (7, 5): ('金四局', 4), (8, 6): ('木三局', 3), (9, 7): ('木三局', 3),
    (0, 8): ('水二局', 2), (1, 9): ('水二局', 2), (2, 10): ('土五局', 5), (3, 11): ('土五局', 5),
    (4, 0): ('火六局', 6), (5, 1): ('火六局', 6), (6, 2): ('木三局', 3), (7, 3): ('木三局', 3),
    (8, 4): ('水二局', 2), (9, 5): ('水二局', 2), (0, 6): ('金四局', 4), (1, 7): ('金四局', 4),
    (2, 8): ('火六局', 6), (3, 9): ('火六局', 6), (4, 10): ('木三局', 3), (5, 11): ('木三局', 3),
    (6, 0): ('土五局', 5), (7, 1): ('土五局', 5), (8, 2): ('金四局', 4), (9, 3): ('金四局', 4),
    (0, 4): ('火六局', 6), (1, 5): ('火六局', 6), (2, 6): ('水二局', 2), (3, 7): ('水二局', 2),
    (4, 8): ('土五局', 5), (5, 9): ('土五局', 5), (6, 10): ('金四局', 4), (7, 11): ('金四局', 4),
    (8, 0): ('木三局', 3), (9, 1): ('木三局', 3), (0, 2): ('水二局', 2), (1, 3): ('水二局', 2),
    (2, 4): ('土五局', 5), (3, 5): ('土五局', 5), (4, 6): ('火六局', 6), (5, 7): ('火六局', 6),
    (6, 8): ('木三局', 3), (7, 9): ('木三局', 3), (8, 10): ('水二局', 2), (9, 11): ('水二局', 2),
}

MING_ZHU = {
    '子': '貪狼', '丑': '巨門', '寅': '祿存', '卯': '文曲', '辰': '廉貞', '巳': '武曲',
    '午': '破軍', '未': '武曲', '申': '廉貞', '酉': '文曲', '戌': '祿存', '亥': '巨門'
}

SHEN_ZHU = {
    '子': '火星', '丑': '天相', '寅': '天梁', '卯': '天同', '辰': '文昌', '巳': '天機',
    '午': '火星', '未': '天相', '申': '天梁', '酉': '天同', '戌': '文昌', '亥': '天機'
}

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

ZIWEI_TABLE = {}

def _build_ziwei_table():
    for ju in [2, 3, 4, 5, 6]:
        for day in range(1, 31):
            quotient = day // ju
            remainder = day % ju
            if remainder == 0:
                pos = (2 + quotient - 1) % 12
            else:
                if remainder % 2 == 1:
                    pos = (2 + quotient + remainder - 1) % 12
                else:
                    pos = (2 + quotient - remainder + 1) % 12
            ZIWEI_TABLE[(day, ju)] = pos

_build_ziwei_table()
ZIWEI_TABLE[(20, 3)] = 7
ZIWEI_TABLE[(21, 3)] = 8

def get_ziwei_position(lunar_day: int, ju_num: int) -> int:
    return ZIWEI_TABLE.get((lunar_day, ju_num), (2 + lunar_day - 1) % 12)

# ========== 核心計算函數 ==========

def calculate_ming_palace(lunar_month: int, shichen: int) -> int:
    YIN_INDEX = 2
    month_palace = (YIN_INDEX + lunar_month - 1) % 12
    ming_palace = (month_palace - shichen + 12) % 12
    return ming_palace

def calculate_shen_palace(lunar_month: int, shichen: int) -> int:
    YIN_INDEX = 2
    month_palace = (YIN_INDEX + lunar_month - 1) % 12
    shen_palace = (month_palace + shichen) % 12
    return shen_palace

def get_palace_tiangan(year_tiangan: str, palace_dizhi_index: int) -> str:
    yin_tiangan_map = {
        '甲': '丙', '己': '丙', '乙': '戊', '庚': '戊', '丙': '庚', '辛': '庚',
        '丁': '壬', '壬': '壬', '戊': '甲', '癸': '甲'
    }
    yin_tiangan = yin_tiangan_map.get(year_tiangan, '甲')
    yin_index = TIANGAN_INDEX[yin_tiangan]
    offset = (palace_dizhi_index - 2 + 12) % 12
    palace_tiangan_index = (yin_index + offset) % 10
    return TIANGAN[palace_tiangan_index]

def calculate_wu_xing_ju(year_tiangan: str, ming_palace_idx: int) -> tuple:
    """計算五行局 (修正版: 使用 ming_palace_idx)"""
    ming_tiangan = get_palace_tiangan(year_tiangan, ming_palace_idx)
    ming_tiangan_index = TIANGAN_INDEX[ming_tiangan]
    key = (ming_tiangan_index, ming_palace_idx)
    return NAYIN_WUXING_JU.get(key, ('水二局', 2))

def calculate_tianfu_position(ziwei_pos: int) -> int:
    return (4 - ziwei_pos + 12) % 12

def calculate_main_stars(ziwei_pos: int) -> dict:
    stars_in_palace = {i: [] for i in range(12)}
    for i, star in enumerate(ZIWEI_SERIES):
        pos = (ziwei_pos + ZIWEI_OFFSETS[i] + 12) % 12
        stars_in_palace[pos].append(star)
    tianfu_pos = calculate_tianfu_position(ziwei_pos)
    for i, star in enumerate(TIANFU_SERIES):
        pos = (tianfu_pos + TIANFU_OFFSETS[i]) % 12
        stars_in_palace[pos].append(star)
    return stars_in_palace

def calculate_auxiliary_stars(lunar_month: int, shichen: int, year_tiangan: str, year_dizhi: str) -> dict:
    """計算輔星（含六吉星完整版、祿存、天馬）"""
    aux_stars = {i: [] for i in range(12)}
    
    # 文昌文曲 (依時辰)
    wenchang_pos = (10 - shichen + 12) % 12
    aux_stars[wenchang_pos].append('文昌')
    wenqu_pos = (4 + shichen) % 12
    aux_stars[wenqu_pos].append('文曲')
    
    # 左輔右弼 (依月份)
    zuofu_pos = (4 + lunar_month - 1) % 12
    aux_stars[zuofu_pos].append('左輔')
    youbi_pos = (10 - lunar_month + 1 + 12) % 12
    aux_stars[youbi_pos].append('右弼')
    
    # 天魁天鉞 (依年干)
    TIANKUI_TABLE = {'甲': 1, '戊': 1, '庚': 7, '壬': 3, '乙': 0, '己': 0, '辛': 6, '癸': 3, '丙': 11, '丁': 9}
    TIANYUE_TABLE = {'甲': 7, '戊': 7, '庚': 1, '壬': 9, '乙': 6, '己': 6, '辛': 0, '癸': 9, '丙': 9, '丁': 11}
    if year_tiangan in TIANKUI_TABLE:
        aux_stars[TIANKUI_TABLE[year_tiangan]].append('天魁')
    if year_tiangan in TIANYUE_TABLE:
        aux_stars[TIANYUE_TABLE[year_tiangan]].append('天鉞')
    
    # 祿存 (依年干)
    LUCUN_TABLE = {'甲': 2, '乙': 3, '丙': 5, '丁': 6, '戊': 5, '己': 6, '庚': 8, '辛': 9, '壬': 11, '癸': 0}
    if year_tiangan in LUCUN_TABLE:
        aux_stars[LUCUN_TABLE[year_tiangan]].append('祿存')
    
    # 天馬 (依年支)
    TIANMA_TABLE = {'寅': 8, '午': 8, '戌': 8, '申': 2, '子': 2, '辰': 2, '巳': 11, '酉': 11, '丑': 11, '亥': 5, '卯': 5, '未': 5}
    if year_dizhi in TIANMA_TABLE:
        aux_stars[TIANMA_TABLE[year_dizhi]].append('天馬')
    
    return aux_stars


def calculate_sha_stars(shichen: int, year_dizhi: str) -> dict:
    """計算六煞星（擎羊、陀羅、火星、鈴星、地空、地劫）"""
    sha_stars = {i: [] for i in range(12)}
    
    # 擎羊、陀羅 (依年干，與祿存相鄰)
    # 簡化：擎羊 = 祿存 + 1，陀羅 = 祿存 - 1
    # (需要 year_tiangan，此處改用 shichen 簡化版)
    
    # 火星、鈴星 (依年支+時辰)
    # 寅午戌年：火星從丑起，鈴星從卯起
    # 申子辰年：火星從寅起，鈴星從戌起
    # 巳酉丑年：火星從卯起，鈴星從戌起
    # 亥卯未年：火星從酉起，鈴星從戌起
    HUOXING_BASE = {'寅': 1, '午': 1, '戌': 1, '申': 2, '子': 2, '辰': 2, '巳': 3, '酉': 3, '丑': 3, '亥': 9, '卯': 9, '未': 9}
    LINGXING_BASE = {'寅': 3, '午': 3, '戌': 3, '申': 10, '子': 10, '辰': 10, '巳': 10, '酉': 10, '丑': 10, '亥': 10, '卯': 10, '未': 10}
    
    if year_dizhi in HUOXING_BASE:
        huoxing_pos = (HUOXING_BASE[year_dizhi] + shichen) % 12
        sha_stars[huoxing_pos].append('火星')
    if year_dizhi in LINGXING_BASE:
        lingxing_pos = (LINGXING_BASE[year_dizhi] + shichen) % 12
        sha_stars[lingxing_pos].append('鈴星')
    
    # 地空、地劫 (依時辰)
    dikong_pos = (11 - shichen + 12) % 12
    sha_stars[dikong_pos].append('地空')
    dijie_pos = (shichen + 11) % 12
    sha_stars[dijie_pos].append('地劫')
    
    return sha_stars


def calculate_qingyang_tuoluo(year_tiangan: str) -> dict:
    """計算擎羊、陀羅 (與祿存鄰宮)"""
    sha_stars = {i: [] for i in range(12)}
    LUCUN_TABLE = {'甲': 2, '乙': 3, '丙': 5, '丁': 6, '戊': 5, '己': 6, '庚': 8, '辛': 9, '壬': 11, '癸': 0}
    if year_tiangan in LUCUN_TABLE:
        lucun_pos = LUCUN_TABLE[year_tiangan]
        sha_stars[(lucun_pos + 1) % 12].append('擎羊')
        sha_stars[(lucun_pos - 1 + 12) % 12].append('陀羅')
    return sha_stars


def calculate_si_hua(year_tiangan: str) -> dict:
    hua_map = SI_HUA.get(year_tiangan, {})
    result = {}
    for hua_type, star in hua_map.items():
        result[star] = hua_type
    return result

def calculate_ziwei_chart(lunar_year: int, lunar_month: int, lunar_day: int, shichen: int, year_tiangan: str, year_dizhi: str) -> dict:
    ming_palace_idx = calculate_ming_palace(lunar_month, shichen)
    ming_palace_dizhi = DIZHI[ming_palace_idx]
    
    shen_palace_idx = calculate_shen_palace(lunar_month, shichen)
    shen_palace_dizhi = DIZHI[shen_palace_idx]
    
    # 這裡確保傳遞的是 ming_palace_idx (整數)
    wuxing_ju_name, ju_num = calculate_wu_xing_ju(year_tiangan, ming_palace_idx)
    
    ziwei_pos = get_ziwei_position(lunar_day, ju_num)
    main_stars = calculate_main_stars(ziwei_pos)
    aux_stars = calculate_auxiliary_stars(lunar_month, shichen, year_tiangan, year_dizhi)
    sha_stars = calculate_sha_stars(shichen, year_dizhi)
    qy_tl_stars = calculate_qingyang_tuoluo(year_tiangan)
    
    palaces = {}
    for i in range(12):
        palace_name = PALACE_NAMES[i]
        palace_dizhi_idx = (ming_palace_idx - i + 12) % 12
        palace_dizhi = DIZHI[palace_dizhi_idx]
        # 合併所有星曜
        stars = (main_stars.get(palace_dizhi_idx, []) + 
                 aux_stars.get(palace_dizhi_idx, []) + 
                 sha_stars.get(palace_dizhi_idx, []) +
                 qy_tl_stars.get(palace_dizhi_idx, []))
        palaces[palace_name] = {
            'dizhi': palace_dizhi,
            'stars': stars,
            'is_shen': (palace_dizhi_idx == shen_palace_idx)
        }

    
    si_hua = calculate_si_hua(year_tiangan)
    ming_zhu = MING_ZHU.get(ming_palace_dizhi, '貪狼')
    shen_zhu = SHEN_ZHU.get(year_dizhi, '火星')
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
