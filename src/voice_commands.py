import speech_recognition as sr

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

def reconhecer_comando():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Diga um comando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        frase = recognizer.recognize_google(audio, language='pt-BR').lower()
        print(f"Você disse: {frase}")
        comando = VOICE_COMMANDS.get(frase)
        if comando:
            print(f"Comando reconhecido: {comando}")
            return comando
        else:
            print("Comando não reconhecido.")
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
    except sr.RequestError:
        print("Erro ao acessar o serviço de reconhecimento.")
    return None

def main():
    print("Modo comando por voz ativado. Diga um comando, ou 'encerrar' para sair.")
    while True:
        comando = reconhecer_comando()
        if comando:
            if comando == "EXIT":
                print("Comando de encerramento detectado. Saindo do modo comando por voz...")
                return "EXIT"
            # Aqui você pode enviar o comando para o Arduino ou outro sistema
            # Exemplo: send_command(comando)
        # Se comando for None ou não EXIT, continua escutando

if __name__ == "__main__":
    main()
