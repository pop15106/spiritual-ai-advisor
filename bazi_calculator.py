
"""
八字計算模組 (Bazi Calculator)
============================
實作專業級八字命盤計算

包含：
- 四柱八字排盤 (年、月、日、時)
- 十神計算 (比肩、劫財...等)
- 藏干與藏干十神
- 納音五行
- 神煞計算 (天乙貴人、桃花...等)
- 大運排列
"""

from lunar_python import Solar, Lunar
from datetime import datetime

# ========== 基礎數據定義 ==========

TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 五行
WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水',
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
    '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

# 陰陽 (True=陽, False=陰)
YINYANG = {
    '甲': True, '乙': False, '丙': True, '丁': False, '戊': True,
    '己': False, '庚': True, '辛': False, '壬': True, '癸': False,
    '子': True, '丑': False, '寅': True, '卯': False, '辰': True, '巳': False,
    '午': True, '未': False, '申': True, '酉': False, '戌': True, '亥': False
}

# 藏干表 (主氣、中氣、餘氣)
HIDDEN_STEMS = {
    '子': ['癸'],
    '丑': ['己', '癸', '辛'],
    '寅': ['甲', '丙', '戊'],
    '卯': ['乙'],
    '辰': ['戊', '乙', '癸'],
    '巳': ['丙', '戊', '庚'],
    '午': ['丁', '己'],
    '未': ['己', '丁', '乙'],
    '申': ['庚', '壬', '戊'],
    '酉': ['辛'],
    '戌': ['戊', '辛', '丁'],
    '亥': ['壬', '甲']
}

# 十神對照表
# key: (日主天干, 他干) -> 十神
# 為了簡化計算，使用五行生剋和陰陽關係計算
TEN_GODS_MAP = {
    ('生我', False): '正印', ('生我', True): '偏印',
    ('我生', False): '傷官', ('我生', True): '食神',
    ('剋我', False): '正官', ('剋我', True): '七殺',
    ('我剋', False): '正財', ('我剋', True): '偏財',
    ('同我', False): '劫財', ('同我', True): '比肩'
}

# 納音表
NAYIN = {
    '甲子': '海中金', '乙丑': '海中金', '丙寅': '爐中火', '丁卯': '爐中火',
    '戊辰': '大林木', '己巳': '大林木', '庚午': '路旁土', '辛未': '路旁土',
    '壬申': '劍鋒金', '癸酉': '劍鋒金', '甲戌': '山頭火', '乙亥': '山頭火',
    '丙子': '澗下水', '丁丑': '澗下水', '戊寅': '城頭土', '己卯': '城頭土',
    '庚辰': '白蠟金', '辛巳': '白蠟金', '壬午': '楊柳木', '癸未': '楊柳木',
    '甲申': '泉中水', '乙酉': '泉中水', '丙戌': '屋上土', '丁亥': '屋上土',
    '戊子': '霹靂火', '己丑': '霹靂火', '庚寅': '松柏木', '辛卯': '松柏木',
    '壬辰': '長流水', '癸巳': '長流水', '甲午': '沙中金', '乙未': '沙中金',
    '丙申': '山下火', '丁酉': '山下火', '戊戌': '平地木', '己亥': '平地木',
    '庚子': '壁上土', '辛丑': '壁上土', '壬寅': '金箔金', '癸卯': '金箔金',
    '甲辰': '覆燈火', '乙巳': '覆燈火', '丙午': '天河水', '丁未': '天河水',
    '戊申': '大驛土', '己酉': '大驛土', '庚戌': '釵釧金', '辛亥': '釵釧金',
    '壬子': '桑柘木', '癸丑': '桑柘木', '甲寅': '大溪水', '乙卯': '大溪水',
    '丙辰': '沙中土', '丁巳': '沙中土', '戊午': '天上火', '己未': '天上火',
    '庚申': '石榴木', '辛酉': '石榴木', '壬戌': '大海水', '癸亥': '大海水'
}

