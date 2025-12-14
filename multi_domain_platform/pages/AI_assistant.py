import streamlit as st
from services.ai_assistant import AIAssistant

# Page title
st.title("AI Assistant")

if "ai" not in st.session_state:
    st.session_state.ai= AIAssistant()

# Display conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history= []

st.subheader("Conversation")
for entry in st.session_state.chat_history:
    role= entry["role"]
    content= entry["content"]
    if role== "user":
        st.markdown(f"**You:** {content}")
    else:
        st.markdown(f"**AI:** {content}")

# User input
user_input= st.text_input("Ask something:")

# Send button
if st.button("Send"):
    if user_input:
        # Send message to AI service
        response= st.session_state.ai.send_message(user_input)
        
        # Update chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Display AI response
        st.markdown(f"**AI:** {response}")

# Clear conversation
if st.button("Clear Conversation"):
    st.session_state.ai.clear_history()
    st.session_state.chat_history = []
    st.success("Conversation cleared!")

