import serial
import time

def check_connection(port='COM6', baudrate=9600, timeout=1):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # esperar conexão estabilizar
        ser.close()
        return True
    except serial.SerialException:
        return False

def send_command(command: str, port='COM6', baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        ser.write((command + '\n').encode('utf-8'))
        response = ser.readline().decode('utf-8').strip()
        ser.close()
        print(f"Enviado: {command} | Recebido: {response}")
    except serial.SerialException as e:
        print(f"Erro ao enviar comando: {e}")

