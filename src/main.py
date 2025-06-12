import speech_recognition as sr
import pyttsx3

# Inicializa engine de voz
engine = pyttsx3.init()
# Seleciona voz feminina (pt-BR)
for v in engine.getProperty('voices'):
    if 'pt' in v.languages or 'Maria' in v.name:
        engine.setProperty('voice', v.id)
        break

# Função para falar
def say(text):
    engine.say(text)
    engine.runAndWait()

# Introdução falada
say("Este programa ativa modos por comando de voz.")

def escolher_modo():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    say("Sou todo ouvidos")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        frase = recognizer.recognize_google(audio, language='pt-BR').lower()
        say(f"Você disse: {frase}")
        if "lira" in frase:
            if any(p in frase for p in ["encerrar", "sair"]):
                return "encerrar"
            elif "comando por voz" in frase:
                return "voice_commands"
            elif "comando por gestos" in frase:
                return "hand_gesture"
            elif "arduino" in frase:
                return "arduino_serial"
            elif "controle ocular" in frase or "controle de olhar" in frase:
                return "eye_control"
        say("Não reconheci um modo válido. Tente novamente.")
    except Exception as e:
        say("Erro no reconhecimento.")
    return None

if __name__ == "__main__":
    while True:
        modo = escolher_modo()
        if modo == "encerrar":
            say("Encerrando o programa. Até mais!")
            break

        elif modo == "voice_commands":
            import voice_commands
            resultado = voice_commands.main()
            if resultado == "EXIT":
                say("Retornando ao menu principal após encerramento do modo comando por voz.")
                continue

        elif modo == "hand_gesture":
            import hand_gesture
            resultado = hand_gesture.main()
            if resultado == "EXIT":
                say("Retornando ao menu principal após encerramento do modo por gestos.")
                continue

        elif modo == "arduino_serial":
            import arduino_serial
            conectado = arduino_serial.check_connection()
            if conectado:
                say("Arduino está conectado ao PC.")
            else:
                say("Arduino não está conectado ao PC.")

        elif modo == "eye_control":
            import eye_control
            resultado = eye_control.main()
            if resultado == "EXIT":
                say("Retornando ao menu principal após encerramento do controle ocular.")
                continue

        else:
            say("Modo inválido, tente novamente.")
