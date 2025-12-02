from openai	import OpenAI

client= OpenAI(api_key="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") 
completion= client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role":"system","content":	"You are a helpful assistant."},

		{"role":"user", "content": "Hello!" "What is AI?"} 
    ]
)

print(completion.choices[0].message.content)