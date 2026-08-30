import psutil
import time
import math
from datetime import datetime


class SentinelEngine:
    def __init__(self):
        self.boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

    def _clean_val(self, val):
        if val is None:
            return 0.0
        try:
            f = float(val)
            return 0.0 if math.isnan(f) else f
        except (ValueError, TypeError):
            return 0.0

    def get_system_stats(self):
        """Obtiene métricas globales de CPU, RAM, Disco y Red."""
        cpu_pct = psutil.cpu_percent(interval=None)
        cpu_cores = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        cpu_mhz = round(cpu_freq.current, 0) if cpu_freq else 0

        # RAM
        ram = psutil.virtual_memory()
        ram_total_gb = round(ram.total / (1024 ** 3), 2)
        ram_used_gb = round(ram.used / (1024 ** 3), 2)
        ram_pct = ram.percent

        # Disco C:
        try:
            disk = psutil.disk_usage('C:\\')
            disk_total_gb = round(disk.total / (1024 ** 3), 2)
            disk_used_gb = round(disk.used / (1024 ** 3), 2)
            disk_pct = disk.percent
        except Exception:
            disk_total_gb = 0.0
            disk_used_gb = 0.0
            disk_pct = 0.0

        # Red
        net_io = psutil.net_io_counters()
        bytes_sent_mb = round(net_io.bytes_sent / (1024 ** 2), 2)
        bytes_recv_mb = round(net_io.bytes_recv / (1024 ** 2), 2)

        return {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "boot_time": self.boot_time,
            "cpu": {
                "percent": cpu_pct,
                "cores": cpu_cores,
                "freq_mhz": cpu_mhz
            },
            "ram": {
                "percent": ram_pct,
                "used_gb": ram_used_gb,
                "total_gb": ram_total_gb
            },
            "disk": {
                "percent": disk_pct,
                "used_gb": disk_used_gb,
                "total_gb": disk_total_gb
            },
            "network": {
                "sent_mb": bytes_sent_mb,
                "recv_mb": bytes_recv_mb
            }
        }

    def get_process_list(self, limit=30, sort_by="memory"):
        """Obtiene una lista de procesos activos ordenada por consumo de RAM o CPU."""
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'status', 'memory_info', 'cpu_percent', 'username']):
            try:
                info = proc.info
                mem_bytes = info['memory_info'].rss if info['memory_info'] else 0
                mem_mb = round(mem_bytes / (1024 ** 2), 1)
                cpu = self._clean_val(info.get('cpu_percent'))

                processes.append({
                    "pid": info['pid'],
                    "name": info['name'] or "Desconocido",
                    "status": info['status'] or "running",
                    "memory_mb": mem_mb,
                    "cpu_pct": cpu,
                    "user": info.get('username') or "Sistema"
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Ordenar procesos
        if sort_by == "cpu":
            processes.sort(key=lambda x: x["cpu_pct"], reverse=True)
        else:
            processes.sort(key=lambda x: x["memory_mb"], reverse=True)

        return processes[:limit]

    def get_process_detail(self, pid):
        """Obtiene detalles avanzados de un proceso por PID."""
        try:
            proc = psutil.Process(pid)
            with proc.oneshot():
                name = proc.name()
                status = proc.status()
                cpu = proc.cpu_percent(interval=0.1)
                mem_mb = round(proc.memory_info().rss / (1024 ** 2), 2)
                create_time = datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S")
                exe = proc.exe() if hasattr(proc, 'exe') else "N/D"

            return {
                "success": True,
                "pid": pid,
                "name": name,
                "status": status,
                "cpu_pct": cpu,
                "memory_mb": mem_mb,
                "create_time": create_time,
                "exe_path": exe
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            return {"success": False, "message": f"No se pudo consultar el proceso {pid}: {str(e)}"}


if __name__ == "__main__":
    engine = SentinelEngine()
    print("=== TEST ENGINE SENTINEL NODE ===")
    print("STATS:", engine.get_system_stats())
    print("PROCESOS TOP 5:", engine.get_process_list(limit=5))
