import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Strict anti-cache headers
@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Initial Veterinary Mock Database
mascotas_db = [
    {
        "id": "PET-101",
        "nome": "Thor",
        "especie": "Cão",
        "raca": "Golden Retriever",
        "idade": "3 anos",
        "peso": "31.5 kg",
        "microchip": "941000028919201",
        "tutor": "Ana Vasconcelos",
        "contacto": "+351 914 556 778",
        "foto": "https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=400&q=80",
        "ultima_consulta": "2026-08-28"
    },
    {
        "id": "PET-102",
        "nome": "Simba",
        "especie": "Gato",
        "raca": "Persa Branco",
        "idade": "2 anos",
        "peso": "4.2 kg",
        "microchip": "941000088192831",
        "tutor": "Gonçalo Mendonça",
        "contacto": "+351 962 114 889",
        "foto": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=400&q=80",
        "ultima_consulta": "2026-09-01"
    },
    {
        "id": "PET-103",
        "nome": "Luna",
        "especie": "Cão",
        "raca": "French Bulldog",
        "idade": "1 ano",
        "peso": "11.0 kg",
        "microchip": "941000077162541",
        "tutor": "Carolina Fonseca",
        "contacto": "+351 933 778 990",
        "foto": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?auto=format&fit=crop&w=400&q=80",
        "ultima_consulta": "2026-09-02"
    },
    {
        "id": "PET-104",
        "nome": "Kiwi",
        "especie": "Exótico",
        "raca": "Papagaio-Cinzento",
        "idade": "4 anos",
        "peso": "0.5 kg",
        "microchip": "941000055443322",
        "tutor": "Dr. Manuel Santos",
        "contacto": "+351 919 443 221",
        "foto": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?auto=format&fit=crop&w=400&q=80",
        "ultima_consulta": "2026-08-15"
    }
]

citas_db = [
    {
        "id": "CIT-501",
        "mascota": "Thor (Golden Retriever)",
        "tutor": "Ana Vasconcelos",
        "veterinario": "Dra. Maria Luz (Clínica Geral)",
        "motivo": "Check-up Anual & Vacina Rábica",
        "data": "2026-09-04",
        "hora": "10:30",
        "estado": "Confirmada"
    },
    {
        "id": "CIT-502",
        "mascota": "Simba (Gato Persa)",
        "tutor": "Gonçalo Mendonça",
        "veterinario": "Dr. Pedro Alves (Felinologia)",
        "motivo": "Limpeza Dentária e Desparasitação",
        "data": "2026-09-04",
        "hora": "11:45",
        "estado": "Em Espera"
    },
    {
        "id": "CIT-503",
        "mascota": "Luna (French Bulldog)",
        "tutor": "Carolina Fonseca",
        "veterinario": "Dra. Maria Luz (Clínica Geral)",
        "motivo": "Avaliação Dermatológica Alérgica",
        "data": "2026-09-03",
        "hora": "16:00",
        "estado": "Concluída"
    }
]

vacunas_db = [
    {
        "id": "VAC-801",
        "mascota": "Thor",
        "vacuna": "Rabisin (Vacina Rábica)",
        "data_aplicacao": "2025-09-05",
        "proxima_dose": "2026-09-05",
        "estado": "Reforço Próximo"
    },
    {
        "id": "VAC-802",
        "mascota": "Simba",
        "vacuna": "Felocell 4 (Polivalente Felina)",
        "data_aplicacao": "2026-03-10",
        "proxima_dose": "2027-03-10",
        "estado": "Em Dia"
    },
    {
        "id": "VAC-803",
        "mascota": "Luna",
        "vacuna": "Eurican DHPPi (Esgana/Parvovirose)",
        "data_aplicacao": "2026-02-14",
        "proxima_dose": "2027-02-14",
        "estado": "Em Dia"
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/mascotas", methods=["GET"])
def get_mascotas():
    return jsonify(mascotas_db)

@app.route("/api/mascotas/criar", methods=["POST"])
def criar_mascota():
    data = request.json or {}
    new_id = f"PET-{100 + len(mascotas_db) + 1}"
    
    # Default pet images by species
    especie = data.get("especie", "Cão")
    foto = "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=400&q=80"
    if especie == "Gato":
        foto = "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=400&q=80"
    elif especie == "Exótico":
        foto = "https://images.unsplash.com/photo-1552728089-57bdde30beb3?auto=format&fit=crop&w=400&q=80"
        
    nova_mascota = {
        "id": new_id,
        "nome": data.get("nome", "Novo Pet"),
        "especie": especie,
        "raca": data.get("raca", "Sem Raça Definida"),
        "idade": data.get("idade", "1 ano"),
        "peso": f"{data.get('peso', '5.0')} kg",
        "microchip": data.get("microchip", "941000000000000"),
        "tutor": data.get("tutor", "Tutor Registado"),
        "contacto": data.get("contacto", "+351 900 000 000"),
        "foto": foto,
        "ultima_consulta": datetime.now().strftime("%Y-%m-%d")
    }
    
    mascotas_db.insert(0, nova_mascota)
    return jsonify({"success": True, "mascota": nova_mascota})

@app.route("/api/citas", methods=["GET"])
def get_citas():
    return jsonify(citas_db)

@app.route("/api/citas/criar", methods=["POST"])
def criar_cita():
    data = request.json or {}
    new_id = f"CIT-{500 + len(citas_db) + 1}"
    
    nova_cita = {
        "id": new_id,
        "mascota": data.get("mascota", "Thor"),
        "tutor": data.get("tutor", "Ana Vasconcelos"),
        "veterinario": data.get("veterinario", "Dra. Maria Luz"),
        "motivo": data.get("motivo", "Consulta Geral"),
        "data": data.get("data", datetime.now().strftime("%Y-%m-%d")),
        "hora": data.get("hora", "14:00"),
        "estado": "Confirmada"
    }
    
    citas_db.insert(0, nova_cita)
    return jsonify({"success": True, "cita": nova_cita})

@app.route("/api/vacunas", methods=["GET"])
def get_vacunas():
    return jsonify(vacunas_db)

@app.route("/api/stats", methods=["GET"])
def get_stats():
    total_pacientes = len(mascotas_db)
    consultas_hoje = len(citas_db)
    vacunas_pendentes = sum(1 for v in vacunas_db if v["estado"] == "Reforço Próximo")
    tutores_ativos = len(set(m["tutor"] for m in mascotas_db))
    
    return jsonify({
        "total_pacientes": total_pacientes,
        "consultas_hoje": consultas_hoje,
        "vacunas_pendentes": vacunas_pendentes,
        "tutores_ativos": tutores_ativos
    })

if __name__ == "__main__":
    print("Iniciando SISTEMA GESTÃO CLÍNICA VETERINÁRIA SAAS em http://localhost:5600")
    app.run(host="0.0.0.0", port=5600, debug=False)
