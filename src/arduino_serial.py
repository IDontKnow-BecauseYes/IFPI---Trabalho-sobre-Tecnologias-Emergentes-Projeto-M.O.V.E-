import serial
import time

# Configure a porta serial de acordo com seu sistema
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # aguarda Arduino resetar


def send_command(command: str):
    """
    Envia string de comando para Arduino e imprime resposta.
    Comandos esperados: ALL_ON, ALL_OFF, BLUE_ON, RED_ON, GREEN_ON
    """
    ser.write((command + '
').encode('utf-8'))
    response = ser.readline().decode('utf-8').strip()
    print(f"Enviado: {command} | Recebido: {response}")
