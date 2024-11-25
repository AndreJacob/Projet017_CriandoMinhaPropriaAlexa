import speech_recognition as sr

recognizer = sr.Recognizer()

def listen_for_command():
    """Escuta o comando de voz e retorna como texto."""
    with sr.Microphone() as source:
        print("Ajustando para ruído de fundo...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Pronto. Fale algo:")
        try:
            audio = recognizer.listen(source, timeout=10)
            command = recognizer.recognize_google(audio, language="pt-BR")
            return command.lower()
        except sr.WaitTimeoutError:
            print("Tempo limite de escuta excedido.")
            return ""
        except sr.UnknownValueError:
            print("Não entendi o que você disse.")
            return ""
        except sr.RequestError as e:
            print(f"Erro no serviço: {e}")
            return ""
