# AI Appointment Chatbot - Senior AI Engineer Assessment

## Overview

A full-stack AI-powered appointment booking chatbot built with:
- **Frontend**: Next.js with TypeScript
- **Backend API**: Node.js with Express
- **AI Service**: Python with LangChain and FastAPI
- **Database**: PostgreSQL

## Architecture

```
┌─────────────────┐
│   Next.js UI    │ (Port 3000)
│   (Frontend)    │
└────────┬────────┘
         │
         │ HTTP/WebSocket
         ▼
┌─────────────────┐
│  Express API    │ (Port 4000)
│   (Backend)     │
└────────┬────────┘
         │
         │ HTTP
         ▼
┌─────────────────┐      ┌──────────────┐
│  Python AI      │◄────►│  PostgreSQL  │
│  (LangChain)    │      │   Database   │
└─────────────────┘      └──────────────┘
   (Port 8000)              (Port 5432)
```

## Features

### Frontend
- Real-time chat interface
- User authentication (signup/login)
- Session management with JWT
- Clean, conversational UX

### Backend API
- `/api/chatbot/token` - Generate short-lived access tokens
- JWT-based authentication
- Request validation middleware
- Rate limiting
- Error handling

### AI Service
- LangChain-powered conversational agent
- Multi-turn conversation state management
- Appointment scheduling workflow:
  - Collect booking details (date, time, service)
  - Check availability
  - Create/update appointments
- Conversation history logging

### Database
- **users** - User profiles and authentication
- **appointments** - Scheduling data and status
- **chat_sessions** - Conversation logs and metadata

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+
- PostgreSQL 14+
- Docker and Docker Compose (recommended)

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repo-url>
cd ai-appointment-chatbot

# Copy environment variables
cp .env.example .env

# Edit .env with your API keys (OpenAI, etc.)
nano .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:4000
# AI Service: http://localhost:8000
# PostgreSQL: localhost:5432
```

### Option 2: Manual Setup

#### 1. Database Setup

```bash
# Create PostgreSQL database
createdb ai_appointment_db

# Run migrations
cd database
psql ai_appointment_db < schema.sql
psql ai_appointment_db < seed_data.sql
```

#### 2. AI Service (Python)

```bash
cd ai-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Run the service
uvicorn main:app --reload --port 8000
```

#### 3. Backend API (Node.js)

```bash
cd backend
npm install

# Configure environment
cp .env.example .env
# Edit .env with database and JWT settings

# Run the server
npm run dev
```

#### 4. Frontend (Next.js)

```bash
cd frontend
npm install

# Configure environment
cp .env.example .env
# Edit .env with backend API URL

# Run the development server
npm run dev
```

## Environment Variables

### AI Service (.env)
```
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://user:password@localhost:5432/ai_appointment_db
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/ai_appointment_db
JWT_SECRET=your_jwt_secret
AI_SERVICE_URL=http://localhost:8000
PORT=4000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:4000
```

## API Documentation

### Backend Endpoints

#### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - Login and receive JWT token
- `GET /api/auth/me` - Get current user (requires auth)

#### Chatbot
- `POST /api/chatbot/token` - Generate short-lived chatbot access token
- `POST /api/chat/message` - Send message to AI chatbot
- `GET /api/chat/history` - Get conversation history

#### Appointments
- `GET /api/appointments` - Get user's appointments
- `GET /api/appointments/:id` - Get specific appointment
- `PUT /api/appointments/:id` - Update appointment
- `DELETE /api/appointments/:id` - Cancel appointment

### AI Service Endpoints

- `POST /chat` - Process chat message with LangChain
- `GET /health` - Health check

## Design Decisions

### 1. Architecture
- **Microservices approach**: Separate AI logic from business logic for scalability
- **Stateless backend**: JWT tokens for horizontal scaling
- **Event-driven**: WebSocket for real-time chat updates

### 2. AI Integration
- **LangChain**: For flexible prompt engineering and conversation memory
- **OpenAI GPT-4**: For natural language understanding (swappable with other providers)
- **Memory**: ConversationBufferMemory for multi-turn context
- **Tools**: Custom function calling for appointment operations

### 3. Security
- JWT tokens with short expiration (15 min access, 7 day refresh)
- Rate limiting on API endpoints
- Input validation on all endpoints
- SQL injection prevention with parameterized queries
- CORS configuration for frontend

### 4. Database Design
- Normalized schema with proper foreign keys
- Indexes on frequently queried columns
- `business_id` column for multi-tenancy support
- Soft deletes for appointments

## Tradeoffs & Limitations

### Current Limitations
1. **In-memory conversation state**: For production, use Redis or database-backed sessions
2. **Simplified availability logic**: Hardcoded business hours (9 AM - 5 PM)
3. **No real-time notifications**: Email/SMS notifications not implemented
4. **Basic error recovery**: LLM failures could be handled more gracefully
5. **No admin panel**: Appointment management is user-facing only

### Scalability Considerations
- AI service can be scaled horizontally with session store
- Backend API is stateless and scales easily
- Database connection pooling configured
- Ready for Redis caching layer

### Production Enhancements
- Add Prometheus metrics and Grafana dashboards
- Implement comprehensive logging (ELK stack)
- Add integration tests and E2E tests
- Set up CI/CD pipeline
- Add API versioning
- Implement WebSocket for real-time updates
- Add LLM response streaming

## Testing

```bash
# Backend tests
cd backend
npm test

# AI service tests
cd ai-service
pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

The application is containerized and can be deployed to:
- AWS (ECS/EKS with RDS)
- Google Cloud Platform (Cloud Run with Cloud SQL)
- Azure (Container Apps with Azure Database)
- Any Kubernetes cluster

## Assumptions

1. Single business/organization (multi-tenancy schema ready but not implemented)
2. Appointments are 1 hour duration by default
3. Business operates 9 AM - 5 PM, Monday-Friday
4. Users book appointments for themselves only
5. English language only
6. No payment processing

## Future Improvements

- [ ] Calendar integration (Google Calendar, Outlook)
- [ ] SMS/Email notifications
- [ ] Voice chat support
- [ ] Multiple languages
- [ ] Admin dashboard
- [ ] Analytics and reporting
- [ ] Payment integration
- [ ] Video call integration (Zoom, Teams)

## License

MIT

## Contact

For questions about this assessment submission, please contact the repository owner.
