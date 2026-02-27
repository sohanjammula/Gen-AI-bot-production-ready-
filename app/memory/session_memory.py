import streamlit as st

class SessionMemory:

    @staticmethod
    def initialize():
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

    @staticmethod
    def add_message(role, content):
        st.session_state.chat_history.append(f"{role}: {content}")

    @staticmethod
    def get_history():
        return st.session_state.chat_history