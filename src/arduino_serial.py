import serial
import time

# Altere para a COM do HC-05 (ver no Gerenciador de Dispositivos)
ser = serial.Serial('COM6', 9600, timeout=1)
time.sleep(2)  # Aguarda conexão estabilizar

def send_command(command: str):
    """
    Envia comando para Arduino via HC-05.
    Comandos esperados: ALL_ON, ALL_OFF, BLUE_ON, RED_ON, GREEN_ON
    """
    ser.write((command + '\n').encode('utf-8'))
    response = ser.readline().decode('utf-8').strip()
    print(f"Enviado: {command} | Recebido: {response}")
