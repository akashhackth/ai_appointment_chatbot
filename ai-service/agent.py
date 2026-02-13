from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json
from services import AppointmentService
from sqlalchemy.orm import Session
import uuid
import re


class AppointmentAgent:
    """LangChain agent for handling appointment booking conversations."""
    
    def __init__(self, openai_api_key: str, model_name: str = "gpt-4-turbo-preview"):
        self.llm = ChatOpenAI(
            api_key=openai_api_key,
            model_name=model_name,
            temperature=0.7
        )
        self.tools = self._create_tools()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
    def _create_tools(self) -> list:
        """Create tools for the agent."""
        return [
            Tool(
                name="check_availability",
                func=self._check_availability_tool,
                description="""Check if appointments are available on a specific date. 
                Input should be a date string in format YYYY-MM-DD. 
                Returns available time slots for that date."""
            ),
            Tool(
                name="book_appointment",
                func=self._book_appointment_tool,
                description="""Book an appointment for the user. 
                Input should be JSON with keys: date (YYYY-MM-DD), time (HH:MM), 
                service_type (optional), notes (optional).
                Returns confirmation of the booked appointment."""
            ),
            Tool(
                name="view_appointments",
                func=self._view_appointments_tool,
                description="""View all upcoming appointments for the user.
                No input required. Returns list of scheduled appointments."""
            ),
            Tool(
                name="cancel_appointment",
                func=self._cancel_appointment_tool,
                description="""Cancel an appointment by its ID.
                Input should be the appointment ID (UUID).
                Returns confirmation of cancellation."""
            ),
        ]
    
    def _check_availability_tool(self, date_str: str) -> str:
        """Tool function to check availability."""
        try:
            # This is a placeholder - actual DB access will be injected
            target_date = datetime.strptime(date_str.strip(), "%Y-%m-%d")
            
            # Simulated response for now
            if target_date.weekday() >= 5:  # Weekend
                return "We are closed on weekends. Please choose a weekday."
            
            # Return available slots (simplified)
            available_times = ["9:00 AM", "10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM", "4:00 PM"]
            return f"Available slots on {target_date.strftime('%B %d, %Y')}: {', '.join(available_times)}"
        
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD format (e.g., 2024-03-15)."
    
    def _book_appointment_tool(self, appointment_json: str) -> str:
        """Tool function to book an appointment."""
        try:
            data = json.loads(appointment_json) if isinstance(appointment_json, str) else appointment_json
            
            date = data.get('date')
            time = data.get('time')
            service = data.get('service_type', 'General Consultation')
            
            # Placeholder response
            return f"✓ Appointment booked successfully!\nDate: {date}\nTime: {time}\nService: {service}\nYou will receive a confirmation email shortly."
        
        except Exception as e:
            return f"Error booking appointment: {str(e)}"
    
    def _view_appointments_tool(self, _: str = "") -> str:
        """Tool function to view appointments."""
        # Placeholder - will fetch from database
        return "You have 1 upcoming appointment:\n• March 15, 2024 at 10:00 AM - General Consultation"
    
    def _cancel_appointment_tool(self, appointment_id: str) -> str:
        """Tool function to cancel an appointment."""
        return f"Appointment {appointment_id} has been cancelled successfully."
    
    def create_agent_executor(self) -> AgentExecutor:
        """Create the agent executor with tools and prompts."""
        
        system_message = """You are a helpful AI assistant for booking appointments. Your role is to:

1. Help users book, view, modify, or cancel appointments
2. Check availability for requested dates and times
3. Collect necessary information: date, time, service type
4. Provide clear, friendly responses
5. Handle ambiguous requests by asking clarifying questions

Guidelines:
- Business hours: Monday-Friday, 9:00 AM - 5:00 PM
- Each appointment is 1 hour long
- Be conversational and empathetic
- If the user's request is unclear, ask for clarification
- Always confirm booking details before finalizing
- Provide alternative options if requested time is unavailable

When booking:
- Confirm date and time explicitly
- Ask about service type if not mentioned
- Provide a summary before final confirmation

Available services:
- General Consultation
- Follow-up Appointment
- Initial Assessment
"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )


class ConversationManager:
    """Manages conversation state and history."""
    
    def __init__(self, db: Session, user_id: uuid.UUID, session_id: Optional[uuid.UUID] = None):
        self.db = db
        self.user_id = user_id
        self.session_id = session_id or uuid.uuid4()
        self.conversation_history = []
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to conversation history."""
        from database import ChatMessage
        
        message = ChatMessage(
            session_id=self.session_id,
            user_id=self.user_id,
            message_type=role,
            content=content,
            metadata=metadata or {}
        )
        
        self.db.add(message)
        self.db.commit()
        
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.utcnow()
        })
    
    def get_history(self, limit: int = 10) -> list:
        """Get recent conversation history."""
        from database import ChatMessage
        
        messages = self.db.query(ChatMessage).filter(
            ChatMessage.session_id == self.session_id
        ).order_by(ChatMessage.created_at.desc()).limit(limit).all()
        
        return [{
            'role': msg.message_type,
            'content': msg.content,
            'timestamp': msg.created_at
        } for msg in reversed(messages)]


def parse_natural_date(date_str: str) -> Optional[datetime]:
    """Parse natural language dates like 'tomorrow', 'next Monday', etc."""
    date_str = date_str.lower().strip()
    today = datetime.now()
    
    if 'today' in date_str:
        return today
    elif 'tomorrow' in date_str:
        return today + timedelta(days=1)
    elif 'next monday' in date_str:
        days_ahead = 0 - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)
    elif 'next tuesday' in date_str:
        days_ahead = 1 - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)
    elif 'next wednesday' in date_str:
        days_ahead = 2 - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)
    elif 'next thursday' in date_str:
        days_ahead = 3 - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)
    elif 'next friday' in date_str:
        days_ahead = 4 - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)
    
    # Try to parse standard date format
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        pass
    
    return None


def parse_natural_time(time_str: str) -> Optional[str]:
    """Parse natural language times like '10am', 'two pm', etc."""
    time_str = time_str.lower().strip()
    
    # Handle formats like "10am", "2pm", "10:30am"
    match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', time_str)
    if match:
        hour = int(match.group(1))
        minute = match.group(2) or '00'
        period = match.group(3)
        
        if period == 'pm' and hour != 12:
            hour += 12
        elif period == 'am' and hour == 12:
            hour = 0
        
        return f"{hour:02d}:{minute}"
    
    return None
