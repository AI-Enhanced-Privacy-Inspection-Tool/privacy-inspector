"""
Flask Application Integration for Website Scanner

This module shows how to integrate the website scanner with the main Flask app.
"""

from flask import Flask, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    """
    Create and configure Flask application with website scanner.
    
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # ============================================
    # Configuration
    # ============================================
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    # Scanner configuration
    app.config['SCANNER_CONFIG'] = {
        'enabled': True,
        'timeout': 10,
        'max_urls_per_request': 20,
        'browser_scan_limit': 50,
        'concurrent_scans': False  # Serial scanning for stability
    }
    
    # ============================================
    # Register Blueprints
    # ============================================
    try:
        from src.api.website_scanner_routes import website_scanner_bp
        app.register_blueprint(website_scanner_bp)
        logger.info("✓ Website Scanner API registered")
    except ImportError as e:
        logger.warning(f"Could not import website scanner: {e}")
    
    # ============================================
    # Health Check Endpoint
    # ============================================
    @app.route('/api/health', methods=['GET'])
    def health():
        """Application health check."""
        return jsonify({
            'status': 'healthy',
            'services': {
                'app': 'running',
                'scanner': app.config['SCANNER_CONFIG']['enabled']
            }
        }), 200
    
    # ============================================
    # Error Handlers
    # ============================================
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Run development server
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║        Privacy Inspector - Website Security Scanner        ║
    ║                  Development Server                        ║
    ╚════════════════════════════════════════════════════════════╝
    
    Available Endpoints:
    
    Scanner API:
    ├── POST  /api/scanner/scan
    ├── POST  /api/scanner/scan/summary
    ├── GET   /api/scanner/active-websites
    ├── GET   /api/scanner/scan-active
    ├── POST  /api/scanner/scan-multiple
    ├── POST  /api/scanner/risky-websites
    └── GET   /api/scanner/health
    
    General:
    └── GET   /api/health
    
    Documentation:
    └── See WEBSITE_SCANNER_GUIDE.md for detailed API documentation
    
    Starting server at http://localhost:5000
    """)
    
    app.run(debug=True, host='localhost', port=5000)
