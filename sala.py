import socket
from datetime import datetime
import threading

semaphore = threading.BoundedSemaphore(5)

def iniciar_servidor():
    # Configuração do servidor
    HOST = '127.0.0.1'  # Endereço local
    PORT = 4444        # Porta para comunicação

    # Criando o socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))     # Associa o socket ao endereço e porta
        s.listen()               # Habilita o servidor para aceitar conexões
        print(f"Sala aberta em {HOST}:{PORT}")
        print(f"Numero de lugares disponiveis: {semaphore._value}\n")

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
                            print(f"Um funcionario tentou entrar numa sala lotada.")
                        else: 
                            semaphore.acquire()
                            resposta = f"Bem vindo!\nVagas ainda disponiveis: {semaphore._value}"
                            print(f"Um funcionario entrou na sala, vagas disponiveis: {semaphore._value}")
                        conn.sendall(resposta.encode())
                    elif data.decode().strip().lower() == "o":
                        if semaphore._value == 5:
                            resposta = "Sala vazia."
                            print(f"Um funcionario tentou sair de uma sala vazia.")
                        else:
                            semaphore.release()
                            resposta = f"Volte sempre!\nVagas disponiveis: {semaphore._value}"
                            print(f"Um funcionario saiu da sala, vagas disponiveis: {semaphore._value}")
                        conn.sendall(resposta.encode())
                    elif data.decode().strip().lower() == "status":
                        resposta = f"Vagas disponiveis: {semaphore._value}"
                        print(f"Um funcionario checou o número de vagas disponiveis: {semaphore._value}")
                        conn.sendall(resposta.encode())
                    else:
                        conn.sendall(b"Mensagem invalida")
                        print(f"Um funcionario enviou um comando invalido.")
            

if __name__ == "__main__":
    iniciar_servidor()
