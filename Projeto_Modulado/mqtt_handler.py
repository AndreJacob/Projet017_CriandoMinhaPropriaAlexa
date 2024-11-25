import paho.mqtt.client as mqtt

BROKER = "10.0.0.97"
PORT = 1885
TOPIC = "ComandoVoz"

client = mqtt.Client()

def connect_mqtt():
    """Conecta ao broker MQTT."""
    client.connect(BROKER, PORT, 60)

def publish_message(message):
    """Publica uma mensagem no tópico do MQTT."""
    client.publish(TOPIC, message)
    print(f"Mensagem enviada: {message}")
