import streamlit as st
import requests
import io
import pandas as pd

st.set_page_config(page_title="HR Resource Chatbot", layout="centered")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💼 HR Resource Chatbot")
st.markdown("Ask questions about employees, departments, roles, etc.")

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message", placeholder="e.g., Who is the manager of the marketing team?")
    submitted = st.form_submit_button("Send")

# When user submits input
if submitted and user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call FastAPI
    try:
        with st.spinner("Chatbot is typing..."):
            response = requests.post(
                "http://127.0.0.1:8000/chat", json={"query": user_input}
            )
            if response.status_code == 200:
                bot_reply = response.json().get("response", "Sorry, no response received.")
            else:
                bot_reply = f"❌ Error {response.status_code}: Could not get a response."
    except Exception as e:
        bot_reply = f"⚠️ Connection error: {e}"

    # Append bot message
    st.session_state.messages.append({"role": "bot", "content": bot_reply})

# Show chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])





if st.button("📥 Download Chat History (CSV)"):
    if st.session_state.messages:
        df = pd.DataFrame(st.session_state.messages)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="chat_history.csv",
            mime="text/csv"
        )
    else:
        st.warning("No chat history to download yet.")