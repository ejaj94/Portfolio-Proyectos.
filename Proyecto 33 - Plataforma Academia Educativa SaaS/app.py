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

# Initial Educational Mock Database (Expanded Disciplines)
carreras_db = [
    {
        "id": "CAR-01",
        "nome": "Engenharia de Software & Inteligência Artificial",
        "duracao": "3 Anos • 6 Semestres",
        "coordenador": "Prof. Dr. Alex Vance",
        "cursos_count": 18,
        "alunos_inscritos": 420,
        "taxa_empregabilidade": "98.4%",
        "descricao": "Formação avançada em arquitetura de sistemas distribuídos, algoritmos de deep learning e desenvolvimento full-stack."
    },
    {
        "id": "CAR-02",
        "nome": "Biologia Molecular, Biotecnologia & Genómica",
        "duracao": "4 Anos • 8 Semestres",
        "coordenador": "Dra. Beatriz Siqueira",
        "cursos_count": 22,
        "alunos_inscritos": 310,
        "taxa_empregabilidade": "97.1%",
        "descricao": "Estudo de bioinformática, edição genética CRISPR, sequenciamento de DNA e biotecnologia farmacêutica."
    },
    {
        "id": "CAR-03",
        "nome": "Engenharia Robótica & Mecatrónica Avançada",
        "duracao": "4 Anos • 8 Semestres",
        "coordenador": "Prof. Ing. Hugo Fonseca",
        "cursos_count": 20,
        "alunos_inscritos": 290,
        "taxa_empregabilidade": "99.0%",
        "descricao": "Desenvolvimento de robôs autónomos, sistemas de visão computacional e automação industrial IoT."
    },
    {
        "id": "CAR-04",
        "nome": "Engenharia Civil & Infraestruturas Sustentáveis",
        "duracao": "4 Anos • 8 Semestres",
        "coordenador": "Prof. Dr. Fernando Ramos",
        "cursos_count": 19,
        "alunos_inscritos": 275,
        "taxa_empregabilidade": "95.8%",
        "descricao": "Conceção de edifícios eco-eficientes, modelação BIM 3D, geotecnia e estruturas resilientes."
    },
    {
        "id": "CAR-05",
        "nome": "Linguística Computacional & Línguas Modernas",
        "duracao": "3 Anos • 6 Semestres",
        "coordenador": "Dra. Isabela Camargo",
        "cursos_count": 16,
        "alunos_inscritos": 210,
        "taxa_empregabilidade": "94.5%",
        "descricao": "Análise de modelos de tradução neural, sintaxe comparada de idiomas e desenvolvimento de motores de linguagem."
    },
    {
        "id": "CAR-06",
        "nome": "Sociologia Digital & Humanidades Digitais",
        "duracao": "3 Anos • 6 Semestres",
        "coordenador": "Prof. Gabriel Nogueira",
        "cursos_count": 15,
        "alunos_inscritos": 195,
        "taxa_empregabilidade": "93.2%",
        "descricao": "Análise sociológica do impacto das redes sociais, comportamento de comunidades digitais e demografia global."
    },
    {
        "id": "CAR-07",
        "nome": "Filosofia da Mente, Lógica & Ética da IA",
        "duracao": "3 Anos • 6 Semestres",
        "coordenador": "Dr. Marcus Aurelius Vane",
        "cursos_count": 14,
        "alunos_inscritos": 180,
        "taxa_empregabilidade": "92.0%",
        "descricao": "Investigação de dilemas éticos em sistemas autónomos, epistemologia contemporânea e filosofia da consciência."
    },
    {
        "id": "CAR-08",
        "nome": "Cybersecurity & Cloud Infrastructure",
        "duracao": "2.5 Anos • 5 Semestres",
        "coordenador": "Prof. Marcus Brody",
        "cursos_count": 15,
        "alunos_inscritos": 245,
        "taxa_empregabilidade": "99.1%",
        "descricao": "Proteção de redes corporativas, análise forense digital, arquitetura zero-trust e gestão de servidores AWS/Azure."
    }
]

