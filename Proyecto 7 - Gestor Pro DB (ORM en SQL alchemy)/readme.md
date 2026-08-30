# Sistema Profesional de Gestión de Usuarios v2.0 (SQLAlchemy ORM + GUI)

Aplicación de escritorio profesional y modular para la gestión de usuarios con **SQLAlchemy ORM**, interfaz gráfica moderna desarrollada en **CustomTkinter**, soporte de base de datos híbrida (MySQL con fallback a SQLite local), generación de reportes PDF inteligentes con **ReportLab** y notificaciones por correo electrónico vía **SMTP (Gmail)**.

---

## 🚀 Características Principales

- **🎨 Interfaz Gráfica de Usuario (GUI Moderna)**:
  - Diseño estilo *Dark Mode / Light Mode* con tarjetas interactivas y bordes redondeados.
  - **Tabla Dinámica (Treeview)**: Visualización limpia de registros con ordenamiento.
  - **Búsqueda en Tiempo Real**: Filtrado instantáneo por ID, Nombre o Apellido.
  - **Tarjetas de Estadísticas (Dashboard)**: Conteo total de usuarios, edad promedio y estado del servicio de correo.
  - **Formularios Modales**: Diálogos con validación de entradas para Crear y Editar usuarios.

- **💾 Base de Datos Híbrida y Resiliente (SQLAlchemy)**:
  - Conexión nativa a **MySQL**.
  - **Conmutación Automática a SQLite (Fallback)**: Si el servidor MySQL no está encendido o falta configurar `.env`, el sistema se conecta automáticamente a la base de datos local `gestor_pro.db` sin interrumpir la experiencia.

- **📄 Reportes Inteligentes y Correo en Segundo Plano**:
  - Generación de reportes **PDF en tiempo real** con auditoría de cambios ("Antes y Después").
  - **Ejecución Asíncrona (Threading)**: La generación de PDF y el envío de emails se realizan en hilos secundarios para que la interfaz nunca se congelé ni se bloquee.

---

## 🛠️ Requisitos e Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/ejaj94/Portfolio-Proyectos..git
   cd "Portfolio de programacion/Proyectos/Proyecto 7 - Gestor Pro DB (ORM en SQL alchemy)"
   ```

2. **Instalar dependencias:**

   ```bash
   pip install -r requeriment.txt
   ```

3. **Configurar variables de entorno (Opcional para MySQL y Gmail):**
   Crea un archivo `.env` en la raíz del proyecto:

   ```text
   DATABASE_USER=root
   DATABASE_PASSWORD=tu_password_mysql
   DATABASE_HOST=localhost
   DATABASE_PORT=3306
   DATABASE_NAME=Clase1

   EMAIL_USER=tu_correo@gmail.com
   EMAIL_PASS=tu_clave_de_aplicacion_google
   ```

---

## 📋 Uso de la Aplicación

### Modo Interfaz Gráfica (GUI - Por defecto)

```bash
python app.py
```

### Modo Consola (CLI)

```bash
python app.py --cli
```

---

## 🏗️ Estructura del Proyecto

- `app.py`: Punto de entrada principal (ejecuta la GUI o CLI mediante `--cli`).
- `gui_app.py`: Interfaz gráfica moderna en CustomTkinter con Dashboard, formularios y tabla.
- `services.py`: Orquestador de lógica de negocio (DB + PDF + Email).
- `user_repository.py`: Consultas ORM y filtros de búsqueda.
- `models.py`: Modelo ORM de la tabla `users`.
- `database.py`: Configuración de SQLAlchemy con fallback automático MySQL / SQLite.
- `generate_report.py`: Generador de reportes PDF en ReportLab.
- `email_service.py`: Servicio de notificaciones por correo SMTP.
