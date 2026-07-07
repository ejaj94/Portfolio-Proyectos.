# update_user.py
from database import SessionLocal
from services import UserActionService # <--- Usamos el Servicio Coordinador

def run():
    db = SessionLocal()
    # Usamos el servicio para que se encargue de la DB + PDF + Email
    servicio = UserActionService(db)

    print("\n" + "="*30)
    print("   MODIFICAR Y NOTIFICAR")
    print("="*30)

    try:
        user_id = int(input("Ingrese el ID del usuario a modificar: "))
        
        # Consultamos la lista para mostrar los datos actuales
        usuarios = servicio.repo.get_all() 
        user = next((u for u in usuarios if u.id == user_id), None)

        if not user:
            print(f"❌ Error: El usuario con ID {user_id} no existe.")
            return

        print(f"\nDatos actuales: {user.name} {user.last_name}, {user.age} años.")
        print("--- (Presione Enter para mantener el valor actual) ---")

        nuevo_nombre = input(f"Nuevo nombre [{user.name}]: ") or None
        nuevo_apellido = input(f"Nuevo apellido [{user.last_name}]: ") or None
        nueva_edad_str = input(f"Nueva edad [{user.age}]: ")
        nueva_edad = int(nueva_edad_str) if nueva_edad_str else None

        # 🚀 LA MAGIA: El servicio ahora hace el update Y envía el email
        user_actualizado = servicio.ejecutar_y_notificar(
            "update", 
            id=user_id, 
            name=nuevo_nombre, 
            last_name=nuevo_apellido, 
            age=nueva_edad
        )

        if user_actualizado:
            print(f"\n✅ ¡Cambios guardados y reporte enviado por email!")
        else:
            print("\n❌ No se pudieron aplicar los cambios.")

    except ValueError:
        print("❌ Error: La edad y el ID deben ser números.")
    finally:
        db.close()

if __name__ == "__main__":
    run()
