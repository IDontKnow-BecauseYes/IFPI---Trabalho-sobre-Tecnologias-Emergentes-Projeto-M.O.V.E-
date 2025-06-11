import speech_recognition as sr

def escolher_modo():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    print("Diga o nome do robô seguido do modo: 'comando por voz', 'comando por gestos', 'arduino' ou 'controle ocular'")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        frase = recognizer.recognize_google(audio, language='pt-BR').lower()
        print(f"Você disse: {frase}")
        if "robo" in frase:
            if "comando por voz" in frase:
                return "voice_commands"
            elif "comando por gestos" in frase:
                return "hand_gesture"
            elif "arduino" in frase:
                return "arduino_serial"
            elif "controle ocular" in frase or "controle de olhar" in frase:
                return "eye_control"
        print("Não reconheci um modo válido. Tente novamente.")
    except Exception as e:
        print("Erro no reconhecimento:", e)
    return None

if __name__ == "__main__":
    modo = None
    while not modo:
        modo = escolher_modo()

    if modo == "voice_commands":
        import voice_commands
        voice_commands.main()  # função do módulo de voz

    elif modo == "hand_gesture":
        import hand_gesture
        hand_gesture.main()    # função do módulo de gestos

    elif modo == "arduino_serial":
        import arduino_serial
        print("Modo Arduino ativo. Comandos podem ser enviados manualmente.")
        # Se desejar executar algo automático, pode chamar uma função aqui

    elif modo == "eye_control":
        import eye_control
        eye_control.main()     # função do módulo de controle ocular

