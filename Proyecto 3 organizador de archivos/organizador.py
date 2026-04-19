#Importamos las librerias necesarias:
import os
import shutil

#Creamos el diccionario para decirle a python como organizar los archivos:

EXTENSIONES = {
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif"],
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Audios": [".mp3", ".wav"],
    "Comprimidos": [".zip", ".rar", ".tar"],
}
#Definimos nuestra funcion:

def organizar_carpeta(ruta):
    os.chdir(ruta)#Le decimos a Python la carpeta que queremos organizar.

#Recorremos todos los archivos que estan dentro y hacemos una lista:
#Obtenemos el nombre y la extension:    

    for archivo in os.listdir():
        print(f"Encontre: {archivo}")
        nombre, ext =os.path.splitext(archivo)
        ext = ext.lower()

#Buscamos a que categoria pertenece la extension:

        for categoria, lista_ext in EXTENSIONES.items():
            if ext in lista_ext:

#Creamos la carpeta donde se guardaran los archivos(caso aun no este creada):

             if not os.path.exists(categoria):
                os.makedirs(categoria)

#Movemos el archivo a la carpeta creada en este caso se llama categoria:

             shutil.move(archivo, os.path.join(categoria, archivo))
             print(f"Movido: {archivo} --> {categoria}")

#Agregamos un "dispositivo de seguridad" para que no mueva ni carpetas ni el propio scrip a otro sitio:

    for archivo in os.listdir():
           if os.path.isdir(archivo):
            continue
           if archivo == "organizador.py": 
            continue

#Llamamos a nuestra funcion con el caracter "." para que python sepa que la carpeta a organizar es en la que estamos:
#En mi caso lo hice con la carpeta de descargas.
#Funciona con cualquier directorio que quieras organizar solo tienes que cambiar la ruta de acceso.
if __name__ =="__main__":
   
   ruta_descargas = r"C:\Users\ANGEL RAFAEL\Downloads"
   organizar_carpeta(ruta_descargas)
