CREATE TABLE hotels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    checkin_time TEXT,
    checkout_time TEXT,
    cancellation_policy TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE room_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hotel_id UUID REFERENCES hotels(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    base_price INTEGER NOT NULL,
    max_guests INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE calls (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hotel_id UUID REFERENCES hotels(id),
    caller_phone TEXT,
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    outcome TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE call_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    call_id UUID REFERENCES calls(id) ON DELETE CASCADE,
    sender TEXT CHECK (sender IN ('USER', 'AI')),
    message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hotel_id UUID REFERENCES hotels(id),
    call_id UUID REFERENCES calls(id),

    guest_name TEXT,
    guest_phone TEXT,

    checkin_date DATE,
    nights INTEGER,
    room_type_id UUID REFERENCES room_types(id),
    guests INTEGER,

    status TEXT CHECK (
        status IN (
            'IN_PROGRESS',
            'PENDING_CONFIRMATION',
            'CONFIRMED',
            'CANCELLED'
        )
    ),

    created_by TEXT CHECK (created_by IN ('AI', 'HUMAN')),
    created_at TIMESTAMP DEFAULT NOW()
);
