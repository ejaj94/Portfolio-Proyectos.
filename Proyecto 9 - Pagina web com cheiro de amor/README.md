# Proyecto 9: Página Web Premium "Com Cheiro de Amor"

Boutique online y catálogo interactivo de alta fidelidad desarrollado para la marca **Com Cheiro de Amor**, especializada en velas aromáticas ecológicas de cera de soja, jabones artesanales botánicos y piezas decorativas de yeso en Portugal.

---

## 🎨 Identidad y Diseño Visual
El diseño del sitio web replica la experiencia estética de una perfumería artesanal francesa de alta gama y boutique de decoración de interiores:
* **Tipografía**: Combinación de `Garamond` (títulos clásicos editoriales) con `Montserrat` (textos modernos y legibilidad limpia).
* **Paleta de Colores**: Tonos HSL cálidos y relajantes (Crema pastel, Oro suave, Terracota y Rosa apagado) que transmiten calma y naturalidad.
* **Micro-animaciones**: Transiciones interactivas fluidas, como la rotación suave de 360° en el hover del logotipo de la marca y la transición lateral en el carrusel de productos.

---

## 🌟 Características Clave

### 1. Sistema Multi-idioma en Tiempo Real (i18n)
* Soporte instantáneo para **Portugués (`pt`)**, **Español (`es`)**, **Inglés (`en`)** y **Francés (`fr`)**.
* Transición visual elegante sin recarga del navegador, aplicando un esvanecimiento rápido del contenido.
* Traducción automática de la base de datos de productos (nombres, aromas, descripciones detalladas) y la interfaz de usuario completa.

### 2. Carrito de Compras Interactiva con WhatsApp
* Permite agregar múltiples productos con cantidades modificables directamente desde las tarjetas del catálogo o el modal de detalles de cada producto.
* Compilación inteligente en tiempo real de los ítems seleccionados para exportar la orden final en un mensaje formateado al chat oficial de WhatsApp.
* **i18n en el Checkout**: El texto y formato del mensaje de WhatsApp se redacta automáticamente en el idioma en el que el usuario estaba navegando.

### 3. Carrusel y Lookbook Deslizante de Productos
* Sistema de paginación fluida en horizontal con límites dinámicos y estados interactivos visuales.
* Sección independiente para jabones artesanales equipada con un carrusel loop infinito responsivo (adaptable para Escritorio, Tablet y Móvil).
* Apertura de popups detallados con fotos completas y propiedades naturales de cada producto sin recortes de imagen.

### 4. Protección y Autenticidad Legal (INPI)
* Incorporación de una sección dedicada que avala el registro y patente oficial de la marca nacional ante el **INPI (Instituto Nacional da Propriedade Industrial)** con el certificado N.º 758901.

---

## 🛠️ Tecnologías Utilizadas
* **Estructura**: HTML5 semántico e inclusivo.
* **Estilos**: CSS3 clásico con variables dinámicas, Flexbox, CSS Grid y Media Queries responsivas.
* **Lógica**: JavaScript vanilla estructurado de forma modular y orientado a eventos del DOM sin dependencias de frameworks externos.

---

## 🚀 Despliegue Local
Para ejecutar el proyecto de forma local en tu máquina:

1. **Opción Directa**:
   Abre el archivo `index.html` en tu navegador preferido.

2. **Opción Servidor de Desarrollo (Recomendada con Autorecarga)**:
   Si tienes Python instalado, puedes iniciar un servidor de pruebas desde la terminal en este directorio:
   ```bash
   pip install -r requirements.txt
   python -m http.server 8000
   ```
   Luego navega a [http://localhost:8000](http://localhost:8000).