# 五行生剋關係: return (關係, 是否同陰陽)
# 關係: 生我, 我生, 剋我, 我剋, 同我
def get_relation(me, other):
    elements = ['木', '火', '土', '金', '水']
    me_elem = WUXING[me]
    other_elem = WUXING[other]
    
    me_idx = elements.index(me_elem)
    other_idx = elements.index(other_elem)
    
    diff = (other_idx - me_idx + 5) % 5
    
    relation = ''
    if diff == 0: relation = '同我'
    elif diff == 1: relation = '我生'
    elif diff == 2: relation = '我剋'
    elif diff == 3: relation = '剋我'
    elif diff == 4: relation = '生我'
    
    same_polarity = (YINYANG[me] == YINYANG[other])
    
    return relation, same_polarity

def get_ten_god(day_master, other_stem):
    """計算十神"""
    if not other_stem or not day_master: return ''
    relation, same_polarity = get_relation(day_master, other_stem)
    return TEN_GODS_MAP.get((relation, same_polarity), '')

# 神煞簡單計算 (部分)
def get_shen_sha(day_gan, day_zhi, month_zhi, p_zhi):
    """計算某個地支的神煞"""
    stars = []
    
    # 天乙貴人 (以日干為主)
    nobleman_map = {
        '甲': ['丑', '未'], '戊': ['丑', '未'], '庚': ['丑', '未'],
        '乙': ['子', '申'], '己': ['子', '申'],
        '丙': ['亥', '酉'], '丁': ['亥', '酉'],
        '壬': ['巳', '卯'], '癸': ['巳', '卯'],
        '辛': ['午', '寅']
    }
    if p_zhi in nobleman_map.get(day_gan, []):
        stars.append('天乙貴人')
        
    # 文昌貴人 (日干)
    wenchang_map = {
        '甲': '巳', '乙': '午', '丙': '申', '戊': '申',
        '丁': '酉', '己': '酉', '庚': '亥', '辛': '子',
        '壬': '寅', '癸': '卯'
    }
    if p_zhi == wenchang_map.get(day_gan):
        stars.append('文昌貴人')
        
    # 桃花 (鹹池) - 以年支或日支查 (這裡簡化用日支)
    peach_map = {
        '申': '酉', '子': '酉', '辰': '酉',
        '寅': '卯', '午': '卯', '戌': '卯',
        '巳': '午', '酉': '午', '丑': '午',
        '亥': '子', '卯': '子', '未': '子'
    }
    if p_zhi == peach_map.get(day_zhi):
        stars.append('桃花')
        
    # 驛馬 - 以年支或日支查 (簡化用日支)
    horse_map = {
        '申': '寅', '子': '寅', '辰': '寅',
        '寅': '申', '午': '申', '戌': '申',
        '巳': '亥', '酉': '亥', '丑': '亥',
        '亥': '巳', '卯': '巳', '未': '巳'
    }
    if p_zhi == horse_map.get(day_zhi):
        stars.append('驛馬')
        
    return stars

# ========== 主計算函數 ==========

