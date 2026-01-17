"""
Supabase Database Module
========================
Database connection and operations for user authentication and reading history.

Environment Variables Required:
- SUPABASE_URL: Your Supabase project URL
- SUPABASE_KEY: Your Supabase anon/service key
"""

import os
from supabase import create_client, Client
from datetime import datetime
from typing import Optional, List, Dict, Any

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

_supabase_client: Optional[Client] = None


def get_supabase() -> Optional[Client]:
    """Get Supabase client (lazy initialization)"""
    global _supabase_client
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("⚠️ Supabase not configured. Set SUPABASE_URL and SUPABASE_KEY in .env")
        return None
    
    if _supabase_client is None:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    return _supabase_client


# ========== User Operations ==========

def get_or_create_user(google_id: str, email: str, name: str = "", avatar_url: str = "") -> Optional[Dict]:
    """Get existing user or create new one from Google login"""
    supabase = get_supabase()
    if not supabase:
        return None
    
    try:
        # Check if user exists
        result = supabase.table("users").select("*").eq("google_id", google_id).execute()
        
        if result.data and len(result.data) > 0:
            # Update last login
            user = result.data[0]
            supabase.table("users").update({
                "name": name,
                "avatar_url": avatar_url,
                "updated_at": datetime.now().isoformat()
            }).eq("id", user["id"]).execute()
            return user
        
        # Create new user
        new_user = {
            "google_id": google_id,
            "email": email,
            "name": name,
            "avatar_url": avatar_url,
            "created_at": datetime.now().isoformat()
        }
        result = supabase.table("users").insert(new_user).execute()
        return result.data[0] if result.data else None
        
    except Exception as e:
        print(f"❌ Error in get_or_create_user: {e}")
        return None


def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Get user by ID"""
    supabase = get_supabase()
    if not supabase:
        return None
    
    try:
        result = supabase.table("users").select("*").eq("id", user_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"❌ Error in get_user_by_id: {e}")
        return None


def update_user_api_key(user_id: int, api_key: str) -> bool:
    """Update user's API key"""
    supabase = get_supabase()
    if not supabase:
        return False
    
    try:
        supabase.table("users").update({
            "api_key": api_key,
            "updated_at": datetime.now().isoformat()
        }).eq("id", user_id).execute()
        return True
    except Exception as e:
        print(f"❌ Error in update_user_api_key: {e}")
        return False


# ========== Reading History Operations ==========

def save_reading(user_id: int, reading_type: str, result: Dict, birth_data: Optional[Dict] = None) -> Optional[Dict]:
    """Save a reading result for a user"""
    supabase = get_supabase()
    if not supabase:
        return None
    
    try:
        reading = {
            "user_id": user_id,
            "type": reading_type,
            "result": result,
            "birth_data": birth_data,
            "created_at": datetime.now().isoformat()
        }
        result = supabase.table("readings").insert(reading).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"❌ Error in save_reading: {e}")
        return None


def get_user_readings(user_id: int, reading_type: Optional[str] = None, limit: int = 50) -> List[Dict]:
    """Get user's reading history"""
    supabase = get_supabase()
    if not supabase:
        return []
    
    try:
        query = supabase.table("readings").select("*").eq("user_id", user_id)
        
        if reading_type:
            query = query.eq("type", reading_type)
        
        result = query.order("created_at", desc=True).limit(limit).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"❌ Error in get_user_readings: {e}")
        return []


def delete_reading(user_id: int, reading_id: int) -> bool:
    """Delete a specific reading (only if owned by user)"""
    supabase = get_supabase()
    if not supabase:
        return False
    
    try:
        supabase.table("readings").delete().eq("id", reading_id).eq("user_id", user_id).execute()
        return True
    except Exception as e:
        print(f"❌ Error in delete_reading: {e}")
        return False


