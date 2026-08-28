# Proyecto 1: Calculadora de Calorías y Tasa Metabólica Basal

Este proyecto es una calculadora de calorías desarrollada en Python con **Interfaz Gráfica de Usuario (GUI)** moderna y soporte para consola (CLI).

## Archivos del Proyecto

- `App.py`: Archivo principal de la aplicación. Ejecuta la Interfaz Gráfica por defecto.
- `gui.py`: Módulo de la interfaz gráfica moderna (desarrollado con CustomTkinter).
- `Calculos.py`: Módulo con las funciones matemáticas para el cálculo de TMB y calorías diarias según el nivel de actividad física.
- `requirements.txt`: Lista de dependencias del proyecto.

## Cómo Ejecutar

1. Asegúrate de tener Python 3.11+ instalado.
2. **Ejecutar la Interfaz Gráfica (GUI)** (Recomendado):
   ```bash
   python App.py
   ```
   o directamente:
   ```bash
   python gui.py
   ```

3. **Ejecutar en Modo Consola (CLI)**:
   ```bash
   python App.py --cli
   ```

## Características de la Interfaz Gráfica (GUI)

- **Diseño Moderno**: Interfaz adaptativa en modo claro/oscuro construida con CustomTkinter.
- **Formulario Completo**: Entradas para Nombre, Peso (kg), Altura (cm), Edad (años), Género y Nivel de Actividad Física.
- **Validación Instantánea**: Alertas para evitar errores en datos numéricos.
- **Resultados Claros**: Muestra la TMB base, calorías de mantenimiento, calorías para superávit (+300 kcal) y déficit (-300 kcal).

## Librerías Destacadas

- **CustomTkinter**: Interfaz gráfica de usuario moderna y estilizada.
- **NumPy / Pandas / Matplotlib**: Herramientas analíticas complementarias.
- **Black**: Formateador de código.

## Configuración del Formateador

- **Black** está configurado como el formateador predeterminado.
- Longitud de línea: 88 caracteres.
