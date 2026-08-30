import sys
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime

from database import SessionLocal, Base, engine, get_db_type
from models import User
from services import UserActionService

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class GestorProGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Asegurar tablas en la BD activa
        Base.metadata.create_all(bind=engine)
        
        # Inicializar sesión y servicio
        self.db = SessionLocal()
        self.service = UserActionService(self.db)

        # Configuración de ventana principal
        self.title("Gestor Pro DB v2.0 - SQLAlchemy ORM")
        self.geometry("1150x720")
        self.minsize(950, 600)

        # Configurar grid de 2 columnas (Sidebar + Main)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Selección activa para edición
        self.selected_user_id = None

        # Construir Interfaz
        self._create_sidebar()
        self._create_main_content()
        
        # Cargar datos iniciales
        self.refresh_data()

    # ==========================================
    # 1. SIDEBAR (PANEL LATERAL NAVEGACIÓN)
    # ==========================================
    def _create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        sidebar.grid_rowconfigure(9, weight=1)

        # Logo y Título
        title_label = ctk.CTkLabel(
            sidebar, 
            text="⚡ Gestor Pro DB", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(25, 5))

        subtitle = ctk.CTkLabel(
            sidebar, 
            text="SQLAlchemy ORM + Reports", 
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Badge de Estado de Base de Datos
        db_type = get_db_type()
        badge_color = "#2fa572" if "MySQL" in db_type else "#3a7ebf"
        
        db_badge_frame = ctk.CTkFrame(sidebar, fg_color=badge_color, corner_radius=8)
        db_badge_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        db_badge_label = ctk.CTkLabel(
            db_badge_frame, 
            text=f"DB: {db_type}", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white"
        )
        db_badge_label.pack(padx=10, pady=6)

        # Opción Enviar Correo Automático
        self.auto_email_var = ctk.BooleanVar(value=False)
        self.auto_email_check = ctk.CTkCheckBox(
            sidebar, 
            text="Email en cada cambio", 
            variable=self.auto_email_var,
            font=ctk.CTkFont(size=12)
        )
        self.auto_email_check.grid(row=3, column=0, padx=20, pady=15, sticky="w")

        # Separador visual
        sep = ctk.CTkFrame(sidebar, height=2, fg_color=("gray70", "gray30"))
        sep.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # Botones de Acción Rápida de Reportes
        pdf_btn = ctk.CTkButton(
            sidebar, 
            text="📄 Generar PDF", 
            fg_color="#1f538d", 
            hover_color="#14375e",
            command=self._on_generar_pdf
        )
        pdf_btn.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        email_btn = ctk.CTkButton(
            sidebar, 
            text="✉️ Enviar Reporte Email", 
            fg_color="#2fa572", 
            hover_color="#1e6b49",
            command=self._on_enviar_email
        )
        email_btn.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        # Toggle Modo Oscuro/Claro
        theme_label = ctk.CTkLabel(sidebar, text="Tema de Interfaz:", font=ctk.CTkFont(size=12))
        theme_label.grid(row=10, column=0, padx=20, pady=(10, 0), sticky="w")

        theme_switch = ctk.CTkSwitch(
            sidebar, 
            text="Modo Oscuro", 
            command=self._toggle_theme,
            onvalue="Dark", 
            offvalue="Light"
        )
        theme_switch.grid(row=11, column=0, padx=20, pady=(5, 20), sticky="w")
        theme_switch.select()

    # ==========================================
    # 2. CONTENIDO PRINCIPAL (DASHBOARD + TABLA)
    # ==========================================
    def _create_main_content(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # A) Tarjetas de Estadísticas Superior
        stats_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Card 1: Total Usuarios
        card1 = ctk.CTkFrame(stats_frame, corner_radius=12)
        card1.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ctk.CTkLabel(card1, text="Total Registrados", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray").pack(padx=15, pady=(12, 2))
        self.lbl_stat_total = ctk.CTkLabel(card1, text="0", font=ctk.CTkFont(size=26, weight="bold"))
        self.lbl_stat_total.pack(padx=15, pady=(0, 12))

        # Card 2: Edad Promedio
        card2 = ctk.CTkFrame(stats_frame, corner_radius=12)
        card2.grid(row=0, column=1, padx=5, sticky="ew")
        ctk.CTkLabel(card2, text="Edad Promedio", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray").pack(padx=15, pady=(12, 2))
        self.lbl_stat_avg_age = ctk.CTkLabel(card2, text="0.0 años", font=ctk.CTkFont(size=26, weight="bold"))
        self.lbl_stat_avg_age.pack(padx=15, pady=(0, 12))

        # Card 3: Servicio Email
        card3 = ctk.CTkFrame(stats_frame, corner_radius=12)
        card3.grid(row=0, column=2, padx=(10, 0), sticky="ew")
        ctk.CTkLabel(card3, text="Servicio de Correo", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray").pack(padx=15, pady=(12, 2))
        self.lbl_stat_email = ctk.CTkLabel(card3, text="Configurado", font=ctk.CTkFont(size=20, weight="bold"), text_color="#2fa572")
        self.lbl_stat_email.pack(padx=15, pady=(0, 12))

        # B) Barra de Búsqueda y Botones de Acción
        action_bar = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_bar.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        action_bar.grid_columnconfigure(0, weight=1)

        # Entrada de búsqueda
        self.search_entry = ctk.CTkEntry(
            action_bar, 
            placeholder_text="🔍 Buscar por ID, Nombre o Apellido...",
            font=ctk.CTkFont(size=13),
            height=38
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._on_search_key)

        # Botón Nuevo Usuario
        btn_add = ctk.CTkButton(
            action_bar, 
            text="+ Nuevo Usuario", 
            height=38, 
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._open_user_form
        )
        btn_add.grid(row=0, column=1, padx=5)

        # Botón Editar
        btn_edit = ctk.CTkButton(
            action_bar, 
            text="✏️ Editar", 
            height=38,
            fg_color="#d97706",
            hover_color="#b45309",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._on_edit_click
        )
        btn_edit.grid(row=0, column=2, padx=5)

        # Botón Eliminar
        btn_del = ctk.CTkButton(
            action_bar, 
            text="🗑️ Eliminar", 
            height=38,
            fg_color="#dc2626",
            hover_color="#991b1b",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._on_delete_click
        )
        btn_del.grid(row=0, column=3, padx=(5, 0))

        # C) Tabla de Datos (Treeview estilizado)
        table_container = ctk.CTkFrame(main_frame, corner_radius=10)
        table_container.grid(row=2, column=0, sticky="nsew")
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        # Estilo ttk para Treeview compatible con Modo Oscuro
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#2a2d2e",
            foreground="white",
            rowheight=32,
            fieldbackground="#2a2d2e",
            bordercolor="#343638",
            font=("Segoe UI", 11)
        )
        style.configure(
            "Treeview.Heading",
            background="#1f2324",
            foreground="white",
            relief="flat",
            font=("Segoe UI", 11, "bold")
        )
        style.map("Treeview", background=[("selected", "#1f538d")])

        # Crear Treeview
        columns = ("id", "name", "last_name", "age", "created_at")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID", anchor="center")
        self.tree.heading("name", text="Nombre", anchor="w")
        self.tree.heading("last_name", text="Apellido", anchor="w")
        self.tree.heading("age", text="Edad", anchor="center")
        self.tree.heading("created_at", text="Fecha de Registro", anchor="center")

        self.tree.column("id", width=70, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("last_name", width=220, anchor="w")
        self.tree.column("age", width=90, anchor="center")
        self.tree.column("created_at", width=200, anchor="center")

        # Scrollbar vertical
        scrollbar = ctk.CTkScrollbar(table_container, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=5)

        self.tree.bind("<Double-1>", lambda e: self._on_edit_click())

        # D) Barra de Estado Inferior
        self.status_label = ctk.CTkLabel(
            main_frame, 
            text="Listo", 
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.grid(row=3, column=0, sticky="w", pady=(10, 0))

    # ==========================================
    # 3. LÓGICA DE NEGOCIO Y EVENTOS
    # ==========================================
    def set_status(self, text, is_error=False):
        color = "#ef4444" if is_error else ("gray70", "gray40")
        self.status_label.configure(text=text, text_color=color)

    def refresh_data(self, query=None):
        """Actualiza los datos de la tabla y los paneles de estadísticas"""
        # Limpiar filas existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Cargar desde BD
        if query:
            users = self.service.search_users(query)
        else:
            users = self.service.repo.get_all()

        for u in users:
            fecha_str = u.created_at.strftime("%d/%m/%Y %H:%M") if u.created_at else "N/A"
            self.tree.insert("", "end", values=(u.id, u.name, u.last_name, u.age, fecha_str))

        # Actualizar estadísticas
        stats = self.service.get_stats()
        self.lbl_stat_total.configure(text=str(stats["total_users"]))
        self.lbl_stat_avg_age.configure(text=f"{stats['avg_age']} años")
        
        if stats["mailer_configured"]:
            self.lbl_stat_email.configure(text="Configurado", text_color="#2fa572")
        else:
            self.lbl_stat_email.configure(text="No Configurado", text_color="#d97706")

        self.set_status(f"Cargados {len(users)} usuarios")

    def _on_search_key(self, event):
        query = self.search_entry.get()
        self.refresh_data(query)

    def _toggle_theme(self):
        mode = ctk.get_appearance_mode()
        new_mode = "Light" if mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        
        # Ajustar estilos de la tabla para modo claro/oscuro
        style = ttk.Style()
        if new_mode == "Light":
            style.configure("Treeview", background="#f3f4f6", foreground="black", fieldbackground="#f3f4f6")
            style.configure("Treeview.Heading", background="#e5e7eb", foreground="black")
        else:
            style.configure("Treeview", background="#2a2d2e", foreground="white", fieldbackground="#2a2d2e")
            style.configure("Treeview.Heading", background="#1f2324", foreground="white")

    # ==========================================
    # 4. DIÁLOGOS DE CREACIÓN Y EDICIÓN
    # ==========================================
    def _open_user_form(self, user_to_edit=None):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Modificar Usuario" if user_to_edit else "Nuevo Usuario")
        dialog.geometry("420x360")
        dialog.resizable(False, False)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog, 
            text="Editar Registro" if user_to_edit else "Registrar Nuevo Usuario", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))

        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(padx=30, fill="x")

        # Campo Nombre
        ctk.CTkLabel(form_frame, text="Nombre:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(5, 2))
        entry_name = ctk.CTkEntry(form_frame, placeholder_text="Ej. Carlos")
        entry_name.pack(fill="x", pady=(0, 10))

        # Campo Apellido
        ctk.CTkLabel(form_frame, text="Apellido:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(5, 2))
        entry_last_name = ctk.CTkEntry(form_frame, placeholder_text="Ej. Mendoza")
        entry_last_name.pack(fill="x", pady=(0, 10))

        # Campo Edad
        ctk.CTkLabel(form_frame, text="Edad:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(5, 2))
        entry_age = ctk.CTkEntry(form_frame, placeholder_text="Ej. 28")
        entry_age.pack(fill="x", pady=(0, 15))

        # Pre-llenar datos si es edición
        if user_to_edit:
            entry_name.insert(0, user_to_edit.name)
            entry_last_name.insert(0, user_to_edit.last_name)
            entry_age.insert(0, str(user_to_edit.age))

        def _save():
            name = entry_name.get().strip()
            last_name = entry_last_name.get().strip()
            age_str = entry_age.get().strip()

            if not name or not last_name or not age_str:
                messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.", parent=dialog)
                return

            try:
                age = int(age_str)
                if age <= 0 or age > 120:
                    raise ValueError("Edad fuera de rango")
            except ValueError:
                messagebox.showerror("Error", "Ingrese una edad numérica válida (1 - 120).", parent=dialog)
                return

            send_email = self.auto_email_var.get()

            if user_to_edit:
                res = self.service.ejecutar_y_notificar(
                    "update", 
                    send_email=send_email,
                    id=user_to_edit.id, 
                    name=name, 
                    last_name=last_name, 
                    age=age
                )
                if res:
                    self.set_status(f"✅ Usuario #{res.id} modificado exitosamente")
            else:
                res = self.service.ejecutar_y_notificar(
                    "add", 
                    send_email=send_email,
                    name=name, 
                    last_name=last_name, 
                    age=age
                )
                if res:
                    self.set_status(f"✅ Usuario '{res.name} {res.last_name}' registrado exitosamente")

            dialog.destroy()
            self.refresh_data()

        btn_save = ctk.CTkButton(
            dialog, 
            text="Guardar Cambios" if user_to_edit else "Registrar Usuario", 
            font=ctk.CTkFont(size=14, weight="bold"),
            height=38,
            command=_save
        )
        btn_save.pack(padx=30, pady=15, fill="x")

    def _on_edit_click(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un usuario de la lista.")
            return

        values = self.tree.item(selected[0], "values")
        user_id = int(values[0])
        user = self.service.repo.get_by_id(user_id)
        if user:
            self._open_user_form(user_to_edit=user)

    def _on_delete_click(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un usuario de la lista a eliminar.")
            return

        values = self.tree.item(selected[0], "values")
        user_id = int(values[0])
        name = f"{values[1]} {values[2]}"

        confirm = messagebox.askyesno(
            "Confirmar eliminación", 
            f"¿Está seguro de que desea eliminar al usuario #{user_id} ({name})?"
        )
        if confirm:
            send_email = self.auto_email_var.get()
            res = self.service.ejecutar_y_notificar("delete", send_email=send_email, id=user_id)
            if res:
                self.set_status(f"✅ Usuario #{user_id} eliminado")
                self.refresh_data()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario seleccionado.")

    # ==========================================
    # 5. ASYNC PDF & EMAIL THREADING
    # ==========================================
    def _on_generar_pdf(self):
        def _task():
            self.set_status("⏳ Generando reporte PDF...")
            ruta = self.service.generar_pdf_manual()
            self.set_status(f"✅ PDF generado exitosamente: {os.path.basename(ruta)}")
            try:
                os.startfile(ruta)
            except Exception:
                pass

        threading.Thread(target=_task, daemon=True).start()

    def _on_enviar_email(self):
        def _task():
            self.set_status("⏳ Generando reporte y enviando email...")
            exito, pdf_path = self.service.enviar_email_manual()
            if exito:
                self.set_status(f"✅ Reporte enviado a {self.service.admin_email}")
                messagebox.showinfo("Éxito", f"Reporte enviado exitosamente a {self.service.admin_email}")
            else:
                self.set_status("❌ Error al enviar el correo. Verifique credenciales .env", is_error=True)
                messagebox.showwarning(
                    "Advertencia de Correo", 
                    "No se pudo enviar el correo.\nVerifique que EMAIL_USER y EMAIL_PASS estén configurados en el archivo .env."
                )

        threading.Thread(target=_task, daemon=True).start()

def main():
    app = GestorProGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
