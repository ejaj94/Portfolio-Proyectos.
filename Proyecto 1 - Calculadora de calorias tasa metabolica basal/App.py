import sys
from Calculos import calcular_tmb, calcular_calorias_totales


def iniciar_programa_cli():
    print("--- Bienvenido a la calculadora nutricional (Modo Consola) ---")

    try:
        nombre = input("¿Como te llamas? ")
        peso = float(input("Introduce tu peso en KG: "))
        altura = float(input("Introduce tu altura en CM: "))
        edad = int(input("¿Que edad tienes? "))
        genero = input("¿Eres hombre o mujer? ")

        resultado_tmb = calcular_tmb(peso, altura, edad, genero)
        print(
            f"\n{nombre}, tu Tasa Metabolica Basal es de: {resultado_tmb:.2f} Kcal."
        )

        print(
            "\n-Escoje entre estos niveles de actividad fisica para calcular tu Tasa Metabolica basal segun ellos: \n-Niveles: sedentario, ligero, moderado, activo, muy activo."
        )
        nivel = input("¿Cual es tu nivel de actividad fisica? ")

        total_calorias = calcular_calorias_totales(resultado_tmb, nivel)

        print("-" * 40)
        print(
            f"{nombre.upper()}. Este es tu tasa metabolica basal segun tu actividad fisica: "
        )
        print(
            f"\nDebes consumir: {total_calorias:.2f} kcal para mantener tu peso."
        )
        print("-" * 40)
        print(
            f"Debes consumir: {total_calorias + 300:.2f} kcal para estar en superavit calorico moderado."
        )
        print("-" * 40)
        print(
            f"Debes consumir: {total_calorias - 300:.2f} kcal para estar en un deficit calorico moderado."
        )
        print("-" * 40)

    except ValueError:
        print(
            "\n❌ ERROR: En peso, altura y edad debes introducir solo números válidos."
        )
        print("Por favor, reinicia el programa e inténtalo de nuevo.")


def iniciar_programa():
    if "--cli" in sys.argv:
        iniciar_programa_cli()
    elif "--web" in sys.argv:
        from web_app import main as iniciar_web

        iniciar_web()
    else:
        try:
            from gui import main as iniciar_gui

            iniciar_gui()
        except Exception as e:
            print(
                f"No se pudo iniciar la interfaz gráfica de escritorio: {e}."
            )
            print("Iniciando versión web local...")
            try:
                from web_app import main as iniciar_web

                iniciar_web()
            except Exception as e_web:
                print(
                    f"No se pudo iniciar la versión web: {e_web}. Iniciando versión consola..."
                )
                iniciar_programa_cli()


if __name__ == "__main__":
    iniciar_programa()