#!/usr/bin/env python3
"""
DEIVERSE API Server - Python Flask Version
Simple API server for connecting repositories
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

# Store connections file path
CONNECTIONS_FILE = os.path.join(os.path.dirname(__file__), 'connections.json')

def get_connections():
    """Load connections from JSON file"""
    try:
        if os.path.exists(CONNECTIONS_FILE):
            with open(CONNECTIONS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f'Error reading connections: {e}')
    return []

def save_connection(connection):
    """Save a new connection to JSON file"""
    try:
        connections = get_connections()
        connection.update({
            'id': int(datetime.now().timestamp() * 1000),
            'connected_at': datetime.now().isoformat(),
            'status': 'active'
        })
        connections.append(connection)
        with open(CONNECTIONS_FILE, 'w') as f:
            json.dump(connections, f, indent=2)
        return True
    except Exception as e:
        print(f'Error saving connection: {e}')
        return False

@app.route('/api/connect-repo', methods=['POST'])
def connect_repo():
    """Connect a repository endpoint"""
    data = request.get_json()
    
    provider = data.get('provider')
    repo_url = data.get('repo_url')
    branch = data.get('branch', 'main')
    
    # Validation
    if not provider or not repo_url:
        return jsonify({'error': 'Provider and repository URL are required'}), 400
    
    # Validate URL format
    url_pattern = r'^https?://(github|gitlab|bitbucket)\.com/[\w\-\.]+/[\w\-\.]+'
    if not re.match(url_pattern, repo_url, re.IGNORECASE):
        return jsonify({'error': 'Invalid repository URL format'}), 400
    
    # Validate provider matches URL
    url_match = re.search(r'github|gitlab|bitbucket', repo_url, re.IGNORECASE)
    if url_match:
        url_provider = url_match.group(0).lower()
        if provider != url_provider:
            return jsonify({
                'error': f'Provider mismatch: URL contains {url_provider} but you selected {provider}'
            }), 400
    
    # Save connection
    connection = {
        'provider': provider,
        'repo_url': repo_url,
        'branch': branch
    }
    
    if save_connection(connection):
        print(f'Repository connected: {repo_url} ({provider})')
        return jsonify({
            'success': True,
            'message': 'Repository connected successfully',
            'data': connection
        })
    else:
        return jsonify({'error': 'Failed to save connection'}), 500

@app.route('/api/connections', methods=['GET'])
def get_all_connections():
    """Get all connections"""
    connections = get_connections()
    return jsonify({'connections': connections})

@app.route('/api/connections/<int:connection_id>', methods=['GET'])
def get_connection(connection_id):
    """Get connection by ID"""
    connections = get_connections()
    connection = next((c for c in connections if c.get('id') == connection_id), None)
    
    if connection:
        return jsonify({'connection': connection})
    else:
        return jsonify({'error': 'Connection not found'}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3001))
    print(f'🚀 DEIVERSE API Server running on http://localhost:{port}')
    print(f'📡 API endpoints:')
    print(f'   POST /api/connect-repo - Connect a repository')
    print(f'   GET  /api/connections - Get all connections')
    print(f'   GET  /api/connections/:id - Get connection by ID')
    print(f'   GET  /api/health - Health check')
    app.run(host='0.0.0.0', port=port, debug=True)

