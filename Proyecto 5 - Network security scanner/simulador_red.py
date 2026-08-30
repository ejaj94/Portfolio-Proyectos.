import time
import json
from datetime import datetime

# Dados estáticos de ativos de rede em Português de Portugal (pt-PT)
DEVICES_MOCK = [
    {
        "ip": "192.168.1.1",
        "mac": "00:1A:2B:3C:4D:5E",
        "hostname": "Router-Gateway-Principal",
        "type": "Router / Firewall",
        "status": "Ativo",
        "simulated_ports": [80, 443],
        "security_score": 95,
        "recommendation": "Firmware atualizado com sucesso."
    },
    {
        "ip": "192.168.1.10",
        "mac": "00:1A:2B:99:88:77",
        "hostname": "Servidor-NAS-Ficheiros",
        "type": "Armazenamento NAS",
        "status": "Ativo",
        "simulated_ports": [22, 80, 443, 445],
        "security_score": 82,
        "recommendation": "Rever permissões de pastas partilhadas SMB."
    },
    {
        "ip": "192.168.1.25",
        "mac": "00:1A:2B:11:22:33",
        "hostname": "Impressora-HP-Escritorio",
        "type": "Impressora de Rede",
        "status": "Ativo",
        "simulated_ports": [9100, 631],
        "security_score": 75,
        "recommendation": "Alterar palavra-passe por omissão do painel web."
    },
    {
        "ip": "192.168.1.50",
        "mac": "00:1A:2B:55:66:77",
        "hostname": "PC-Desenvolvimento-Win11",
        "type": "Estação de Trabalho",
        "status": "Ativo",
        "simulated_ports": [3389],
        "security_score": 90,
        "recommendation": "Manter RDP com autenticação a nível de rede (NLA)."
    },
    {
        "ip": "192.168.1.100",
        "mac": "00:1A:2B:AA:BB:CC",
        "hostname": "Camara-IP-Seguranca",
        "type": "Câmara IoT",
        "status": "Inativo",
        "simulated_ports": [],
        "security_score": 60,
        "recommendation": "Dispositivo fora de linha na última verificação."
    }
]


class NetworkSimulatorEngine:
    def __init__(self):
        self.devices = DEVICES_MOCK

    def run_simulated_scan(self, network_range="192.168.1.0/24"):
        """Gera dados de inventário para demonstração profissional em Português de Portugal."""
        time.sleep(0.5)

        total_devices = len(self.devices)
        active_devices = [d for d in self.devices if d["status"] == "Ativo"]
        avg_score = sum(d["security_score"] for d in active_devices) / max(len(active_devices), 1)

        return {
            "success": True,
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
    print("=== MONITOR DE INVENTÁRIO DE REDE PRO (PT-PT) ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
