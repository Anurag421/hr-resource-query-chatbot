import streamlit as st
import requests

st.set_page_config(page_title="HR Resource Chatbot", page_icon="🤖")
st.title("🤖 HR Resource Query Chatbot")
st.markdown("Ask in natural language to find the right employee (e.g., *Python + AWS with 2+ years experience*)")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.text_input("Enter your query:", key="user_input")

# Handle submit
if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call FastAPI
    try:
        with st.spinner("Chatbot is thinking..."):
            response = requests.post(
                "http://localhost:8000/chat",
                json={"query": user_input}
            )

            if response.status_code == 200:
                data = response.json()
                gpt_reply = data.get("response", "No response generated.")
                results = data.get("results", [])

                # Save GPT reply
                st.session_state.messages.append({"role": "bot", "content": gpt_reply})

                # Show GPT reply
                st.markdown(f"#### 🤖 Chatbot Recommendation")
                st.markdown(gpt_reply)

                # Show matched profiles
                st.markdown("---")
                st.markdown("### 👥 Matched Profiles")
                for emp in results:
                    with st.container():
                        st.subheader(emp["name"])
                        st.markdown(f"**Experience:** {emp['experience_years']} years")
                        st.markdown(f"**Skills:** {', '.join(emp['skills'])}")
                        st.markdown(f"**Projects:** {', '.join(emp['projects'])}")
                        st.markdown(f"**Availability:** `{emp['availability']}`")
                        st.markdown("---")
            else:
                st.error(f"❌ API Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"⚠️ Connection error: {e}")

# Display past messages
with st.expander("🕘 Chat History", expanded=False):
    for msg in st.session_state.messages:
        role = "👤 You" if msg["role"] == "user" else "🤖 Bot"
        st.markdown(f"**{role}:** {msg['content']}")
