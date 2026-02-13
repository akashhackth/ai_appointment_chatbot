# API Documentation

## Base URL
- Production: `https://your-domain.com`
- Development: `http://localhost:4000`

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

### Token Expiration
- Access Token: 15 minutes
- Refresh Token: 7 days

---

## Endpoints

### Authentication

#### POST /api/auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "fullName": "John Doe",
  "phoneNumber": "+1-555-0123" // optional
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "fullName": "John Doe"
  }
}
```

---

#### POST /api/auth/login
Login and receive JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "fullName": "John Doe"
  },
  "accessToken": "jwt-access-token",
  "refreshToken": "jwt-refresh-token"
}
```

---

#### POST /api/auth/refresh
Refresh expired access token.

**Request Body:**
```json
{
  "refreshToken": "jwt-refresh-token"
}
```

**Response (200):**
```json
{
  "message": "Token refreshed",
  "accessToken": "new-jwt-access-token",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "fullName": "John Doe"
  }
}
```

---

#### GET /api/auth/me
Get current user information. **[Protected]**

**Response (200):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "fullName": "John Doe",
    "phoneNumber": "+1-555-0123",
    "createdAt": "2024-03-15T10:00:00Z"
  }
}
```

---

### Chat

#### POST /api/chat/message
Send a message to the AI chatbot. **[Protected]**

**Request Body:**
```json
{
  "message": "I want to book an appointment for next Monday",
  "sessionId": "uuid" // optional, for continuing conversation
}
```

**Response (200):**
```json
{
  "success": true,
  "response": "I'd be happy to help you book an appointment...",
  "session_id": "uuid",
  "timestamp": "2024-03-15T10:30:00Z"
}
```

---

#### GET /api/chat/history/:sessionId
Get chat history for a session. **[Protected]**

**Query Parameters:**
- `limit` (optional): Maximum number of messages (default: 50, max: 100)

**Response (200):**
```json
{
  "sessionId": "uuid",
  "messages": [
    {
      "id": "uuid",
      "type": "user",
      "content": "I want to book an appointment",
      "timestamp": "2024-03-15T10:00:00Z"
    },
    {
      "id": "uuid",
      "type": "assistant",
      "content": "I'd be happy to help...",
      "timestamp": "2024-03-15T10:00:05Z"
    }
  ]
}
```

---

#### GET /api/chat/sessions
Get user's chat sessions. **[Protected]**

**Response (200):**
```json
{
  "sessions": [
    {
      "id": "uuid",
      "startedAt": "2024-03-15T10:00:00Z",
      "endedAt": null,
      "isActive": true,
      "sessionMetadata": {}
    }
  ]
}
```

---

#### POST /api/chat/session
Create a new chat session. **[Protected]**

**Response (201):**
```json
{
  "sessionId": "uuid",
  "message": "Session created"
}
```

---

#### DELETE /api/chat/session/:sessionId
End a chat session. **[Protected]**

**Response (200):**
```json
{
  "message": "Session ended"
}
```

---

#### POST /api/chatbot/token
Generate a short-lived chatbot access token. **[Protected]**

**Response (200):**
```json
{
  "token": "short-lived-jwt-token",
  "expiresIn": 300,
  "user": {
    "id": "uuid",
    "email": "user@example.com"
  }
}
```

---

## AI Service Endpoints

These endpoints are typically called by the backend, but can be used directly for testing.

### POST /chat
Process a chat message with the AI.

**Request Body:**
```json
{
  "user_id": "uuid",
  "message": "I want to book an appointment",
  "session_id": "uuid" // optional
}
```

**Response (200):**
```json
{
  "response": "I'd be happy to help you book an appointment...",
  "session_id": "uuid",
  "timestamp": "2024-03-15T10:30:00Z"
}
```

---

### POST /availability
Check available appointment slots.

**Request Body:**
```json
{
  "date": "2024-03-20"
}
```

**Response (200):**
```json
{
  "date": "2024-03-20",
  "available_slots": [
    {
      "time": "09:00 AM",
      "datetime": "2024-03-20T09:00:00"
    },
    {
      "time": "10:00 AM",
      "datetime": "2024-03-20T10:00:00"
    }
  ]
}
```

---

### POST /appointments
Create a new appointment.

**Request Body:**
```json
{
  "user_id": "uuid",
  "date": "2024-03-20",
  "time": "10:00",
  "service_type": "General Consultation",
  "notes": "Initial consultation"
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "appointment_date": "2024-03-20",
  "appointment_time": "10:00",
  "service_type": "General Consultation",
  "status": "scheduled",
  "created_at": "2024-03-15T10:30:00Z"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Status Codes
- `400` - Bad Request (validation error)
- `401` - Unauthorized (missing or invalid token)
- `404` - Not Found
- `409` - Conflict (e.g., resource already exists)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error

---

## Rate Limiting

- Window: 15 minutes
- Max Requests: 100 per window
- Applies to all `/api/*` endpoints

When rate limit is exceeded:
```json
{
  "error": "Too many requests from this IP, please try again later."
}
```
