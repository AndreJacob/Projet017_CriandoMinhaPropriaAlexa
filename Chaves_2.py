import speech_recognition as sr
import openai
import paho.mqtt.client as mqtt
import pyttsx3  # Biblioteca para conversão de texto para fala

# Configuração do MQTT
BROKER = "10.0.0.97"  # Endereço do broker MQTT
PORT = 1885  # Porta do broker MQTT
TOPIC = "ComandoVoz"  # Tópico do MQTT

# Inicializa o cliente MQTT
client = mqtt.Client()  # Cria uma instância do cliente MQTT
client.connect(BROKER, PORT, 60)  # Conecta o cliente MQTT ao broker


# Configuração da API do OpenAI (ChatGPT)
openai.api_key = 'minha chave api'  # Sua chave de API OpenAI

# Função para interação com o ChatGPT
def pesquisar_com_gpt(pergunta):
    resposta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=pergunta,
        max_tokens=150
    )
    return resposta.choices[0].text.strip()

# Função para acender o LED 3 (exemplo de ação com MQTT)
def acender_led3():
    client.publish(TOPIC, "4")
    print("LED 3 aceso.")

# Função para desligar o LED 3
def desligar_led3():
    client.publish(TOPIC, "5")
    print("LED 3 desligado.")

# Função para converter texto em áudio
def falar_resposta(resposta):
    engine = pyttsx3.init()  # Inicializa o engine de TTS
    engine.setProperty('rate', 150)  # Define a velocidade da fala
    engine.setProperty('volume', 1)  # Define o volume (0.0 a 1.0)
    engine.say(resposta)  # Converte a resposta em fala
    engine.runAndWait()  # Reproduz a fala

# Inicializa o reconhecedor de voz
recognizer = sr.Recognizer()

# Função para escutar um comando de voz
def ouvir_comando():
    with sr.Microphone() as source:
        print("Ajustando para ruído de fundo...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Pronto. Fale algo:")
        try:
            audio = recognizer.listen(source, timeout=10)
            comando = recognizer.recognize_google(audio, language="pt-BR")
            return comando.lower()
        except sr.WaitTimeoutError:
            print("Tempo limite de escuta excedido.")
            return ""
        except sr.UnknownValueError:
            print("Não entendi o que você disse.")
            return ""
        except sr.RequestError as e:
            print(f"Erro no serviço: {e}")
            return ""

# Função para processar o comando de voz
def processar_comando(comando):
    if "chaves" in comando:  # Verifica se o comando contém "chaves"
        pergunta = comando.replace("chaves", "").strip()  # Remove a palavra "chaves"
        resposta = pesquisar_com_gpt(pergunta)  # Envia a pergunta para o ChatGPT
        print("Resposta do ChatGPT:", resposta)  # Exibe a resposta do ChatGPT
        falar_resposta(resposta)  # Converte e fala a resposta
        client.publish(TOPIC, resposta)  # Envia a resposta via MQTT (opcional)
    elif "ligar lâmpada" in comando:
        client.publish(TOPIC, "1")
        print("Comando enviado: Ligar lâmpada")
    elif "desligar lâmpada" in comando:
        client.publish(TOPIC, "0")
        print("Comando enviado: Desligar lâmpada")
    elif "sair do programa" in comando:
        print("Saindo do programa...")
        client.disconnect()
        exit()

# Loop principal
while True:
    comando = ouvir_comando()  # Escuta o comando de voz
    if comando:
        processar_comando(comando)  # Processa o comando
    else:
        desligar_led3()  # Desliga o LED 3 se não houver comando