import requests

BASE_URL = "http://127.0.0.1:8000"

class BackendClient:
    def __init__(self, hotel_id: str, caller_phone: str | None = None):
        self.hotel_id = hotel_id
        self.caller_phone = caller_phone
        self.call_id = None
        self.booking_id = None   # 👈 NEW

    # -----------------------------
    # CALL LIFECYCLE
    # -----------------------------
    def start_call(self):
        res = requests.post(
            f"{BASE_URL}/calls/start",
            json={
                "hotel_id": self.hotel_id,
                "caller_phone": self.caller_phone
            }
        )
        res.raise_for_status()
        self.call_id = res.json()["call_id"]

    def log_user(self, text: str):
        if not self.call_id:
            return
        requests.post(
            f"{BASE_URL}/calls/{self.call_id}/messages",
            json={"sender": "USER", "message": text}
        )

    def log_ai(self, text: str):
        if not self.call_id:
            return
        requests.post(
            f"{BASE_URL}/calls/{self.call_id}/messages",
            json={"sender": "AI", "message": text}
        )

    def end_call(self, outcome="ANSWERED"):
        if not self.call_id:
            return
        requests.post(
            f"{BASE_URL}/calls/{self.call_id}/end",
            json={"outcome": outcome}
        )

    # -----------------------------
    # BOOKING TRANSACTION
    # -----------------------------
    def start_booking(self):
        """
        Creates an IN_PROGRESS booking linked to this call.
        """
        if not self.call_id:
            return None

        res = requests.post(
            f"{BASE_URL}/bookings/start",
            params={"call_id": self.call_id}
        )
        res.raise_for_status()

        self.booking_id = res.json()["booking_id"]
        return self.booking_id

    def update_booking(self, data: dict):
        """
        Incrementally update booking details.
        Example:
            {"checkin_date_raw": "tomorrow"}
            {"nights": "2"}
        """
        if not self.booking_id:
            return

        requests.patch(
            f"{BASE_URL}/bookings/{self.booking_id}",
            json=data
        )

    def cancel_booking(self):
        """
        Cancels an in-progress booking.
        """
        if not self.booking_id:
            return

        requests.post(
            f"{BASE_URL}/bookings/{self.booking_id}/cancel"
        )
