import socket
import threading
import customtkinter as ctk

esta_corriendo = threading.Event()
esta_corriendo.set()  # Iniciar el evento en True.

# Configuración de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(1.0)  # Establecer un timeout de 1 segundo en el socket

server_ip = "127.0.0.1"
server_port = 8000

# Establecer conexión con el servidor
try:
    client.connect((server_ip, server_port))
    conectado = True
except socket.error as e:
    conectado = False
    print(f"Error de conexión: {e}")

# Crear la ventana principal
app = ctk.CTk()
app.title("Chat Client")
app.geometry("400x400")

# Función para recibir mensajes
def receive_messages():
    try:
        while esta_corriendo.is_set():
            try:
                response = client.recv(1024)
                if not response:
                    break  # Conexión cerrada por el servidor
                response = response.decode("utf-8")
                text_area.configure(state="normal")
                text_area.insert(ctk.END, f"{response}\n")
                text_area.configure(state="disabled")
            except socket.timeout:
                continue  # Si no recibe nada, vuelve a intentar
            except OSError:
                # Capturar el error si el socket ya está cerrado
                break
    except Exception as e:
        print(f"Error en la recepción de mensajes: {e}")
    finally:
        client.close()
        print("Conexión con el servidor cerrada")

# Función para enviar mensajes al servidor
def send_message():
    message = message_entry.get()
    if message:
        try:
            client.send(message.encode('utf-8'))
            message_entry.delete(0, ctk.END)
        except Exception as e:
            print(f"Error al enviar el mensaje: {e}")

# Función para cerrar la aplicación
def close_app():
    esta_corriendo.clear()  # Detener el bucle del hilo
    try:
        client.send("close".encode('utf-8'))
    except Exception as e:
        print(f"Error enviando mensaje de cierre: {e}")
    finally:
        client.close()  # Cerrar el socket
        print("Cliente cerrado manualmente")
        app.destroy()  # Cerrar la interfaz

# Configurar el evento para cerrar la ventana
app.protocol("WM_DELETE_WINDOW", close_app)

# Configuración de la UI
text_area = ctk.CTkTextbox(app)
text_area.pack(pady=10, padx=10, fill=ctk.BOTH, expand=True)
text_area.configure(state="disabled")

message_entry = ctk.CTkEntry(app)
message_entry.pack(pady=10, padx=10, fill=ctk.X)

send_button = ctk.CTkButton(app, text="Enviar", command=send_message)
send_button.pack(pady=10)

exit_button = ctk.CTkButton(app, text="Salir", command=close_app, fg_color="#fa4b54", hover_color="#db3039")
exit_button.pack(pady=10)

# Crear y arrancar hilos para enviar y recibir mensajes
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Iniciar el bucle principal de la aplicación
app.mainloop()

# Esperar a que el hilo de recepción termine al cerrar la app
receive_thread.join()
