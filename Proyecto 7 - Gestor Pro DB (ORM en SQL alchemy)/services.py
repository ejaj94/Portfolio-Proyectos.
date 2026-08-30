from datetime import datetime
from user_repository import UserRepository
from generate_report import crear_pdf
from email_service import EmailService

# UserActionService aplica el principio de Responsabilidad Única (S)
# centralizando la coordinación de base de datos, PDF y correos.
class UserActionService:
    def __init__(self, db):
        # Inyección de dependencias: recibe la conexión de DB y levanta los servicios
        self.repo = UserRepository(db)
        self.mailer = EmailService()
        self.admin_email = "enmanuelejaj@gmail.com" # Destinatario por defecto

    def get_stats(self):
        """Retorna estadísticas calculadas de la base de datos para las tarjetas del GUI"""
        users = self.repo.get_all()
        total = len(users)
        if total > 0:
            avg_age = round(sum(u.age for u in users if u.age) / total, 1)
        else:
            avg_age = 0.0
        return {
            "total_users": total,
            "avg_age": avg_age,
            "mailer_configured": bool(self.mailer.email_user and self.mailer.email_pass)
        }

    def search_users(self, query: str):
        """Busca usuarios filtrando por término"""
        return self.repo.search(query)

    def generar_pdf_manual(self):
        """Genera un PDF con el listado general actual y retorna la ruta"""
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        lista_actual = self.repo.get_all()
        str_lista = [f"ID: {u.id} | {u.name} {u.last_name} ({u.age} años)" for u in lista_actual]
        lineas = [f"Fecha de consulta: {ahora}", f"Total usuarios: {len(lista_actual)}", "--- LISTADO DE USUARIOS ---"] + str_lista
        return crear_pdf("REPORTE GENERAL DE USUARIOS", lineas)

    def enviar_email_manual(self, destinatario=None, archivo_pdf=None):
        """Envía el PDF especificado o uno nuevo generado al destinatario"""
        target_email = destinatario or self.admin_email
        pdf_path = archivo_pdf or self.generar_pdf_manual()
        exito = self.mailer.enviar_reporte(target_email, pdf_path)
        return exito, pdf_path

    def ejecutar_y_notificar(self, accion, send_email=True, **kwargs):
        """
        Método principal que decide qué acción ejecutar en la DB 
        y qué información incluir en el reporte PDF.
        """
        lineas_reporte = []
        titulo = ""
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        res = None

        try:
            # Capturamos el estado de la lista ANTES de cualquier cambio para el reporte
            lista_actual = self.repo.get_all()
            str_lista = [f"ID: {u.id} - {u.name} {u.last_name} ({u.age} años)" for u in lista_actual]

            # --- Lógica de Negocio según la acción solicitada ---

            if accion == "list":
                res = lista_actual
                titulo = "REPORTE DE LISTADO GENERAL"
                lineas_reporte = [f"Fecha de consulta: {ahora}", "--- USUARIOS EN SISTEMA ---"] + str_lista

            elif accion == "add":
                # Agrega un usuario y prepara el reporte de bienvenida
                res = self.repo.add(kwargs.get('name'), kwargs.get('last_name'), kwargs.get('age'))
                titulo = "REPORTE DE NUEVO REGISTRO"
                lineas_reporte = [f"Fecha: {ahora}", f"Agregado: {res.name} {res.last_name} ({res.age} años)"]

            elif accion == "delete":
                u_id = kwargs.get('id')
                user_obj = self.repo.get_by_id(u_id) # Buscamos datos antes de borrar
                if not user_obj: return None
                
                datos_borrado = f"{user_obj.name} {user_obj.last_name} ({user_obj.age} años)"
                res = self.repo.delete(u_id)
                
                titulo = "REPORTE DE ELIMINACIÓN"
                lineas_reporte = [f"Hora: {ahora}", "--- LISTA ANTERIOR ---"] + str_lista + ["", f"ELIMINADO: {datos_borrado}"]

            elif accion == "update":
                u_id = kwargs.get('id')
                user_obj = self.repo.get_by_id(u_id)
                if not user_obj: return None
                
                # Congelamos datos actuales para comparar en el "ANTES" del reporte
                datos_antes = f"{user_obj.name} {user_obj.last_name} ({user_obj.age} años)"
                f_previa = user_obj.updated_at.strftime("%d/%m/%Y %H:%M") if user_obj.updated_at else "Sin cambios previos"
                
                # Ejecutamos el cambio en la base de datos
                res = self.repo.update(u_id, kwargs.get('name'), kwargs.get('last_name'), kwargs.get('age'))
                
                titulo = "REPORTE DE MODIFICACIÓN"
                lineas_reporte = [
                    f"Fecha Actual: {ahora}", 
                    f"Fecha Previa: {f_previa}", 
                    "", 
                    f"ANTES: {datos_antes}", 
                    f"DESPUÉS: {res.name} {res.last_name} ({res.age} años)"
                ]

            # --- Generación de Notificaciones Automáticas ---
            if res and send_email:
                if accion != "list" and accion != "add":
                    lista_final = self.repo.get_all()
                    str_final = [f"ID: {u.id} - {u.name} {u.last_name} ({u.age} años)" for u in lista_final]
                    lineas_reporte += ["", "--- LISTA ACTUALIZADA ---"] + str_final
                
                print(f"[PDF] Generando PDF y enviando reporte: {titulo}")
                archivo = crear_pdf(titulo, lineas_reporte)
                self.mailer.enviar_reporte(self.admin_email, archivo)
            
            return res

        except Exception as e:
            print(f"[!] Error en el servicio: {e}")
            return None

