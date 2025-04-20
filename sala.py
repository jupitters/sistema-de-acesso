import socket
from datetime import datetime
import threading

semaphore = threading.BoundedSemaphore(5)
global vagas

def acesso_funcionario(funcionario_id):
    print(f"Funcionatio {funcionario_id} entrando na sala...")
    with semaphore:
        print(f"Funcionario {funcionario_id} entrou na sala.")
        vagas += 1
        threading.Event().wait(1)
    print(f"Funcionario {funcionario_id} saiu da sala.")

def iniciar_servidor():
    # Configuração do servidor
    HOST = '127.0.0.1'  # Endereço local
    PORT = 4444        # Porta para comunicação

    # Criando o socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))     # Associa o socket ao endereço e porta
        s.listen()               # Habilita o servidor para aceitar conexões
        print(f"Sala aberta em {HOST}:{PORT}")

        # threads = [threading.Thread(target=acesso_funcionario, args=(i,)) for i in range ]
        while True:
            conn, addr = s.accept()
            
            with conn:
                print(f"Conectado por {addr}")
                while True:
                    data = conn.recv(1024)  
                    if not data:
                        break
                    if data.decode().strip().lower() == "i":
                        if semaphore._value == 0:
                            resposta = "Não há vagas disponiveis"
                        else: 
                            semaphore.acquire()
                            resposta = f"Vagas disponiveis: {semaphore._value}"
                        conn.sendall(resposta.encode()) # Envia a resposta ao cliente
                    elif data.decode().strip().lower() == "o":
                        if semaphore._value == 5:
                            resposta = "Sala vazia."
                        else:
                            semaphore.release()
                            resposta = f"Vagas disponiveis: {semaphore._value}"
                        conn.sendall(resposta.encode())
                    elif data.decode().strip().lower() == "status":
                        resposta = f"Vagas disponiveis: {semaphore._value}"
                        conn.sendall(resposta.encode())
                    else:
                        conn.sendall(b"Mensagem invalida")
            # Aguarda uma conexão
            

if __name__ == "__main__":
    iniciar_servidor()
