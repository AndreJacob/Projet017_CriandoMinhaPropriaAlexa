from voice_recognition import listen_for_command
from led_control import acender_led3, desligar_led3
from audio_handler import play_audio
from mqtt_handler import connect_mqtt, publish_message

# Conectar ao broker MQTT
connect_mqtt()

def processar_comando(comando):
    """Processa o comando de voz e publica no MQTT."""
    if "chaves" in comando:
        acender_led3()
        play_audio("audios/chaves-isso-isso-isso.mp3")
        print("Diga um comando para a lâmpada.")
        return
    
    if comando == "ligar lâmpada":
        publish_message("1")
        play_audio("audios/chaves-ta-bom-mas-nao-se-irrite.mp3")
        desligar_led3()
    
    elif comando == "desligar lâmpada":
        publish_message("0")
        play_audio("audios/chaves-queBurro.mp3")
        play_audio("audios/chaves-senhor-barriga-tinha-que-ser-o-chaves-de-novo.mp3")
        desligar_led3()
    
    elif comando == "ligar led":
        publish_message("2")
        play_audio("audios/chaves-ta-bom-mas-nao-se-irrite.mp3")
        desligar_led3()
    
    elif comando == "desligar led":
        publish_message("3")
        play_audio("audios/chaves-queBurro.mp3")
        play_audio("audios/chaves-senhor-barriga-tinha-que-ser-o-chaves-de-novo.mp3")
        desligar_led3()

    elif comando == "sair do programa":
        print("Saindo do programa...")
        publish_message("Sair")
        exit()

# Loop principal
while True:
    comando = listen_for_command()
    if comando:
        processar_comando(comando)
    else:
        desligar_led3()
