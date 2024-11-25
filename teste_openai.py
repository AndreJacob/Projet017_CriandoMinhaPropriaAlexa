
import openai

# Substitua 'sua_chave_api' pela sua chave real
openai.api_key = "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"


response = openai.Completion.create(
  engine="gpt-3.5-turbo",  # Use a newer model here
  prompt="Hello, how are you?",
  max_tokens=100,
  n=1,
  stop=None,
  temperature=0.5,
)

print(response.choices[0].text.strip())

