import streamlit as st
import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Hotel AI Dashboard", layout="wide")

st.title("🏨 Hotel Receptionist Dashboard")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Calls", "Bookings"])

# -----------------------------
# CALLS PAGE
# -----------------------------
if page == "Calls":
    st.subheader("📞 Calls Overview")

    calls = requests.get(f"{BASE_URL}/calls").json()

    if not calls:
        st.info("No calls yet.")
    else:
        for call in calls:
            with st.expander(f"Call {call['id']}"):
                col1, col2, col3 = st.columns(3)

                col1.write(f"**Caller:** {call['caller_phone']}")
                col2.write(f"**Started:** {call['started_at']}")
                col3.write(f"**Outcome:** {call['outcome']}")

                st.markdown("### Conversation")

                messages = requests.get(
                    f"{BASE_URL}/calls/{call['id']}/messages"
                ).json()

                for msg in messages:
                    if msg["sender"] == "USER":
                        st.markdown(f"🧑 **Guest:** {msg['message']}")
                    else:
                        st.markdown(f"🤖 **AI:** {msg['message']}")

# -----------------------------
# BOOKINGS PAGE
# -----------------------------
elif page == "Bookings":
    st.subheader("📋 Bookings")

    bookings = requests.get(f"{BASE_URL}/bookings").json()

    if not bookings:
        st.info("No bookings yet.")
    else:
        st.table(bookings)
