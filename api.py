"""
REST API for Autonomous Agent System
Allows external applications to trigger agents
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from agents.orchestrator_agent import OrchestratorAgent
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Initialize orchestrator once
print("🚀 Initializing Orchestrator...")
orchestrator = OrchestratorAgent()
print("✓ API Ready!")


@app.route('/', methods=['GET'])
def home():
    """API documentation"""
    return jsonify({
        "name": "Autonomous Agent System API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Check API health",
            "/agents": "List available agents",
            "/execute": "Execute a task (POST)",
            "/history": "Get execution history"
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents_available": len(orchestrator.agents)
    })


@app.route('/agents', methods=['GET'])
def list_agents():
    """List all available agents"""
    return jsonify({
        "agents": [
            {
                "name": agent.name,
                "role": agent.role,
                "type": name
            }
            for name, agent in orchestrator.agents.items()
        ]
    })


@app.route('/execute', methods=['POST'])
def execute_task():
    """
    Execute a task via agent system
    
    Request body:
    {
        "task": "Monitor https://httpbin.org/status/200"
    }
    """
    try:
        data = request.json
        task = data.get('task')
        
        if not task:
            return jsonify({"error": "No task provided"}), 400
        
        print(f"\n📥 API Request: {task}")
        result = orchestrator.run(task)
        print(f"✅ Task completed\n")
        
        return jsonify({
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "result": result
        })
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/history', methods=['GET'])
def get_history():
    """Get orchestrator execution history"""
    return jsonify({
        "history": orchestrator.execution_log[-10:] if orchestrator.execution_log else []
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)