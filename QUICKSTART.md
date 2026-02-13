# Quick Start Guide

Get the AI Appointment Chatbot running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Steps

### 1. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env
```

Edit the `OPENAI_API_KEY` line:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 2. Start Services

```bash
# Run the setup script
./setup.sh

# Or manually with docker-compose
docker-compose up -d
```

### 3. Wait for Services

Services take 30-60 seconds to start. Check status:
```bash
docker-compose logs -f
```

Look for:
- ✓ Database: "database system is ready to accept connections"
- ✓ Backend: "Status: Running ✓"
- ✓ AI Service: "Application startup complete"
- ✓ Frontend: "Ready in X ms"

### 4. Access the Application

Open your browser to: **http://localhost:3000**

### 5. Login

Use the demo credentials:
- **Email**: john.doe@example.com
- **Password**: password123

Or create a new account by clicking "create a new account"

### 6. Start Chatting!

Try these prompts:
- "I want to book an appointment"
- "What times are available next week?"
- "Book me for Monday at 10am"
- "Show my appointments"

---

## Troubleshooting

### Services Won't Start

```bash
# Check if ports are already in use
lsof -i :3000 -i :4000 -i :5432 -i :8000

# Stop and restart
docker-compose down
docker-compose up -d
```

### Database Connection Error

```bash
# Check database is ready
docker-compose logs database

# Restart just the database
docker-compose restart database
```

### OpenAI API Error

Make sure your `.env` file has a valid OpenAI API key:
```bash
cat .env | grep OPENAI_API_KEY
```

### Port Already in Use

If you get "port already allocated" error:

```bash
# Option 1: Stop the conflicting service
# Option 2: Edit docker-compose.yml to use different ports
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f frontend
docker-compose logs -f backend
docker-compose logs -f ai-service
docker-compose logs -f database
```

---

## Useful Commands

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v

# Restart a specific service
docker-compose restart backend

# Rebuild images
docker-compose up -d --build

# View running containers
docker-compose ps

# Access database
docker-compose exec database psql -U postgres ai_appointment_db
```

---

## Manual Setup (Without Docker)

If you prefer to run services individually:

### 1. Database
```bash
createdb ai_appointment_db
psql ai_appointment_db < database/schema.sql
psql ai_appointment_db < database/seed_data.sql
```

### 2. AI Service
```bash
cd ai-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your OpenAI key
uvicorn main:app --reload --port 8000
```

### 3. Backend
```bash
cd backend
npm install
cp .env.example .env
# Edit .env
npm run dev
```

### 4. Frontend
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local
npm run dev
```

---

## What's Next?

- 📖 Read [README.md](README.md) for full documentation
- 🔌 Check [API_DOCS.md](API_DOCS.md) for API reference
- 🚀 See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- 📋 View [SUBMISSION.md](SUBMISSION.md) for project overview

---

## Need Help?

If you encounter issues:
1. Check the logs: `docker-compose logs -f`
2. Verify environment variables in `.env`
3. Make sure Docker has enough resources (4GB RAM minimum)
4. Review the main README.md for detailed setup

---

**Happy Testing! 🎉**
