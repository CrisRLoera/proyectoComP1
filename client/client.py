import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = "127.0.0.1"  # dirección IP del server
server_port = 10000  # puerto del servidor
# Establecer conexión con el server

try:
    client.connect((server_ip, server_port))
    conectado = True
except client.error as e:
    conectado = False

def receive_messages():
    try:
        while True:
            # Recibidor de mensajes del server
            response = client.recv(1024)
            response = response.decode("utf-8")


            # Cierre de cliente
            if response.lower() == "closed":
                break

            print(f"{response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cerrar conexión del cliente con el servidor
        client.close()
        conectado = False
        print("Connection to server closed")

# Función para enviar mensajes al servidor
def send_message():
    while conectado:
        message = f'{input("")}'
        client.send(message.encode('utf-8'))

# Crear y arrancar hilos para enviar y recibir mensajes
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()