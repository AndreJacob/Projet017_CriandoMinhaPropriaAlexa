import speech_recognition as sr  # Importa a biblioteca para reconhecimento de fala
import paho.mqtt.client as mqtt  # Importa a biblioteca para comunicação MQTT
import time  # Importa a biblioteca de tempo para controlar delays

# Configuração do MQTT
BROKER = "10.0.0.97"  # Define o endereço IP do broker MQTT
PORT = 1885  # Define a porta de conexão com o broker MQTT
TOPIC = "ComandoVoz"  # Define o tópico para enviar os comandos

# Inicializa o cliente MQTT
client = mqtt.Client()  # Cria uma instância do cliente MQTT
client.connect(BROKER, PORT, 60)  # Conecta o cliente MQTT ao broker

# Inicializa o reconhecedor de voz
recognizer = sr.Recognizer()  # Cria uma instância do reconhecedor de voz

# Função para acender o LED 3
def acender_led3():
    client.publish(TOPIC, "4")  # Envia comando MQTT para acender o LED 3
    print("LED 3 aceso.")  # Imprime no terminal que o LED 3 foi aceso

# Função para desligar o LED 3
def desligar_led3():
    client.publish(TOPIC, "5")  # Envia comando MQTT para desligar o LED 3
    print("LED 3 desligado.")  # Imprime no terminal que o LED 3 foi desligado

def ouvir_comando():
    """Função para escutar um comando de voz."""
    with sr.Microphone() as source:  # Utiliza o microfone como fonte de áudio
        print("Ajustando para ruído de fundo...")  # Ajusta o reconhecimento para o ruído ambiente
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Ajusta o filtro para o ruído de fundo
        print("Pronto. Fale algo:")  # Solicita ao usuário para falar
        try:
            audio = recognizer.listen(source, timeout=10)  # Escuta o comando de voz, com timeout de 5 segundos
            comando = recognizer.recognize_google(audio, language="pt-BR")  # Converte o áudio em texto
            return comando.lower()  # Retorna o comando em minúsculo
        except sr.WaitTimeoutError:  # Captura erro se o tempo de espera para escutar for excedido
            print("Tempo limite de escuta excedido.")  # Imprime erro de timeout
            return ""  # Retorna string vazia
        except sr.UnknownValueError:  # Captura erro se o comando não for reconhecido
            print("Não entendi o que você disse.")  # Imprime erro de comando incompreendido
            return ""  # Retorna string vazia
        except sr.RequestError as e:  # Captura erro de requisição com o serviço de reconhecimento
            print(f"Erro no serviço: {e}")  # Imprime erro no serviço
            return ""  # Retorna string vazia

def processar_comando(comando):
    """Processa o comando de voz e publica no MQTT."""
    if "chaves" in comando:  # Se o comando contiver "chaves"
        acender_led3()  # Acende o LED 3
        print("Diga um comando para a lâmpada.")  # Solicita comando para a lâmpada
        return  # Retorna, sem processar mais comandos

    if comando == "ligar lâmpada":  # Se o comando for "ligar lâmpada"
        client.publish(TOPIC, "1")  # Envia comando MQTT para ligar a lâmpada
        print("Comando enviado: Ligar lâmpada")  # Imprime que o comando foi enviado
        desligar_led3()  # Desliga o LED 3 após o comando ser enviado
    elif comando == "desligar lâmpada":  # Se o comando for "desligar lâmpada"
        client.publish(TOPIC, "0")  # Envia comando MQTT para desligar a lâmpada
        print("Comando enviado: Desligar lâmpada")  # Imprime que o comando foi enviado
        desligar_led3()  # Desliga o LED 3 após o comando ser enviado
    elif comando == "sair do programa":  # Se o comando for "sair do programa"
        print("Saindo do programa...")  # Imprime que o programa está sendo encerrado
        client.disconnect()  # Desconecta do broker MQTT
        exit()  # Sai do programa

# Loop principal
while True:  # Loop infinito para escutar os comandos continuamente
    comando = ouvir_comando()  # Chama a função para ouvir o comando
    if comando:  # Se um comando for reconhecido
        processar_comando(comando)  # Processa o comando
    else:
        desligar_led3()  # Desliga o LED 3 caso não haja comando ou erro de reconhecimento
