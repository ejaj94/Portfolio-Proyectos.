import time
import threading
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import customtkinter as ctk

# Configuración inicial de apariencia
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MonitorPreciosApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("🕷️ Monitor de Precios Inteligente - Web Scraper GUI")
        self.geometry("720x680")
        self.minsize(640, 600)

        # Variables de control
        self.ejecutando = False
        self.hilo_monitoreo = None

        # Encabezado para peticiones HTTP
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        # Construir la interfaz de usuario
        self._crear_interfaz()

    def _crear_interfaz(self):
        # Configurar rejilla principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- TITULO ---
        self.titulo_label = ctk.CTkLabel(
            self,
            text="🕷️ Monitor de Precios Inteligente",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.titulo_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")

        # --- FRAME DE CONFIGURACIÓN ---
        self.frame_config = ctk.CTkFrame(self)
        self.frame_config.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.frame_config.grid_columnconfigure(1, weight=1)

        # Campo: URL
        self.label_url = ctk.CTkLabel(self.frame_config, text="URL del Producto:", font=ctk.CTkFont(weight="bold"))
        self.label_url.grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")

        self.entry_url = ctk.CTkEntry(
            self.frame_config,
            placeholder_text="https://ejemplo.com/producto"
        )
        self.entry_url.grid(row=0, column=1, columnspan=2, padx=15, pady=(12, 5), sticky="ew")
        self.entry_url.insert(0, "https://www.trendyventa.com/products/smart-lock-fingerprint-padlock")

        # Campo: Presupuesto Objetivo
        self.label_presupuesto = ctk.CTkLabel(self.frame_config, text="Presupuesto Objetivo ($):", font=ctk.CTkFont(weight="bold"))
        self.label_presupuesto.grid(row=1, column=0, padx=15, pady=8, sticky="w")

        self.entry_presupuesto = ctk.CTkEntry(self.frame_config, placeholder_text="10.00")
        self.entry_presupuesto.grid(row=1, column=1, padx=15, pady=8, sticky="ew")
        self.entry_presupuesto.insert(0, "10.00")

        # Campo: Frecuencia de revisión
        self.label_intervalo = ctk.CTkLabel(self.frame_config, text="Intervalo (segundos):", font=ctk.CTkFont(weight="bold"))
        self.label_intervalo.grid(row=1, column=2, padx=(5, 5), pady=8, sticky="w")

        self.entry_intervalo = ctk.CTkEntry(self.frame_config, width=80, placeholder_text="60")
        self.entry_intervalo.grid(row=1, column=3, padx=(0, 15), pady=8, sticky="w")
        self.entry_intervalo.insert(0, "60")

        # --- BOTONES DE CONTROL ---
        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.frame_botones.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_iniciar = ctk.CTkButton(
            self.frame_botones,
            text="▶ Iniciar Vigilancia",
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(weight="bold"),
            command=self.iniciar_monitoreo
        )
        self.btn_iniciar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.btn_detener = ctk.CTkButton(
            self.frame_botones,
            text="⏹ Detener Vigilancia",
            fg_color="#dc3545",
            hover_color="#c82333",
            font=ctk.CTkFont(weight="bold"),
            state="disabled",
            command=self.detener_monitoreo
        )
        self.btn_detener.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.btn_escanear = ctk.CTkButton(
            self.frame_botones,
            text="⚡ Escanear Ahora",
            fg_color="#17a2b8",
            hover_color="#138496",
            font=ctk.CTkFont(weight="bold"),
            command=self.escanear_ahora
        )
        self.btn_escanear.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # --- INSIGNIA DE ESTADO ---
        self.label_estado = ctk.CTkLabel(
            self,
            text="Estado: 🔴 Detenido",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#dc3545"
        )
        self.label_estado.grid(row=3, column=0, padx=20, pady=5, sticky="w")

        # --- PANEL DE LOGS / REGISTROS ---
        self.label_logs = ctk.CTkLabel(self, text="Historial de Monitoreo:", font=ctk.CTkFont(weight="bold"))
        self.label_logs.grid(row=4, column=0, padx=20, pady=(5, 0), sticky="w")

        self.textbox_logs = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox_logs.grid(row=5, column=0, padx=20, pady=(5, 15), sticky="nsew")
        self.grid_rowconfigure(5, weight=1)

        self.agregar_log("Sistema listo. Presiona '▶ Iniciar Vigilancia' o '⚡ Escanear Ahora'.")

    def agregar_log(self, mensaje):
        """Agrega un mensaje con estampa de tiempo al cuadro de texto de logs de forma segura."""
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        linea = f"[{ahora}] {mensaje}\n"

        def _actualizar():
            self.textbox_logs.insert("end", linea)
            self.textbox_logs.see("end")

        self.after(0, _actualizar)

    def actualizar_estado(self, texto, color):
        """Actualiza el texto y color del badge de estado en el hilo principal."""
        def _actualizar():
            self.label_estado.configure(text=f"Estado: {texto}", text_color=color)

        self.after(0, _actualizar)

    def consultar_precio(self):
        """Realiza la petición HTTP y parsea el precio desde la web."""
        url = self.entry_url.get().strip()
        try:
            presupuesto = float(self.entry_presupuesto.get().strip())
        except ValueError:
            self.agregar_log("❌ Error: El presupuesto debe ser un número válido (ej. 10.00).")
            return

        if not url:
            self.agregar_log("❌ Error: La URL no puede estar vacía.")
            return

        try:
            respuesta = requests.get(url, headers=self.headers, timeout=10)
            if respuesta.status_code != 200:
                self.agregar_log(f"⚠️ La web respondió con código de estado: {respuesta.status_code}")
                return

            sopa = BeautifulSoup(respuesta.content, "html.parser")
            precio_etiqueta = sopa.find("span", class_="price")

            if not precio_etiqueta:
                self.agregar_log("⚠️ No se encontró la etiqueta del precio ('span.price') en la página.")
                return

            precio_texto = precio_etiqueta.text.strip()
            precio_limpio = precio_texto.replace("$", "").replace(",", "")
            precio_final = float(precio_limpio)

            if precio_final <= presupuesto:
                self.agregar_log(f"🎉 ¡OFERTA DETECTADA! Precio: {precio_texto} (Objetivo: ${presupuesto:.2f})")
                self.actualizar_estado("🔔 ¡OFERTA ENCONTRADA!", "#28a745")
            else:
                self.agregar_log(f"🔎 Precio actual: {precio_texto} (Aún supera tu presupuesto de ${presupuesto:.2f})")
                if self.ejecutando:
                    self.actualizar_estado("🟢 Vigilando activo", "#28a745")

        except requests.exceptions.RequestException as err:
            self.agregar_log(f"❌ Error de red o conexión: {err}")
        except ValueError:
            self.agregar_log(f"❌ Error al convertir el precio leído ('{precio_texto}') a número.")
        except Exception as ex:
            self.agregar_log(f"❌ Error inesperado: {ex}")

    def escanear_ahora(self):
        """Ejecuta una consulta única en un hilo secundario para no congelar la UI."""
        self.agregar_log("⚡ Iniciando escaneo instantáneo...")
        threading.Thread(target=self.consultar_precio, daemon=True).start()

    def _bucle_monitoreo(self):
        """Bucle continuo ejecutado en segundo plano."""
        try:
            intervalo = int(self.entry_intervalo.get().strip())
            if intervalo < 5:
                intervalo = 5
        except ValueError:
            intervalo = 60

        self.agregar_log(f"🚀 Vigilancia iniciada. Intervalo: cada {intervalo} segundos.")
        self.actualizar_estado("🟢 Vigilando activo", "#28a745")

        while self.ejecutando:
            self.consultar_precio()
            # Dormir en pequeñas fracciones para responder rápido al botón detener
            for _ in range(intervalo):
                if not self.ejecutando:
                    break
                time.sleep(1)

        self.actualizar_estado("🔴 Detenido", "#dc3545")
        self.agregar_log("⏹ Vigilancia detenida por el usuario.")

    def iniciar_monitoreo(self):
        """Inicia el hilo de monitoreo continuo."""
        if self.ejecutando:
            return

        self.ejecutando = True
        self.btn_iniciar.configure(state="disabled")
        self.btn_detener.configure(state="normal")

        self.hilo_monitoreo = threading.Thread(target=self._bucle_monitoreo, daemon=True)
        self.hilo_monitoreo.start()

    def detener_monitoreo(self):
        """Detiene la ejecución del monitoreo continuo."""
        self.ejecutando = False
        self.btn_iniciar.configure(state="normal")
        self.btn_detener.configure(state="disabled")


if __name__ == "__main__":
    app = MonitorPreciosApp()
    app.mainloop()