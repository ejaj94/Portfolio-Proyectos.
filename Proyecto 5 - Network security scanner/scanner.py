#importamos nuestras bibliotecas:

from scapy.all import ARP, Ether, srp, conf, dev_from_index, get_if_hwaddr
import asyncio
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# CONFIGURACIÓN PARA WINDOWS: Forzamos el uso de tu tarjeta Realtek (Índice 7)
mi_interfaz = dev_from_index(7)
conf.iface = mi_interfaz
# Obtenemos tu dirección MAC real para que no use el Loopback por error
mi_mac = get_if_hwaddr(mi_interfaz)

#Creamos una peticion ARP para el rango:
def scan_network(ip_range):
    # Forzamos hwsrc con tu MAC real para evitar el ValueError en la capa ARP
    arp_request = ARP(pdst=ip_range, hwsrc=mi_mac)

#Creamos un frame para enviarlo por broadcast:
    # AGREGAMOS src=mi_mac aquí también para evitar que busque el Loopback en la capa Ethernet
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff", src=mi_mac)

#Combinamos los 2 paquetes:
    combined_packet = broadcast / arp_request

#En esta parte es que enviamos y recibimos respuestas ponemos un intervalo de 2 segundos para que no se sobrecargue y se quede colgado:
    # Capturamos solo la lista de respondidos [0]
    answered_list = srp(combined_packet, timeout=2, verbose=False, iface=mi_interfaz)[0]

    clients_list = []
    for sent, received in answered_list:
        client_dict = {"ip": received.psrc, "mac": received.hwsrc, "ports": []}
        clients_list.append(client_dict)

    return clients_list

#REvisamos un puerto:
async def check_port(ip, port):
    try:

#Abrimos conexion con 1 segundo de tiempo de espera si el resultado es positivo nos dara el puerto abierto sino el puerto estara cerrado:
        conn = asyncio.open_connection(ip, port)
        reader, writer = await asyncio.wait_for(conn, timeout=1.0)
        writer.close()
        await writer.wait_closed()
        return port
    except: 
        return None
    
#Ahora para hacerlo mas rapido cordinamos muchos puertos al mismo tiempo:
async def scan_ports_async(ip,port_list):

#Creamos una lista de taks o tareas para cada uno de los puertos:
    tasks = [check_port(ip, p) for p in port_list]

#Ejecutamos todas las tareas al mismo tiempo y esperamos ls resultados:
    results = await asyncio.gather(*tasks)

#Filtramos los puertos y devolvemos solo los que no fallaron:
    return [p for p in results if p is not None]

#Esta es la funcion para el PDF:
def generate_pdf_report(scan_data):
    filename = f"reporte_seguridad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Título del Reporte
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Informe de Seguridad de Red")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.line(50, height - 80, 550, height - 80)

    # Contenido
    y = height - 100
    for device in scan_data:
        if y < 100: # Crear nueva página si se acaba el espacio
            c.showPage()
            y = height - 50

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Dispositivo: {device['ip']}")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(70, y, f"MAC: {device['mac']}")
        y -= 15
        puertos = ", ".join(map(str, device['ports'])) if device['ports'] else "Ninguno"
        c.drawString(70, y, f"Puertos Abiertos: {puertos}")
        y -= 30
    
    c.save()
    print(f"\n[✔] Reporte guardado como: {filename}")

#Obtenemos los ips:
async def run_scanner():
    target_net = "10.29.219.0/24"
    print(f"[*] Buscando equipos en {target_net}...")
    devices = scan_network(target_net)

#Decimos que puertos queremos revisar:
    ports_to_check = [21, 22, 80, 443, 3389]

#Escanemos cada dispositivo encontrado:
    for device in devices:
        ip = device['ip']
        print(f"[*] Revisando puertos en {ip}...")
        open_found = await scan_ports_async(ip, ports_to_check)
        device['ports'] = open_found # Guardamos para el PDF
        print(f" Puertos abiertos: {open_found}")

    # Preguntamos si quiere el PDF
    if devices:
        opcion = input("\n¿Deseas descargar el reporte PDF? (s/n): ")
        if opcion.lower() == 's':
            generate_pdf_report(devices)
    else:
        print("[!] No se encontraron dispositivos activos.")

# Ejecutamos todo en Windows
if __name__ == "__main__":
    # IMPORTANTE: Ejecutar VS Code o la Terminal como ADMINISTRADOR
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_scanner())