# Project File Index

Complete reference of all files in this project.

## Root Directory

- **README.md** - Main project documentation
- **QUICKSTART.md** - 5-minute setup guide
- **SUBMISSION.md** - Assessment submission summary
- **API_DOCS.md** - Complete API reference
- **DEPLOYMENT.md** - Production deployment guide
- **.gitignore** - Git ignore patterns
- **.env.example** - Environment variables template
- **docker-compose.yml** - Multi-service orchestration
- **setup.sh** - Automated setup script (executable)

## Database (`/database`)

- **schema.sql** - Complete PostgreSQL DDL (tables, indexes, triggers, views)
- **seed_data.sql** - Sample data for testing
- **README.md** - Database documentation

### Tables Created
- `users` - User accounts and authentication
- `appointments` - Appointment scheduling
- `chat_sessions` - Conversation sessions
- `chat_messages` - Individual messages
- `availability_slots` - Business hours
- `refresh_tokens` - JWT token storage

## AI Service (`/ai-service`)

Python FastAPI service with LangChain integration.

### Core Files
- **main.py** - FastAPI application and endpoints
- **agent.py** - LangChain agent configuration
- **services.py** - Appointment business logic
- **database.py** - SQLAlchemy models
- **config.py** - Settings management
- **requirements.txt** - Python dependencies
- **Dockerfile** - Container configuration
- **.env.example** - Environment template
- **README.md** - Service documentation

### Key Features
- LangChain agent with custom tools
- OpenAI GPT-4 integration
- Conversation memory
- Appointment CRUD operations

## Backend (`/backend`)

Node.js Express REST API.

### Structure
```
backend/
├── src/
│   ├── middleware/
│   │   ├── auth.js              # JWT authentication
│   │   ├── validation.js        # Input validation
│   │   └── errorHandler.js      # Error handling
│   ├── routes/
│   │   ├── auth.js              # Auth endpoints
│   │   └── chat.js              # Chat endpoints
│   ├── services/
│   │   ├── authService.js       # Auth business logic
│   │   └── chatService.js       # Chat operations
│   ├── config.js                # Configuration
│   ├── database.js              # PostgreSQL connection
│   └── server.js                # Express app
├── package.json
├── Dockerfile
├── .env.example
└── README.md
```

### API Endpoints
- `/api/auth/*` - Authentication
- `/api/chat/*` - Chat operations
- `/api/chatbot/token` - Token generation
- `/health` - Health check

## Frontend (`/frontend`)

Next.js with TypeScript and Tailwind CSS.

### Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatWindow.tsx       # Chat interface
│   │   └── Layout.tsx           # App layout
│   ├── contexts/
│   │   └── AuthContext.tsx      # Auth state management
│   ├── lib/
│   │   └── api.ts               # API client with interceptors
│   ├── pages/
│   │   ├── _app.tsx             # App wrapper
│   │   ├── _document.tsx        # HTML document
│   │   ├── index.tsx            # Home/chat page
│   │   ├── login.tsx            # Login page
│   │   └── register.tsx         # Registration page
│   └── styles/
│       └── globals.css          # Global styles
├── package.json
├── tsconfig.json                # TypeScript config
├── tailwind.config.js           # Tailwind config
├── next.config.js               # Next.js config
├── postcss.config.js            # PostCSS config
├── .eslintrc.json               # ESLint config
├── Dockerfile
├── .env.example
└── README.md
```

### Pages
- `/` - Chat interface (protected)
- `/login` - User login
- `/register` - User registration

## Docker Configuration

### docker-compose.yml Services
1. **database** - PostgreSQL 15
2. **ai-service** - Python FastAPI (port 8000)
3. **backend** - Node.js Express (port 4000)
4. **frontend** - Next.js (port 3000)

### Individual Dockerfiles
- `ai-service/Dockerfile` - Python 3.11 slim
- `backend/Dockerfile` - Node 18 alpine
- `frontend/Dockerfile` - Node 18 alpine

## Documentation Files

### For Users
- **QUICKSTART.md** - Get started in 5 minutes
- **README.md** - Complete overview and instructions

### For Developers
- **API_DOCS.md** - API endpoint reference
- **DEPLOYMENT.md** - Production deployment guide
- Service-specific READMEs in each directory

### For Assessment
- **SUBMISSION.md** - Project summary for reviewers

## Environment Configuration

Each service has its own `.env.example`:

- **Root** - Shared variables
- **ai-service** - OpenAI key, database URL
- **backend** - JWT secret, database URL, service URLs
- **frontend** - Backend API URL

## Scripts

- **setup.sh** - Automated setup with Docker Compose
  - Checks prerequisites
  - Creates .env from template
  - Starts all services
  - Displays access URLs

## Key Technologies

### Frontend
- Next.js 14
- TypeScript
- React 18
- Tailwind CSS
- Axios

### Backend
- Node.js 18
- Express
- PostgreSQL driver (pg)
- JWT (jsonwebtoken)
- Bcrypt
- Express-validator

### AI Service
- Python 3.11
- FastAPI
- LangChain
- OpenAI
- SQLAlchemy
- Pydantic

### Database
- PostgreSQL 15
- UUID extension
- JSONB support
- Triggers and functions

### DevOps
- Docker
- Docker Compose
- Multi-stage builds

## File Statistics

- **Total Files**: ~50+
- **Lines of Code**: ~5,000+
- **Languages**: TypeScript, JavaScript, Python, SQL
- **Documentation**: 6 markdown files
- **Configuration**: 10+ config files

## Getting Started

1. Start here: **QUICKSTART.md**
2. Then read: **README.md**
3. For API details: **API_DOCS.md**
4. For deployment: **DEPLOYMENT.md**

## Development Workflow

```bash
# Setup
./setup.sh

# View logs
docker-compose logs -f

# Restart service
docker-compose restart <service-name>

# Stop all
docker-compose down

# Clean restart
docker-compose down -v && docker-compose up -d
```

## Production Checklist

See **DEPLOYMENT.md** for:
- [ ] Environment configuration
- [ ] Security hardening
- [ ] Database migration
- [ ] Service deployment
- [ ] Monitoring setup
- [ ] Backup strategy
- [ ] CI/CD pipeline

## Support

For questions:
1. Check relevant README.md
2. Review API_DOCS.md
3. Consult DEPLOYMENT.md
4. See code comments

---

**Last Updated**: February 6, 2026
