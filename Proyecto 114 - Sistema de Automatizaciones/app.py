import os
from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)

# Initialize DB on start
database.init_db()

@app.route('/')
def index():
    return render_template('index.html')

# 1. Dashboard Metrics
@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        metrics = database.get_dashboard_metrics()
        return jsonify({"success": True, "metrics": metrics})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 2. Integrations
@app.route('/api/integrations', methods=['GET'])
def list_integrations():
    try:
        integrations = database.get_all_integrations()
        return jsonify({"success": True, "integrations": integrations})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/integrations/<int:iid>/status', methods=['POST'])
def update_integration(iid):
    data = request.json or {}
    new_status = data.get('status', 'Conectado')
    try:
        database.update_integration_status(iid, new_status)
        return jsonify({"success": True, "message": f"Integracao atualizada para {new_status}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 3. Triggers & Actions
@app.route('/api/triggers', methods=['GET'])
def list_triggers():
    try:
        triggers = database.get_all_triggers()
        return jsonify({"success": True, "triggers": triggers})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/actions', methods=['GET'])
def list_actions():
    try:
        actions = database.get_all_actions()
        return jsonify({"success": True, "actions": actions})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 4. Workflows
@app.route('/api/workflows', methods=['GET', 'POST'])
def handle_workflows():
    if request.method == 'GET':
        workflows = database.get_all_workflows()
        return jsonify({"success": True, "workflows": workflows})

    data = request.json or {}
    try:
        wid = database.add_workflow(
            title=data.get('title'),
            description=data.get('description', ''),
            trigger_id=int(data.get('trigger_id')),
            action_id=int(data.get('action_id')),
            condition_field=data.get('condition_field', ''),
            condition_operator=data.get('condition_operator', '=='),
            condition_value=data.get('condition_value', ''),
            action_template=data.get('action_template', '')
        )
        return jsonify({"success": True, "workflow_id": wid, "message": "Fluxo de automacao criado com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/workflows/<int:wid>/toggle', methods=['POST'])
def toggle_workflow(wid):
    data = request.json or {}
    is_active = int(data.get('is_active', 1))
    try:
        database.toggle_workflow_status(wid, is_active)
        state_str = "ativado" if is_active == 1 else "pausado"
        return jsonify({"success": True, "message": f"Fluxo {state_str} com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/workflows/<int:wid>/run', methods=['POST'])
def trigger_workflow_run(wid):
    data = request.json or {}
    custom_payload = data.get('payload')
    try:
        result = database.execute_workflow_engine(wid, custom_payload)
        if result:
            return jsonify({"success": True, "execution": result, "message": f"Execucao finalizada com estado: {result['status']}"})
        return jsonify({"success": False, "error": "Fluxo nao encontrado"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/workflows/<int:wid>', methods=['DELETE'])
def remove_workflow(wid):
    try:
        database.delete_workflow(wid)
        return jsonify({"success": True, "message": "Fluxo eliminado com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 5. Execution History
@app.route('/api/history', methods=['GET'])
def list_history():
    try:
        logs = database.get_execution_history(limit=50)
        return jsonify({"success": True, "history": logs})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6967))
    print(f">> AutoFlow Platform rodando em http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
