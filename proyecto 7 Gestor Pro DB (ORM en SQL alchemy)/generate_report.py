from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os

# Función universal para la creación de reportes en formato PDF
def crear_pdf(titulo, contenido_lineas):
    # 1. Gestión de directorios: Crea la carpeta 'reports' si no existe para mantener el orden
    folder = "reports"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # 2. Generación de nombre único: Usa la hora exacta (H-M-S) para evitar sobreescribir archivos
    nombre_archivo = f"reporte_{datetime.now().strftime('%H%M%S')}.pdf"
    # Une el nombre de la carpeta con el nombre del archivo de forma segura según el sistema operativo
    ruta_completa = os.path.join(folder, nombre_archivo)
    
    # 3. Inicialización del documento: Se define el lienzo (Canvas) y el tamaño de hoja A4
    c = canvas.Canvas(ruta_completa, pagesize=A4)
    ancho, alto = A4 # Dimensiones de la hoja para referencias de posición
    
    # 4. Dibujo del Título: Se establece fuente negrita y se posiciona en la parte superior
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, alto - 50, titulo)
    
    # 5. Dibujo del Contenido: Se cambia a fuente normal y se itera sobre las líneas recibidas
    c.setFont("Helvetica", 10)
    y = alto - 90 # Punto de partida vertical para el listado
    
    for linea in contenido_lineas:
        # Control de salto de página: Si el texto llega al borde inferior (50), crea hoja nueva
        if y < 50:
            c.showPage()
            y = alto - 50 # Reinicia la posición en la nueva hoja
            c.setFont("Helvetica", 10)
            
        # Dibuja la línea de texto actual en la coordenada (x, y)
        c.drawString(50, y, linea)
        y -= 15 # Baja 15 puntos para la siguiente línea (interlineado)
        
    # 6. Finalización: Guarda el archivo físicamente en el disco
    c.save()
    
    # IMPORTANTE: Retornamos la ruta completa para que el EmailService sepa dónde recoger el adjunto
    return ruta_completa 

# Bloque de ejecución directa para pruebas rápidas del módulo
if __name__ == "__main__":
    lineas_prueba = ["Línea de prueba 1", "Línea de prueba 2"]
    crear_pdf("TITULO DE PRUEBA", lineas_prueba)
    print("✅ PDF de prueba generado.")
