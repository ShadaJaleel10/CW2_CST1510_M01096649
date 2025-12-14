from typing import List, Dict # [cite: 215]

class AIAssistant:
    """Simple wrapper around an AI/chat model.""" 

    def __init__(self, system_prompt: str= "You are a helpful assistant."):
        self._system_prompt= system_prompt
        self._history: List[Dict[str, str]] = [] 

    def send_message(self, user_message: str):
        """Send a message and get a (fake) response. Replace this body with your real API call.""" 
        self._history.append({"role": "user", "content": user_message}) 
        response = f"[AI reply to]: {user_message[:50]}" 
        self._history.append({"role": "assistant", "content": response}) 
        return response
    
    def clear_history(self):
        self._history.clear() 