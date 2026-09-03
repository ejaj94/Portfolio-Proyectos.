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

# Initial Veterinary Mock Database (12 Full Pet Patients)
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
        "foto": "https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=600&q=80",
        "diagnostico_servico": "Diagnóstico: Otite Externa Biliar Ligeira • Serviço: Limpeza Auricular & Antibiótico",
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
        "foto": "/static/images/simba_persa.jpg",
        "diagnostico_servico": "Serviço: Tartrectomia Dentária Ultrassónica & Desparasitação Interna",
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
        "foto": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?auto=format&fit=crop&w=600&q=80",
        "diagnostico_servico": "Diagnóstico: Dermatite Atópica Canina • Serviço: Champôterapia & Hipoalergénico",
        "ultima_consulta": "2026-09-02"
    },
    {
        "id": "PET-104",
        "nome": "Kiwi",
        "especie": "Exótico",
        "raca": "Papagaio-Cinzento (Psittacus erithacus)",
        "idade": "4 anos",
        "peso": "0.48 kg",
        "microchip": "941000055443322",
        "tutor": "Dr. Manuel Santos",
        "contacto": "+351 919 443 221",
        "foto": "/static/images/kiwi_papagaio.jpg",
        "diagnostico_servico": "Serviço: Corte Pedicura de Unhas, Manutenção de Bico & Exame Parasitológico de Penas",
        "ultima_consulta": "2026-08-15"
    },
    {
        "id": "PET-105",
        "nome": "Rex",
        "especie": "Cão",
        "raca": "Pastor Alemão",
        "idade": "5 anos",
        "peso": "38.0 kg",
        "microchip": "941000099881122",
        "tutor": "Ricardo Alvares",
        "contacto": "+351 912 345 678",
        "foto": "https://images.unsplash.com/photo-1589941013453-ec89f33b5e95?auto=format&fit=crop&w=600&q=80",
        "diagnostico_servico": "Diagnóstico: Displasia Coxofemoral Grau I • Serviço: Fisioterapia & Condroprotetores",
        "ultima_consulta": "2026-09-02"
    },
    {
        "id": "PET-106",
        "nome": "Mimi",
        "especie": "Gato",
        "raca": "Siamês Tradicional",
        "idade": "3 anos",
        "peso": "3.8 kg",
        "microchip": "941000044556677",
        "tutor": "Beatriz Lima",
        "contacto": "+351 965 432 109",
        "foto": "/static/images/mimi_siames.jpg",
        "diagnostico_servico": "Diagnóstico: Gastroenterite Ligeira • Serviço: Fluidoterapia & Dieta Gastrointestinal",
        "ultima_consulta": "2026-09-03"
    },
    {
        "id": "PET-107",
        "nome": "Barnabé",
        "especie": "Exótico",
        "raca": "Coelho Holland Lop",
        "idade": "1 ano",
        "peso": "1.8 kg",
        "microchip": "941000033221100",
        "tutor": "Sofia Carvalhal",
        "contacto": "+351 931 112 233",
        "foto": "/static/images/barnabe_coelho.jpg",
        "diagnostico_servico": "Serviço: Desgaste Dentário Preventivo, Vacinação Mixomatose & Suplementação Feno",
        "ultima_consulta": "2026-08-30"
    },
    {
        "id": "PET-108",
        "nome": "Oliver",
        "especie": "Gato",
        "raca": "Maine Coon",
        "idade": "4 anos",
        "peso": "8.5 kg",
        "microchip": "941000066778899",
        "tutor": "Tiago Carvalhal",
        "contacto": "+351 918 776 554",
        "foto": "/static/images/oliver_mainecoon.jpg",
        "diagnostico_servico": "Serviço: Ecocardiograma Preventivo & Reforço de Vacina Leucemia Felina (FeLV)",
        "ultima_consulta": "2026-09-01"
    },
    {
        "id": "PET-109",
        "nome": "Bella",
        "especie": "Cão",
        "raca": "Beagle Tricolor",
        "idade": "2 anos",
        "peso": "13.2 kg",
        "microchip": "941000011223344",
        "tutor": "Fernanda Torres",
        "contacto": "+351 922 113 355",
        "foto": "/static/images/bella_beagle.jpg",
        "diagnostico_servico": "Diagnóstico: Conjuntivite Alérgica • Serviço: Gotas Oftálmicas & Limpeza Ocular",
        "ultima_consulta": "2026-09-03"
    },
    {
        "id": "PET-110",
        "nome": "Tobias",
        "especie": "Exótico",
        "raca": "Tartaruga Terrestre Russa",
        "idade": "8 anos",
        "peso": "1.2 kg",
        "microchip": "941000088990011",
        "tutor": "Alexandre Fontes",
        "contacto": "+351 931 445 566",
        "foto": "/static/images/tobias_tartaruga.jpg",
        "diagnostico_servico": "Serviço: Check-up de Carapaça, Calcinose Preventiva & Desparasitação de Réptil",
        "ultima_consulta": "2026-08-20"
    },
    {
        "id": "PET-111",
        "nome": "Nina",
        "especie": "Exótico",
        "raca": "Chinchila Cinzenta",
        "idade": "2 anos",
        "peso": "0.6 kg",
        "microchip": "941000077889900",
        "tutor": "Clara Medeiros",
        "contacto": "+351 915 667 788",
        "foto": "/static/images/nina_chinchila.jpg",
        "diagnostico_servico": "Serviço: Inspeção de Dentes Incisivos & Avaliação de Banho de Areia Vulcânica",
        "ultima_consulta": "2026-08-25"
    },
    {
        "id": "PET-112",
        "nome": "Max",
        "especie": "Cão",
        "raca": "Labrador Chocolate",
        "idade": "4 anos",
        "peso": "34.0 kg",
        "microchip": "941000055667788",
        "tutor": "Dr. Fernando Siqueira",
        "contacto": "+351 922 889 900",
        "foto": "/static/images/max_labrador.jpg",
        "diagnostico_servico": "Serviço: Vacina Antirrábica Anual, Desparasitação & Corte de Unhas Canino",
        "ultima_consulta": "2026-09-02"
    }
]

