import socket
import threading
import customtkinter as ctk

esta_corriendo = True

# Configuración de CustomTkinter
ctk.set_appearance_mode("Dark")  # Modo de apariencia: "Dark", "Light", "System"
ctk.set_default_color_theme("blue")  # Tema de color: "blue", "green", "dark-blue", etc.

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = "127.0.0.1"  # dirección IP del server
server_port = 8000  # puerto del servidor

# Establecer conexión con el server
try:
    client.connect((server_ip, server_port))
    conectado = True
except socket.error as e:
    conectado = False
    print(f"Error de conexión: {e}")

# Crear la ventana principal
app = ctk.CTk()  
app.title("Chat Client")  # Título de la ventana
app.geometry("400x400")  # Tamaño de la ventana

# Función para recibir mensajes
def receive_messages():
    global esta_corriendo 
    try:
        while esta_corriendo:
            # Recibidor de mensajes del server
            response = client.recv(1024)
            response = response.decode("utf-8")

            # Agregar el mensaje recibido al área de texto
            text_area.insert(ctk.END, f"{response}\n")
    except Exception as e:
        print(f"Error en la recepción de mensajes: {e}")
    finally:
        client.close()
        app.destroy()  # Cerrar la aplicación
        print("Conexión con el servidor cerrada")

# Función para enviar mensajes al servidor
def send_message():
    message = message_entry.get()  # Obtener el mensaje del campo de entrada
    if message:
        client.send(message.encode('utf-8'))
        message_entry.delete(0, ctk.END)  # Limpiar el campo de entrada

def close_app():
    global esta_corriendo 
    try:
        client.send("close".encode('utf-8'))
    except Exception as e:
        print(f"Error enviando mensaje de cierre: {e}")
    finally:
        print("Cliente cerrado manualmente")
        esta_corriendo = False

# Configuración de la UI
text_area = ctk.CTkTextbox(app)  # Área de texto para mostrar mensajes
text_area.pack(pady=10, padx=10, fill=ctk.BOTH, expand=True)

message_entry = ctk.CTkEntry(app)  # Campo de entrada para enviar mensajes
message_entry.pack(pady=10, padx=10, fill=ctk.X)

send_button = ctk.CTkButton(app, text="Enviar", command=send_message)  # Botón para enviar mensajes
send_button.pack(pady=10)

exit_button = ctk.CTkButton(app, text="Salir", command=close_app)
exit_button.pack(pady=10)

# Crear y arrancar hilos para enviar y recibir mensajes
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Iniciar el bucle principal de la aplicación
app.mainloop()