cursos_db = [
    {
        "id": "CRS-101",
        "codigo": "CS-301",
        "titulo": "Arquitetura de Microserviços & Cloud Native",
        "carrera": "Engenharia de Software & IA",
        "professor": "Prof. Dr. Alex Vance",
        "modulos": 12,
        "duracao_horas": 80,
        "progresso_medio": 78,
        "alunos": 142,
        "classificacao": "4.95 ⭐"
    },
    {
        "id": "CRS-102",
        "codigo": "BIO-201",
        "titulo": "Genómica Computacional & Edição Genética CRISPR",
        "carrera": "Biologia Molecular & Biotecnologia",
        "professor": "Dra. Beatriz Siqueira",
        "modulos": 14,
        "duracao_horas": 90,
        "progresso_medio": 81,
        "alunos": 115,
        "classificacao": "4.97 ⭐"
    },
    {
        "id": "CRS-103",
        "codigo": "ROB-302",
        "titulo": "Robótica Móvel & Visão Computacional em Tempo Real",
        "carrera": "Engenharia Robótica & Mecatrónica",
        "professor": "Prof. Ing. Hugo Fonseca",
        "modulos": 15,
        "duracao_horas": 100,
        "progresso_medio": 73,
        "alunos": 108,
        "classificacao": "4.94 ⭐"
    },
    {
        "id": "CRS-104",
        "codigo": "CIV-104",
        "titulo": "Engenharia Estrutural & BIM (Building Info Modeling)",
        "carrera": "Engenharia Civil & Infraestruturas",
        "professor": "Prof. Dr. Fernando Ramos",
        "modulos": 11,
        "duracao_horas": 75,
        "progresso_medio": 84,
        "alunos": 98,
        "classificacao": "4.89 ⭐"
    },
    {
        "id": "CRS-105",
        "codigo": "LNG-105",
        "titulo": "Tradução Neural & Processamento Sintático Multilingue",
        "carrera": "Linguística Computacional & Línguas",
        "professor": "Dra. Isabela Camargo",
        "modulos": 10,
        "duracao_horas": 60,
        "progresso_medio": 88,
        "alunos": 85,
        "classificacao": "4.91 ⭐"
    },
    {
        "id": "CRS-106",
        "codigo": "SOC-202",
        "titulo": "Sociologia Algorítmica & Dinâmica de Redes Sociais",
        "carrera": "Sociologia Digital",
        "professor": "Prof. Gabriel Nogueira",
        "modulos": 9,
        "duracao_horas": 55,
        "progresso_medio": 86,
        "alunos": 92,
        "classificacao": "4.88 ⭐"
    },
    {
        "id": "CRS-107",
        "codigo": "PHI-301",
        "titulo": "Ética da Inteligência Artificial & Filosofia da Mente",
        "carrera": "Filosofia da Mente & Ética",
        "professor": "Dr. Marcus Aurelius Vane",
        "modulos": 12,
        "duracao_horas": 70,
        "progresso_medio": 90,
        "alunos": 95,
        "classificacao": "4.96 ⭐"
    },
    {
        "id": "CRS-108",
        "codigo": "SEC-401",
        "titulo": "Ethical Hacking & Testes de Penetração Zero-Trust",
        "carrera": "Cybersecurity & Cloud",
        "professor": "Prof. Marcus Brody",
        "modulos": 13,
        "duracao_horas": 90,
        "progresso_medio": 82,
        "alunos": 104,
        "classificacao": "4.96 ⭐"
    }
]

alunos_db = [
    {
        "id": "ALU-901",
        "nome": "Mariana Silva",
        "matricula": "20240182",
        "carrera": "Engenharia de Software & IA",
        "email": "mariana.silva@lumen.edu",
        "progresso_geral": 84,
        "media_gpa": "18.6 / 20",
        "estado": "Ativo",
        "foto": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": "ALU-902",
        "nome": "Diogo Fernandes",
        "matricula": "20240214",
        "carrera": "Biologia Molecular & Biotecnologia",
        "email": "diogo.fernandes@lumen.edu",
        "progresso_geral": 92,
        "media_gpa": "19.2 / 20",
        "estado": "Ativo",
        "foto": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": "ALU-903",
        "nome": "Beatriz Albuquerque",
        "matricula": "20240305",
        "carrera": "Filosofia da Mente & Ética",
        "email": "beatriz.albuquerque@lumen.edu",
        "progresso_geral": 76,
        "media_gpa": "17.8 / 20",
        "estado": "Ativo",
        "foto": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": "ALU-904",
        "nome": "Lucas Vasconcelos",
        "matricula": "20240412",
        "carrera": "Engenharia Robótica & Mecatrónica",
        "email": "lucas.vasconcelos@lumen.edu",
        "progresso_geral": 88,
        "media_gpa": "18.9 / 20",
        "estado": "Ativo",
        "foto": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": "ALU-905",
        "nome": "Camila Oliveira",
        "matricula": "20240590",
        "carrera": "Linguística Computacional",
        "email": "camila.oliveira@lumen.edu",
        "progresso_geral": 95,
        "media_gpa": "19.6 / 20",
        "estado": "Graduando",
        "foto": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=400&q=80"
    }
]

