# SINCROFLASK
---
## Descripción

Esta aplicación permite la sincronización automática de archivos entre una carpeta en SharePoint y una carpeta local. Utiliza Flask para crear un servicio web simple que realiza la transferencia de archivos desde SharePoint hacia el almacenamiento local.

---

## Estructura de Archivos ⬇️

1. **app.py**: Archivo principal que ejecuta la aplicación Flask y sincroniza archivos.
2. **config.ini**: Archivo de configuración que contiene las credenciales y rutas necesarias para conectarse a SharePoint.
3. **sharepoint_manager.py**: Gestión de archivos entre SharePoint y el almacenamiento local. Clase proporcionada por CesarZHX.
4. **sharepoint.py**: Módulo que maneja la conexión con SharePoint y las operaciones sobre archivos.

---

## Requisitos

- Python 3.10 o superior.

## Librerias Usadas 
Estan contenidas en el archivo requirements.txt
y Puedes instalarlas utilizando el siguiente comando:

```bash
pip install requirements.txt
```
---
## Archivo Principal , app.py ⬇️
```bash
1. app.py
Este archivo es el punto de entrada de la aplicación. Inicia un servidor Flask que ejecuta el proceso de sincronización de archivos en segundo plano. Cada vez que accedes a la ruta principal /, devuelve el estado de sincronización.

Funciones clave:
run_sync_once(): Ejecuta la sincronización de archivos una vez.
start_sync_thread(): Inicia el hilo de sincronización en segundo plano.
```
---
## Archivo Config.ini ⬇️ 
```bash
2. config.ini
Contiene las credenciales y configuraciones necesarias para conectarse al sitio de SharePoint. Configura las siguientes secciones:

CREDENTIALS: Correo y contraseña del usuario de SharePoint.
PATH: Dominio, sitio y raíz de la carpeta compartida en SharePoint.
```
---
## Archivo sharepoint_manager.py ⬇️
```bash
3. sharepoint_manager.py
Este archivo gestiona la lógica de transferencia de archivos entre SharePoint y el almacenamiento local. Descarga archivos desde SharePoint y los guarda en una carpeta local.

Funciones clave:
transfer_files(): Ciclo de sincronización que descarga archivos de SharePoint y los guarda en local.
get_files_from_sharepoint(): Obtiene la lista de archivos desde SharePoint.
save_files(): Guarda los archivos descargados en el almacenamiento local.
```
---
## Archivo sharepoint.py
```bash
4. sharepoint.py ⬇️
** Este módulo maneja la conexión con SharePoint y las operaciones sobre los archivos (descarga, subida, obtención de propiedades, etc.).

Funciones clave: ⬇️
get_files(): Obtiene la lista de archivos desde una carpeta en SharePoint.
download_file(): Descarga un archivo específico desde SharePoint.
upload_file(): Sube un archivo a SharePoint