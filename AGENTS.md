# AGENTS.md - Spiritual AI Advisor 開發指南

## 📋 專案概述
這是一個結合多種占卜系統與 AI 解讀的 Python Flask API 服務，提供塔羅牌、八字、人類圖、占星與紫微斗數的計算與解讀功能。

## 🚀 建置/執行命令

### 基本執行
```bash
# 啟動 API 服務 (開發環境)
python api.py

# 啟動 Streamlit 前端 (可選)
streamlit run app.py
```

### 測試命令
```bash
# 執行所有 API 測試
python test_api.py

# 執行特定功能測試
python test_ai_connection.py          # AI 連接測試
python test_ziwei_endpoint.py         # 紫微斗數端點測試
python test_astro_min.py              # 占星功能測試
python test_all_calculations.py       # 所有計算功能測試
python test_integration_endpoint.py   # 整合分析端點測試

# 執行單一測試檔案
python -m pytest test_api.py -v       # 使用 pytest (如果安裝)
python test_api.py                    # 直接執行
```

### 環境設定
```bash
# 安裝依賴
pip install -r requirements.txt

# 設定環境變數
cp .env.example .env
# 編輯 .env 檔案填入 API Keys
```

## 🎨 代碼風格指南

### 檔案編碼與結構
- **編碼**: 所有 Python 檔案必須以 `# -*- coding: utf-8 -*-` 開頭
- **文件字串**: 使用三重引號 `"""` 撰寫模組級文檔
- **分隔符**: 使用 `==========` 分隔程式碼區塊

### 導入風格
```python
# 標準庫導入
import os
import json
from datetime import datetime, timedelta

# 第三方庫導入
from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt

# 本地模組導入
from gates_iching_data import GATES_ICHING_DETAILED
from bazi_calculator import calculate_bazi_chart
```

### 命名慣例
- **常量**: `UPPER_SNAKE_CASE` (例: `MAJOR_ARCANA`, `TIANGAN`)
- **函數**: `snake_case` (例: `calculate_bazi_chart`, `get_gate_from_longitude`)
- **類別**: `PascalCase` (例: `SpiritualAdvisor`, `TarotDeck`)
- **變數**: `snake_case` (例: `birth_datetime`, `api_response`)
- **檔案名**: `snake_case.py` (例: `ziwei_calculator.py`, `auth.py`)

### 錯誤處理模式
```python
# 全域錯誤處理器 (Flask)
@app.errorhandler(Exception)
def handle_exception(e):
    """全域錯誤處理器"""
    import traceback
    print(f"🔥 Unhandled Exception: {e}")
    traceback.print_exc()
    return jsonify({"success": False, "error": str(e)}), 500

# 函數級錯誤處理
def calculate_something(data):
    try:
        # 主要邏輯
        result = process_data(data)
        return {"success": True, "data": result}
    except Exception as e:
        print(f"❌ Error in calculate_something: {e}")
        return {"success": False, "error": str(e)}
```

### API 回應格式
```python
# 成功回應
{
    "success": True,
    "data": {...},
    "message": "操作成功"
}

# 錯誤回應
{
    "success": False,
    "error": "錯誤訊息",
    "details": {...}  # 可選
}
```

## 📁 專案結構慣例

### 核心模組
- `api.py` - 主要 Flask API 伺服器
- `auth.py` - JWT 認證與權限管理
- `usage_tracker.py` - 使用量追蹤系統
- `bazi_calculator.py` - 八字計算核心
- `ziwei_calculator.py` - 紫微斗數計算核心
- `tarot_deck.py` - 塔羅牌資料與邏輯

### 資料模組
- `gates_iching_data.py` - 64 閘門易經資料
- `channels_data.py` - 36 通道詳細資料
- `hd_gate_mapping.py` - 閘門對照與計算函數

### 測試檔案
- `test_*.py` - 所有測試檔案以 `test_` 開頭
- `test_api.py` - 完整 API 端點測試
- `test_*_endpoint.py` - 特定功能端點測試