citas_db = [
    {
        "id": "CIT-501",
        "mascota": "Thor (Golden Retriever)",
        "tutor": "Ana Vasconcelos",
        "veterinario": "Dra. Maria Luz (Clínica Geral)",
        "motivo": "Check-up Anual & Vacina Rábica",
        "diagnostico_previsto": "Limpeza Auricular & Vacinação",
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
        "diagnostico_previsto": "Tartrectomia Ultrassónica",
        "data": "2026-09-04",
        "hora": "11:45",
        "estado": "Em Espera"
    },
    {
        "id": "CIT-503",
        "mascota": "Kiwi (Papagaio-Cinzento)",
        "tutor": "Dr. Manuel Santos",
        "veterinario": "Dr. Hugo Rocha (Animais Exóticos)",
        "motivo": "Corte de Unhas & Exame de Penas",
        "diagnostico_previsto": "Check-up Aviário & Pedicura",
        "data": "2026-09-04",
        "hora": "15:00",
        "estado": "Confirmada"
    },
    {
        "id": "CIT-504",
        "mascota": "Rex (Pastor Alemão)",
        "tutor": "Ricardo Alvares",
        "veterinario": "Dra. Maria Luz (Ortopedia)",
        "motivo": "Sessão de Fisioterapia Coxofemoral",
        "diagnostico_previsto": "Reabilitação Articular",
        "data": "2026-09-05",
        "hora": "09:30",
        "estado": "Confirmada"
    },
    {
        "id": "CIT-505",
        "mascota": "Mimi (Gato Siamês)",
        "tutor": "Beatriz Lima",
        "veterinario": "Dr. Pedro Alves (Felinologia)",
        "motivo": "Revisão Gastroenterite & Nutrição",
        "diagnostico_previsto": "Ecografia Abdominal",
        "data": "2026-09-05",
        "hora": "14:15",
        "estado": "Em Espera"
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
        "mascota": "Kiwi",
        "vacuna": "Suplementação & Vitaminas Penas",
        "data_aplicacao": "2026-06-01",
        "proxima_dose": "2026-12-01",
        "estado": "Em Dia"
    },
    {
        "id": "VAC-804",
        "mascota": "Rex",
        "vacuna": "Eurican DHPPi (Esgana/Parvovirose)",
        "data_aplicacao": "2026-01-20",
        "proxima_dose": "2027-01-20",
        "estado": "Em Dia"
    },
    {
        "id": "VAC-805",
        "mascota": "Barnabé",
        "vacuna": "Nobivac Myxo-RHD (Mixomatose Coelho)",
        "data_aplicacao": "2026-04-15",
        "proxima_dose": "2027-04-15",
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
    
    especie = data.get("especie", "Cão")
    foto = "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=600&q=80"
    if especie == "Gato":
        foto = "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=600&q=80"
    elif especie == "Exótico":
        foto = "https://images.unsplash.com/photo-1522926193341-e9ffd686c60f?auto=format&fit=crop&w=600&q=80"
        
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
        "diagnostico_servico": data.get("diagnostico_servico", "Serviço: Check-up Clínico Geral & Desparasitação"),
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
        "diagnostico_previsto": data.get("diagnostico_previsto", "Avaliação Médica"),
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
    print("Iniciando SISTEMA GESTÃO CLÍNICA VETERINÁRIA SAAS em http://localhost:5650")
    app.run(host="0.0.0.0", port=5650, debug=False)
