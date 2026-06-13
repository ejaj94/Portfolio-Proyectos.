# Logleve - Plataforma Premium de Entregas de Alta Performance

Logleve es una plataforma digital de logística y distribución de última milla que conecta **Clientes, Estafetas (Repartidores) y Restaurantes** en tiempo real. Este proyecto implementa una arquitectura unificada que acopla de manera eficiente las vistas del navegador con contenedores WebView nativos para dispositivos móviles (Android).

El sistema se rige bajo principios de diseño limpio (**SOLID**), desacoplamiento de dependencias y el **Patrón de Repositorio**, lo que permite una escalabilidad total y facilita el cambio de motores de base de datos o APIs de terceros con mínimo esfuerzo.

---

## 🛠️ Arquitectura y Tecnologías Core

- **Backend Framework:** Python 3.12+ con **Flask** para el enrutamiento de la aplicación y controladores de vistas.
- **Real-Time Communication:** **Flask-SocketIO** (WebSockets) con soporte asíncrono para la transmisión instantánea del radar GPS y notificaciones del KDS de cocina.
- **Motor de Base de Datos:** SQLite como persistencia ágil basada en ficheros mediante el **Repository Pattern** (`BaseRepository` y `SqliteRepository`).
- **Pasarela de Pagos:** Integración segura con **Stripe API** para la retención y liberación de saldos, y simulación integrada de pagos por **MB WAY**.
- **Internacionalización (i18n):** **Flask-Babel** configurado para traducción dinámica del sistema a los **30 idiomas más hablados del mundo** con selector en tiempo de ejecución.
- **Clientes Móviles (Android):** Aplicaciones envolventes nativas en Kotlin/Gradle estructuradas mediante contenedores WebView de alto rendimiento para garantizar interfaces ligeras pero responsivas en carretera.

---

## 🌟 Características de las Sub-Aplicaciones

### 📱 1. App del Cliente
- **Menú y Selección Interactiva:** Lista de platos configurables directamente de la cocina con soporte de carrito de compras local.
- **Pasarela Check-Out Seguro:** Procesamiento de transacciones de Stripe y soporte nacional portugués para MB WAY.
- **Rastreo GPS en Tiempo Real:** Monitorización visual del trayecto del estafeta vía satélite directamente sobre un mapa integrado.
- **Seguridad en Registro:** Método de verificación de cuenta preferido por el usuario (**SMS o Correo Electrónico**) mediante códigos PIN de 4 dígitos (con soporte integrado de Twilio).

### 🛵 2. App del Estafeta (Repartidor)
- **Registro Inteligente y OCR por IA:** Carga de documentos de identidad, licencia de conducción y seguro con análisis automatizado de visión por IA para aprobación de candidaturas.
- **Exención de Matrícula:** Filtro automático que exime a **Bicicletas** y **Trotinetes Eléctricas** de la obligatoriedad de aportar matrícula, seguro o licencia de conducción.
- **Radar de Comisiones:** Panel táctico en carretera para aceptar, recoger y entregar pedidos dinámicamente.
- **Monedero Virtual:** Secuencia de facturación y cobro semanal con retiros (*cashout*) inmediatos vía Stripe Connect/IBAN.

### 🍳 3. Portal del Restaurante
- **Kitchen Display System (KDS):** Monitor táctil de cocina con alertas sonoras instantáneas al recibir pedidos nuevos.
- **Gestión de Menú Dinámico:** Herramienta interna para subir fotos de platos, actualizar precios y definir stock en tiempo real.

### 🎧 4. Centro de Soporte Dedicado (`/support`)
- **Chatbot de IA Empático:** Asistente de soporte conversacional que adapta sus respuestas según el perfil operativo del usuario (Cliente, Repartidor, Local).
- **Controlador de Frustración:** Algoritmo de análisis lingüístico que detecta enfado o retrasos en el texto, emitiendo respuestas altamente conciliadoras y derivando el chat de forma prioritaria a un supervisor humano sénior simulado.

### ⚙️ 5. Consola Administrativa Centralizada (`/admin/couriers`)
- **Visualizador de Base de Datos:** Interfaz restringida bajo palabra-passe administrativa que renderiza un listado completo de todos los estafetas en producción.
- **Validación de Documentos:** Descargas directas de licencias, seguros y fotos de perfil subidas por los repartidores en el portal para su aprobación manual.
- **Modificación Rápida:** Cambios en caliente del saldo de su billetera, tipo de vehículo asignado, matrícula y estado operacional (`approved`, `rejected`, `pending`).

---

## 📂 Estructura del Directorio del Proyecto

```markdown
├── app.py                     # Punto de entrada de la aplicación Flask
├── reset_db.py                # Script de inicialización y migración SQLite
├── requirements.txt           # Dependencias oficiales del proyecto
├── .gitignore                 # Configuración de archivos excluidos de Git
├── README.md                  # Documentación oficial del proyecto
│
├── delivery_app/              # Carpeta principal del código fuente
│   ├── api/                   # Blueprints y endpoints JSON de la API REST
│   ├── controllers/           # Controladores Flask y vistas HTML de las Apps
│   ├── entities/              # Clases modelo de dominio del negocio (SOLID)
│   ├── infrastructure/        # Configuración de persistencia y base de datos
│   ├── repositories/          # Mapeo y lógica SQL (Repository Pattern)
│   ├── services/              # Casos de uso y lógica de verificación de documentos (IA)
│   ├── static/                # Archivos estáticos corporativos (Imágenes, CSS, Favicons)
│   ├── templates/             # Plantillas HTML optimizadas (Jinja2)
│   └── translations/          # Diccionarios de internacionalización Babel
│
└── android/                   # Códigos fuente nativos de aplicaciones Android
    ├── client/                # App Android Cliente (WebView wrapper)
    ├── courier/               # App Android Estafeta (WebView wrapper)
    └── restaurant/            # App Android Restaurante (WebView wrapper)
```

---

## 🚀 Instalación y Puesta en Marcha

### Prerrequisitos
- Python 3.12 o superior.
- Git instalado en tu máquina local.

### Paso 1: Clonar y Preparar Entorno
Clona la carpeta a tu entorno de desarrollo y crea un entorno virtual de Python:
```bash
python -m venv .venv
# Activar en Windows
.venv\Scripts\activate
# Activar en Linux/macOS
source .venv/bin/activate
```

### Paso 2: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 3: Inicializar Base de Datos SQLite
Genera el archivo local de la base de datos `delivery_app.db` con toda la estructura del esquema actualizada y los datos semilla para pruebas:
```bash
python reset_db.py
```

### Paso 4: Configurar Variables de Entorno (Opcional)
Para habilitar el envío real de SMS y Correos, configura en tus variables de sistema:
```bash
# SMS Twilio
export TWILIO_ACCOUNT_SID="tu_sid_aqui"
export TWILIO_AUTH_TOKEN="tu_token_aqui"
export TWILIO_FROM_NUMBER="tu_numero_twilio"

# Email SMTP
export SMTP_SERVER="smtp.ejemplo.com"
export SMTP_USER="tu_correo"
export SMTP_PASS="tu_contraseña"

# Acceso Administrador
export APP_ADMIN_PASSWORD="tu_clave_secreta"
```
*Si no las defines, el sistema funcionará en modo de Simulación imprimiendo todos los códigos generados en los logs de la terminal para agilizar el testeo.*

### Paso 5: Iniciar el Servidor de Desarrollo
```bash
python app.py
```
Abre en tu navegador la dirección **`http://127.0.0.1:5001`** para experimentar el ecosistema.
