"""
Enhanced Portfolio Dashboard - Dynamic Backend with WebSocket Support
Adds real-time updates, data uploads, and async simulations
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os
import threading
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd
from io import StringIO

# Import existing engines
from data_connectors.mock_portfolio import MockPortfolioGenerator
from engines.portfolio_optimizer import PortfolioOptimizer
from engines.scenario_analyzer import ScenarioAnalyzer
from engines.recommendation_engine import RecommendationEngine

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'portfolio-agent-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialize SocketIO for real-time updates
socketio = SocketIO(app, cors_allowed_origins="*")

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global portfolio data and filters
PORTFOLIO_DATA = None
PORTFOLIO_FILTERS = {
    'lob': None,
    'geography': None,
    'status': None,
    'rorac_min': None,
    'rorac_max': None
}

def load_portfolio():
    """Load or generate portfolio data"""
    global PORTFOLIO_DATA
    portfolio = MockPortfolioGenerator.generate_portfolio(treaty_count=50)
    
    # Ensure portfolio is a list of dictionaries
    if isinstance(portfolio, dict):
        treaties = portfolio.get('treaties', []) if 'treaties' in portfolio else list(portfolio.values())
    else:
        treaties = portfolio
    
    # Filter out any non-dict items
    treaties = [t for t in treaties if isinstance(t, dict)]
    
    if not treaties:
        # Fallback to empty portfolio
        treaties = []
    
    PORTFOLIO_DATA = {
        'timestamp': datetime.now().isoformat(),
        'treaties': treaties,
        'treaty_count': len(treaties),
        'portfolio_value': sum(t.get('premium', 0) for t in treaties),
        'capital_utilization': sum(t.get('capital_requirement', 0) for t in treaties) / 10000000 * 100 if treaties else 0,
        'average_rorac': sum(t.get('rorac', 0) for t in treaties) / len(treaties) if treaties else 0,
        'diversification_score': calculate_diversification_score(treaties) if treaties else 0,
        'by_lob': group_by_lob(treaties) if treaties else {},
        'by_geography': group_by_geography(treaties) if treaties else {},
        'lob_list': list(set(t.get('lob', '') for t in treaties if 'lob' in t)),
        'geography_list': list(set(t.get('geography', '') for t in treaties if 'geography' in t))
    }
    
    return PORTFOLIO_DATA

def calculate_diversification_score(portfolio):
    """Calculate concentration/diversification metric (0-1)"""
    if not portfolio:
        return 0
    lobs = [t.get('lob', '') for t in portfolio if 'lob' in t]
    if not lobs:
        return 0
    lob_counts = {}
    for lob in lobs:
        lob_counts[lob] = lob_counts.get(lob, 0) + 1
    
    if not lob_counts:
        return 0
    max_concentration = max(lob_counts.values()) / len(lobs)
    diversification = 1 - max_concentration
    return min(1.0, diversification)

def group_by_lob(portfolio):
    """Group treaties by Line of Business"""
    grouped = {}
    for treaty in portfolio:
        if not isinstance(treaty, dict):
            continue
        lob = treaty.get('lob', 'Unknown')
        if lob not in grouped:
            grouped[lob] = {'count': 0, 'premium': 0, 'avg_rorac': 0, 'avg_loss_ratio': 0}
        grouped[lob]['count'] += 1
        grouped[lob]['premium'] += treaty.get('premium', 0)
        grouped[lob]['avg_rorac'] += treaty.get('rorac', 0)
        grouped[lob]['avg_loss_ratio'] += treaty.get('loss_ratio', 0)
    
    for lob in grouped:
        if grouped[lob]['count'] > 0:
            grouped[lob]['avg_rorac'] /= grouped[lob]['count']
            grouped[lob]['avg_loss_ratio'] /= grouped[lob]['count']
    
    return grouped

def group_by_geography(portfolio):
    """Group treaties by Geography"""
    grouped = {}
    for treaty in portfolio:
        if not isinstance(treaty, dict):
            continue
        geo = treaty.get('geography', 'Unknown')
        if geo not in grouped:
            grouped[geo] = {'count': 0, 'premium': 0, 'avg_rorac': 0, 'avg_loss_ratio': 0}
        grouped[geo]['count'] += 1
        grouped[geo]['premium'] += treaty.get('premium', 0)
        grouped[geo]['avg_rorac'] += treaty.get('rorac', 0)
        grouped[geo]['avg_loss_ratio'] += treaty.get('loss_ratio', 0)
    
    for geo in grouped:
        if grouped[geo]['count'] > 0:
            grouped[geo]['avg_rorac'] /= grouped[geo]['count']
            grouped[geo]['avg_loss_ratio'] /= grouped[geo]['count']
    
    return grouped

def apply_filters(treaties):
    """Apply filters to treaties"""
    filtered = treaties
    
    if PORTFOLIO_FILTERS['lob']:
        filtered = [t for t in filtered if isinstance(t, dict) and t.get('lob') == PORTFOLIO_FILTERS['lob']]
    
    if PORTFOLIO_FILTERS['geography']:
        filtered = [t for t in filtered if isinstance(t, dict) and t.get('geography') == PORTFOLIO_FILTERS['geography']]
    
    if PORTFOLIO_FILTERS['status']:
        filtered = [t for t in filtered if isinstance(t, dict) and t.get('status') == PORTFOLIO_FILTERS['status']]
    
    if PORTFOLIO_FILTERS['rorac_min'] is not None:
        filtered = [t for t in filtered if isinstance(t, dict) and t.get('rorac', 0) >= PORTFOLIO_FILTERS['rorac_min']]
    
    if PORTFOLIO_FILTERS['rorac_max'] is not None:
        filtered = [t for t in filtered if isinstance(t, dict) and t.get('rorac', 0) <= PORTFOLIO_FILTERS['rorac_max']]
    
    return filtered

# ============ BEFORE REQUEST HANDLER ============

@app.before_request
def before_request():
    """Ensure portfolio is loaded before any request"""
    global PORTFOLIO_DATA
    if PORTFOLIO_DATA is None or not PORTFOLIO_DATA:
        print("Loading portfolio before request...")
        load_portfolio()
        print(f"Portfolio loaded: {len(PORTFOLIO_DATA.get('treaties', []))} treaties")

# ============ ROUTES ============

@app.route('/')
def dashboard():
    return render_template('dashboard-dynamic.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio-dynamic.html')

@app.route('/scenarios')
def scenarios():
    return render_template('scenarios-dynamic.html')

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations-dynamic.html')

@app.route('/reports')
def reports():
    return render_template('reports-dynamic.html')

# ============ API ENDPOINTS ============

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """Get full portfolio with applied filters"""
    if not PORTFOLIO_DATA:
        load_portfolio()
    
    filtered_treaties = apply_filters(PORTFOLIO_DATA['treaties'])
    
    return jsonify({
        'timestamp': PORTFOLIO_DATA['timestamp'],
        'treaties': filtered_treaties,
        'treaty_count': len(filtered_treaties),
        'portfolio_value': sum(t['premium'] for t in filtered_treaties),
        'capital_utilization': sum(t['capital_requirement'] for t in filtered_treaties) / 10000000 * 100,
        'average_rorac': sum(t['rorac'] for t in filtered_treaties) / len(filtered_treaties) if filtered_treaties else 0,
        'lob_list': PORTFOLIO_DATA['lob_list'],
        'geography_list': PORTFOLIO_DATA['geography_list']
    })

@app.route('/api/portfolio/summary', methods=['GET'])
def get_portfolio_summary():
    """Get portfolio summary metrics"""
    try:
        global PORTFOLIO_DATA
        print(f"get_portfolio_summary called. PORTFOLIO_DATA is None: {PORTFOLIO_DATA is None}")
        
        if PORTFOLIO_DATA is None:
            print("Loading portfolio...")
            load_portfolio()
            print(f"Portfolio loaded: {PORTFOLIO_DATA}")
        
        if not PORTFOLIO_DATA:
            print("ERROR: PORTFOLIO_DATA is empty")
            return jsonify({'error': 'Portfolio data not loaded'}), 500
        
        if 'treaties' not in PORTFOLIO_DATA:
            print(f"ERROR: 'treaties' not in PORTFOLIO_DATA. Keys: {list(PORTFOLIO_DATA.keys())}")
            return jsonify({'error': 'No treaties in portfolio data'}), 500
        
        treaties = PORTFOLIO_DATA.get('treaties', [])
        print(f"Number of treaties: {len(treaties)}")
        
        if not treaties:
            print("ERROR: No treaties in portfolio")
            return jsonify({'error': 'No treaties in portfolio'}), 500
        
        filtered_treaties = apply_filters(treaties)
        print(f"Filtered treaties: {len(filtered_treaties)}")
        
        # Safe attribute access
        total_premium = sum(t.get('premium', 0) for t in filtered_treaties if isinstance(t, dict))
        total_capital = sum(t.get('capital_requirement', 0) for t in filtered_treaties if isinstance(t, dict))
        total_rorac = sum(t.get('rorac', 0) for t in filtered_treaties if isinstance(t, dict))
        
        print(f"Total premium: {total_premium}, Total capital: {total_capital}, Total rorac: {total_rorac}")
        
        avg_rorac = total_rorac / len(filtered_treaties) if filtered_treaties else 0
        capital_util = (total_capital / 10000000 * 100) if total_capital > 0 else 0
        
        result = {
            'portfolio_value': total_premium,
            'capital_utilization': capital_util,
            'average_rorac': avg_rorac,
            'diversification_score': calculate_diversification_score(filtered_treaties) if filtered_treaties else 0,
            'by_lob': group_by_lob(filtered_treaties),
            'by_geography': group_by_geography(filtered_treaties),
            'timestamp': datetime.now().isoformat()
        }
        print(f"Returning result: {result}")
        return jsonify(result)
    except Exception as e:
        import traceback
        error_msg = f"Error in get_portfolio_summary: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/api/filters/update', methods=['POST'])
def update_filters():
    """Update portfolio filters and return filtered data"""
    global PORTFOLIO_FILTERS
    
    try:
        data = request.json
        PORTFOLIO_FILTERS = {
            'lob': data.get('lob'),
            'geography': data.get('geography'),
            'status': data.get('status'),
            'rorac_min': data.get('rorac_min'),
            'rorac_max': data.get('rorac_max')
        }
        
        filtered_treaties = apply_filters(PORTFOLIO_DATA['treaties'])
        
        total_premium = sum(t.get('premium', 0) for t in filtered_treaties if isinstance(t, dict))
        total_rorac = sum(t.get('rorac', 0) for t in filtered_treaties if isinstance(t, dict))
        avg_rorac = total_rorac / len(filtered_treaties) if filtered_treaties else 0
        
        return jsonify({
            'success': True,
            'treaty_count': len(filtered_treaties),
            'portfolio_value': total_premium,
            'average_rorac': avg_rorac
        })
    except Exception as e:
        print(f"Error in update_filters: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-portfolio', methods=['POST'])
def upload_portfolio():
    """Upload CSV portfolio data"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Read CSV
        stream = StringIO(file.stream.read().decode('UTF-8'))
        df = pd.read_csv(stream)
        
        # Convert to portfolio format
        treaties = df.to_dict('records')
        
        global PORTFOLIO_DATA
        PORTFOLIO_DATA['treaties'] = treaties
        PORTFOLIO_DATA['treaty_count'] = len(treaties)
        PORTFOLIO_DATA['timestamp'] = datetime.now().isoformat()
        
        # Notify all connected clients
        socketio.emit('portfolio_updated', {
            'timestamp': PORTFOLIO_DATA['timestamp'],
            'treaty_count': len(treaties),
            'portfolio_value': sum(t.get('premium', 0) for t in treaties)
        }, broadcast=True)
        
        return jsonify({
            'success': True,
            'message': f'Portfolio updated with {len(treaties)} treaties',
            'timestamp': PORTFOLIO_DATA['timestamp']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scenario/simulate', methods=['POST'])
def run_scenario_async():
    """Run scenario simulation asynchronously"""
    data = request.json
    scenario_type = data.get('type', 'monte_carlo')
    
    def run_simulation():
        try:
            portfolio = apply_filters(PORTFOLIO_DATA['treaties'])
            analyzer = ScenarioAnalyzer(portfolio)
            
            if scenario_type == 'monte_carlo':
                result = analyzer.run_monte_carlo(simulations=1000)
            elif scenario_type == 'interest_rate':
                rate_change = data.get('rate_change', 50)
                result = analyzer.stress_test_interest_rates(rate_change)
            elif scenario_type == 'catastrophe':
                event_type = data.get('event_type', 'hurricane')
                return_period = data.get('return_period', 100)
                result = analyzer.catastrophe_stress_test(event_type, return_period)
            elif scenario_type == 'comparison':
                result = analyzer.scenario_comparison()
            
            # Send result to all clients
            socketio.emit('scenario_completed', {
                'scenario_type': scenario_type,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }, broadcast=True)
        
        except Exception as e:
            socketio.emit('scenario_error', {
                'error': str(e),
                'scenario_type': scenario_type
            }, broadcast=True)
    
    # Run in background thread
    thread = threading.Thread(target=run_simulation)
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'Simulation started', 'scenario_type': scenario_type})

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get portfolio recommendations"""
    filtered_treaties = apply_filters(PORTFOLIO_DATA['treaties'])
    engine = RecommendationEngine(filtered_treaties)
    
    return jsonify(engine.generate_comprehensive_recommendations())

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'treaties_count': len(PORTFOLIO_DATA['treaties']) if PORTFOLIO_DATA else 0
    })

# ============ WEBSOCKET EVENTS ============

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')
    emit('response', {'data': 'Connected to Portfolio Agent'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')

@socketio.on('request_portfolio_update')
def handle_portfolio_update():
    """Send portfolio summary to requesting client"""
    if PORTFOLIO_DATA:
        emit('portfolio_data', {
            'timestamp': PORTFOLIO_DATA['timestamp'],
            'portfolio_value': PORTFOLIO_DATA['portfolio_value'],
            'capital_utilization': PORTFOLIO_DATA['capital_utilization'],
            'average_rorac': PORTFOLIO_DATA['average_rorac']
        })

@socketio.on('request_live_filter')
def handle_live_filter(data):
    """Apply filter and broadcast to all clients"""
    global PORTFOLIO_FILTERS
    PORTFOLIO_FILTERS = {
        'lob': data.get('lob'),
        'geography': data.get('geography'),
        'status': data.get('status'),
        'rorac_min': data.get('rorac_min'),
        'rorac_max': data.get('rorac_max')
    }
    
    filtered_treaties = apply_filters(PORTFOLIO_DATA['treaties'])
    
    socketio.emit('filter_updated', {
        'treaty_count': len(filtered_treaties),
        'portfolio_value': sum(t['premium'] for t in filtered_treaties),
        'average_rorac': sum(t['rorac'] for t in filtered_treaties) / len(filtered_treaties) if filtered_treaties else 0,
        'filters': PORTFOLIO_FILTERS
    }, broadcast=True)

# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============ INITIALIZATION ============

if __name__ == '__main__':
    # Load portfolio on startup
    load_portfolio()
    print("✅ Portfolio loaded successfully")
    print(f"   Timestamp: {PORTFOLIO_DATA['timestamp']}")
    print(f"   Portfolio Value: ${PORTFOLIO_DATA['portfolio_value']:,.0f}")
    print(f"   Treaties: {PORTFOLIO_DATA['treaty_count']}")
    print(f"   Capital Utilization: {PORTFOLIO_DATA['capital_utilization']:.1f}%")
    print(f"\n🚀 Starting Dynamic Portfolio Agent on http://localhost:5001")
    print(f"   With WebSocket support for real-time updates")
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5001)),
        debug=True if os.getenv('AZURE_ENV') != 'production' else False
    )
