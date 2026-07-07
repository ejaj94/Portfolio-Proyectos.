#Importamos nuestras funciones ya creadas:

from Calculos import calcular_tmb, calcular_calorias_totales

#Definimos el ejemplo de uso de nuestro programa:

def iniciar_programa():
    print("--- Bienvenido a la calculadora nutricional ---")

#Recojemos los datos necesarios para calcular la tasa metabolica basal:
#Manejamos los errores qe puedan ocurrir:
    try:

     nombre = input("¿Como te llamas? ")
     peso = float(input("Introduce tu peso en KG: "))
     altura =  float(input("Introduce tu altura en CM: "))
     edad = int(input("¿Que edad tienes? "))
     genero = input("¿Eres hombre o mujer? ")

#Calculamos la tasa metabolica basal:

     resultado_tmb = calcular_tmb(peso, altura, edad, genero)
     print(f"\n{nombre}, tu Tasa Metabolica Basal es de: ¨{resultado_tmb:.2f} Kcal.")

#Calculamos la Tasa Metabolica Basal segun el nivel de actividad de la persona:

     print("\n-Escoje entre estos niveles de actividad fisica para calcular tu Tasa Metabolica basal segun ellos: \n-Niveles: sedentario, ligero, moderado, activo, muy activo.")
     nivel = input("¿Cual es tu nivel de actividad fisica? ")

     total_calorias = calcular_calorias_totales(resultado_tmb, nivel)

#Damos el resultado final de las Kcal que debe consumir la persona para mantener su peso:

     print("-" * 40)
     print(f"{nombre.upper()}. Este es tu tasa metabolica basal segun tu actividad fisica: ")
     print(f"\nDebes consumir: {total_calorias:.2f} kcal para mantener tu peso.")
     print("-" * 40)

#Damos el resultado final de las Kcal que debe consumir la persona para aumentar de peso:

     print(f"Debes consumir: {total_calorias + 300:.2f} kcal para estar en superavit calorico moderado.")
     print("-" * 40)

#Damos el resultado final de las Kcal que debe consumir la persona para bajar de peso:

     print(f"Debes consumir: {total_calorias - 300:.2f} kcal para estar en un deficit calorico moderado.")
     print("-" * 40)
    
    except ValueError:

     print("\n❌ ERROR: En peso, altura y edad debes introducir solo números enteros.")
     print("Por favor, reinicia el programa e inténtalo de nuevo.")


#Hacemos que el programa de ejecute al abrir el archivo:
if __name__ == "__main__":
    iniciar_programa()