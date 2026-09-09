import uuid
from sqlalchemy import (
    Column, String, Integer, Date, DateTime,
    ForeignKey, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)
    checkin_time = Column(String)
    checkout_time = Column(String)
    cancellation_policy = Column(String)
    created_at = Column(DateTime, server_default=func.now())


class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id = Column(UUID(as_uuid=True), ForeignKey("hotels.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    base_price = Column(Integer, nullable=False)
    max_guests = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())

    hotel = relationship("Hotel")


class Call(Base):
    __tablename__ = "calls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id = Column(UUID(as_uuid=True), ForeignKey("hotels.id"))
    caller_phone = Column(String)
    started_at = Column(DateTime, server_default=func.now())
    ended_at = Column(DateTime)
    outcome = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    hotel = relationship("Hotel")


class CallMessage(Base):
    __tablename__ = "call_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id", ondelete="CASCADE"))
    sender = Column(String)
    message = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    call = relationship("Call")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id = Column(UUID(as_uuid=True), ForeignKey("hotels.id"))
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"))

    guest_name = Column(String)
    guest_phone = Column(String)

    checkin_date = Column(Date)
    nights = Column(Integer)
    room_type_id = Column(UUID(as_uuid=True), ForeignKey("room_types.id"))
    guests = Column(Integer)

    status = Column(String)
    created_by = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    hotel = relationship("Hotel")
    room_type = relationship("RoomType")
    call = relationship("Call")

    __table_args__ = (
        CheckConstraint(
            status.in_(["IN_PROGRESS", "PENDING_CONFIRMATION", "CONFIRMED", "CANCELLED"]),
            name="booking_status_check"
        ),
        CheckConstraint(
            created_by.in_(["AI", "HUMAN"]),
            name="booking_creator_check"
        ),
    )
