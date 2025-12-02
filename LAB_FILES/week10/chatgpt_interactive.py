from openai	import OpenAI

client= OpenAI(api_key="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")

messages=[
    {"role":"system","content":	"You are a helpful assistant."}
]

print("ChatGPT Console Chat (type 'quit' to	exit)")
print("-" * 50)
while True:
	user_input= input("You:	")
	if user_input.lower()== 'quit':
		print("Goodbye!")
		break
				
messages.append({"role": "user", "content":	user_input})
				
completion= client.chat.completions.create(
	model="gpt-4o",
	messages=messages
	)

assistant_message= completion.choices[0].message.content
				
messages.append({"role": "assistant", "content": assistant_message})

print(f"AI:	{assistant_message}\n") 