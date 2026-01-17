-- Supabase Database Schema for Spiritual Advisor
-- Run this in Supabase SQL Editor

-- ========== Users Table ==========
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    google_id VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    avatar_url TEXT,
    api_key TEXT,
    free_trials INTEGER DEFAULT 10,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster Google ID lookups
CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ========== Readings Table ==========
CREATE TABLE IF NOT EXISTS readings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,  -- tarot, bazi, humandesign, astrology, ziwei, integration
    birth_data JSONB,           -- Stored birth info for reproducibility
    result JSONB NOT NULL,      -- The reading result
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_readings_user_id ON readings(user_id);
CREATE INDEX IF NOT EXISTS idx_readings_type ON readings(type);
CREATE INDEX IF NOT EXISTS idx_readings_created_at ON readings(created_at DESC);

-- ========== Row Level Security (Optional) ==========
-- Enable RLS for production security
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE readings ENABLE ROW LEVEL SECURITY;

-- ========== Sample Data (Optional - for testing) ==========
-- INSERT INTO users (google_id, email, name) 
-- VALUES ('test123', 'test@example.com', 'Test User');
