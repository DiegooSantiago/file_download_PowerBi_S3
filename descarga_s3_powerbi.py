import os
import boto3
import tkinter as tk
from tkinter import messagebox
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Versión dcruz_240727

def download_files_from_s3(bucket_name, local_directory, aws_access_key_id, aws_secret_access_key):
    """Descarga todos los archivos del bucket de S3 y los guarda en el directorio local."""
    
    # Crear el cliente de S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    
    # Crear el directorio local si no existe
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)

    # Lista para almacenar los nombres de los archivos descargados
    downloaded_files = []

    try:
        # Listar todos los objetos en el bucket
        response = s3.list_objects_v2(Bucket=bucket_name)

        # Verificar si hay contenido en el bucket
        if 'Contents' in response:
            for obj in response['Contents']:
                # Obtener el nombre del archivo
                file_name = obj['Key']

                # Definir la ruta completa del archivo local
                local_file_path = os.path.join(local_directory, file_name)

                # Crear subdirectorios si es necesario
                local_subdirectory = os.path.dirname(local_file_path)
                if not os.path.exists(local_subdirectory):
                    os.makedirs(local_subdirectory)

                # Descargar el archivo del bucket de S3
                s3.download_file(bucket_name, file_name, local_file_path)
                downloaded_files.append(file_name)

            # Mostrar listado de archivos descargados
            show_downloaded_files(downloaded_files, local_directory)
        else:
            show_message("El bucket está vacío o no existe.", "Advertencia")

    except NoCredentialsError:
        show_message("Error: No se encontraron las credenciales de AWS.", "Error de Credenciales")
    except PartialCredentialsError:
        show_message("Error: Las credenciales de AWS están incompletas.", "Error de Credenciales")
    except Exception as e:
        show_message(f"Error al descargar los archivos: {e}", "Error")

def show_message(message, title):
    """Muestra un mensaje en una ventana emergente."""
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    messagebox.showinfo(title, message)

def show_downloaded_files(files, directory):
    """Muestra una ventana con el listado de archivos descargados y abre el explorador de archivos."""
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    if files:
        file_list = "\n".join(files)
        messagebox.showinfo("Archivos Descargados", f"Los siguientes archivos fueron descargados:\n\n{file_list}")
        
        # Abrir el explorador de archivos en la ubicación de descarga
        open_explorer(directory)
    else:
        messagebox.showinfo("Archivos Descargados", "No se descargaron archivos.")

def open_explorer(directory):
    """Abre el explorador de archivos en el directorio especificado."""
    try:
        os.startfile(directory)
    except Exception as e:
        show_message(f"No se pudo abrir el explorador de archivos: {e}", "Error")

if __name__ == '__main__':
    # Configurar los parámetros
    bucket_name = 'powerbigim'
    local_directory = r'C:\PowerBi'

    # Credenciales de AWS
    aws_access_key_id = 'AKIAYHVKENECJRZZDMOD'
    aws_secret_access_key = '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'

    # Ejecutar la función para descargar archivos
    download_files_from_s3(bucket_name, local_directory, aws_access_key_id, aws_secret_access_key)
