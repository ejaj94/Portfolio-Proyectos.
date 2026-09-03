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

# Initial Supercar Workshop Mock Database
veiculos_db = [
    {"id": "VEH-901", "matricula": "99-ZZ-88", "vin": "ZFF83CFA00025419", "marca_modelo": "Ferrari F8 Tributo V8 Turbo", "potencia": "720 cv", "proprietario": "Carlos Vasconcelos", "contacto": "+351 912 887 766"},
    {"id": "VEH-902", "matricula": "11-AA-99", "vin": "WP0ZZZ99ZLS29811", "marca_modelo": "Porsche 911 GT3 RS (992)", "potencia": "525 cv", "proprietario": "Gonçalo Mendonça", "contacto": "+351 965 112 233"},
    {"id": "VEH-903", "matricula": "55-HH-44", "vin": "HW1123884992011", "marca_modelo": "Lamborghini Huracán EVO V10", "potencia": "640 cv", "proprietario": "Alexandre Fontes", "contacto": "+351 931 445 566"},
    {"id": "VEH-904", "matricula": "77-XX-22", "vin": "SBM11AAR80019288", "marca_modelo": "McLaren 720S Spider Performance", "potencia": "720 cv", "proprietario": "Sofia Carvalhal", "contacto": "+351 918 776 554"},
    {"id": "VEH-905", "matricula": "33-BB-11", "vin": "SCFBDCCW8MG001928", "marca_modelo": "Aston Martin DBS Superleggera V12", "potencia": "725 cv", "proprietario": "Dr. Fernando Siqueira", "contacto": "+351 922 889 900"},
    {"id": "VEH-906", "matricula": "88-MM-55", "vin": "WBS83AY0005519283", "marca_modelo": "BMW M4 CSL Track Edition", "potencia": "550 cv", "proprietario": "Ricardo Santos", "contacto": "+351 912 345 678"},
    {"id": "VEH-907", "matricula": "44-CC-66", "vin": "WDD1903791A009821", "marca_modelo": "Mercedes-AMG GT Black Series", "potencia": "730 cv", "proprietario": "Beatriz Vasconcelos", "contacto": "+351 965 432 109"},
    {"id": "VEH-908", "matricula": "22-DD-11", "vin": "WAUZZZ4S0G0019281", "marca_modelo": "Audi R8 V10 Performance quattro", "potencia": "620 cv", "proprietario": "Tiago Carvalhal", "contacto": "+351 931 112 233"}
]

