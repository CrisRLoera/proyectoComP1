import socket
import threading

clients = []
lock = threading.Lock()  # Lock para sincronización

# Función para retransmitir un mensaje a los clientes
def transmit(msg):
    with lock:  # Usar lock para evitar condiciones de carrera
        for client in clients:
            try:
                client.send(msg)
            except Exception as e:
                print(f"Error transmitiendo mensaje: {e}")

def handle_client(client_socket, addr):
    try:
        while True:
            request = client_socket.recv(1024).decode("utf-8")
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                with lock:
                    clients.remove(client_socket)
                transmit(f"{addr[1]} ha dejado el chat".encode('utf-8'))
                break
            print(f"Received: {request} from {addr[1]}")
            transmit(f"{addr[1]}: {request}".encode('utf-8'))
    except Exception as e:
        print(f"Error en handling client: {e}")
    finally:
        client_socket.close()
        print(f"Conexión del cliente ({addr[0]}:{addr[1]}) cerrada")

def run_server():
    server_ip = "127.0.0.1"
    port = 8000
    server_running = True  # Variable de control para detener el servidor
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, port))
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while server_running:
            try:
                client_socket, addr = server.accept()
                print(f"Accepted connection from {addr[0]}:{addr[1]}")
                with lock:
                    clients.append(client_socket)
                transmit(f"{addr[1]} se ha unido".encode('utf-8'))
                thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
                thread.start()
            except KeyboardInterrupt:
                print("Servidor detenido manualmente.")
                server_running = False
            except Exception as e:
                print(f"Error al aceptar conexión: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        with lock:
            for client in clients:
                client.close()  # Cerrar todas las conexiones
        server.close()
        print("Servidor cerrado.")

run_server()
