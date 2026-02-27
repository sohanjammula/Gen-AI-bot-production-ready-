class PromptManager:

    SYSTEM_PROMPT = """
    You are an expert Career Advisor chatbot.

    Rules:
    - Give structured answers
    - Be concise but helpful
    - Stay within career guidance domain
    - If question is outside domain, politely refuse
    """

    @staticmethod
    def build_prompt(user_query, chat_history):
        history_text = "\n".join(chat_history)

        return f"""
        {PromptManager.SYSTEM_PROMPT}

        Chat History:
        {history_text}

        User Question:
        {user_query}

        Assistant:
        """