
MAJOR_ARCANA = [
    "0 愚者 (The Fool)", "I 魔術師 (The Magician)", "II 女祭司 (The High Priestess)", "III 皇后 (The Empress)", 
    "IV 皇帝 (The Emperor)", "V 教皇 (The Hierophant)", "VI 戀人 (The Lovers)", "VII 戰車 (The Chariot)", 
    "VIII 力量 (Strength)", "IX 隱士 (The Hermit)", "X 命運之輪 (Wheel of Fortune)", "XI 正義 (Justice)", 
    "XII 吊人 (The Hanged Man)", "XIII 死神 (Death)", "XIV 節制 (Temperance)", "XV 惡魔 (The Devil)", 
    "XVI 高塔 (The Tower)", "XVII 星星 (The Star)", "XVIII 月亮 (The Moon)", "XIX 太陽 (The Sun)", 
    "XX審判 (Judgement)", "XXI 世界 (The World)"
]

SUITS = ["權杖 (Wands)", "聖杯 (Cups)", "寶劍 (Swords)", "錢幣 (Pentacles)"]
RANKS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "侍者 (Page)", "騎士 (Knight)", "皇后 (Queen)", "國王 (King)"]

MINOR_ARCANA = [f"{suit} {rank}" for suit in SUITS for rank in RANKS]

FULL_DECK = MAJOR_ARCANA + MINOR_ARCANA
