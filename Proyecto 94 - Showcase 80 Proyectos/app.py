import os
from flask import Flask, render_template, jsonify
from database import get_projects

app = Flask(__name__)

@app.route('/')
def index():
    projects = get_projects()
    return render_template('index.html', projects=projects)

@app.route('/showcase')
def showcase():
    projects = get_projects()
    return render_template('index.html', projects=projects)

@app.route('/api/projects')
def api_projects():
    return jsonify(get_projects())

if __name__ == '__main__':
    print("Iniciando Showcase 80 Proyectos en 80 Días na porta 6947...")
    app.run(host='0.0.0.0', port=6947, debug=True)
