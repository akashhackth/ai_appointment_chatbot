# Backend API - Node.js Express

RESTful API for authentication, session management, and communication with the AI service.

## Features

- JWT-based authentication (access + refresh tokens)
- User registration and login
- Session management
- Rate limiting and security headers
- Input validation
- Error handling
- PostgreSQL database integration

## Setup

```bash
# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run in development
npm run dev

# Run in production
npm start
```

## API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - Register new user
- `POST /login` - Login user
- `POST /refresh` - Refresh access token
- `GET /me` - Get current user (protected)

### Chat (`/api/chat`)
- `POST /message` - Send message to chatbot (protected)
- `GET /history/:sessionId` - Get chat history (protected)
- `GET /sessions` - Get user sessions (protected)
- `POST /session` - Create new session (protected)
- `DELETE /session/:sessionId` - End session (protected)
- `POST /chatbot/token` - Generate chatbot token (protected)

### Health
- `GET /` - Root endpoint
- `GET /health` - Health check

## Architecture

```
┌─────────────────┐
│   Express App   │
└────────┬────────┘
         │
    ┌────┴────┐
    │ Routes  │
    └────┬────┘
         │
    ┌────┴────────┐
    │ Middleware  │
    │ - Auth      │
    │ - Validate  │
    │ - Error     │
    └────┬────────┘
         │
    ┌────┴────────┐
    │  Services   │
    └────┬────────┘
         │
    ┌────┴────────┐
    │  Database   │
    └─────────────┘
```

## Security

- Helmet.js for security headers
- CORS configuration
- Rate limiting
- JWT token expiration
- Password hashing with bcrypt
- Input validation
- SQL injection prevention

## Example Requests

### Register
```bash
curl -X POST http://localhost:4000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "fullName": "John Doe",
    "phoneNumber": "+1-555-0123"
  }'
```

### Login
```bash
curl -X POST http://localhost:4000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Send Chat Message
```bash
curl -X POST http://localhost:4000/api/chat/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "I want to book an appointment",
    "sessionId": "optional-session-uuid"
  }'
```

## Testing

```bash
npm test
```
