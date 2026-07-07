#Definimos la funcion que calcula la tasa metabolica basal:

def calcular_tmb(peso, altura, edad, genero):
    if genero.lower() == "hombre":
        return (10 * peso) + (6.25 * altura) - (5 * edad) + 5
    else:
        return (10 * peso) + (6.25 * altura) - (5 * edad) - 161
    
#Creamos la funcion para el gasto calorico segun la actividad:

def calcular_calorias_totales(tmb_resultado, nivel_elegido):

#Creamos un diccionario con los diferentes tipos de estados principales de actividad del ser humano:
    
    actividad = {
    "sedentario": 1.2,
    "ligero": 1.375,
    "moderado": 1.55,
    "activo": 1.725,
    "muy activo": 1.9,
}

#calculamos la tasa metabolica basal segin el nivel de actividad elegido y lo guardamos en una variable:

    factor = actividad.get(nivel_elegido.lower(), 1.2)
    return tmb_resultado * factor
