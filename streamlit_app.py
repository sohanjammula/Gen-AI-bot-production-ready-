import streamlit as st
from app.services.gemini_service import GeminiService
from app.prompts.prompt_manager import PromptManager
from app.memory.session_memory import SessionMemory

st.set_page_config(page_title="GenAI Career Chatbot", layout="wide")

st.title("🤖 Production GenAI Career Chatbot")

SessionMemory.initialize()
gemini = GeminiService()

user_input = st.chat_input("Ask your career question...")

# Display history
for msg in st.session_state.chat_history:
    role, content = msg.split(":", 1)
    with st.chat_message(role.lower()):
        st.write(content)

if user_input:
    SessionMemory.add_message("User", user_input)

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            prompt = PromptManager.build_prompt(
                user_input,
                SessionMemory.get_history()
            )
            response = gemini.generate_response(prompt)
            st.write(response)

    SessionMemory.add_message("Assistant", response)