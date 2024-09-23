from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from requests.exceptions import HTTPError, ConnectionError
from office365.sharepoint.files.file import File
from xml.etree.ElementTree import ParseError

class SharePoint:
    @property
    def client_context(self):
        return ClientContext(self.site_url).with_credentials(self.user_credential)

    @property
    def web(self):  
        return self.client_context.web

    def __init__(self, email: str, password: str, domain: str, site: str, root: str):
        """root use to be Shared Documents"""
        self.email, self.domain, self.site, self.root = email, domain, site, root
        self.site_url = f'https://{self.domain}.sharepoint.com/sites/{self.site}'
        self.relative_url = (f'/sites/{self.site}/{self.root}/{{}}').format
        self.user_credential = UserCredential(email, password)

    def get_folder(self, folder_name: str):
        try:
            folder_url = f'{self.root}/{folder_name}'
            return self.web.get_folder_by_server_relative_url(folder_url).expand(["Files", "Folders"]).get().execute_query()
        except (ClientRequestException, HTTPError) as e:
            if e.response is None:
                print(f'Error de solicitud del cliente: {e}')
                raise e
            if e.response.status_code in (429, 500, 503):
                print(f'Error temporal, reintentando: {e}')
                return self.get_folder(folder_name)
            print(f'Error HTTP: {e}')
            raise e
        except (AttributeError, ConnectionError, ParseError, ValueError) as e:
            print(f'Error en el proceso: {e}')
            return self.get_folder(folder_name)
        except Exception as e:
            print(f'Error inesperado con el archivo "{folder_name}": {e}')
            raise e

    def get_files(self, folder_name: str):
        return self.get_folder(folder_name).files

    def get_folders(self, folder_name: str):
        return self.get_folder(folder_name).folders

    def download_file(self, file_name: str, folder_name: str) -> bytes:
        try:
            file_url = self.relative_url(f'{folder_name}/{file_name}')
            file = File.open_binary(self.client_context, file_url)
            return file.content
        except HTTPError as e:
            if e.response.status_code in (429, 500, 503):
                print(f'Error temporal,reintentando: {e}')
                return self.download_file(file_name, folder_name)
            print(f'Error HTTP: {e}')
            raise e
        except (AttributeError, ValueError) as e:
            print(f'Error en el proceso: {e}')
            return self.download_file(file_name, folder_name)
        except Exception as e:
            print(f'Error inesperado con el archivo "{file_name}": {e}')
            raise e

    def download_latest_file(self, folder_name: str):
        files = {file.name: file.time_last_modified for file in self.get_files(folder_name) if file.name and file.time_last_modified}
        if not files:
            raise ValueError("No se encontraron archivos en la carpeta especificada.")
        sorted_files = {key: value for key, value in sorted(files.items(), key=lambda item: item[1], reverse=True)}
        latest_file_name = next(iter(sorted_files))
        content = self.download_file(latest_file_name, folder_name)
        return latest_file_name, content

    def upload_file(self, file_name: str, folder_name: str, content: str):
        target_folder = self.web.get_folder_by_server_relative_path(self.relative_url(folder_name))
        return target_folder.upload_file(file_name, content).execute_query()

    def upload_file_in_chunks(self, file_path: str, folder_name: str, chunk_size: int, chunk_uploaded=None, **kwargs):
        """Untested"""
        target_folder = self.web.get_folder_by_server_relative_path(self.relative_url(folder_name))
        return target_folder.files.create_upload_session(
            source_path=file_path,
            chunk_size=chunk_size,
            chunk_uploaded=chunk_uploaded,
            **kwargs
        ).execute_query()

    def get_list(self, list_name: str):
        """Untested"""
        target_list = self.web.lists.get_by_title(list_name)
        return target_list.items.get().execute_query()

    def get_file_properties_from_folder(self, folder_name: str):
        return [
            {
                'file_id': file.unique_id,
                'file_name': file.name,
                'major_version': file.major_version,
                'minor_version': file.minor_version,
                'file_size': file.length,
                'time_created': file.time_created,
                'time_last_modified': file.time_last_modified
            } for file in self.get_files(folder_name)
        ]
