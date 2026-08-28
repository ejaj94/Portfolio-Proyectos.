import customtkinter as ctk
from tkinter import messagebox
from Calculos import calcular_tmb, calcular_calorias_totales

# Configuración inicial de la apariencia (Modo Claro)
ctk.set_appearance_mode("Light")  # "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class CalculadoraCaloriasGUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("TITAN GYM - Calculadora de Calorías y TMB")
        self.geometry("520x680")
        self.resizable(False, False)

        # Contenedor Principal
        self.main_frame = ctk.CTkFrame(
            self, corner_radius=15, fg_color="#FFFFFF"
        )
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Badge Gym & Título
        self.badge_label = ctk.CTkLabel(
            self.main_frame,
            text="🏋️‍♂️ TITAN GYM",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#EA580C",
        )
        self.badge_label.pack(pady=(15, 2))

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Calculadora Nutricional & TMB",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#0F172A",
        )
        self.title_label.pack(pady=(0, 10))

        # Formulario de Entradas
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.form_frame.pack(padx=20, fill="x")

        # Nombre
        self.lbl_nombre = ctk.CTkLabel(
            self.form_frame, text="Nombre del Atleta:", anchor="w"
        )
        self.lbl_nombre.pack(fill="x", pady=(5, 0))
        self.entry_nombre = ctk.CTkEntry(
            self.form_frame, placeholder_text="Tu nombre"
        )
        self.entry_nombre.pack(fill="x", pady=(0, 10))

        # Peso
        self.lbl_peso = ctk.CTkLabel(
            self.form_frame, text="Peso (kg):", anchor="w"
        )
        self.lbl_peso.pack(fill="x", pady=(5, 0))
        self.entry_peso = ctk.CTkEntry(
            self.form_frame, placeholder_text="Ej: 70.5"
        )
        self.entry_peso.pack(fill="x", pady=(0, 10))

        # Altura
        self.lbl_altura = ctk.CTkLabel(
            self.form_frame, text="Altura (cm):", anchor="w"
        )
        self.lbl_altura.pack(fill="x", pady=(5, 0))
        self.entry_altura = ctk.CTkEntry(
            self.form_frame, placeholder_text="Ej: 175"
        )
        self.entry_altura.pack(fill="x", pady=(0, 10))

        # Edad
        self.lbl_edad = ctk.CTkLabel(
            self.form_frame, text="Edad (años):", anchor="w"
        )
        self.lbl_edad.pack(fill="x", pady=(5, 0))
        self.entry_edad = ctk.CTkEntry(
            self.form_frame, placeholder_text="Ej: 25"
        )
        self.entry_edad.pack(fill="x", pady=(0, 10))

        # Género y Nivel de Actividad en 2 columnas
        self.options_frame = ctk.CTkFrame(
            self.form_frame, fg_color="transparent"
        )
        self.options_frame.pack(fill="x", pady=(5, 10))

        self.lbl_genero = ctk.CTkLabel(
            self.options_frame, text="Género:", anchor="w"
        )
        self.lbl_genero.grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.combo_genero = ctk.CTkOptionMenu(
            self.options_frame, values=["Hombre", "Mujer"]
        )
        self.combo_genero.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        self.lbl_actividad = ctk.CTkLabel(
            self.options_frame, text="Nivel de Actividad:", anchor="w"
        )
        self.lbl_actividad.grid(row=0, column=1, sticky="w")

        self.combo_actividad = ctk.CTkOptionMenu(
            self.options_frame,
            values=[
                "Sedentario",
                "Ligero",
                "Moderado",
                "Activo",
                "Muy activo",
            ],
        )
        self.combo_actividad.grid(row=1, column=1, sticky="ew")
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)

        # Botón Calcular
        self.btn_calcular = ctk.CTkButton(
            self.main_frame,
            text="Calcular Calorías",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#EA580C",
            hover_color="#C2410C",
            height=40,
            command=self.calcular,
        )
        self.btn_calcular.pack(padx=20, pady=15, fill="x")

        # Frame de Resultados
        self.result_frame = ctk.CTkFrame(
            self.main_frame, corner_radius=10, fg_color="#F8FAFC"
        )
        self.result_frame.pack(padx=20, pady=(0, 15), fill="both", expand=True)

        self.lbl_res_header = ctk.CTkLabel(
            self.result_frame,
            text="Resultados",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#0F172A",
        )
        self.lbl_res_header.pack(pady=(10, 5))

        self.lbl_tmb = ctk.CTkLabel(
            self.result_frame,
            text="TMB Base: -- Kcal",
            font=ctk.CTkFont(size=13),
            text_color="#7E22CE",
        )
        self.lbl_tmb.pack(pady=2)

        self.lbl_mantener = ctk.CTkLabel(
            self.result_frame,
            text="Mantenimiento: -- Kcal",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#1D4ED8",
        )
        self.lbl_mantener.pack(pady=2)

        self.lbl_superavit = ctk.CTkLabel(
            self.result_frame,
            text="Superávit (+300 kcal): -- Kcal",
            font=ctk.CTkFont(size=13),
            text_color="#15803D",
        )
        self.lbl_superavit.pack(pady=2)

        self.lbl_deficit = ctk.CTkLabel(
            self.result_frame,
            text="Déficit (-300 kcal): -- Kcal",
            font=ctk.CTkFont(size=13),
            text_color="#B91C1C",
        )
        self.lbl_deficit.pack(pady=2)

    def calcular(self):
        nombre = self.entry_nombre.get().strip()
        peso_raw = self.entry_peso.get().strip()
        altura_raw = self.entry_altura.get().strip()
        edad_raw = self.entry_edad.get().strip()
        genero = self.combo_genero.get()
        actividad = self.combo_actividad.get()

        if not peso_raw or not altura_raw or not edad_raw:
            messagebox.showwarning(
                "Campos incompletos",
                "Por favor llena los campos de Peso, Altura y Edad.",
            )
            return

        try:
            peso = float(peso_raw)
            altura = float(altura_raw)
            edad = int(edad_raw)

            if peso <= 0 or altura <= 0 or edad <= 0:
                messagebox.showerror(
                    "Valores inválidos",
                    "Peso, altura y edad deben ser números positivos.",
                )
                return

        except ValueError:
            messagebox.showerror(
                "Error de Entrada",
                "Por favor ingresa valores numéricos válidos en Peso, Altura y Edad.",
            )
            return

        saludo = f"Para {nombre}:" if nombre else "Resultados:"
        self.lbl_res_header.configure(text=saludo)

        resultado_tmb = calcular_tmb(peso, altura, edad, genero)
        total_calorias = calcular_calorias_totales(resultado_tmb, actividad)

        self.lbl_tmb.configure(
            text=f"Tasa Metabólica Basal (TMB): {resultado_tmb:.2f} Kcal"
        )
        self.lbl_mantener.configure(
            text=f"Mantenimiento: {total_calorias:.2f} Kcal/día"
        )
        self.lbl_superavit.configure(
            text=f"Superávit Moderado: {total_calorias + 300:.2f} Kcal/día"
        )
        self.lbl_deficit.configure(
            text=f"Déficit Moderado: {total_calorias - 300:.2f} Kcal/día"
        )


def main():
    app = CalculadoraCaloriasGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
