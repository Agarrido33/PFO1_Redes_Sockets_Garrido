import socket

def iniciar_cliente(host='localhost', puerto=5000):
    # Configuración del socket TCP/IP para el cliente
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Intento conectarme al servidor local
        cliente_socket.connect((host, puerto))
        print(f"Conectado exitosamente a {host}:{puerto}")
        print("Ya podés escribir. Ingresá 'éxito' para finalizar la sesión.\n")
        
        while True:
            # Capturo lo que ingreso por consola
            mensaje = input("Mensaje: ")
            
            # Verifico la condición de salida que pide la consigna
            if mensaje.strip().lower() == 'éxito':
                print("Cerrando la conexión...")
                break
                
            # Evito mandar tráfico inútil si la cadena está vacía
            if not mensaje:
                continue
                
            # Mando el mensaje al servidor codificado en UTF-8
            cliente_socket.send(mensaje.encode('utf-8'))
            
            # Quedo a la espera de la confirmación
            respuesta = cliente_socket.recv(1024).decode('utf-8')
            print(f"[Servidor] {respuesta}\n")
            
    except ConnectionRefusedError:
        print("[Error] No me pude conectar. Verificá que el servidor esté levantado en el puerto 5000.")
    finally:
        # Cierro mi socket antes de salir para no dejar conexiones colgadas
        cliente_socket.close()

if __name__ == "__main__":
    iniciar_cliente()
