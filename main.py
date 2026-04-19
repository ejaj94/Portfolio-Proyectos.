#Importamos nuestras librerias:

import requests
from bs4 import BeautifulSoup

#Importamos time para que el programa se ejecute cada cierto tiempo en el bucle infinito:
import time

#Importamos data time para saber las hora y fecha exacta en la que se analiza el precio:
from datetime import datetime

#Anexamos el url del producto que queremos vigilar lo ponemos en una variable:

url = "https://www.trendyventa.com/products/smart-lock-fingerprint-padlock"

#Usamos un user agent para que la web no asuma que somos un robot malicioso:

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; X64) AppleWebKit/537."}

#Definimos nuestra funcion para consultar el precio:

def consultar_precio():
    respuesta = requests.get(url, headers=headers) #Aqui pedirmos al web site su contenido.

    sopa = BeautifulSoup(respuesta.content, 'html.parser') #Aqui hacemos que python comprenda el contenido del web site.

    precio_etiqueta = sopa.find("span", class_="price") #Aqui es donde buscamos el precio por la etiqueta del web site.

#Ahora necesitamos que el resultado no se de tipo string sino de tipo numero entonces le damos forma de float.

    precio_texto = precio_etiqueta.text

#Reemplazamos el signo de dolar por un espacio vacio:

    precio_numero = precio_texto.replace("$", "")

#Usamos el metodo strip para evitar espacios y que despues de error por eso:
#Convertimos el precio a float para poder compararlo a otros:

    precio_final = float(precio_numero.strip())

#Printeamos a ver si encontro el precio:

    print(f"El precio encontrado es: {precio_etiqueta.text}")

#Creamos una variable con el presupuesto que tenemos para comprar el producto:

    presupuesto = 10.00

#Le damos una condicion al scrip para que cuando el precio sea igual o menor al presupuesto nos avise y poder comprar el producto:

    if precio_final <= presupuesto:
        print("¡El precio ha bajado ahora puedes comprarlo!")
    else:
        print("El precio aun es muy alto. Aun no puedes comprarlo.")

#Usamos el datetime para que aparezcan la fecha y hora exacta:

    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{ahora}] El precio encontrado es: {precio_etiqueta.text}")
    print("-"*40)

#Llamamos a la funcion:

if __name__ == "__main__":

#Creamos un bucle infinito para que se convierta en un vigilante real:
 
 while True:
     consultar_precio()
     time.sleep(100)