from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from helper import models
from typing import Optional
from helper.database import engine, get_db
from helper import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Voice Receptionist Backend")

class CallStartIn(BaseModel):
    hotel_id: UUID
    caller_phone: str | None = None

class BookingUpdateIn(BaseModel):
    checkin_date_raw: Optional[str] = None
    nights: Optional[str] = None
    status: Optional[str] = None

    
@app.post("/calls/start")
def start_call(payload: CallStartIn, db: Session = Depends(get_db)):
    call = models.Call(
        hotel_id=payload.hotel_id,
        caller_phone=payload.caller_phone,
        outcome="IN_PROGRESS"
    )
    db.add(call)
    db.commit()
    db.refresh(call)
    return {"call_id": call.id}

class MessageIn(BaseModel):
    sender: str  # USER or AI
    message: str


@app.post("/calls/{call_id}/messages")
def log_message(
    call_id: UUID,
    payload: MessageIn,
    db: Session = Depends(get_db)
):
    msg = models.CallMessage(
        call_id=call_id,
        sender=payload.sender,
        message=payload.message
    )
    db.add(msg)
    db.commit()
    return {"status": "ok"}

class CallEndIn(BaseModel):
    outcome: str  # ANSWERED, ESCALATED, BOOKING_STARTED


@app.post("/calls/{call_id}/end")
def end_call(
    call_id: UUID,
    payload: CallEndIn,
    db: Session = Depends(get_db)
):
    call = db.query(models.Call).get(call_id)
    if not call:
        return {"error": "call not found"}

    call.ended_at = datetime.utcnow()
    call.outcome = payload.outcome

    db.commit()
    return {"status": "ended"}

@app.get("/calls")
def list_calls(db: Session = Depends(get_db)):
    calls = (
        db.query(models.Call)
        .order_by(models.Call.started_at.desc())
        .all()
    )

    return [
        {
            "id": c.id,
            "caller_phone": c.caller_phone,
            "started_at": c.started_at,
            "ended_at": c.ended_at,
            "outcome": c.outcome
        }
        for c in calls
    ]

@app.get("/calls/{call_id}/messages")
def get_call_messages(call_id: UUID, db: Session = Depends(get_db)):
    messages = (
        db.query(models.CallMessage)
        .filter(models.CallMessage.call_id == call_id)
        .order_by(models.CallMessage.created_at)
        .all()
    )

    return [
        {
            "sender": m.sender,
            "message": m.message,
            "created_at": m.created_at
        }
        for m in messages
    ]


@app.get("/bookings")
def list_bookings(db: Session = Depends(get_db)):
    bookings = db.query(models.Booking).order_by(models.Booking.created_at.desc()).all()

    return [
        {
            "id": b.id,
            "status": b.status,
            "checkin_date": b.checkin_date,
            "nights": b.nights,
            "guests": b.guests,
            "created_by": b.created_by
        }
        for b in bookings
    ]


@app.post("/bookings/start")
def start_booking(call_id: UUID, db: Session = Depends(get_db)):
    call = db.query(models.Call).get(call_id)
    if not call:
        return {"error": "Call not found"}

    booking = models.Booking(
        hotel_id=call.hotel_id,
        call_id=call.id,
        status="IN_PROGRESS",
        created_by="AI"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {"booking_id": booking.id}

@app.patch("/bookings/{booking_id}")
def update_booking(
    booking_id: UUID,
    payload: BookingUpdateIn,
    db: Session = Depends(get_db)
):
    booking = db.query(models.Booking).get(booking_id)

    if not booking:
        return {"error": "Booking not found"}

    # Update only provided fields
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(booking, field, value)

    db.commit()
    db.refresh(booking)

    return {
        "id": booking.id,
        "status": booking.status,
        "checkin_date_raw": booking.checkin_date_raw,
        "nights": booking.nights
    }