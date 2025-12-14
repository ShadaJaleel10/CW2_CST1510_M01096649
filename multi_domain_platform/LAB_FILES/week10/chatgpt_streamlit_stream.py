import streamlit	as st
from openai	import OpenAI

client	= OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(
	page_title="ChatGPT	Assistant",
	page_icon="💬",
	layout="wide"
)

st.title("ChatGPT- OpenAI API")
st.caption("Powered	by	GPT-4o")

if 'messages' not in st.session_state:
	st.session_state.messages= []

with st.sidebar:
	st.subheader("Chat	Controls")
				
message_count= len([m for m	in st.session_state.messages if m["role"]!= "system"])
st.metric("Messages", message_count)
				
if st.button(" Clear Chat",	use_container_width=True):
	st.session_state.messages	= []
	st.rerun()
				
model= st.selectbox(
	"Model",
	["gpt-4o",	"gpt-4o-mini"],
	index=0
	)
				
temperature= st.slider(
	"temperature", 
	min_value=0.0,
	max_value=2.0,
	value=1.0,
	step=0.1,
	help="Higher values	make output	more random" 
	)


for message	in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])

prompt= st.chat_input("Say	something...")
if prompt:
	with st.chat_message("user"):
		st.markdown(prompt)
				
st.session_state.messages.append({
	"role":	"user",
	"content":	prompt
	})
				
with st.spinner("Thinking..."):
	completion= client.chat.completions.create(
		model=model,
		messages=st.session_state.messages,
		temperature=temperature,
		stream=True
		)
				
with st.chat_message("assistant"):
	container= st.empty()
	full_reply= ""
								
for chunk in completion:
	delta= chunk.choices[0].delta
	if delta.content:
		full_reply+= delta.content
		container.markdown(full_reply + "▌")
								
container.markdown(full_reply)
				
st.session_state.messages.append({
	"role":	"assistant",
	"content":	full_reply
	})
