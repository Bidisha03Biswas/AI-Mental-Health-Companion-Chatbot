#Step1:SetUp Streamlit
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("🧠 AI Mental Health Therapist")

#Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Step2: User is able to as questions
#Chat input
user_input = st.chat_input("What's on your mind today?")
if user_input:
    #Append user's message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    #AI agent exists here (Setting up a dummy response)
    response = requests.post(BACKEND_URL, json={"message": user_input})  #Pay load to backend
    st.session_state.chat_history.append({"role": "assistant", "content": f'{response.json()["response"]} WITH TOOL: [{response.json()["tool_called"]}]'})
# Step3: Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

