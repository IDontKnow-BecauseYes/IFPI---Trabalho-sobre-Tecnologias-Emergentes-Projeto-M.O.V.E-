import speech_recognition as sr

# Mapeia frases de voz para comandos internos
VOICE_COMMANDS = {
    "ligar tudo": "ALL_ON",
    "desligar tudo": "ALL_OFF",
    "ligar azul": "BLUE_ON",
    "ligar vermelho": "RED_ON",
    "ligar verde": "GREEN_ON"
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
    print("Modo comando por voz ativado. Diga 'ESC' para sair.")
    while True:
        comando = reconhecer_comando()
        if comando:
            # Aqui você pode enviar o comando para o Arduino ou outro sistema
            # Exemplo: send_command(comando)
            pass
        # Para sair, pode usar uma palavra chave, exemplo "esc"
        # Se quiser implementar isso, pode alterar o reconhecimento:
        if comando == "ESC":
            print("Saindo do modo comando por voz.")
            break

if __name__ == "__main__":
    main()

