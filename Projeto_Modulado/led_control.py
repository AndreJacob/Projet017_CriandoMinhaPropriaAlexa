from mqtt_handler import publish_message

def acender_led3():
    """Acende o LED 3 através do MQTT."""
    publish_message("4")  # Envia comando para acender o LED
    print("LED 3 aceso.")

def desligar_led3():
    """Desliga o LED 3 através do MQTT."""
    publish_message("5")  # Envia comando para desligar o LED
    print("LED 3 desligado.")
