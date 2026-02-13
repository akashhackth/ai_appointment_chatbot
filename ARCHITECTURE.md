# System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                                  │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │              Next.js Frontend (Port 3000)                       │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │   │
│  │  │  Login   │  │ Register │  │   Chat   │  │   Layout     │  │   │
│  │  │  Page    │  │   Page   │  │  Window  │  │  Component   │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │   │
│  │                                                                 │   │
│  │  ┌─────────────────────────────────────────────────────────┐  │   │
│  │  │           AuthContext (JWT State Management)            │  │   │
│  │  └─────────────────────────────────────────────────────────┘  │   │
│  │                                                                 │   │
│  │  ┌─────────────────────────────────────────────────────────┐  │   │
│  │  │    API Client (Axios with Auto Token Refresh)           │  │   │
│  │  └─────────────────────────────────────────────────────────┘  │   │
│  └────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ HTTP/HTTPS
                               │ JWT Token in Header
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Express Backend API (Port 4000)                      │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │                      Middleware Layer                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │   │
│  │  │  Auth    │  │  CORS    │  │   Rate   │  │    Error     │  │   │
│  │  │  (JWT)   │  │  Helmet  │  │  Limit   │  │   Handler    │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │                       API Routes                                │   │
│  │                                                                  │   │
│  │  /api/auth/*                    /api/chat/*                    │   │
│  │  ├─ POST /register              ├─ POST /message               │   │
│  │  ├─ POST /login                 ├─ GET /history/:id            │   │
│  │  ├─ POST /refresh               ├─ GET /sessions               │   │
│  │  └─ GET /me                     └─ POST /chatbot/token         │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │                      Service Layer                              │   │
│  │  ┌─────────────────┐              ┌──────────────────┐         │   │
│  │  │  authService    │              │   chatService    │         │   │
│  │  │  - register()   │              │   - sendMessage()│         │   │
│  │  │  - login()      │              │   - getHistory() │         │   │
│  │  │  - refresh()    │              │   - getSessions()│         │   │
│  │  └─────────────────┘              └──────────────────┘         │   │
│  └────────────────────────────────────────────────────────────────┘   │
└──────────────────┬──────────────────────────────┬─────────────────────┘
                   │                               │
                   │ PostgreSQL                    │ HTTP POST
                   │ Queries                       │ /chat
                   ▼                               ▼
┌─────────────────────────────┐    ┌──────────────────────────────────────┐
│  PostgreSQL Database         │    │   Python AI Service (Port 8000)     │
│      (Port 5432)             │    │                                      │
│                              │    │  ┌────────────────────────────────┐ │
│  ┌────────────────────────┐ │    │  │      FastAPI Endpoints          │ │
│  │ Tables:                │ │    │  │  - POST /chat                   │ │
│  │  • users               │ │    │  │  - POST /availability           │ │
│  │  • appointments        │ │◄───┼──┤  - POST /appointments          │ │
│  │  • chat_sessions       │ │    │  │  - GET /health                 │ │
│  │  • chat_messages       │ │    │  └────────────────────────────────┘ │
│  │  • refresh_tokens      │ │    │                                      │
│  │  • availability_slots  │ │    │  ┌────────────────────────────────┐ │
│  └────────────────────────┘ │    │  │      LangChain Agent            │ │
│                              │    │  │                                 │ │
│  ┌────────────────────────┐ │    │  │  ┌──────────────────────────┐ │ │
│  │ Indexes:               │ │    │  │  │   OpenAI GPT-4           │ │ │
│  │  • email               │ │    │  │  │   Temperature: 0.7       │ │ │
│  │  • user_id             │ │    │  │  └──────────────────────────┘ │ │
│  │  • appointment_date    │ │    │  │                                 │ │
│  │  • session_id          │ │    │  │  ┌──────────────────────────┐ │ │
│  └────────────────────────┘ │    │  │  │  Conversation Memory     │ │ │
│                              │    │  │  │  Buffer (Multi-turn)     │ │ │
│  ┌────────────────────────┐ │    │  │  └──────────────────────────┘ │ │
│  │ Views:                 │ │    │  │                                 │ │
│  │  • upcoming_appts      │ │    │  │  ┌──────────────────────────┐ │ │
│  │  • user_history        │ │    │  │  │   Custom Tools:          │ │ │
│  └────────────────────────┘ │    │  │  │   - check_availability   │ │ │
│                              │    │  │  │   - book_appointment     │ │ │
└──────────────────────────────┘    │  │  │   - view_appointments    │ │ │
                                     │  │  │   - cancel_appointment   │ │ │
                                     │  │  └──────────────────────────┘ │ │
                                     │  └────────────────────────────────┘ │
                                     │                                      │
                                     │  ┌────────────────────────────────┐ │
                                     │  │    Appointment Service          │ │
                                     │  │  - Availability checking        │ │
                                     │  │  - Conflict detection           │ │
                                     │  │  - CRUD operations              │ │
                                     │  └────────────────────────────────┘ │
                                     └──────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW EXAMPLE                               │
│                                                                          │
│  1. User types: "Book appointment for Monday at 10am"                  │
│                                                                          │
│  2. Frontend → POST /api/chat/message                                   │
│     Headers: Authorization: Bearer <jwt-token>                          │
│     Body: { message: "...", sessionId: "..." }                         │
│                                                                          │
│  3. Backend validates JWT token                                         │
│                                                                          │
│  4. Backend → POST http://ai-service:8000/chat                          │
│     Body: { user_id, message, session_id }                             │
│                                                                          │
│  5. AI Service:                                                         │
│     a. LangChain Agent analyzes message                                │
│     b. Extracts intent: "book_appointment"                             │
│     c. Extracts entities: date="Monday", time="10am"                   │
│     d. Calls tool: check_availability(date, time)                      │
│     e. Calls tool: book_appointment(...)                               │
│     f. Saves to database via SQLAlchemy                                │
│     g. Generates response via GPT-4                                    │
│                                                                          │
│  6. AI Service → Backend                                                │
│     Response: { response: "...", session_id, timestamp }               │
│                                                                          │
│  7. Backend saves chat message to database                              │
│                                                                          │
│  8. Backend → Frontend                                                  │
│     Response: { success: true, response: "..." }                       │
│                                                                          │
│  9. Frontend displays response in chat window                           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                      SECURITY LAYERS                                    │
│                                                                          │
│  Layer 1: Frontend                                                      │
│  • Input validation                                                     │
│  • XSS prevention                                                       │
│  • HTTPS only                                                          │
│                                                                          │
│  Layer 2: Backend                                                       │
│  • JWT authentication                                                   │
│  • Rate limiting (100 req/15min)                                       │
│  • CORS restrictions                                                    │
│  • Helmet security headers                                             │
│  • Input sanitization                                                   │
│                                                                          │
│  Layer 3: Database                                                      │
│  • Parameterized queries (SQL injection prevention)                    │
│  • Password hashing (bcrypt)                                           │
│  • Connection pooling                                                   │
│  • Row-level security ready                                            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                     DEPLOYMENT TOPOLOGY                                 │
│                                                                          │
│  Development:                                                           │
│  • All services on localhost                                           │
│  • Docker Compose orchestration                                        │
│  • Hot reload enabled                                                  │
│                                                                          │
│  Production (Example - AWS):                                           │
│  • Frontend: S3 + CloudFront (CDN)                                     │
│  • Backend: ECS Fargate (Auto-scaling)                                │
│  • AI Service: ECS Fargate (Auto-scaling)                             │
│  • Database: RDS PostgreSQL (Multi-AZ)                                │
│  • Load Balancer: ALB                                                  │
│  • Secrets: AWS Secrets Manager                                       │
│  • Monitoring: CloudWatch                                             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Design Patterns

### 1. Microservices Architecture
- Independent services with clear boundaries
- Each service can scale independently
- Technology-appropriate choices per service

### 2. Layered Architecture
```
Presentation → API → Service → Data
(Frontend)   (REST)  (Logic)  (Database)
```

### 3. Authentication Flow
```
Login → JWT Access Token (15min) + Refresh Token (7d)
      → Store tokens in localStorage
      → Include in Authorization header
      → Auto-refresh when expired
```

### 4. Chat Flow
```
User Input → Frontend → Backend → AI Service → LangChain → OpenAI
                                                         ↓
                                          Tools (DB Operations)
                                                         ↓
                                              Generate Response
```

### 5. Error Handling
```
Error Occurs → Try/Catch → Log Error → Format Response → User Feedback
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js + TypeScript | Modern React framework with SSR |
| **UI** | Tailwind CSS | Utility-first CSS framework |
| **Backend** | Express.js | RESTful API server |
| **AI Engine** | LangChain | LLM orchestration framework |
| **LLM** | OpenAI GPT-4 | Natural language understanding |
| **Database** | PostgreSQL | Relational data storage |
| **Auth** | JWT | Stateless authentication |
| **Container** | Docker | Service isolation |
| **Orchestration** | Docker Compose | Multi-service management |

## Scalability Strategy

### Horizontal Scaling
- Frontend: CDN + multiple instances
- Backend: Load balanced instances
- AI Service: Multiple workers
- Database: Read replicas

### Caching
- Redis for session storage
- CDN for static assets
- API response caching

### Performance
- Database indexes
- Connection pooling
- Lazy loading
- Code splitting