ordens_servico_db = [
    {
        "id": "OS-2026/101",
        "matricula": "99-ZZ-88",
        "vin": "ZFF83CFA00025419",
        "veiculo": "Ferrari F8 Tributo V8 Turbo",
        "cliente": "Carlos Vasconcelos",
        "mecanico_chefe": "Mestre Miguel Silva (Tuning Spec)",
        "servico": "Manutenção Periódica 10.000km + Sistema de Escape Titanium Capristo",
        "estagio": "manutencao",      # diagnostico, manutencao, dyno, pronto
        "orcamento": 14850.00,
        "data_entrada": "2026-09-01",
        "previsao_entrega": "2026-09-05",
        "diagnostico_notas": "Pressão de turbo otimizada. Substituição de travões de cerâmica Brembo."
    },
    {
        "id": "OS-2026/102",
        "matricula": "11-AA-99",
        "vin": "WP0ZZZ99ZLS29811",
        "veiculo": "Porsche 911 GT3 RS (992)",
        "cliente": "Gonçalo Mendonça",
        "mecanico_chefe": "Mestre Pedro Alvo (Porsche Motorsport)",
        "servico": "Ensaio em Bancada Dyno & Afinação de Geometria de Suspensão Track Day",
        "estagio": "dyno",
        "orcamento": 6500.00,
        "data_entrada": "2026-09-02",
        "previsao_entrega": "2026-09-04",
        "diagnostico_notas": "Mapeamento ECU Stage 2 concluído. 548 cv medidos em banco."
    },
    {
        "id": "OS-2026/103",
        "matricula": "55-HH-44",
        "vin": "HW1123884992011",
        "veiculo": "Lamborghini Huracán EVO V10",
        "cliente": "Alexandre Fontes",
        "mecanico_chefe": "Mestre Miguel Silva (Tuning Spec)",
        "servico": "Revisão Geral de Transmissão Dupla Embraiagem + Detalhamento Cerâmico",
        "estagio": "pronto",
        "orcamento": 9200.00,
        "data_entrada": "2026-08-28",
        "previsao_entrega": "2026-09-03",
        "diagnostico_notas": "Veículo testado e aprovado. Pronto para entrega com certificação."
    },
    {
        "id": "OS-2026/104",
        "matricula": "77-XX-22",
        "vin": "SBM11AAR80019288",
        "veiculo": "McLaren 720S Spider Performance",
        "cliente": "Sofia Carvalhal",
        "mecanico_chefe": "Mestre Hugo Rocha (ECU Remap Spec)",
        "servico": "Diagnóstico Telemétrico de Suspensão Proactive Chassis Control II & Mapeamento Stage 1",
        "estagio": "diagnostico",
        "orcamento": 11500.00,
        "data_entrada": "2026-09-03",
        "previsao_entrega": "2026-09-08",
        "diagnostico_notas": "Análise de telemetria completa. Calibração de sensores de pressão de óleo."
    },
    {
        "id": "OS-2026/105",
        "matricula": "33-BB-11",
        "vin": "SCFBDCCW8MG001928",
        "veiculo": "Aston Martin DBS Superleggera V12",
        "cliente": "Dr. Fernando Siqueira",
        "mecanico_chefe": "Mestre Miguel Silva (Tuning Spec)",
        "servico": "Instalação de Kit Aerodinâmico Carbon Spec & Linha de Escape Akrapovič Titanium",
        "estagio": "manutencao",
        "orcamento": 18200.00,
        "data_entrada": "2026-09-02",
        "previsao_entrega": "2026-09-07",
        "diagnostico_notas": "Montagem de difusor traseiro e ponteiras em fibra de carbono concluída."
    },
    {
        "id": "OS-2026/106",
        "matricula": "88-MM-55",
        "vin": "WBS83AY0005519283",
        "veiculo": "BMW M4 CSL Track Edition",
        "cliente": "Ricardo Santos",
        "mecanico_chefe": "Mestre Pedro Alvo (Porsche Motorsport)",
        "servico": "Calibração de Suspensão KW Competition & Teste Dyno 4x4",
        "estagio": "dyno",
        "orcamento": 7800.00,
        "data_entrada": "2026-09-02",
        "previsao_entrega": "2026-09-06",
        "diagnostico_notas": "Testes de telemetria em banco a 280 km/h concluídos com sucesso."
    },
    {
        "id": "OS-2026/107",
        "matricula": "44-CC-66",
        "vin": "WDD1903791A009821",
        "veiculo": "Mercedes-AMG GT Black Series",
        "cliente": "Beatriz Vasconcelos",
        "mecanico_chefe": "Mestre Hugo Rocha (ECU Remap Spec)",
        "servico": "Substituição de Discos de Cerâmica AMG Carbon & Teste de Aerodinâmica Ativa",
        "estagio": "diagnostico",
        "orcamento": 21500.00,
        "data_entrada": "2026-09-03",
        "previsao_entrega": "2026-09-09",
        "diagnostico_notas": "Inspeção inicial de travagem e alinhamento de asa traseira ajustável."
    },
    {
        "id": "OS-2026/108",
        "matricula": "22-DD-11",
        "vin": "WAUZZZ4S0G0019281",
        "veiculo": "Audi R8 V10 Performance quattro",
        "cliente": "Tiago Carvalhal",
        "mecanico_chefe": "Mestre Miguel Silva (Tuning Spec)",
        "servico": "Revisão Anual de Motor V10 5.2 FSI & Proteção Paint Protection Film (PPF)",
        "estagio": "pronto",
        "orcamento": 8400.00,
        "data_entrada": "2026-08-29",
        "previsao_entrega": "2026-09-03",
        "diagnostico_notas": "Aplicação de cerâmica PPF concluída. Pronta para levantamento pelo cliente."
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/ordens", methods=["GET"])
def get_ordens():
    return jsonify(ordens_servico_db)

@app.route("/api/veiculos", methods=["GET"])
def get_veiculos():
    return jsonify(veiculos_db)

@app.route("/api/ordens/criar", methods=["POST"])
def criar_ordem():
    data = request.json or {}
    new_id = f"OS-2026/{100 + len(ordens_servico_db) + 1}"
    
    nova_os = {
        "id": new_id,
        "matricula": data.get("matricula", "00-AA-00"),
        "vin": data.get("vin", "VIN-0000000000"),
        "veiculo": data.get("veiculo", "Supercar Exótico"),
        "cliente": data.get("cliente", "Cliente VIP"),
        "mecanico_chefe": data.get("mecanico_chefe", "Mestre Miguel Silva"),
        "servico": data.get("servico", "Manutenção Geral de Alta Performance"),
        "estagio": "diagnostico",
        "orcamento": float(data.get("orcamento", 5000.0)),
        "data_entrada": datetime.now().strftime("%Y-%m-%d"),
        "previsao_entrega": data.get("previsao_entrega", "2026-09-10"),
        "diagnostico_notas": data.get("diagnostico_notas", "Diagnóstico telemétrico inicial.")
    }
    
    ordens_servico_db.insert(0, nova_os)
    return jsonify({"success": True, "ordem": nova_os})

@app.route("/api/ordens/avancar/<ordem_id>", methods=["POST"])
def avancar_estagio(ordem_id):
    estagios = ["diagnostico", "manutencao", "dyno", "pronto"]
    for os in ordens_servico_db:
        if os["id"] == ordem_id:
            curr_idx = estagios.index(os["estagio"]) if os["estagio"] in estagios else 0
            if curr_idx < len(estagios) - 1:
                next_stage = estagios[curr_idx + 1]
                os["estagio"] = next_stage
                return jsonify({"success": True, "ordem": os})
                
    return jsonify({"success": False, "message": "Ordem não encontrada"}), 404

@app.route("/api/stats", methods=["GET"])
def get_stats():
    total_faturacao = sum(os["orcamento"] for os in ordens_servico_db)
    em_reparacao = sum(1 for os in ordens_servico_db if os["estagio"] in ["diagnostico", "manutencao", "dyno"])
    concluidos = sum(1 for os in ordens_servico_db if os["estagio"] == "pronto")
    
    return jsonify({
        "total_faturacao": f"{total_faturacao:,.2f} €".replace(",", " ").replace(".", ","),
        "em_reparacao": em_reparacao,
        "concluidos": concluidos,
        "potencia_preparada": "5.210 cv"
    })

if __name__ == "__main__":
    print("Iniciando SISTEMA TALLER MECÁNICO ALTA PERFORMANCE SUPERCARS em http://localhost:5500")
    app.run(host="0.0.0.0", port=5500, debug=False)
