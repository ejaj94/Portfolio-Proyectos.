# Comenzamos con la interfaz gráfica:
# Importamos nuestra biblioteca:
import customtkinter as ctk
import psutil

# Definimos la clase y le damos parámetros de título, apariencia y resolución:
class SentinelNodeUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SentinelNode - Dashboard de seguridad")
        self.geometry("900x600")

        # En este caso lo pondremos modo oscuro:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variable para controlar si el monitoreo está activo o no:
        self.monitoring = False

        # Creamos la barra laterales, filas, columnas, área principal, título:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="SENTINEL NODE", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Botón de Inicio/Parada en la barra lateral:
        self.btn_monitor = ctk.CTkButton(self.sidebar, 
                                         text="INICIAR MONITOREO", 
                                         command=self.toggle_monitoring)
        self.btn_monitor.grid(row=1, column=0, padx=20, pady=20)

        # Creamos la tabla de visualización, frame, título, consola:
        self.main_content = ctk.CTkFrame(self, corner_radius=15)
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.status_label = ctk.CTkLabel(self.main_content, text="Procesos Activos y Conexiones", font=("Helvetica", 16))
        self.status_label.pack(pady=10)
        
        self.monitor_console = ctk.CTkTextbox(self.main_content, width=600, height=400)
        self.monitor_console.pack(padx=20, pady=10, fill="both", expand=True)

    # Definimos una función para el botón de inicio del sentinelnodeui:
    def toggle_monitoring(self):
        # Si el botón está en azul, lo pasamos a verde y activamos el ciclo
        if self.btn_monitor.cget("fg_color") == "blue" or self.btn_monitor.cget("fg_color") == ["#3B8ED0", "#1F6AA5"]:
            self.monitoring = True
            self.btn_monitor.configure(text="MONITOREO ACTIVO", fg_color="green")
            self.monitor_console.insert("end", "[>] Iniciando escaneo de procesos...\n")
            # Llamamos a la función que actualiza los datos:
            self.update_processes()
        else:
            # Si ya estaba activo, lo detenemos y limpiamos la variable:
            self.monitoring = False
            self.btn_monitor.configure(text="INICIAR MONITOREO", fg_color="blue")
            self.monitor_console.delete("1.0", "end")
            self.monitor_console.insert("end", "[!] Vigilancia detenida.\n")

    # Nueva función para obtener y mostrar los procesos reales:
    def update_processes(self):
        # Si el usuario detuvo el monitoreo, salimos de la función:
        if not self.monitoring:
            return
        
        # Limpiamos la consola antes de poner la info nueva:
        self.monitor_console.delete("1.0", "end")
        self.monitor_console.insert("end", f"{'PID':<10} {'NOMBRE':<35} {'ESTADO':<15}\n")
        self.monitor_console.insert("end", "-"*60 + "\n")

        # Recorremos los procesos del sistema:
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                p_info = proc.info
                linea = f"{p_info['pid']:<10} {p_info['name']:<35} {p_info['status']:<15}\n"
                self.monitor_console.insert("end", linea)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Si el proceso se cierra o no tenemos permiso, lo saltamos:
                continue
        
        # Hacemos que la función se llame a sí misma cada 2 segundos para actualizar:
        self.after(2000, self.update_processes)


# Lo ponemos en marcha:
if __name__ == "__main__":
    app = SentinelNodeUI()
    app.mainloop()
