"""人類圖模板 (組合式強化版)"""
import random
from greetings_closings import get_greeting, get_closing

TYPES = {
    "生產者":{"strategy":"等待回應","signature":"滿足","not_self":"挫敗","energy":"薦骨能量持久"},
    "顯示者":{"strategy":"告知","signature":"平和","not_self":"憤怒","energy":"可發起行動"},
    "投射者":{"strategy":"等待邀請","signature":"成功","not_self":"苦澀","energy":"引導他人能量"},
    "反映者":{"strategy":"等待月循環","signature":"驚喜","not_self":"失望","energy":"反映環境能量"},
    "顯示生產者":{"strategy":"等待回應後告知","signature":"滿足與平和","not_self":"挫敗與憤怒","energy":"高效多工"}
}

PROFILES = {
    "1/3":{"name":"研究者/烈士","desc":"透過探索和試錯學習","life":"不斷嘗試中成長"},
    "1/4":{"name":"研究者/機會者","desc":"深入研究並透過網絡分享","life":"知識建立影響力"},
    "2/4":{"name":"隱士/機會者","desc":"天生才華需被召喚","life":"等待被看見"},
    "2/5":{"name":"隱士/異端","desc":"獨特天賦解決問題","life":"被期待帶來改變"},
    "3/5":{"name":"烈士/異端","desc":"試錯帶來實用方案","life":"經驗成為智慧"},
    "3/6":{"name":"烈士/角色模範","desc":"前半生試錯，後半生成榜樣","life":"三階段成長"},
    "4/6":{"name":"機會者/角色模範","desc":"透過網絡影響他人，成為榜樣","life":"人脈建立權威"},
    "4/1":{"name":"機會者/研究者","desc":"熟悉領域深耕分享","life":"專精一方"},
    "5/1":{"name":"異端/研究者","desc":"為他人提供實用的研究成果","life":"解決問題"},
    "5/2":{"name":"異端/隱士","desc":"被期待解決問題的天才","life":"保持退隱"},
    "6/2":{"name":"角色模範/隱士","desc":"經歷三階段成長成為榜樣","life":"時間累積智慧"},
    "6/3":{"name":"角色模範/烈士","desc":"透過人生經驗成為智者","life":"歷練成就權威"}
}

AUTHORITIES = {
    "情緒權威":{"desc":"等情緒波動完整週期","wait":"數日或一週"},
    "薦骨權威":{"desc":"聆聽薦骨直覺回應","wait":"當下回應"},
    "脾直覺權威":{"desc":"相信當下直覺智慧","wait":"即時決定"},
    "自我投射權威":{"desc":"在說話中找答案","wait":"說出來就知道"},
    "環境權威":{"desc":"觀察環境反饋","wait":"感受環境"},
    "月循環權威":{"desc":"等待月循環完整","wait":"28天"}
}

CENTERS = {
    "頭腦中心": {
        "defined": "有固定的思考方式和靈感來源，不需要外界刺激也能產生想法。",
        "undefined": "思維開放，容易被他人的想法影響，可能過度思考不重要的問題。",
        "not_self": "「我必須回答所有問題」的壓力"
    },
    "邏輯中心": {
        "defined": "有穩定的思考和分析模式，能夠持續處理資訊。",
        "undefined": "容易被他人的觀點影響，試圖證明自己的確定性。",
        "not_self": "「我必須確定」的焦慮"
    },
    "喉嚨中心": {
        "defined": "有固定的表達和行動方式，能夠持續地將想法轉化為行動或言語。",
        "undefined": "表達方式多變，可能過度說話以引起注意。",
        "not_self": "「我必須引起注意/被聽見」的衝動"
    },
    "G中心": {
        "defined": "有穩定的身份認同和人生方向，知道自己是誰和要去哪裡。",
        "undefined": "身份認同受環境影響，可能感到迷失或尋找歸屬。",
        "not_self": "「我必須知道我是誰和我要去哪裡」的困惑"
    },
    "意志力中心": {
        "defined": "有穩定的意志力和承諾能力，能夠持續努力達成目標。",
        "undefined": "意志力不穩定，可能過度承諾或低估自己的價值。",
        "not_self": "「我必須證明自己的價值」的壓力"
    },
    "情緒中心": {
        "defined": "情緒有固定的波動週期，需要時間來達到清明。",
        "undefined": "容易吸收他人的情緒，可能避免衝突或過度敏感。",
        "not_self": "「我必須避免真相和衝突」的逃避"
    },
    "薦骨中心": {
        "defined": "（僅生產者/顯示生產者）有持久的生命力和工作能量。",
        "undefined": "能量不穩定，需要學習何時該休息，可能過度工作。",
        "not_self": "「我不知道何時該停下來」的過勞"
    },
    "脾中心": {
        "defined": "有穩定的直覺和生存本能，能夠即時感知危險。",
        "undefined": "健康和安全感不穩定，可能過度擔心或忽視直覺。",
        "not_self": "「我必須緊抓不放」的恐懼"
    },
    "根中心": {
        "defined": "有穩定的壓力處理方式，能夠持續應對壓力。",
        "undefined": "容易吸收外界壓力，可能覺得急迫或焦慮。",
        "not_self": "「我必須盡快完成」的急迫感"
    }
}

