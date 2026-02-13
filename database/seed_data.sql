-- ============================================
-- Sample Data for Testing
-- ============================================

-- Insert sample users
-- Password: 'password123' hashed with bcrypt
INSERT INTO users (id, email, password_hash, full_name, phone_number) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'john.doe@example.com', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'John Doe', '+1-555-0101'),
('b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'jane.smith@example.com', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'Jane Smith', '+1-555-0102'),
('c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'bob.wilson@example.com', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'Bob Wilson', '+1-555-0103');

-- Insert sample appointments
INSERT INTO appointments (id, user_id, appointment_date, appointment_time, end_time, service_type, status, notes) VALUES
-- Future appointments
('d0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', CURRENT_DATE + INTERVAL '3 days', '10:00:00', '11:00:00', 'Consultation', 'scheduled', 'Initial consultation'),
('d1eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', CURRENT_DATE + INTERVAL '7 days', '14:00:00', '15:00:00', 'Follow-up', 'confirmed', 'Follow-up session'),
('d2eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', 'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', CURRENT_DATE + INTERVAL '5 days', '11:00:00', '12:00:00', 'Consultation', 'scheduled', NULL),
-- Past appointments
('d3eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', CURRENT_DATE - INTERVAL '10 days', '09:00:00', '10:00:00', 'Consultation', 'completed', 'Completed successfully'),
('d4eebc99-9c0b-4ef8-bb6d-6bb9bd380a18', 'c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', CURRENT_DATE - INTERVAL '5 days', '15:00:00', '16:00:00', 'Consultation', 'cancelled', 'Cancelled by user');

-- Insert sample chat sessions
INSERT INTO chat_sessions (id, user_id, session_metadata) VALUES
('e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', '{"intent": "book_appointment", "entities": {"date": "next Monday", "time": "10am"}}'),
('e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a20', 'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', '{"intent": "check_availability", "entities": {}}');

-- Insert sample chat messages
INSERT INTO chat_messages (session_id, user_id, message_type, content, metadata) VALUES
-- Session 1 messages
('e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'user', 'I would like to book an appointment', '{"intent": "book_appointment", "confidence": 0.95}'),
('e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'assistant', 'I''d be happy to help you book an appointment. What date and time would work best for you?', '{"action": "collect_info"}'),
('e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'user', 'How about next Monday at 10am?', '{"entities": {"date": "next Monday", "time": "10am"}}'),
('e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'assistant', 'Perfect! I have availability on Monday at 10:00 AM. Your appointment has been scheduled. You''ll receive a confirmation email shortly.', '{"action": "appointment_created", "appointment_id": "d0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14"}'),
-- Session 2 messages
('e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a20', 'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'user', 'What times are available this week?', '{"intent": "check_availability"}'),
('e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a20', 'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'assistant', 'Let me check our availability for this week. We have openings on Wednesday at 11am, Thursday at 2pm, and Friday at 9am. Would any of these work for you?', '{"available_slots": ["Wed 11am", "Thu 2pm", "Fri 9am"]}');

-- Insert default availability slots (Monday-Friday, 9am-5pm)
INSERT INTO availability_slots (day_of_week, start_time, end_time) VALUES
-- Monday
(1, '09:00:00', '10:00:00'),
(1, '10:00:00', '11:00:00'),
(1, '11:00:00', '12:00:00'),
(1, '13:00:00', '14:00:00'),
(1, '14:00:00', '15:00:00'),
(1, '15:00:00', '16:00:00'),
(1, '16:00:00', '17:00:00'),
-- Tuesday
(2, '09:00:00', '10:00:00'),
(2, '10:00:00', '11:00:00'),
(2, '11:00:00', '12:00:00'),
(2, '13:00:00', '14:00:00'),
(2, '14:00:00', '15:00:00'),
(2, '15:00:00', '16:00:00'),
(2, '16:00:00', '17:00:00'),
-- Wednesday
(3, '09:00:00', '10:00:00'),
(3, '10:00:00', '11:00:00'),
(3, '11:00:00', '12:00:00'),
(3, '13:00:00', '14:00:00'),
(3, '14:00:00', '15:00:00'),
(3, '15:00:00', '16:00:00'),
(3, '16:00:00', '17:00:00'),
-- Thursday
(4, '09:00:00', '10:00:00'),
(4, '10:00:00', '11:00:00'),
(4, '11:00:00', '12:00:00'),
(4, '13:00:00', '14:00:00'),
(4, '14:00:00', '15:00:00'),
(4, '15:00:00', '16:00:00'),
(4, '16:00:00', '17:00:00'),
-- Friday
(5, '09:00:00', '10:00:00'),
(5, '10:00:00', '11:00:00'),
(5, '11:00:00', '12:00:00'),
(5, '13:00:00', '14:00:00'),
(5, '14:00:00', '15:00:00'),
(5, '15:00:00', '16:00:00'),
(5, '16:00:00', '17:00:00');

-- Verification queries
-- SELECT * FROM users;
-- SELECT * FROM appointments ORDER BY appointment_date, appointment_time;
-- SELECT * FROM upcoming_appointments;
-- SELECT * FROM user_appointment_history;
