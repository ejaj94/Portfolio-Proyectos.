# delete_user.py
from database import SessionLocal
from services import UserActionService # <--- Importamos el "Gerente"

def run():
    db = SessionLocal()
    # Creamos al gerente y le damos la conexión a la DB
    servicio = UserActionService(db)

    print("--- ELIMINAR Y NOTIFICAR POR EMAIL ---")
    try:
        user_id = int(input("ID del usuario a eliminar: "))
        
        # En una sola línea: Borra de la DB + Crea PDF + Envía Email
        exito = servicio.ejecutar_y_notificar("delete", id=user_id)
        
        if exito:
            print("✅ El proceso completo (borrado y reporte) terminó con éxito.")
        else:
            print("❌ El usuario no existía, no se envió reporte.")
            
    except ValueError:
        print("❌ Error: ID no válido.")
    finally:
        db.close()

if __name__ == "__main__":
    run()