# 類型+權威組合
TYPE_AUTH_COMBOS = {
    ("生產者","薦骨權威"):"薦骨的即時回應是您最可靠的指南針",
    ("生產者","情緒權威"):"雖有薦骨能量，仍需等待情緒清明",
    ("投射者","脾直覺權威"):"被邀請時，直覺會告訴您對錯",
    ("投射者","自我投射權威"):"在對話中，您會聽到自己的答案",
    ("顯示者","情緒權威"):"行動前，讓情緒沉澱，再做告知",
    ("反映者","月循環權威"):"您需要一整個月來做重大決定"
}

def generate_hd_interpretation(hd_type, profile=None, authority=None, centers=None):
    t = TYPES.get(hd_type, TYPES["生產者"])
    out = [f"{get_greeting('humandesign')}\n"]
    out.append(f"## 🔷 類型：{hd_type}")
    out.append(f"\n{t['energy']}")
    out.append(f"\n\n**策略**：{t['strategy']}")
    out.append(f"\n**正確標誌**：{t['signature']} | **非自己**：{t['not_self']}")
    
    if profile:
        clean_profile = profile.strip()
        if clean_profile in PROFILES:
            p = PROFILES[clean_profile]
            out.append(f"\n\n## 📊 人生角色：{clean_profile} ({p['name']})")
            out.append(f"\n{p['desc']}")
            out.append(f"\n人生主題：{p['life']}")
    
    if authority:
        clean_auth = authority.strip()
        if clean_auth in AUTHORITIES:
            a = AUTHORITIES[clean_auth]
            out.append(f"\n\n## 🎯 內在權威：{clean_auth}")
            out.append(f"\n{a['desc']}")
            out.append(f"\n決策時間：{a['wait']}")
            
            # 類型+權威組合
            combo_key = (hd_type, clean_auth)
            if combo_key in TYPE_AUTH_COMBOS:
                out.append(f"\n\n💫 **組合洞見**：{TYPE_AUTH_COMBOS[combo_key]}")
    
    if centers and isinstance(centers, dict):
        out.append("\n\n## ⚡ 能量中心狀態")
        # 簡單列出定義與未定義
        defined = [k for k,v in centers.items() if v]
        undefined = [k for k,v in centers.items() if not v]
        
        if defined:
            out.append(f"\n\n🔹 **定義中心** (固有天賦)：{', '.join(defined[:3])} 等")
            # 隨機挑選一個定義中心做解釋
            c = random.choice(defined)
            if c in CENTERS:
                 out.append(f"\n- **{c}**：{CENTERS[c]['defined']}")

        if undefined:
            out.append(f"\n\n🔸 **空白中心** (學習課題)：{', '.join(undefined[:3])} 等")
            # 隨機挑選一個空白中心做解釋
            c = random.choice(undefined)
            if c in CENTERS:
                 out.append(f"\n- **{c}**：{CENTERS[c]['undefined']}")
                 out.append(f"\n  ⚠️ 非自己主題：{CENTERS[c]['not_self']}")

    out.append(get_closing('humandesign'))
    return "".join(out)
