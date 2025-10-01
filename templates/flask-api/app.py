"""
{{PROJECT_NAME}} - Flask API Application
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///{{PROJECT_NAME}}.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Routes
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Welcome to {{PROJECT_NAME}} API!',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'api': '/api/v1'
            }
        })
    
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'service': '{{PROJECT_NAME}}',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connected'
        })
    
    @app.route('/api/v1/items')
    def get_items():
        return jsonify({
            'items': [
                {'id': 1, 'name': 'Sample Item 1', 'description': 'This is a sample item'},
                {'id': 2, 'name': 'Sample Item 2', 'description': 'Another sample item'}
            ],
            'total': 2
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)