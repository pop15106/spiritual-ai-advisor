# 🏗️ Spiritual AI Advisor - 技術文件

本文檔詳細說明專案的技術架構、API 規格與資料庫設計。

---

## 1. 系統架構 (System Architecture)

本系統採用前後端分離架構，透過 RESTful API 進行通訊。

```mermaid
graph TD
    User[使用者] --> Frontend[前端 (Next.js 15)]
    Frontend --> |REST API| Backend[後端 (Flask)]
    Backend --> |SQL| DB[(SQLite Database)]
    Backend --> |Generative AI| Gemini[Google Gemini API]
    
    subgraph "Backend Services"
        Auth[認證系統 (JWT)]
        Logic[命理計算核心]
        Usage[使用量追蹤]
    end
    
    Backend --> Logic
    Backend --> Auth
    Backend --> Usage
```

---

## 2. 技術堆疊 (Technology Stack)

### 🎨 前端 (Frontend)
- **框架**: Next.js 15 (App Router)
- **語言**: TypeScript
- **樣式**: Tailwind CSS (含 Gradient 視覺效果)
- **圖標**: Lucide React
- **HTTP 客戶端**: Fetch API

### ⚙️ 後端 (Backend)
- **框架**: Flask (Python 3.9+)
- **資料庫**: SQLite 3 (無需安裝，Python 內建)
- **認證**: PyJWT (JWT Token Base)
- **AI 模型**: Google Generative AI (Gemini 2.5 Flash/Pros)
- **命理計算庫**:
  - `ephem`: 天文星體位置計算 (用於西洋占星、人類圖)
  - `lunar-python`: 農曆與干支計算 (用於八字、紫微斗數)

---

## 3. 資料庫設計 (Database Schema)

資料庫採用 SQLite，檔案位於 `data/app.db`。

### `admin` 表 (管理員)
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | INTEGER PK | 主鍵 |
| username | TEXT | 帳號 (Unique) |
| password_hash | TEXT | SHA-256 密碼雜湊 |
| api_key | TEXT | 資料庫儲存的 Gemini API Key |
| updated_at | TEXT | 更新時間 (ISO 8601) |

### `usage_logs` 表 (使用量記錄)
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | INTEGER PK | 主鍵 |
| feature | TEXT | 功能名稱 (e.g., tarot, bazi) |
| timestamp | TEXT | 完整時間戳 (ISO 8601) |
| year, month, day | INTEGER | 用於快速篩選的索引欄位 |
| hour, minute | INTEGER | 詳細時間欄位 |

---

## 4. API 規格說明 (API Specification)

所有 API Base URL: `http://localhost:5000`

### 🛂 認證與管理 (Auth & Admin)

#### 1. 管理員登入
- **URL**: `/api/admin/login`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "admin",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "token": "eyJhbGcu...",
    "message": "登入成功"
  }
  ```

#### 2. 獲取 API Keys
- **URL**: `/api/admin/api-key`
- **Method**: `GET`
- **Header**: `Authorization: Bearer <token>`
- **Response**:
  ```json
  {
    "success": true,
    "db_key_masked": "AIza...5gT7",  // 資料庫中的 Key
    "env_keys": [                    // .env 中的 Keys
      {"key": "AIza...vO7i", "full": "AIzaSy..."}
    ],
    "has_db_key": true
  }
  ```

#### 3. 更新 API Key
- **URL**: `/api/admin/api-key`
- **Method**: `PUT`
- **Header**: `Authorization: Bearer <token>`
- **Body**:
  ```json
  {
    "api_key": "AIzaSy..."
  }
  ```

#### 4. 獲取使用量統計
- **URL**: `/api/admin/usage/summary`
- **Method**: `GET`
- **Header**: `Authorization: Bearer <token>`
- **Response**:
  ```json
  {
      "success": true,
      "summary": {
          "total": 150,
          "today": 12,
          "this_month": 150,
          "by_feature": {
              "tarot": { "total": 50, "today": 5, "this_month": 50 }
              // ...
          }
      }
  }
  ```

---

### 🔮 命理功能 (Features)

#### 1. 塔羅抽牌 (Tarot)
- **URL**: `/api/tarot/draw`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "type": "daily" // 選填，抽牌類型
  }
  ```
- **Response**: 返回抽出的卡牌陣列與 AI 解讀。

#### 2. 八字計算 (Bazi)
- **URL**: `/api/bazi/calculate`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "birthDate": "1990-01-01",
    "birthTime": "12:00",
    "gender": "male"
  }
  ```

#### 3. 人類圖計算 (Human Design)
- **URL**: `/api/humandesign/calculate`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "birthDate": "1990-01-01",
    "birthTime": "12:00"
  }
  ```

#### 4. 西洋占星 (Astrology)
- **URL**: `/api/astrology/calculate`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "birthDate": "1990-01-01",
    "birthTime": "12:00",
    "city": "Taipei"
  }
  ```

#### 5. 紫微斗數 (Ziwei)
- **URL**: `/api/ziwei/calculate`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "birthDate": "1990-01-01",
    "birthHour": 6 // 時辰索引 (0-12)
  }
  ```

#### 6. 綜合分析 (Integration)
- **URL**: `/api/integration/analysis`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "selectedSystems": ["tarot", "bazi", "astrology"],
    "birthData": {
        "date": "1990-01-01",
        "time": "12:00",
        "humanDesignDate": "1990-01-01T12:00"
    },
    "question": "我的事業運勢如何？" (選填)
  }
  ```

---

## 5. 環境變數設定

### 後端 (`.env`)
```env
GOOGLE_API_KEYS=key1,key2...  # Gemini API Keys
JWT_SECRET=secret_key         # JWT 加密金鑰
```

### 前端 (`.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```
