INSERT INTO hotels (name, phone, checkin_time, checkout_time)
VALUES ('Hotel Sunrise', '+91-9876543210', '12:00 PM', '11:00 AM');


INSERT INTO room_types (hotel_id, name, base_price, max_guests)
SELECT id, 'Standard', 1500, 2 FROM hotels;

INSERT INTO room_types (hotel_id, name, base_price, max_guests)
SELECT id, 'Deluxe', 2200, 3 FROM hotels;


INSERT INTO calls (hotel_id, caller_phone, outcome)
SELECT id, '+91-9999999999', 'BOOKING_STARTED' FROM hotels;