def get_reading_count(user_id: int) -> Dict[str, int]:
    """Get count of readings by type for a user"""
    supabase = get_supabase()
    if not supabase:
        return {}
    
    try:
        result = supabase.table("readings").select("type").eq("user_id", user_id).execute()
        counts = {}
        if result.data:
            for reading in result.data:
                t = reading["type"]
                counts[t] = counts.get(t, 0) + 1
        return counts
    except Exception as e:
        print(f"❌ Error in get_reading_count: {e}")
        return {}


# ========== Free Trial Operations ==========

def check_and_reset_daily_trials(user_id: int) -> None:
    """Check if daily trials need reset (new day) and reset if necessary"""
    supabase = get_supabase()
    if not supabase:
        return
    
    try:
        result = supabase.table("users").select("last_reset_date").eq("id", user_id).execute()
        if not result.data or len(result.data) == 0:
            return
        
        last_reset = result.data[0].get("last_reset_date")
        today = datetime.now().date().isoformat()
        
        # If last reset was before today, reset daily trials
        if last_reset is None or str(last_reset) < today:
            supabase.table("users").update({
                "daily_trials": 5,
                "last_reset_date": today,
                "updated_at": datetime.now().isoformat()
            }).eq("id", user_id).execute()
            print(f"✅ Reset daily trials for user {user_id}")
    except Exception as e:
        print(f"❌ Error in check_and_reset_daily_trials: {e}")


def get_user_free_trials(user_id: int) -> int:
    """Get remaining free trials for a user (initial + daily combined)"""
    details = get_user_trial_details(user_id)
    return details.get("total", 0)


def get_user_trial_details(user_id: int) -> Dict[str, Any]:
    """Get detailed trial stats including next reset time"""
    supabase = get_supabase()
    if not supabase:
        return {"total": 0, "initial": 0, "daily": 0}
    
    try:
        # First check and reset daily trials if needed
        check_and_reset_daily_trials(user_id)
        
        result = supabase.table("users").select("free_trials, daily_trials").eq("id", user_id).execute()
        
        initial = 0
        daily = 0
        
        if result.data and len(result.data) > 0:
            initial = result.data[0].get("free_trials", 0) or 0
            daily = result.data[0].get("daily_trials", 0) or 0
            
        # Calculate next reset time (tomorrow 00:00:00 server time)
        tomorrow = datetime.now().date() + timedelta(days=1)
        next_reset = datetime.combine(tomorrow, datetime.min.time()).isoformat()
            
        return {
            "total": initial + daily,
            "initial": initial,
            "daily": daily,
            "next_reset": next_reset
        }
    except Exception as e:
        print(f"❌ Error in get_user_trial_details: {e}")
        return {"total": 0, "initial": 0, "daily": 0}


def use_free_trial(user_id: int) -> Dict[str, Any]:
    """
    Use one free trial for a user.
    Priority: 1. Initial free_trials (10), 2. Daily trials (5)
    """
    supabase = get_supabase()
    if not supabase:
        return {"success": False, "error": "Database not configured", "remaining": 0}
    
    try:
        # Check and reset daily trials first
        check_and_reset_daily_trials(user_id)
        
        # Get current trials
        details = get_user_trial_details(user_id)
        free_trials = details["initial"]
        daily_trials = details["daily"]
        
        total = free_trials + daily_trials
        if total <= 0:
            return {"success": False, "error": "No free trials remaining", "remaining": 0}
        
        # Priority: use initial free_trials first, then daily_trials
        update_data = {"updated_at": datetime.now().isoformat()}
        if free_trials > 0:
            update_data["free_trials"] = free_trials - 1
            new_total = (free_trials - 1) + daily_trials
        else:
            update_data["daily_trials"] = daily_trials - 1
            new_total = free_trials + (daily_trials - 1)
        
        supabase.table("users").update(update_data).eq("id", user_id).execute()
        
        return {"success": True, "remaining": new_total}
    except Exception as e:
        print(f"❌ Error in use_free_trial: {e}")
        return {"success": False, "error": str(e), "remaining": 0}

