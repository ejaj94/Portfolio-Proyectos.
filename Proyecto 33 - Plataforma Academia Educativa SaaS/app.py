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

# Initial Educational Mock Database
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
        "nome": "Design de Experiência Digital & Product Design",
        "duracao": "2.5 Anos • 5 Semestres",
        "coordenador": "Prof. Elena Rostova",
        "cursos_count": 14,
        "alunos_inscritos": 315,
        "taxa_empregabilidade": "96.2%",
        "descricao": "Especialização em arquitetura de informação, sistemas de design escaláveis, pesquisa de utilizadores e prototipagem 3D."
    },
    {
        "id": "CAR-03",
        "nome": "Ciência de Dados, Big Data & Analytics",
        "duracao": "3 Anos • 6 Semestres",
        "coordenador": "Dr. Carlos Mendes",
        "cursos_count": 16,
        "alunos_inscritos": 280,
        "taxa_empregabilidade": "97.8%",
        "descricao": "Domínio de modelos estatísticos avançados, engenharia de dados em nuvem e inteligência de negócios."
    },
    {
        "id": "CAR-04",
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
        "codigo": "AI-402",
        "titulo": "Deep Learning & Processamento de Linguagem Natural",
        "carrera": "Engenharia de Software & IA",
        "professor": "Dra. Sophia Chen",
        "modulos": 14,
        "duracao_horas": 95,
        "progresso_medio": 64,
        "alunos": 128,
        "classificacao": "4.98 ⭐"
    },
    {
        "id": "CRS-103",
        "codigo": "UX-201",
        "titulo": "Design Systems & UI Architecture em Scale",
        "carrera": "Design de Experiência Digital",
        "professor": "Prof. Elena Rostova",
        "modulos": 10,
        "duracao_horas": 65,
        "progresso_medio": 85,
        "alunos": 110,
        "classificacao": "4.90 ⭐"
    },
    {
        "id": "CRS-104",
        "codigo": "DS-305",
        "titulo": "Engenharia de Pipelines de Dados & Spark",
        "carrera": "Ciência de Dados & Big Data",
        "professor": "Dr. Carlos Mendes",
        "modulos": 11,
        "duracao_horas": 75,
        "progresso_medio": 71,
        "alunos": 95,
        "classificacao": "4.92 ⭐"
    },
    {
        "id": "CRS-105",
        "codigo": "SEC-401",
        "titulo": "Ethical Hacking & Testes de Penetração",
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
        "carrera": "Design de Experiência Digital",
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
        "carrera": "Ciência de Dados & Big Data",
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
        "carrera": "Cybersecurity & Cloud",
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
        "carrera": "Engenharia de Software & IA",
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
        "nome": "Prof. Elena Rostova",
        "titulo": "Mestre em Human-Computer Interaction (RCA)",
        "departamento": "Product Design",
        "cursos_lecionados": 3,
        "avaliacao": "4.90 ⭐",
        "email": "elena.rostova@lumen.edu",
        "foto": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": "DOC-703",
        "nome": "Dra. Sophia Chen",
        "titulo": "PhD em Inteligência Artificial (Stanford)",
        "departamento": "IA & Data Science",
        "cursos_lecionados": 3,
        "avaliacao": "4.98 ⭐",
        "email": "sophia.chen@lumen.edu",
        "foto": "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": "DOC-704",
        "nome": "Prof. Marcus Brody",
        "titulo": "Especialista Principal em Segurança Cibernética",
        "departamento": "Cybersecurity",
        "cursos_lecionados": 4,
        "avaliacao": "4.96 ⭐",
        "email": "marcus.brody@lumen.edu",
        "foto": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=400&q=80"
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
        "disciplina": "Deep Learning & NLP",
        "tipo": "Projeto de Tese Intermédio",
        "data": "2026-09-15",
        "duracao": "240 Minutos",
        "alunos_inscritos": 128,
        "estado": "Agendado"
    },
    {
        "id": "EXM-303",
        "disciplina": "Design Systems & UI",
        "tipo": "Avaliação de Portfólio",
        "data": "2026-09-02",
        "duracao": "120 Minutos",
        "alunos_inscritos": 110,
        "estado": "Concluído"
    },
    {
        "id": "EXM-304",
        "disciplina": "Ethical Hacking",
        "tipo": "Desafio CTF Red Team",
        "data": "2026-09-18",
        "duracao": "300 Minutos",
        "alunos_inscritos": 104,
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
    taxa_conclusao = "94.8%"
    media_gpa = "18.4 / 20"
    total_docentes = len(profesores_db)
    
    return jsonify({
        "total_alunos": total_alunos,
        "total_cursos": total_cursos,
        "taxa_conclusao": taxa_conclusao,
        "media_gpa": media_gpa,
        "total_docentes": total_docentes
    })

if __name__ == "__main__":
    print("Iniciando PLATAFORMA ACADEMIA EDUCATIVA SAAS em http://localhost:5750")
    app.run(host="0.0.0.0", port=5750, debug=False)
