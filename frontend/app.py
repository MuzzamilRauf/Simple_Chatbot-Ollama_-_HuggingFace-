import streamlit as st
import requests

# Set the FastAPI URL
API_URL = "http://127.0.0.1:8080/chats"

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize input text if it's not already in session state
if "input_text" not in st.session_state:
    st.session_state.input_text = ""


def get_chatbot_response(query):
    try:
        # Send the query as a JSON request
        response = requests.post(API_URL, json={"query": query})
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json().get("response")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the chatbot API: {e}")
        return None


# Streamlit UI Layout
st.title("What can I help with?")

# Display chat history
for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Assistant:** {chat['bot']}")

# User input field at the bottom
user_input = st.chat_input("Type your message and press Enter...")

# Process user input after the input is submitted
if user_input:
    response = get_chatbot_response(user_input)

    if response:
        # Store the conversation in session state
        st.session_state.chat_history.append({"user": user_input, "bot": response})

        # Clear the input field after submission by setting the value in session state
        st.session_state.input_text = ""

        # Refresh the page to display updated history
        st.rerun()  # Updated method to rerun the Streamlit app

