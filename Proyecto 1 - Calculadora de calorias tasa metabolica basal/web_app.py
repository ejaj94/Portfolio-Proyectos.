import sys
from flask import Flask, render_template, request, jsonify
from Calculos import calcular_tmb, calcular_calorias_totales

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/calcular", methods=["POST"])
def api_calcular():
    try:
        data = request.get_json() or {}

        nombre = str(data.get("nombre", "")).strip()
        peso = float(data.get("peso", 0))
        altura = float(data.get("altura", 0))
        edad = int(data.get("edad", 0))
        genero = str(data.get("genero", "Hombre")).strip()
        actividad = str(data.get("actividad", "Sedentario")).strip()

        if peso <= 0 or altura <= 0 or edad <= 0:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Peso, altura y edad deben ser valores numéricos mayores a 0.",
                    }
                ),
                400,
            )

        resultado_tmb = calcular_tmb(peso, altura, edad, genero)
        total_calorias = calcular_calorias_totales(resultado_tmb, actividad)

        return jsonify(
            {
                "success": True,
                "nombre": nombre if nombre else "Usuario",
                "tmb": round(resultado_tmb, 2),
                "mantenimiento": round(total_calorias, 2),
                "superavit": round(total_calorias + 300, 2),
                "deficit": round(total_calorias - 300, 2),
            }
        )

    except (ValueError, TypeError) as e:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Entrada de datos inválida. Asegúrate de ingresar números para peso, altura y edad.",
                }
            ),
            400,
        )


def main(host="127.0.0.1", port=5000, debug=False):
    print(f"\n[OK] Servidor Web iniciado en http://{host}:{port}")
    print("Abre esa direccion en tu navegador para usar la aplicacion.\n")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main(debug=False)
