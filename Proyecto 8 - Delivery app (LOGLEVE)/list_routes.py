import click
from flask import Flask

def register_commands(app: Flask):
    """Registra comandos personalizados en la CLI de Flask."""
    
    @app.cli.command("routes")
    def list_routes():
        """Muestra todas las rutas registradas en la aplicación de forma ordenada."""
        output = []
        for rule in app.url_map.iter_rules():
            options = {}
            for arg in rule.arguments:
                options[arg] = f"<{arg}>"
                
            methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
            url = str(rule)
            line = f"{rule.endpoint:50} {methods:20} {url}"
            output.append(line)
            
        print("\n=== MAPA DE RUTAS REGISTRADAS EN EL SERVIDOR ===")
        for line in sorted(output):
            print(line)
        print("================================================\n")
