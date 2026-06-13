# Paquete para la app app_entregador
from .blueprint import init_app

# Exponer la función directamente hacia la app principal
__all__ = ['init_app']
