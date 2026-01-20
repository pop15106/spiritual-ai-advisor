import os
import requests
import time

# Target directory
TARGET_DIR = r"c:\Users\7010\.gemini\antigravity\scratch\spiritual-advisor-web\public\tarot"

if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

# Base URL (Sacred Texts - PKT)
BASE_URL = "https://www.sacred-texts.com/tarot/pkt/img"

def try_download(filenames, save_name):
    """Try multiple filenames until one works"""
    for fname in filenames:
        url = f"{BASE_URL}/{fname}"
        save_path = os.path.join(TARGET_DIR, save_name)
        try:
            print(f"Trying {fname} -> {save_name}...")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"Success: {save_name}")
                return
        except Exception as e:
            print(f"Error {fname}: {e}")
            
    print(f"FAILED ALL for {save_name}")

# 1. Major Arcana
for i in range(22):
    src = f"ar{i:02d}.jpg"
    dst = f"Major_{i:02d}.jpg"
    try_download([src], dst)

# 2. Minor Arcana
suit_map = {
    'cu': 'Cups',
    'wa': 'Wands',
    'sw': 'Swords',
    'pe': 'Pentacles'
}

for code, suit_name in suit_map.items():
    for i in range(1, 15):
        # Determine source filename candidates
        candidates = []
        
        # Ace
        if i == 1:
            candidates.append(f"{code}ac.jpg")
            candidates.append(f"{code}01.jpg") # Fallback
            rank = "Ace"
            
        # Numbers 2-10
        elif i <= 10:
            candidates.append(f"{code}{i:02d}.jpg")
            rank = f"{i:02d}"
            
        # Court Cards
        elif i == 11:
            candidates.append(f"{code}pa.jpg")
            candidates.append(f"{code}pg.jpg")
            candidates.append(f"{code}11.jpg")
            rank = "Page"
        elif i == 12:
            candidates.append(f"{code}kn.jpg")
            candidates.append(f"{code}cn.jpg") # Knight sometimes Cavalier? No, usually kn
            candidates.append(f"{code}12.jpg")
            rank = "Knight"
        elif i == 13:
            candidates.append(f"{code}qu.jpg")
            candidates.append(f"{code}qn.jpg")
            candidates.append(f"{code}13.jpg")
            rank = "Queen"
        elif i == 14:
            candidates.append(f"{code}ki.jpg")
            candidates.append(f"{code}kg.jpg") 
            candidates.append(f"{code}14.jpg")
            rank = "King"
            
        dst = f"{suit_name}_{rank}.jpg"
        try_download(candidates, dst)

# Back
try_download(["cardback.jpg", "back.jpg"], "Card_Back.jpg")
