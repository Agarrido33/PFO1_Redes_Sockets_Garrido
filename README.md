# PFO N° 1 - Chat Cliente-Servidor con Sockets TCP

**Alumno:** Andrés Garrido  
**Materia:** Programación sobre Redes (3er Año)  
**Carrera:** Tecnicatura Superior en Desarrollo de Software  

---

## Descripción del Proyecto

Este repositorio contiene mi entrega para la Propuesta Formativa Obligatoria N° 1. En este trabajo implementé un sistema de chat básico operando bajo una arquitectura Cliente-Servidor. 

El objetivo del proyecto fue trabajar directamente con la capa de transporte, utilizando Sockets para establecer una conexión TCP, gestionar el envío y recepción de mensajes, y guardar el historial de la conversación en una base de datos local.

## Tecnologías y Herramientas que utilicé

Para armar este proyecto usé:
* **Lenguaje:** Python 3
* **Redes:** Protocolo TCP/IP (mediante la librería estándar socket)
* **Base de Datos:** SQLite (mediante la librería estándar sqlite3) para la persistencia de los mensajes.