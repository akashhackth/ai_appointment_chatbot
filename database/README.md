# Database Setup

This directory contains the PostgreSQL database schema and seed data.

## Files

- `schema.sql` - Complete database schema with tables, indexes, and views
- `seed_data.sql` - Sample data for testing

## Tables

### Core Tables
- **users** - User authentication and profiles
- **appointments** - Appointment scheduling data
- **chat_sessions** - Conversation sessions metadata
- **chat_messages** - Individual chat messages

### Supporting Tables
- **availability_slots** - Business hours and available time slots
- **refresh_tokens** - JWT refresh tokens storage

## Setup

### Using Docker
```bash
# Database will be automatically initialized via docker-compose
docker-compose up database
```

### Manual Setup
```bash
# Create database
createdb ai_appointment_db

# Run schema
psql ai_appointment_db < schema.sql

# Insert sample data
psql ai_appointment_db < seed_data.sql
```

## Sample Credentials

Test users (password: `password123`):
- john.doe@example.com
- jane.smith@example.com
- bob.wilson@example.com

## Queries

```sql
-- View upcoming appointments
SELECT * FROM upcoming_appointments;

-- View user statistics
SELECT * FROM user_appointment_history;

-- Find available slots on a specific date
SELECT * FROM availability_slots WHERE day_of_week = 1; -- Monday
```
