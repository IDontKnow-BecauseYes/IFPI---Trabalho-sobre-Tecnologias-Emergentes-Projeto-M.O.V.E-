import speech_recognition as sr
import pyttsx3

VOICE_COMMANDS = {
    "ligar tudo": "ALL_ON",
    "ligar todos": "ALL_ON",
    "acionar tudo": "ALL_ON",
    "acionar todos": "ALL_ON",
    "desligar tudo": "ALL_OFF",
    "ligar azul": "BLUE_ON",
    "acionar azul": "BLUE_ON",
    "ligar vermelho": "RED_ON",
    "acionar vermelho": "RED_ON",
    "ligar verde": "GREEN_ON",
    "acionar verde": "GREEN_ON",
    "encerrar": "EXIT",
    "finalizar": "EXIT",
    "terminar": "EXIT",
    "acabar": "EXIT",
    "cessar": "EXIT",
    "interromper": "EXIT"
}

# Inicializa a voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "brazil" in voice.name.lower() or "pt" in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break

def say(text):
    engine.say(text)
    engine.runAndWait()

def reconhecer_comando():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        say("Diga um comando")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        frase = recognizer.recognize_google(audio, language='pt-BR').lower()
        print(f"Você disse: {frase}")

        if "lira" in frase:
            say("Estou ouvindo")
            if "tutorial" in frase:
                say("Modo por voz ativado por Lira. Aqui está o tutorial.")
                say("Diga ligar tudo para acender todas as luzes.")
                say("Diga desligar tudo para apagar todas.")
                say("Diga ligar azul, vermelho ou verde para acender uma cor específica.")
                say("Diga encerrar ou finalizar para sair.")
                return None

        comando = VOICE_COMMANDS.get(frase)
        if comando:
            say(f"Comando reconhecido: {comando}")
            return comando
        else:
            say("Comando não reconhecido.")
    except sr.UnknownValueError:
        say("Não entendi o que você disse.")
    except sr.RequestError:
        say("Erro ao acessar o serviço de reconhecimento.")

    return None

def main():
    say("Modo comando por voz ativado. Diga um comando ou encerrar para sair.")
    while True:
        comando = reconhecer_comando()
        if comando:
            if comando == "EXIT":
                say("Comando de encerramento detectado. Saindo do modo comando por voz.")
                return "EXIT"
            # Aqui você pode chamar: send_command(comando)

if __name__ == "__main__":
    main()
