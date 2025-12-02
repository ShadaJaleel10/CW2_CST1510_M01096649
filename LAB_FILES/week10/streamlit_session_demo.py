import streamlit as st 

st.title("Chat History	with Session State")

if 'messages' not in st.session_state:
	st.session_state.messages	= []

for message	in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])

prompt= st.chat_input("Say something...")
if prompt:
	st.session_state.messages.append({
		"role":	"user",
		"content": prompt
		})

ai_response = f"You said: {prompt}"

with st.chat_message("assistant"):
	st.markdown(ai_response)