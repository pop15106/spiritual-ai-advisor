# 🔮 Spiritual AI Advisor (靈性 AI 顧問 API)

一個結合多種占卜系統與 AI 解讀的 Python Flask API 服務，為前端應用提供塔羅牌、八字、人類圖、占星與紫微斗數的計算與解讀功能。

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![Gemini AI](https://img.shields.io/badge/Gemini-AI-4285F4?logo=google)

## ✨ 功能特色

- 🃏 **塔羅牌 API** - 22張大阿爾克納牌抽牌與解讀
- 📅 **八字計算** - 使用 `lunar-python` 精準計算四柱八字
- 🧬 **人類圖計算** - 使用 `ephem` 天文計算行星位置、閘門與通道
- ⭐ **西洋占星** - 行星位置與相位計算
- 🌙 **紫微斗數** - 十二宮位主星分析
- 🤖 **AI 解讀** - 整合 Google Gemini AI 提供專業解讀

## 🚀 快速開始

### 前置需求

- Python 3.9+
- Google Gemini API Key

### 安裝步驟

```bash
# 複製專案
git clone https://github.com/pop15106/spiritual-ai-advisor.git
cd spiritual-ai-advisor

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 設定環境變數
cp .env.example .env
# 編輯 .env 填入你的 API Key
```

### 環境設定

編輯 `.env` 檔案：

```env
# 單一 API Key
GOOGLE_API_KEY=your_api_key_here

# 或多個 API Keys (逗號分隔，支援自動輪替)
GOOGLE_API_KEYS=key1,key2,key3
```

### 啟動服務

```bash
python api.py
```

API 服務將在 [http://localhost:5001](http://localhost:5001) 啟動。

## 📡 API 端點

| 端點 | 方法 | 說明 |
|------|------|------|
| `/api/health` | GET | 健康檢查 |
| `/api/tarot/draw` | POST | 抽塔羅牌 |
| `/api/tarot/cards` | GET | 取得所有塔羅牌資料 |
| `/api/bazi/calculate` | POST | 計算八字命盤 |
| `/api/humandesign/calculate` | POST | 計算人類圖 |
| `/api/humandesign/line-explanation` | POST | 取得閘門爻解釋 |
| `/api/astrology/calculate` | POST | 計算占星盤 |
| `/api/ziwei/calculate` | POST | 計算紫微斗數 |
| `/api/integration/analysis` | POST | AI 綜合分析 |

## 📁 專案結構

```
spiritual-ai-advisor/
├── api.py              # 主要 API 伺服器 (Flask)
├── app.py              # 備用入口 (Streamlit UI)
├── gates_iching_data.py    # 64閘門易經資料
├── channels_data.py        # 36通道詳細資料
├── hd_gate_mapping.py      # 閘門對照與計算函數
├── tarot_agent.py          # 塔羅牌代理程式
├── bazi_agent.py           # 八字代理程式
├── requirements.txt        # Python 依賴
└── .env.example            # 環境變數範本
```

## 🔧 相關專案

- **前端網站**: [spiritual-advisor-web](https://github.com/pop15106/spiritual-advisor-web) - Next.js 前端應用

## 📝 授權

MIT License

## 👤 作者

- GitHub: [@pop15106](https://github.com/pop15106)
