import paho.mqtt.client as mqtt

# Configuração do MQTT
BROKER = "10.0.0.97"  # Endereço do broker MQTT
PORT = 1885  # Porta do broker MQTT
TOPIC = "ComandoVoz"  # Tópico do MQTT

# Função chamada quando a conexão é estabelecida com o broker
def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker com código de resultado: {rc}")
    # Após a conexão, publicamos uma mensagem no tópico
    client.publish(TOPIC, "Teste de Conexão MQTT")

# Função chamada quando a mensagem é publicada
def on_publish(client, userdata, mid):
    print("Mensagem publicada com sucesso.")

# Inicializa o cliente MQTT
client = mqtt.Client()  # Cria uma instância do cliente MQTT

# Define as funções de callback
client.on_connect = on_connect
client.on_publish = on_publish

# Conecta ao broker MQTT
client.connect(BROKER, PORT, 60)

# Loop de conexão e espera de mensagens
client.loop_forever()
