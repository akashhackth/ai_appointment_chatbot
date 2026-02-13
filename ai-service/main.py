from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from config import get_settings
from database import get_db, ChatSession, ChatMessage
from agent import AppointmentAgent, ConversationManager
from services import AppointmentService

# Initialize FastAPI app
app = FastAPI(
    title="AI Appointment Chatbot Service",
    description="LangChain-powered conversational appointment booking",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:4000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get settings
settings = get_settings()

# Initialize agent (singleton)
agent_executor = None


def get_agent():
    """Get or create agent instance."""
    global agent_executor
    if agent_executor is None:
        agent = AppointmentAgent(
            openai_api_key=settings.openai_api_key,
            model_name=settings.openai_model
        )
        agent_executor = agent.create_agent_executor()
    return agent_executor


# Pydantic models
class ChatRequest(BaseModel):
    user_id: str = Field(..., description="User ID")
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")


class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime


class AvailabilityRequest(BaseModel):
    date: str = Field(..., description="Date in YYYY-MM-DD format")


class AvailabilityResponse(BaseModel):
    date: str
    available_slots: List[dict]


class AppointmentRequest(BaseModel):
    user_id: str
    date: str
    time: str
    service_type: Optional[str] = "General Consultation"
    notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: str
    user_id: str
    appointment_date: str
    appointment_time: str
    service_type: str
    status: str
    created_at: datetime


# API Routes
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "AI Appointment Chatbot",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected",
        "openai": "configured" if settings.openai_api_key else "not configured"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint. Processes user messages through LangChain agent.
    """
    try:
        user_id = uuid.UUID(request.user_id)
        session_id = uuid.UUID(request.session_id) if request.session_id else uuid.uuid4()
        
        # Get or create chat session
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id
        ).first()
        
        if not session:
            session = ChatSession(
                id=session_id,
                user_id=user_id,
                is_active=True
            )
            db.add(session)
            db.commit()
        
        # Initialize conversation manager
        conv_manager = ConversationManager(db, user_id, session_id)
        
        # Save user message
        conv_manager.add_message('user', request.message)
        
        # Get agent and process message
        agent = get_agent()
        
        try:
            result = agent.invoke({
                "input": request.message
            })
            
            response_text = result.get('output', 'I apologize, but I encountered an issue. Could you please rephrase your request?')
        
        except Exception as e:
            print(f"Agent error: {e}")
            response_text = "I apologize for the inconvenience. I'm having trouble processing your request. Could you please try again or rephrase your question?"
        
        # Save assistant response
        conv_manager.add_message('assistant', response_text)
        
        return ChatResponse(
            response=response_text,
            session_id=str(session_id),
            timestamp=datetime.utcnow()
        )
    
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
        )


@app.get("/chat/history/{session_id}")
async def get_chat_history(
    session_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get chat history for a session."""
    try:
        session_uuid = uuid.UUID(session_id)
        
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_uuid
        ).order_by(ChatMessage.created_at).limit(limit).all()
        
        return {
            "session_id": session_id,
            "messages": [
                {
                    "id": str(msg.id),
                    "type": msg.message_type,
                    "content": msg.content,
                    "timestamp": msg.created_at.isoformat()
                }
                for msg in messages
            ]
        }
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID format")


@app.post("/availability", response_model=AvailabilityResponse)
async def check_availability(
    request: AvailabilityRequest,
    db: Session = Depends(get_db)
):
    """Check available appointment slots for a specific date."""
    try:
        target_date = datetime.strptime(request.date, "%Y-%m-%d")
        
        # Check if it's a weekend
        if target_date.weekday() >= 5:
            return AvailabilityResponse(
                date=request.date,
                available_slots=[]
            )
        
        slots = AppointmentService.get_available_slots(db, target_date)
        
        return AvailabilityResponse(
            date=request.date,
            available_slots=slots
        )
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")


@app.post("/appointments", response_model=AppointmentResponse)
async def create_appointment(
    request: AppointmentRequest,
    db: Session = Depends(get_db)
):
    """Create a new appointment."""
    try:
        user_id = uuid.UUID(request.user_id)
        appointment_datetime = datetime.strptime(f"{request.date} {request.time}", "%Y-%m-%d %H:%M")
        
        # Check availability
        if not AppointmentService.check_availability(db, appointment_datetime, appointment_datetime):
            raise HTTPException(status_code=409, detail="Time slot not available")
        
        # Create appointment
        appointment = AppointmentService.create_appointment(
            db=db,
            user_id=user_id,
            appointment_date=appointment_datetime,
            appointment_time=appointment_datetime,
            service_type=request.service_type,
            notes=request.notes
        )
        
        return AppointmentResponse(
            id=str(appointment.id),
            user_id=str(appointment.user_id),
            appointment_date=appointment.appointment_date.isoformat(),
            appointment_time=appointment.appointment_time.strftime("%H:%M"),
            service_type=appointment.service_type,
            status=appointment.status,
            created_at=appointment.created_at
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")


@app.get("/appointments/user/{user_id}")
async def get_user_appointments(
    user_id: str,
    include_past: bool = False,
    db: Session = Depends(get_db)
):
    """Get all appointments for a user."""
    try:
        user_uuid = uuid.UUID(user_id)
        appointments = AppointmentService.get_user_appointments(db, user_uuid, include_past)
        
        return {
            "user_id": user_id,
            "appointments": [
                {
                    "id": str(apt.id),
                    "date": apt.appointment_date.isoformat(),
                    "time": apt.appointment_time.strftime("%H:%M"),
                    "service_type": apt.service_type,
                    "status": apt.status,
                    "notes": apt.notes
                }
                for apt in appointments
            ]
        }
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")


@app.delete("/appointments/{appointment_id}")
async def cancel_appointment(
    appointment_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    """Cancel an appointment."""
    try:
        apt_uuid = uuid.UUID(appointment_id)
        user_uuid = uuid.UUID(user_id)
        
        appointment = AppointmentService.cancel_appointment(db, apt_uuid, user_uuid)
        
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        return {
            "message": "Appointment cancelled successfully",
            "appointment_id": appointment_id
        }
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