def calculate_bazi_chart(year, month, day, hour, gender='male'):
    """
    計算八字完整命盤
    Args:
        year, month, day: 國曆日期
        hour: 小時 (0-23)
        gender: 'male' / 'female'
    """
    # 1. 建立 Solar 對象
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lunar = solar.getLunar()
    
    # 2. 獲取四柱 (lunar_python 已經處理好氣節交換)
    # getEightChar() 獲取八字對象
    eight_char = lunar.getEightChar()
    
    year_gan = eight_char.getYearGan()
    year_zhi = eight_char.getYearZhi()
    month_gan = eight_char.getMonthGan()
    month_zhi = eight_char.getMonthZhi()
    day_gan = eight_char.getDayGan()
    day_zhi = eight_char.getDayZhi()
    hour_gan = eight_char.getTimeGan()
    hour_zhi = eight_char.getTimeZhi()
    
    pillars = {
        'year': {'gan': year_gan, 'zhi': year_zhi},
        'month': {'gan': month_gan, 'zhi': month_zhi},
        'day': {'gan': day_gan, 'zhi': day_zhi},
        'hour': {'gan': hour_gan, 'zhi': hour_zhi}
    }
    
    # 3. 計算十神 (相對於日主)
    day_master = day_gan
    
    for key, p in pillars.items():
        # 天干十神
        if key == 'day':
            p['ten_god'] = '日主'
        else:
            p['ten_god'] = get_ten_god(day_master, p['gan'])
            
        # 藏干與藏干十神
        hiddens = HIDDEN_STEMS.get(p['zhi'], [])
        p['hidden_stems'] = []
        for h in hiddens:
            p['hidden_stems'].append({
                'gan': h,
                'ten_god': get_ten_god(day_master, h)
            })
            
        # 納音
        gz = p['gan'] + p['zhi']
        p['nayin'] = NAYIN.get(gz, '')
        
        # 神煞 (基本)
        p['shen_sha'] = get_shen_sha(day_master, day_zhi, month_zhi, p['zhi'])

    # 4. 計算大運 (Da Yun)
    # 陽男陰女順行，陰男陽女逆行
    is_yang_year = YINYANG.get(year_gan, True)
    is_male = (gender == 'male' or gender == '乾造')
    
    forward = False
    if is_yang_year and is_male: forward = True
    if not is_yang_year and not is_male: forward = True
    
    sex = 1 if is_male else 0
    # lunar_python 計算大運
    yun = eight_char.getYun(sex)
    
    start_age = yun.getStartYear()
    start_month = yun.getStartMonth()
    
    da_yun_list = yun.getDaYun()
    
    fortune_cycles = []
    # 取前 10 步大運
    for i in range(10): 
        if i >= len(da_yun_list): break
        dy = da_yun_list[i]
        
        start_y = dy.getStartYear()
        end_y = dy.getEndYear()
        gan_zhi = dy.getGanZhi()
        if not gan_zhi or len(gan_zhi) < 2:
             continue
        gan = gan_zhi[0]
        zhi = gan_zhi[1]
        
        fortune_cycles.append({
            'start_age': dy.getStartAge(),
            'start_year': start_y,
            'end_year': end_y,
            'gan': gan,
            'zhi': zhi,
            'gan_ten_god': get_ten_god(day_master, gan),
            'zhi_ten_god': get_ten_god(day_master, zhi), # 簡化：以地支本氣計算
            'nayin': NAYIN.get(gan_zhi, '')
        })
        
    # 5. 計算未來 5 年流年
    current_year = datetime.now().year
    liunian_list = []
    for i in range(5):
        y = current_year + i
        # 簡單推算流年干支: 1984是甲子年
        offset = (y - 1984) % 60
        gan_idx = offset % 10
        zhi_idx = offset % 12
        gan = TIANGAN[gan_idx]
        zhi = DIZHI[zhi_idx]
        
        # 簡單評分邏輯 (隨機或基於喜用神，這裡暫時給模擬分)
        # TODO: 實作喜用神評分
        import random
        score = round(random.uniform(5.0, 9.0), 1)
        
        liunian_list.append({
            'year': y,
            'ganzhi': gan + zhi,
            'score': score
        })

    return {
        'pillars': pillars,
        'day_master': day_master,
        'lunar_date_str': f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}",
        'solar_date_str': f"{year}年{month}月{day}日",
        'da_yun': fortune_cycles,
        'liunian': liunian_list,
        'start_age': start_age,
        'gender': '乾造' if is_male else '坤造'
    }

if __name__ == '__main__':
    # 測試
    res = calculate_bazi_chart(1990, 1, 31, 4, 'male')
    print("日主:", res['day_master'])
    print("年柱:", res['pillars']['year'])
    print("大運:", res['da_yun'][0])

