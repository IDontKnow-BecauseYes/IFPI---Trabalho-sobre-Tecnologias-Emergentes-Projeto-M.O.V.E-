import serial
import time

DEFAULT_PORT = 'COM6'
DEFAULT_BAUDRATE = 9600
DEFAULT_TIMEOUT = 1
STABILIZE_DELAY = 2  # segundos para estabilizar a conexão
READ_TIMEOUT = 1     # timeout para leitura de resposta

def check_connection(port: str = DEFAULT_PORT,
                     baudrate: int = DEFAULT_BAUDRATE,
                     timeout: float = DEFAULT_TIMEOUT) -> bool:
    """
    Tenta abrir a porta serial e fecha em seguida para verificar se está disponível.
    Retorna True se conseguir conectar, False caso contrário.
    """
    try:
        with serial.Serial(port=port, baudrate=baudrate, timeout=timeout) as ser:
            # aguarda a placa resetar/estabilizar (por exemplo, Arduino faz reset ao abrir USB)
            time.sleep(STABILIZE_DELAY)
        return True
    except serial.SerialException as e:
        print(f"[check_connection] Erro abrindo {port}: {e}")
        return False


def send_command(command: str,
                 port: str = DEFAULT_PORT,
                 baudrate: int = DEFAULT_BAUDRATE,
                 timeout: float = DEFAULT_TIMEOUT) -> str | None:
    """
    Envia um comando pela serial (adicionando '\n') e espera por uma linha de resposta.
    Retorna a resposta (string sem o '\n'), ou None em caso de erro.
    """
    try:
        with serial.Serial(port=port, baudrate=baudrate, timeout=READ_TIMEOUT) as ser:
            # aguarda estabilização e possível reset da placa
            time.sleep(STABILIZE_DELAY)

            # envia comando e força envio imediato
            ser.write(f"{command}\n".encode('utf-8'))
            ser.flush()

            # lê resposta até '\n' ou timeout
            raw = ser.readline()
            try:
                response = raw.decode('utf-8', errors='replace').strip()
            except Exception:
                response = raw.decode('latin-1', errors='replace').strip()

            print(f"[send_command] Enviado: '{command}' | Recebido: '{response}'")
            return response
    except serial.SerialException as e:
        print(f"[send_command] Erro ao enviar comando '{command}' em {port}: {e}")
        return None


if __name__ == "__main__":
    # Exemplo de uso rápido
    if check_connection():
        resp = send_command("ALL_ON")
        if resp is not None:
            print("Comando executado com sucesso.")
        else:
            print("Falha ao executar o comando.")
    else:
        print("Porta serial não disponível.")
