-- ============================================
-- AI Appointment Chatbot - Database Schema
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- Table: users
-- Stores user authentication and profile data
-- ============================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    business_id UUID -- For multi-tenancy support
);

-- Indexes for users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_business_id ON users(business_id);
CREATE INDEX idx_users_created_at ON users(created_at);

-- ============================================
-- Table: appointments
-- Stores appointment scheduling data
-- ============================================
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    end_time TIME NOT NULL,
    service_type VARCHAR(255),
    status VARCHAR(50) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'confirmed', 'cancelled', 'completed', 'no-show')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP,
    business_id UUID, -- For multi-tenancy support
    metadata JSONB -- For additional flexible data
);

-- Indexes for appointments table
CREATE INDEX idx_appointments_user_id ON appointments(user_id);
CREATE INDEX idx_appointments_date_time ON appointments(appointment_date, appointment_time);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_appointments_business_id ON appointments(business_id);
CREATE INDEX idx_appointments_created_at ON appointments(created_at);

-- Composite index for finding available slots
CREATE INDEX idx_appointments_availability ON appointments(appointment_date, appointment_time, status) 
WHERE status NOT IN ('cancelled');

-- ============================================
-- Table: chat_sessions
-- Stores conversation metadata and state
-- ============================================
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    session_metadata JSONB, -- Store conversation state, context, etc.
    business_id UUID
);

-- Indexes for chat_sessions table
CREATE INDEX idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_started_at ON chat_sessions(started_at);
CREATE INDEX idx_chat_sessions_is_active ON chat_sessions(is_active);
CREATE INDEX idx_chat_sessions_business_id ON chat_sessions(business_id);

-- ============================================
-- Table: chat_messages
-- Stores individual chat messages
-- ============================================
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message_type VARCHAR(50) NOT NULL CHECK (message_type IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB, -- For storing intent, entities, confidence scores, etc.
    token_count INTEGER
);

-- Indexes for chat_messages table
CREATE INDEX idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX idx_chat_messages_created_at ON chat_messages(created_at);
CREATE INDEX idx_chat_messages_type ON chat_messages(message_type);

-- ============================================
-- Table: availability_slots (Optional)
-- Pre-defined available time slots
-- ============================================
CREATE TABLE availability_slots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6), -- 0=Sunday, 6=Saturday
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    business_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for availability lookup
CREATE INDEX idx_availability_day_time ON availability_slots(day_of_week, start_time, is_available);

-- ============================================
-- Table: refresh_tokens
-- Store refresh tokens for JWT authentication
-- ============================================
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMP,
    is_revoked BOOLEAN DEFAULT FALSE
);

-- Indexes for refresh_tokens
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
CREATE INDEX idx_refresh_tokens_token_hash ON refresh_tokens(token_hash);

-- ============================================
-- Functions and Triggers
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for users table
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Trigger for appointments table
CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Views
-- ============================================

-- View for upcoming appointments
CREATE VIEW upcoming_appointments AS
SELECT 
    a.id,
    a.user_id,
    u.full_name,
    u.email,
    a.appointment_date,
    a.appointment_time,
    a.end_time,
    a.service_type,
    a.status,
    a.notes
FROM appointments a
JOIN users u ON a.user_id = u.id
WHERE a.appointment_date >= CURRENT_DATE
    AND a.status NOT IN ('cancelled', 'completed')
ORDER BY a.appointment_date, a.appointment_time;

-- View for user appointment history
CREATE VIEW user_appointment_history AS
SELECT 
    u.id as user_id,
    u.full_name,
    u.email,
    COUNT(a.id) as total_appointments,
    COUNT(CASE WHEN a.status = 'completed' THEN 1 END) as completed_appointments,
    COUNT(CASE WHEN a.status = 'cancelled' THEN 1 END) as cancelled_appointments,
    MAX(a.appointment_date) as last_appointment_date
FROM users u
LEFT JOIN appointments a ON u.id = a.user_id
GROUP BY u.id, u.full_name, u.email;

-- ============================================
-- Performance Notes
-- ============================================
-- 1. UUID primary keys provide good distribution for sharding
-- 2. Indexes on foreign keys for JOIN performance
-- 3. Composite indexes for common query patterns
-- 4. JSONB columns for flexible schema evolution
-- 5. CHECK constraints for data integrity
-- 6. Cascading deletes for data consistency
-- 7. Timestamp indexes for time-based queries
-- 8. business_id for future multi-tenancy support
