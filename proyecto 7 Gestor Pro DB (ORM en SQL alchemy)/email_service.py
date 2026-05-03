import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Carga las variables de entorno para no exponer correos ni claves en el código
load_dotenv()

class EmailService:
    def __init__(self):
        # 1. Configuración de credenciales desde el archivo .env
        self.email_user = os.getenv("EMAIL_USER")
        self.email_pass = os.getenv("EMAIL_PASS")
        
        # 2. Configuración del servidor de salida de Gmail (puerto 465 para SSL)
        self.smtp_server = "smtp.gmail.com" 
        self.smtp_port = 465

        # Validación preventiva para evitar errores de conexión al arrancar
        if not self.email_user or not self.email_pass:
            print("⚠️ Advertencia: Credenciales de email no configuradas en .env")

    def enviar_reporte(self, destinatario, archivo_adjunto):
        """
        Prepara y envía un correo electrónico con el archivo PDF adjunto.
        """
        # Validación: Asegura que el reporte PDF realmente exista en la carpeta /reports
        if not os.path.exists(archivo_adjunto):
            print(f"❌ Error: El archivo {archivo_adjunto} no existe.")
            return False

        # 3. Construcción del mensaje usando la librería moderna EmailMessage
        msg = EmailMessage()
        msg['Subject'] = 'Reporte de Usuarios'
        msg['From'] = self.email_user
        msg['To'] = destinatario
        msg.set_content('Hola, adjunto encontrarás el reporte de usuarios solicitado.')

        # 4. Lectura del archivo PDF en modo binario ('rb') para adjuntarlo correctamente
        with open(archivo_adjunto, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(
                file_data,
                maintype='application',
                subtype='pdf',
                filename=os.path.basename(archivo_adjunto) # Envía solo el nombre del archivo, no la ruta
            )

        try:
            # 5. Conexión segura SMTP_SSL para el inicio de sesión y envío
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as smtp:
                smtp.login(self.email_user, self.email_pass)
                smtp.send_message(msg)
            return True
        except Exception as e:
            # Captura errores comunes como contraseñas incorrectas o falta de internet
            print(f"❌ Error al enviar email: {e}")
            return False
