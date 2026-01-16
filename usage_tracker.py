"""
使用量追蹤模組 (SQLite 版本)
============================
記錄每個功能的使用次數和完整時間戳，支援時間區間查詢
"""

import sqlite3
import os
from datetime import datetime
from collections import defaultdict

# 資料庫路徑 (與 auth.py 共用)
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'app.db')

def get_db():
    """獲取資料庫連線"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def track_usage(feature_name):
    """
    記錄功能使用
    
    Args:
        feature_name: 功能名稱 (tarot, bazi, astrology, humandesign, ziwei, integration)
    """
    now = datetime.now()
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO usage_logs (feature, timestamp, year, month, day, hour, minute)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (feature_name, now.isoformat(), now.year, now.month, now.day, now.hour, now.minute))
    
    conn.commit()
    conn.close()
    return True

def get_usage_stats(feature_name=None, start_date=None, end_date=None, 
                    year=None, month=None, day=None, hour=None):
    """
    獲取使用量統計
    
    Args:
        feature_name: 指定功能名稱，None 表示全部
        start_date: 開始日期 (ISO format)
        end_date: 結束日期 (ISO format)
        year, month, day, hour: 時間篩選條件
    
    Returns:
        dict: 統計結果
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # 構建 WHERE 條件
    conditions = []
    params = []
    
    if feature_name:
        conditions.append("feature = ?")
        params.append(feature_name)
    if start_date:
        conditions.append("timestamp >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("timestamp <= ?")
        params.append(end_date)
    if year is not None:
        conditions.append("year = ?")
        params.append(year)
    if month is not None:
        conditions.append("month = ?")
        params.append(month)
    if day is not None:
        conditions.append("day = ?")
        params.append(day)
    if hour is not None:
        conditions.append("hour = ?")
        params.append(hour)
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    # 獲取各功能統計
    result = {}
    
    # 獲取所有功能的總數
    cursor.execute(f'''
        SELECT feature, COUNT(*) as count 
        FROM usage_logs 
        WHERE {where_clause}
        GROUP BY feature
    ''', params)
    
    for row in cursor.fetchall():
        result[row['feature']] = {
            "filtered_count": row['count'],
            "logs": []
        }
    
    # 獲取最近 100 筆記錄
    cursor.execute(f'''
        SELECT * FROM usage_logs 
        WHERE {where_clause}
        ORDER BY timestamp DESC 
        LIMIT 100
    ''', params)
    
    logs_by_feature = defaultdict(list)
    for row in cursor.fetchall():
        logs_by_feature[row['feature']].append({
            "timestamp": row['timestamp'],
            "year": row['year'],
            "month": row['month'],
            "day": row['day'],
            "hour": row['hour'],
            "minute": row['minute']
        })
    
    for feat, logs in logs_by_feature.items():
        if feat in result:
            result[feat]['logs'] = logs
    
    # 獲取各功能的總使用量
    cursor.execute('SELECT feature, COUNT(*) as count FROM usage_logs GROUP BY feature')
    for row in cursor.fetchall():
        if row['feature'] in result:
            result[row['feature']]['total_count'] = row['count']
        else:
            result[row['feature']] = {
                "total_count": row['count'],
                "filtered_count": 0,
                "logs": []
            }
    
    conn.close()
    return result

def get_summary_stats():
    """
    獲取摘要統計
    
    Returns:
        dict: 包含各功能總使用量、今日使用量、本月使用量
    """
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now()
    
    summary = {
        "total": 0,
        "today": 0,
        "this_month": 0,
        "by_feature": {}
    }
    
    # 各功能總數
    cursor.execute('SELECT feature, COUNT(*) as count FROM usage_logs GROUP BY feature')
    for row in cursor.fetchall():
        summary['by_feature'][row['feature']] = {"total": row['count'], "today": 0, "this_month": 0}
        summary['total'] += row['count']
    
    # 今日使用量
    cursor.execute('''
        SELECT feature, COUNT(*) as count FROM usage_logs 
        WHERE year = ? AND month = ? AND day = ?
        GROUP BY feature
    ''', (now.year, now.month, now.day))
    for row in cursor.fetchall():
        if row['feature'] in summary['by_feature']:
            summary['by_feature'][row['feature']]['today'] = row['count']
        summary['today'] += row['count']
    
    # 本月使用量
    cursor.execute('''
        SELECT feature, COUNT(*) as count FROM usage_logs 
        WHERE year = ? AND month = ?
        GROUP BY feature
    ''', (now.year, now.month))
    for row in cursor.fetchall():
        if row['feature'] in summary['by_feature']:
            summary['by_feature'][row['feature']]['this_month'] = row['count']
        summary['this_month'] += row['count']
    
    conn.close()
    return summary

def get_hourly_stats(feature_name=None, date=None):
    """
    獲取每小時統計
    
    Args:
        feature_name: 功能名稱，None 表示全部
        date: 日期 (YYYY-MM-DD)，None 表示今天
    
    Returns:
        dict: 每小時使用量 {0: count, 1: count, ...}
    """
    conn = get_db()
    cursor = conn.cursor()
    
    if date:
        target_year, target_month, target_day = map(int, date.split('-'))
    else:
        now = datetime.now()
        target_year, target_month, target_day = now.year, now.month, now.day
    
    conditions = ["year = ?", "month = ?", "day = ?"]
    params = [target_year, target_month, target_day]
    
    if feature_name:
        conditions.append("feature = ?")
        params.append(feature_name)
    
    where_clause = " AND ".join(conditions)
    
    cursor.execute(f'''
        SELECT hour, COUNT(*) as count FROM usage_logs 
        WHERE {where_clause}
        GROUP BY hour
    ''', params)
    
    hourly = {}
    for row in cursor.fetchall():
        hourly[row['hour']] = row['count']
    
    conn.close()
    return hourly

# 功能中文名稱對照
FEATURE_NAMES = {
    "tarot": "塔羅牌",
    "bazi": "八字命理",
    "astrology": "西洋占星",
    "humandesign": "人類圖",
    "ziwei": "紫微斗數",
    "integration": "多系統整合"
}
