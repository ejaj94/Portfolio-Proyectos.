import time
import json
import random
from datetime import datetime

# Datos estáticos de demostración 100% ficticios
DEVICES_MOCK = [
    {
        "ip": "192.168.1.1",
        "mac": "00:1A:2B:3C:4D:5E",
        "hostname": "Router-Gateway-Demo",
        "type": "Router / Firewall",
        "status": "Activo",
        "simulated_ports": [80, 443],
        "security_score": 95,
        "recommendation": "Firmware actualizado correctamente."
    },
    {
        "ip": "192.168.1.10",
        "mac": "00:1A:2B:99:88:77",
        "hostname": "NAS-Servidor-Archivos",
        "type": "Almacenamiento NAS",
        "status": "Activo",
        "simulated_ports": [22, 80, 443, 445],
        "security_score": 82,
        "recommendation": "Revisar permisos de carpetas compartidas SMB."
    },
    {
        "ip": "192.168.1.25",
        "mac": "00:1A:2B:11:22:33",
        "hostname": "Impresora-HP-Oficina",
        "type": "Impresora de Red",
        "status": "Activo",
        "simulated_ports": [9100, 631],
        "security_score": 75,
        "recommendation": "Cambiar contraseña por defecto del panel web."
    },
    {
        "ip": "192.168.1.50",
        "mac": "00:1A:2B:55:66:77",
        "hostname": "PC-Desarrollo-Win11",
        "type": "Estación de Trabajo",
        "status": "Activo",
        "simulated_ports": [3389],
        "security_score": 90,
        "recommendation": "Mantener RDP con autenticación a nivel de red (NLA)."
    },
    {
        "ip": "192.168.1.100",
        "mac": "00:1A:2B:AA:BB:CC",
        "hostname": "Camara-IP-Seguridad",
        "type": "Cámara IoT",
        "status": "Inactivo (Simulado)",
        "simulated_ports": [],
        "security_score": 60,
        "recommendation": "Dispositivo fuera de línea en la última simulación."
    }
]


class NetworkSimulatorEngine:
    def __init__(self):
        self.devices = DEVICES_MOCK

    def run_simulated_scan(self, network_range="192.168.1.0/24"):
        """Simula una sesión de auditoría e inventario con retraso artificial didáctico."""
        time.sleep(1.0) # Simula el tiempo de procesamiento

        total_devices = len(self.devices)
        active_devices = [d for d in self.devices if d["status"] == "Activo"]
        avg_score = sum(d["security_score"] for d in active_devices) / max(len(active_devices), 1)

        return {
            "success": True,
            "simulated": True,
            "network_range": network_range,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_found": total_devices,
                "active_found": len(active_devices),
                "avg_security_score": round(avg_score, 1)
            },
            "devices": self.devices
        }


if __name__ == "__main__":
    engine = NetworkSimulatorEngine()
    result = engine.run_simulated_scan()
    print("=== SIMULADOR DE INVENTARIO DE RED DE MUESTRA ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
