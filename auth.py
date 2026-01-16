"""
管理員認證模組 (SQLite 版本)
============================
提供管理員登入、JWT token 驗證功能
"""

import jwt
import hashlib
import sqlite3
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

# JWT 密鑰 (生產環境應使用環境變數)
JWT_SECRET = os.environ.get('JWT_SECRET', 'spiritual-advisor-secret-key-2026')
JWT_EXPIRY_HOURS = 24

# 資料庫路徑
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'app.db')

def ensure_data_dir():
    """確保 data 目錄存在"""
    data_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

def get_db():
    """獲取資料庫連線"""
    ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫 (建立表格)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 管理員表格
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            api_key TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    
    # 使用量記錄表格
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            hour INTEGER NOT NULL,
            minute INTEGER NOT NULL
        )
    ''')
    
    # 建立索引加速查詢
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_usage_feature ON usage_logs(feature)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_usage_date ON usage_logs(year, month, day)')
    
    conn.commit()
    
    # 檢查是否需要建立預設管理員
    cursor.execute('SELECT COUNT(*) FROM admin')
    if cursor.fetchone()[0] == 0:
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO admin (username, password_hash, api_key, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', hash_password('admin123'), os.environ.get('GEMINI_API_KEY', ''), now, now))
        conn.commit()
    
    conn.close()

def hash_password(password):
    """密碼雜湊"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_admin_data():
    """讀取管理員資料"""
    init_db()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admin LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def save_admin_data(data):
    """更新管理員資料"""
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
    cursor.execute('''
        UPDATE admin SET 
            password_hash = ?,
            api_key = ?,
            updated_at = ?
        WHERE id = 1
    ''', (data.get('password_hash', ''), data.get('api_key', ''), now))
    
    conn.commit()
    conn.close()

def verify_admin(username, password):
    """驗證管理員帳號密碼"""
    admin_data = get_admin_data()
    if admin_data and admin_data['username'] == username:
        if admin_data['password_hash'] == hash_password(password):
            return True
    return False

def generate_token(username):
    """產生 JWT token"""
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verify_token(token):
    """驗證 JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def admin_required(f):
    """裝飾器：需要管理員權限"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 從 header 取得 token
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
        
        if not token:
            return jsonify({'success': False, 'error': '缺少認證 token'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'success': False, 'error': 'Token 無效或已過期'}), 401
        
        return f(*args, **kwargs)
    return decorated

def get_api_key():
    """獲取目前的 API Key"""
    admin_data = get_admin_data()
    return admin_data.get('api_key', '') if admin_data else ''

def update_api_key(new_key):
    """更新 API Key"""
    admin_data = get_admin_data()
    if admin_data:
        admin_data['api_key'] = new_key
        save_admin_data(admin_data)
        # 同時更新環境變數
        os.environ['GEMINI_API_KEY'] = new_key
    return True

def update_password(new_password):
    """更新管理員密碼"""
    admin_data = get_admin_data()
    if admin_data:
        admin_data['password_hash'] = hash_password(new_password)
        save_admin_data(admin_data)
    return True

def mask_api_key(api_key):
    """遮蔽 API Key 中間部分"""
    if not api_key or len(api_key) < 10:
        return api_key
    return api_key[:6] + '...' + api_key[-4:]

# 初始化資料庫
init_db()