## 🔧 開發環境設定

### 必要套件 (requirements.txt)
```
google-generativeai
python-dotenv
streamlit
lunar-python
plotly
flask
flask-cors
ephem
kerykeion
```

### 環境變數 (.env)
```env
# Google Gemini API Keys (支援多個，逗號分隔)
GOOGLE_API_KEYS=key1,key2,key3

# JWT 認證密鑰
JWT_SECRET=your_jwt_secret_key

# 可選：其他配置
FLASK_ENV=development
FLASK_DEBUG=True
```

## 🧪 測試指南

### 測試模式
1. **單元測試**: 測試單一函數或模組
2. **整合測試**: 測試 API 端點完整流程
3. **連接測試**: 測試外部 API (如 Gemini AI) 連接

### 測試檔案命名
- `test_[功能].py` - 功能測試 (例: `test_bazi.py`)
- `test_[功能]_endpoint.py` - API 端點測試 (例: `test_ziwei_endpoint.py`)
- `test_[功能]_verification.py` - 驗證測試 (例: `test_astro_fallback_verification.py`)

### 測試執行順序
1. 先執行 `test_ai_connection.py` 確認 AI 服務可用
2. 執行 `test_api.py` 進行完整 API 測試
3. 執行特定功能測試檔案

## 📊 資料庫與快取

### SQLite 資料庫
- 路徑: `data/app.db`
- 用途: 認證、使用量追蹤、管理員資料
- 自動建立: 首次執行時自動建立資料表

### 快取機制
- Kerykeion 占星資料快取: `cache/kerykeion_geonames_cache.sqlite`
- API Key 輪替: 自動在多個 Keys 間輪替使用

## 🔒 安全慣例

### API Key 管理
- 使用環境變數儲存 API Keys
- 支援多個 Keys 自動輪替
- 避免在程式碼中硬編碼 Keys

### JWT 認證
- Token 有效期: 24 小時
- 密鑰從環境變數讀取
- 管理員端點需要認證

## 🌐 部署相關

### Vercel 部署
- 入口檔案: `api/index.py`
- 配置檔案: `vercel.json`
- 自動 Python 環境建置

### 本地開發
- API 服務: `http://localhost:5000`
- CORS 設定: 允許 `http://localhost:3000` (前端)
- 支援 credentials: True

## 📝 代碼註解慣例

### 函數文檔
```python
def calculate_bazi_chart(birth_datetime, location):
    """
    計算八字命盤
    
    Args:
        birth_datetime (datetime): 出生日期時間
        location (dict): 地理位置資訊 {'lat': float, 'lng': float}
    
    Returns:
        dict: 八字命盤資料，包含四柱、十神、神煞等
    """
```

### 區塊註解
```python
# ========== 資料定義區 ==========
# ========== 計算核心區 ==========
# ========== API 端點區 ==========
```

## 🎯 新功能開發檢查清單

1. [ ] 檔案編碼設定為 UTF-8
2. [ ] 撰寫模組級文檔字串
3. [ ] 遵循命名慣例
4. [ ] 實作適當錯誤處理
5. [ ] API 回應格式統一
6. [ ] 撰寫對應測試檔案
7. [ ] 更新 requirements.txt (如需新套件)
8. [ ] 測試所有相關端點
9. [ ] 確認 CORS 設定正確
10. [ ] 檢查環境變數需求

## 🐞 常見問題排除

### API 連接問題
- 檢查 `.env` 檔案中的 API Keys
- 確認網路連接正常
- 查看 `ai_debug.log` 錯誤記錄

### 計算錯誤
- 確認輸入日期時間格式正確
- 檢查地理位置資料
- 查看相關測試檔案範例

### 資料庫問題
- 確認 `data/` 目錄存在
- 檢查 SQLite 檔案權限
- 重新啟動服務自動建表