profesores_db = [
    {
        "id": "DOC-701",
        "nome": "Prof. Dr. Alex Vance",
        "titulo": "Doutor em Ciência da Computação (MIT)",
        "departamento": "Engenharia de Software",
        "cursos_lecionados": 4,
        "avaliacao": "4.95 ⭐",
        "email": "alex.vance@lumen.edu",
        "foto": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": "DOC-702",
        "nome": "Dra. Beatriz Siqueira",
        "titulo": "Doutora em Genética Molecular (Oxford)",
        "departamento": "Biotecnologia & Biologia",
        "cursos_lecionados": 5,
        "avaliacao": "4.97 ⭐",
        "email": "beatriz.siqueira@lumen.edu",
        "foto": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": "DOC-703",
        "nome": "Prof. Ing. Hugo Fonseca",
        "titulo": "Mestre em Robótica & Controlo Autónomo (ETH Zürich)",
        "departamento": "Engenharia Robótica",
        "cursos_lecionados": 4,
        "avaliacao": "4.94 ⭐",
        "email": "hugo.fonseca@lumen.edu",
        "foto": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": "DOC-704",
        "nome": "Dr. Marcus Aurelius Vane",
        "titulo": "PhD em Filosofia Contemporânea & Ética (Cambridge)",
        "departamento": "Filosofia & Humanidades",
        "cursos_lecionados": 3,
        "avaliacao": "4.96 ⭐",
        "email": "marcus.vane@lumen.edu",
        "foto": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80"
    }
]

examenes_db = [
    {
        "id": "EXM-301",
        "disciplina": "Arquitetura de Microserviços",
        "tipo": "Exame Final Prático",
        "data": "2026-09-12",
        "duracao": "180 Minutos",
        "alunos_inscritos": 142,
        "estado": "Agendado"
    },
    {
        "id": "EXM-302",
        "disciplina": "Genómica Computacional",
        "tipo": "Projeto de Investigação em Laboratório",
        "data": "2026-09-14",
        "duracao": "210 Minutos",
        "alunos_inscritos": 115,
        "estado": "Agendado"
    },
    {
        "id": "EXM-303",
        "disciplina": "Robótica Móvel & Visão",
        "tipo": "Demonstração Prática com Prototipagem",
        "data": "2026-09-16",
        "duracao": "240 Minutos",
        "alunos_inscritos": 108,
        "estado": "Agendado"
    },
    {
        "id": "EXM-304",
        "disciplina": "Ética da Inteligência Artificial",
        "tipo": "Ensaio Epistemológico Defesa",
        "data": "2026-09-18",
        "duracao": "150 Minutos",
        "alunos_inscritos": 95,
        "estado": "Agendado"
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/carreras", methods=["GET"])
def get_carreras():
    return jsonify(carreras_db)

@app.route("/api/cursos", methods=["GET"])
def get_cursos():
    return jsonify(cursos_db)

@app.route("/api/alunos", methods=["GET"])
def get_alunos():
    return jsonify(alunos_db)

@app.route("/api/alunos/criar", methods=["POST"])
def criar_aluno():
    data = request.json or {}
    new_id = f"ALU-{900 + len(alunos_db) + 1}"
    new_mat = f"2024{len(alunos_db) + 100}"
    
    novo_aluno = {
        "id": new_id,
        "nome": data.get("nome", "Novo Aluno"),
        "matricula": new_mat,
        "carrera": data.get("carrera", "Engenharia de Software & IA"),
        "email": data.get("email", "aluno@lumen.edu"),
        "progresso_geral": 10,
        "media_gpa": "16.0 / 20",
        "estado": "Ativo",
        "foto": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80"
    }
    
    alunos_db.insert(0, novo_aluno)
    return jsonify({"success": True, "aluno": novo_aluno})

@app.route("/api/profesores", methods=["GET"])
def get_profesores():
    return jsonify(profesores_db)

@app.route("/api/examenes", methods=["GET"])
def get_examenes():
    return jsonify(examenes_db)

@app.route("/api/stats", methods=["GET"])
def get_stats():
    total_alunos = sum(c["alunos_inscritos"] for c in carreras_db)
    total_cursos = len(cursos_db)
    taxa_conclusao = "95.6%"
    media_gpa = "18.5 / 20"
    total_docentes = len(profesores_db)
    
    return jsonify({
        "total_alunos": total_alunos,
        "total_cursos": total_cursos,
        "taxa_conclusao": taxa_conclusao,
        "media_gpa": media_gpa,
        "total_docentes": total_docentes
    })

if __name__ == "__main__":
    print("Iniciando PLATAFORMA ACADEMIA EDUCATIVA SAAS em http://localhost:5800")
    app.run(host="0.0.0.0", port=5800, debug=False)
