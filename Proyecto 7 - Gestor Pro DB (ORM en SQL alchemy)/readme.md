# Sistema de Gestión de Usuarios (SOLID)

Este proyecto es una aplicación de consola para gestionar usuarios en una base de datos MySQL, aplicando los principios **SOLID**. El sistema genera reportes automáticos en PDF y los envía por correo electrónico tras cada acción (crear, listar, modificar o eliminar).

## 🚀 Características

- **Arquitectura Limpia**: Separación de responsabilidades (Repository, Service, UI).
- **Reportes Inteligentes**: Generación de PDF con el estado "Antes y Después" de cada modificación.
- **Notificaciones**: Envío automático de reportes vía Gmail (SMTP).
- **Formateo Automático**: Los nombres siempre se guardan con la primera letra en mayúscula.

## 🛠️ Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone <url-del-repo>
   cd "SQL alchemy"
   ```

2. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:**
   Crea un archivo `.env` en la raíz del proyecto con el siguiente formato:

   ```text
   DATABASE_USER=root
   DATABASE_PASSWORD=tu_password_mysql
   DATABASE_HOST=localhost
   DATABASE_PORT=3306
   DATABASE_NAME=Clase1

   EMAIL_USER=tu_correo@gmail.com
   EMAIL_PASS=tu_clave_de_aplicacion_google
   ```

4. **Crear la Base de Datos:**
   Asegúrate de crear la base de datos en MySQL antes de correr el programa:
   ```sql
   CREATE DATABASE Clase1;
   ```

## 📋 Uso

Ejecuta el programa principal:

```bash
python app.py
```

## 🏗️ Estructura del Proyecto

- `app.py`: Interfaz de usuario y menú principal.
- `services.py`: Orquestador de lógica (DB + PDF + Email).
- `user_repository.py`: Manejo de consultas SQLAlchemy.
- `models.py`: Definición de la tabla de usuarios.
- `database.py`: Configuración de la conexión.
- `generate_report.py`: Lógica de creación de archivos PDF.
- `email_service.py`: Servicio de envío de correos.
