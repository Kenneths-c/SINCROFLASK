import asyncio
import time
from asyncio import to_thread, gather
from configparser import ConfigParser
from pathlib import Path
from sharepoint import ClientRequestException, ConnectionError, SharePoint, File

class SharePointManager:
    def __init__(self, folder: str, storage: Path, sharepoint: SharePoint | None = None):
        self.folder = folder
        self.folder_path = storage
        self.folder_path.mkdir(parents=True, exist_ok=True)
        self.sharepoint = sharepoint or self.get_sharepoint_from_config()

    async def transfer_files(self):
        try:
            while True:  # Ejecutar en un bucle infinito con retraso
                # Obtén los archivos en la carpeta SharePoint
                files = await self.get_files_from_sharepoint(self.folder)
                
                # Guarda los archivos en la carpeta local
                await self.save_files(files)
                print('Listo , Funcionó')

                # Retraso de 1 segundo entre actualizaciones
                await asyncio.sleep(1)
                
        except Exception as e:
            print(f'Error en transfer_files: {e}')

    async def save_files(self, files: dict[str, bytes]):
        async def save_file(file_name: str, content: bytes):
            try:
                local_path = self.folder_path / file_name
                local_path.write_bytes(content)
                print(f'Archivo "{file_name}" guardado en {local_path}.')  # Mensaje de depuración
            except Exception as e:
                print(f'Error al guardar el archivo {file_name}: {e}')

        tasks = [
            save_file(file_name, content)
            for file_name, content in files.items()
        ]
        await gather(*tasks)

    async def get_files_from_sharepoint(self, folder_name: str):
        def get_file(file: File):
            try:
                # Descargar el archivo sin await
                content = self.sharepoint.download_file(file.name, folder_name)
                return {
                    file.name: content
                }
            except Exception as e:
                print(f'Error al descargar el archivo {file.name}: {e}')
                return {}

        # Obtiene la lista de archivos en la carpeta SharePoint
        try:
            files = await to_thread(self.sharepoint.get_files, folder_name)  # Asegúrate de esperar correctamente
            tasks = [to_thread(get_file, file) for file in files if file.name]
            file_contents = await gather(*tasks)
            return {k: v for d in file_contents for k, v in d.items()}
        except ClientRequestException as e:
            print(f'Error al obtener los archivos: {e}')
            return {}

    def get_sharepoint_from_config(self):
        cp = ConfigParser()
        cp.read('config.ini')
        return SharePoint(
            email=cp['CREDENTIALS']['sharepoint_email'],
            password=cp['CREDENTIALS']['sharepoint_password'],
            domain=cp['PATH']['sharepoint_domain'],
            site=cp['PATH']['sharepoint_site'],
            root=cp['PATH']['sharepoint_root']
        )

    def run(self):
        asyncio.run(self.transfer_files())  # Inicia la transferencia de archivos
