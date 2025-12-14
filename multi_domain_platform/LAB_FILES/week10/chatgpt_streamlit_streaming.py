import streamlit as st
from openai	import OpenAI

client= OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.title("ChatGPT with Streaming")

if 'messages' not in st.session_state:
	st.session_state.messages= []

for message	in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])
		
prompt= st.chat_input("Say	something...")
		
if prompt:
	with st.chat_message("user"):
		st.markdown(prompt)
				
st.session_state.messages.append({
	"role":	"user",
	"content":prompt
	})
				
completion= client.chat.completions.create(
	model="gpt-4o",
	messages=st.session_state.messages,
	stream=True
	)
				
with st.chat_message("assistant"):
	container= st.empty()
	full_reply= ""		
								
for chunk in completion:
	delta= chunk.choices[0].delta
	if delta.content:
		full_reply+= delta.content
		container.markdown(full_reply)	
				
st.session_state.messages.append({
	"role":	"assistant",
	"content":full_reply
	})