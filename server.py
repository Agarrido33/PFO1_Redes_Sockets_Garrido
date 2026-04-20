import socket
import sqlite3
import datetime

def inicializar_db():
    # Me conecto al archivo de SQLite; si no existe, la librería lo crea automáticamente
    try:
        conexion = sqlite3.connect('chat_db.sqlite')
        cursor = conexion.cursor()
        
        # Armo la tabla 'mensajes' con los campos solicitados en la consigna
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        conexion.commit()
        conexion.close()
        print("[Servidor] Base de datos inicializada correctamente.")
    except sqlite3.Error as e:
        print(f"[Error] Falló la conexión a la base de datos: {e}")
        exit(1) # Corto la ejecución si no hay persistencia

def guardar_mensaje(contenido, ip_cliente):
    # Función para insertar cada mensaje que recibo en la base
    try:
        conexion = sqlite3.connect('chat_db.sqlite')
        cursor = conexion.cursor()
        
        # Genero el timestamp actual para el registro
        fecha_envio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute(
            'INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)',
            (contenido, fecha_envio, ip_cliente)
        )
        conexion.commit()
        conexion.close()
        
        # Devuelvo la fecha para poder armar la confirmación al cliente
        return fecha_envio 
    except sqlite3.Error as e:
        print(f"[Error] No pude guardar el mensaje en la BD: {e}")
        return None

# Configuración del socket TCP/IP
def iniciar_socket(host='localhost', puerto=5000):
    try:
        # Defino el socket para IPv4 (AF_INET) y TCP (SOCK_STREAM)
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Le indico al SO que me deje reutilizar el puerto para evitar el error de "Address already in use" si reinicio rápido
        servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Asocio el socket al puerto local
        servidor_socket.bind((host, puerto))
        
        # Lo pongo a escuchar con una cola máxima de 5 conexiones entrantes
        servidor_socket.listen(5)
        print(f"[Servidor] Escuchando conexiones en {host}:{puerto}...")
        return servidor_socket
    except OSError as e:
        print(f"[Error] El puerto {puerto} está ocupado: {e}")
        exit(1)

def manejar_conexiones(servidor_socket):
    # Bucle principal para mantener el servidor corriendo
    while True:
        # Acepto la conexión entrante
        cliente_socket, direccion = servidor_socket.accept()
        ip_cliente = direccion[0]
        print(f"[Servidor] Se conectó un cliente desde {ip_cliente}")
        
        try:
            while True:
                # Recibo los datos en paquetes de 1024 bytes
                datos = cliente_socket.recv(1024)
                
                # Si no me llegan datos, asumo que el cliente cerró la conexión del otro lado
                if not datos:
                    break 
                
                # Decodifico el mensaje recibido
                mensaje = datos.decode('utf-8')
                print(f"[Mensaje de {ip_cliente}] -> {mensaje}")
                
                # Impacto el mensaje en la base SQLite
                timestamp = guardar_mensaje(mensaje, ip_cliente)
                
                # Armo la respuesta según lo que pide el TP
                if timestamp:
                    respuesta = f"Mensaje recibido: {timestamp}"
                else:
                    respuesta = "Error del servidor al intentar guardar el registro."
                    
                # Mando la respuesta codificada de vuelta
                cliente_socket.send(respuesta.encode('utf-8'))
                
        except ConnectionResetError:
            print(f"[Servidor] La conexión con {ip_cliente} se cortó de forma inesperada.")
        finally:
            # Me aseguro de liberar el recurso y cerrar el socket del cliente
            cliente_socket.close()
            print(f"[Servidor] Conexión finalizada con {ip_cliente}")

if __name__ == "__main__":
    # Ejecuto el flujo principal
    inicializar_db()
    server = iniciar_socket()
    manejar_conexiones(server)
