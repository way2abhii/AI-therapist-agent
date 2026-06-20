# Step1: Setup Streamlit
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("🧠 SafeSpace – AI Mental Health Therapist")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Step2: User is able to ask question
# Chat input
user_input = st.chat_input("What's on your mind today?")
if user_input:
    # Append user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    response = None
    try:
        response = requests.post(
            BACKEND_URL,
            json={"message": user_input},
            timeout=60
        )

        st.write("Status Code:", response.status_code)
        st.write("Response Text:", response.text)

        data = response.json()
        # If backend returned an error (e.g., rate limit), show it and skip adding to chat
        if isinstance(data, dict) and "error" in data:
            st.error(f"Backend error: {data['error']}")
        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f'{data["response"]} WITH TOOL: [{data["tool_called"]}]'
            })

    except Exception as e:
        st.error(f"Error: {e}")
        st.code(response.text if response is not None else "No response received")
        
# Step3: Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])