
import openai

# Substitua 'sua_chave_api' pela sua chave real
openai.api_key = "minha chave api"


response = openai.Completion.create(
  engine="gpt-3.5-turbo",  # Use a newer model here
  prompt="Hello, how are you?",
  max_tokens=100,
  n=1,
  stop=None,
  temperature=0.5,
)

print(response.choices[0].text.strip())

