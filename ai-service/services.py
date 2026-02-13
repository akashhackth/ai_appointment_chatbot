from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from database import Appointment
import uuid


class AppointmentService:
    """Service for managing appointments."""
    
    @staticmethod
    def check_availability(
        db: Session,
        date: datetime,
        time: datetime,
        duration_minutes: int = 60
    ) -> bool:
        """Check if a time slot is available."""
        end_time = time + timedelta(minutes=duration_minutes)
        
        # Check for overlapping appointments
        conflicting = db.query(Appointment).filter(
            and_(
                Appointment.appointment_date == date.date(),
                Appointment.status.in_(['scheduled', 'confirmed']),
                or_(
                    # New appointment starts during existing
                    and_(
                        Appointment.appointment_time <= time,
                        Appointment.end_time > time
                    ),
                    # New appointment ends during existing
                    and_(
                        Appointment.appointment_time < end_time,
                        Appointment.end_time >= end_time
                    ),
                    # New appointment encompasses existing
                    and_(
                        Appointment.appointment_time >= time,
                        Appointment.end_time <= end_time
                    )
                )
            )
        ).first()
        
        return conflicting is None
    
    @staticmethod
    def get_available_slots(
        db: Session,
        date: datetime,
        duration_minutes: int = 60
    ) -> List[Dict]:
        """Get available time slots for a given date."""
        available_slots = []
        
        # Business hours: 9 AM to 5 PM
        start_hour = 9
        end_hour = 17
        
        for hour in range(start_hour, end_hour):
            slot_time = datetime.combine(date.date(), datetime.min.time()).replace(hour=hour)
            
            if AppointmentService.check_availability(db, date, slot_time, duration_minutes):
                available_slots.append({
                    'time': slot_time.strftime('%I:%M %p'),
                    'datetime': slot_time.isoformat()
                })
        
        return available_slots
    
    @staticmethod
    def create_appointment(
        db: Session,
        user_id: uuid.UUID,
        appointment_date: datetime,
        appointment_time: datetime,
        service_type: str = "General Consultation",
        notes: Optional[str] = None,
        duration_minutes: int = 60
    ) -> Appointment:
        """Create a new appointment."""
        end_time = appointment_time + timedelta(minutes=duration_minutes)
        
        appointment = Appointment(
            user_id=user_id,
            appointment_date=appointment_date.date(),
            appointment_time=appointment_time,
            end_time=end_time,
            service_type=service_type,
            status='scheduled',
            notes=notes
        )
        
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        
        return appointment
    
    @staticmethod
    def get_user_appointments(
        db: Session,
        user_id: uuid.UUID,
        include_past: bool = False
    ) -> List[Appointment]:
        """Get all appointments for a user."""
        query = db.query(Appointment).filter(Appointment.user_id == user_id)
        
        if not include_past:
            query = query.filter(Appointment.appointment_date >= datetime.now().date())
        
        return query.order_by(Appointment.appointment_date, Appointment.appointment_time).all()
    
    @staticmethod
    def cancel_appointment(
        db: Session,
        appointment_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Optional[Appointment]:
        """Cancel an appointment."""
        appointment = db.query(Appointment).filter(
            and_(
                Appointment.id == appointment_id,
                Appointment.user_id == user_id
            )
        ).first()
        
        if appointment:
            appointment.status = 'cancelled'
            appointment.cancelled_at = datetime.utcnow()
            db.commit()
            db.refresh(appointment)
        
        return appointment
    
    @staticmethod
    def update_appointment(
        db: Session,
        appointment_id: uuid.UUID,
        user_id: uuid.UUID,
        **kwargs
    ) -> Optional[Appointment]:
        """Update an appointment."""
        appointment = db.query(Appointment).filter(
            and_(
                Appointment.id == appointment_id,
                Appointment.user_id == user_id
            )
        ).first()
        
        if appointment:
            for key, value in kwargs.items():
                if hasattr(appointment, key):
                    setattr(appointment, key, value)
            
            db.commit()
            db.refresh(appointment)
        
        return appointment
