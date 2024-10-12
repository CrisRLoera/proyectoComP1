import socket
import threading

clients = []

# Función para retransmitir un mensaje a los clientes
def transmit(msg):
    for client in clients:
        client.send(msg)

def handle_client(client_socket, addr):
    try:
        while True:
            # Recibe y maneja los mensajes de los clientes
            request = client_socket.recv(1024).decode("utf-8")
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                clients.remove(client_socket)
                transmit(f"{addr[1]} a dejado el chat".encode('utf-8'))
                break
            print(f"Received: {request} from {addr[1]}")
            # Retransmición a los demas clientes
            transmit(f"{addr[1]}:{request}".encode('utf-8'))
    except Exception as e:
        print(f"Error en hanlding client: {e}")
    finally:
        client_socket.close()
        print(f"Conexión del cliente ({addr[0]}:{addr[1]}) cerrada")


def run_server():
    server_ip = "127.0.0.1"  # dirección IP
    port = 8000  # puerto
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conexion del socket a por puerto y dirección
        server.bind((server_ip, port))
        # Escuchar conecciones entrantes
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
            # Aceptar conecciones entrantes
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            clients.append(client_socket)
            transmit(f"{addr[1]} se a unido".encode('utf-8'))
            # Iniciar un nuevo hilo para el cliente
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


run_server()
