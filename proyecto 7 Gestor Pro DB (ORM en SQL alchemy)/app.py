from database import SessionLocal, engine, Base
from user_repository import UserRepository 
from services import UserActionService

# Función para mostrar el menú visual en la terminal
def mostrar_menu():
    print("\n" + "="*40)
    print("   SISTEMA DE GESTIÓN PROFESIONAL")
    print("="*40)
    print("1. Registrar usuario")
    print("2. Listar usuarios (Generar Reporte)")
    print("3. Eliminar usuario")
    print("4. Modificar usuario")
    print("5. Salir")
    print("="*40)
    return input("Seleccione una opción: ")

# Interfaz para capturar datos de un nuevo usuario
def registrar_ui(service):
    print("\n[REGISTRAR USUARIO]")
    n = input("Nombre: ")
    a = input("Apellido: ")
    try:
        e = int(input("Edad: "))
        # Llama al servicio para guardar en DB, crear PDF y enviar Email
        service.ejecutar_y_notificar("add", name=n, last_name=a, age=e)
        print("✅ Usuario registrado con éxito.")
    except ValueError: 
        print("❌ Edad inválida.")

# Interfaz para mostrar el listado y disparar el reporte masivo
def listar_usuarios_ui(service):
    print("\n" + "="*30)
    print("   LISTADO Y REPORTE")
    print("="*30)
    # Solicita la acción 'list' al servicio para PDF y Email automático
    usuarios = service.ejecutar_y_notificar("list")
    
    if not usuarios:
        print("La base de datos está vacía.")
    else:
        for u in usuarios:
            print(f"ID: {u.id} | {u.name} {u.last_name} ({u.age} años)")
        print("\n✅ Reporte PDF generado y enviado por email.")

# Interfaz inteligente para modificar datos existentes
def modificar_ui(service):
    print("\n[MODIFICAR USUARIO]")
    try:
        id_u = int(input("ID a modificar: "))
        # Consultamos al repo a través del servicio para mostrar datos actuales
        user = service.repo.get_by_id(id_u)
        if not user:
            print("❌ ID no encontrado."); return

        print(f"\nActual: {user.name} {user.last_name} ({user.age} años)")
        print("--- Presione Enter para mantener el valor actual ---")
        
        # Lógica 'or None': si el input está vacío, la variable será None
        nuevo_n = input(f"Nuevo Nombre [{user.name}]: ").strip() or None
        nuevo_a = input(f"Nuevo Apellido [{user.last_name}]: ").strip() or None
        nueva_e_s = input(f"Nueva Edad [{user.age}]: ").strip()
        nueva_e = int(nueva_e_s) if nueva_e_s else None

        # El servicio procesará el reporte de "Antes y Después" automáticamente
        service.ejecutar_y_notificar("update", id=id_u, name=nuevo_n, last_name=nuevo_a, age=nueva_e)
        print("✅ Proceso de modificación completado.")
    except ValueError: 
        print("❌ Error: Use números válidos.")

# Interfaz para eliminación segura de registros
def eliminar_ui(service):
    print("\n[ELIMINAR USUARIO]")
    try:
        id_u = int(input("Ingrese el ID a eliminar: "))
        confirmar = input(f"¿Seguro que desea eliminar al ID {id_u}? (s/n): ")
        if confirmar.lower() == 's':
            # Al eliminar, el servicio también enviará el reporte de cómo quedó la lista
            res = service.ejecutar_y_notificar("delete", id=id_u)
            if res:
                print(f"✅ Usuario {id_u} eliminado y reporte enviado.")
            else:
                print("❌ No se pudo eliminar (ID inexistente).")
    except ValueError:
        print("❌ Error: Ingrese un ID numérico.")

# Punto de entrada principal de la aplicación
def main():
    # Asegura que las tablas se creen en MySQL según el modelo definido
    Base.metadata.create_all(bind=engine)
    
    # Creamos la sesión y el servicio coordinador
    db = SessionLocal()
    service = UserActionService(db)

    # Bucle principal de ejecución
    while True:
        op = mostrar_menu()
        if op == "1": 
            registrar_ui(service)
        elif op == "2": 
            listar_usuarios_ui(service)
        elif op == "3": 
            eliminar_ui(service)
        elif op == "4": 
            modificar_ui(service)
        elif op == "5": 
            print("Saliendo del sistema...")
            break
        else:
            print("⚠️ Opción no válida.")
            
    db.close() # Cierre de conexión al salir del programa

if __name__ == "__main__":
    main()
