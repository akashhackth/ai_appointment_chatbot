# AI Service - Python LangChain Microservice

This service handles conversational AI for appointment booking using LangChain and OpenAI.

## Features

- LangChain agent with custom tools
- Multi-turn conversation memory
- Appointment scheduling logic
- Natural language date/time parsing
- Conversation history logging

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Run the service
uvicorn main:app --reload --port 8000
```

## API Endpoints

### Chat
- `POST /chat` - Send message to chatbot
- `GET /chat/history/{session_id}` - Get conversation history

### Appointments
- `POST /availability` - Check available time slots
- `POST /appointments` - Create new appointment
- `GET /appointments/user/{user_id}` - Get user appointments
- `DELETE /appointments/{appointment_id}` - Cancel appointment

### Health
- `GET /` - Root endpoint
- `GET /health` - Health check

## Architecture

```
┌─────────────────┐
│   FastAPI       │
│   Routes        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  LangChain      │◄────►│  Appointment     │
│  Agent          │      │  Service         │
└────────┬────────┘      └────────┬─────────┘
         │                        │
         │                        ▼
         │               ┌──────────────────┐
         └──────────────►│   PostgreSQL     │
                         │   Database       │
                         └──────────────────┘
```

## LangChain Components

- **ChatOpenAI**: GPT-4 model integration
- **AgentExecutor**: Orchestrates tool usage
- **Tools**: Custom functions for appointment operations
- **Memory**: ConversationBufferMemory for context
- **Prompts**: System prompt for appointment booking

## Example Usage

```python
# Chat request
POST /chat
{
    "user_id": "user-uuid",
    "message": "I want to book an appointment for next Monday at 10am",
    "session_id": "session-uuid"  # optional
}

# Response
{
    "response": "I'd be happy to help you book an appointment...",
    "session_id": "session-uuid",
    "timestamp": "2024-03-15T10:30:00"
}
```

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=. --cov-report=html
```
