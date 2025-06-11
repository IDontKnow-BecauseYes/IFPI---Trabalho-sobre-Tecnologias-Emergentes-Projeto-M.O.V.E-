import speech_recognition as sr

def escolher_modo():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    print("Diga o nome do robô seguido do modo: 'comando por voz', 'comando por gestos', 'arduino', 'controle ocular' ou 'ira encerrar' para sair.")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        frase = recognizer.recognize_google(audio, language='pt-BR').lower()
        print(f"Você disse: {frase}")
        if "robo" in frase:
            if "ira encerrar" in frase or "vai encerrar" in frase or "vai sair" in frase or "ira sair" in frase:
                return "encerrar"
            elif "comando por voz" in frase:
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
    while True:
        modo = escolher_modo()
        if modo == "encerrar":
            print("Encerrando o programa. Até mais!")
            break

        elif modo == "voice_commands":
            import voice_commands
            resultado = voice_commands.main()
            if resultado == "EXIT":
                print("Retornando ao menu principal após encerramento do modo comando por voz.")
                continue  # volta para escolher modo

        elif modo == "hand_gesture":
           import hand_gesture
           resultado = hand_gesture.main()
           if resultado == "EXIT":
               print("Retornando ao menu principal após encerramento do modo por gestos.")
               continue


        elif modo == "arduino_serial":
            import arduino_serial
            conectado = arduino_serial.check_connection()
            if conectado:
                print("Arduino está conectado ao PC.")
            else:
                print("Arduino NÃO está conectado ao PC.")
            # volta para pedir modo

        elif modo == "eye_control":
            import eye_control
            resultado = eye_control.main()
            if resultado == "EXIT":
                print("Retornando ao menu principal após encerramento do controle ocular.")
                continue


        else:
            print("Modo inválido, tente novamente.")
