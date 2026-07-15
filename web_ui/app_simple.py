"""
Simple Portfolio Dashboard - Working Version
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data_connectors.mock_portfolio import MockPortfolioGenerator
from engines.scenario_analyzer import ScenarioAnalyzer

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'portfolio-secret-key'

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Global portfolio data
PORTFOLIO_DATA = None

def load_portfolio():
    """Load portfolio data"""
    global PORTFOLIO_DATA
    portfolio = MockPortfolioGenerator.generate_portfolio()
    PORTFOLIO_DATA = portfolio
    return PORTFOLIO_DATA

# ============ ROUTES ============

@app.route('/')
def dashboard():
    """Main dashboard"""
    print("\n=== ROUTE: dashboard ===")
    portfolio = load_portfolio()
    print(f"Portfolio loaded, rendering template: dashboard.html")
    return render_template('dashboard.html')

@app.route('/portfolio')
def portfolio_view():
    """Portfolio details view"""
    load_portfolio()
    return render_template('portfolio-dynamic.html')

@app.route('/scenarios')
def scenarios_view():
    """Scenario analysis view"""
    return render_template('scenarios-dynamic.html')

@app.route('/recommendations')
def recommendations_view():
    """Recommendations view"""
    return render_template('recommendations-dynamic.html')

@app.route('/reports')
def reports_view():
    """Reports view"""
    return render_template('reports-fixed.html')

# ============ API ENDPOINTS ============

@app.route('/api/portfolio/summary', methods=['GET'])
def get_portfolio_summary():
    """Get portfolio summary metrics"""
    try:
        print("\n=== API CALL: get_portfolio_summary ===")
        if PORTFOLIO_DATA is None:
            print("PORTFOLIO_DATA is None, loading...")
            load_portfolio()
        
        print(f"PORTFOLIO_DATA keys: {list(PORTFOLIO_DATA.keys()) if PORTFOLIO_DATA else 'None'}")
        p = PORTFOLIO_DATA
        response = {
            'portfolio_value': p.get('portfolio_value', 0),
            'capital_utilization': p.get('capital_utilization', 0),
            'average_rorac': p.get('avg_rorac', 0),
            'diversification_score': p.get('diversification_score', 0),
            'by_lob': p.get('lob_breakdown', {}),
            'by_geography': p.get('geography_breakdown', {}),
            'timestamp': datetime.now().isoformat()
        }
        print(f"Returning: {response}")
        return jsonify(response)
    except Exception as e:
        import traceback
        print(f"ERROR in get_portfolio_summary: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """Get full portfolio"""
    if PORTFOLIO_DATA is None:
        load_portfolio()
    
    treaties = PORTFOLIO_DATA.get('treaties', [])
    lob_list = list(set(t.get('lob', '') for t in treaties))
    geo_list = list(set(t.get('geography', '') for t in treaties))
    
    return jsonify({
        'treaties': treaties,
        'lob_list': lob_list,
        'geography_list': geo_list,
        'treaty_count': len(treaties)
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok'})

@app.route('/api/portfolio/metrics', methods=['GET'])
def get_portfolio_metrics():
    """Get detailed portfolio metrics"""
    if PORTFOLIO_DATA is None:
        load_portfolio()
    
    return jsonify({
        'rorac': PORTFOLIO_DATA.get('avg_rorac', 0),
        'capital_efficiency': PORTFOLIO_DATA.get('capital_utilization', 0),
        'top_treaties': PORTFOLIO_DATA.get('treaties', [])[:10],
        'lob_breakdown': PORTFOLIO_DATA.get('lob_breakdown', {}),
        'geography_breakdown': PORTFOLIO_DATA.get('geography_breakdown', {}),
        'performance_distribution': PORTFOLIO_DATA.get('performance_distribution', {})
    })

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get portfolio recommendations"""
    return jsonify({
        'recommendations': [
            {
                'id': 'rec-001',
                'title': 'Rebalance Property Cat Exposure',
                'business_justification': 'Current concentration in Property Catastrophe exceeds target allocation. Reduce capital at risk by 15%.',
                'priority': 'High',
                'confidence_score': 0.92
            },
            {
                'id': 'rec-002',
                'title': 'Diversify into Specialty Lines',
                'business_justification': 'Specialty Lines offers better RORAC with lower concentration risk. Improve average RORAC by 5-8%.',
                'priority': 'Medium',
                'confidence_score': 0.85
            },
            {
                'id': 'rec-003',
                'title': 'Optimize Geographic Mix',
                'business_justification': 'Asia Pacific region shows strong growth opportunities. Expand market share by 12% with improved returns.',
                'priority': 'Medium',
                'confidence_score': 0.78
            }
        ]
    })

@app.route('/api/scenario/simulate', methods=['POST'])
def simulate_scenario():
    """Run scenario simulation"""
    try:
        data = request.get_json()
        simulation_type = data.get('simulation_type', 'monte_carlo')
        
        if PORTFOLIO_DATA is None:
            load_portfolio()
        
        # Initialize scenario analyzer
        analyzer = ScenarioAnalyzer(PORTFOLIO_DATA)
        
        # Run appropriate simulation
        if simulation_type == 'monte_carlo':
            simulations = data.get('simulations', 1000)
            results = analyzer.run_monte_carlo(simulations=simulations)
        elif simulation_type == 'interest_rate':
            rate_change = data.get('rate_change', 50)
            results = analyzer.stress_test_interest_rates(rate_change=rate_change)
        elif simulation_type == 'catastrophe':
            return_period = data.get('return_period', 200)
            results = analyzer.catastrophe_stress_test(event_type='hurricane', return_period=return_period)
        elif simulation_type == 'comparison':
            comparison = analyzer.scenario_comparison()
            results = {
                'scenarios': comparison['scenarios'],
                'expected_weighted_outcome': comparison['expected_weighted_outcome']
            }
        else:
            return jsonify({'error': f'Unknown simulation type: {simulation_type}'}), 400
        
        return jsonify(results)
    except Exception as e:
        import traceback
        print(f"ERROR in simulate_scenario: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# ============ WEBSOCKET EVENTS ============

@socketio.on('connect')
def handle_connect():
    print(f'Client connected')
    emit('connect_response', {'data': 'Connected to Portfolio Agent'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected')

@socketio.on('request_portfolio_update')
def handle_portfolio_update():
    """Send portfolio summary to requesting client"""
    if PORTFOLIO_DATA:
        emit('portfolio_data', {
            'timestamp': PORTFOLIO_DATA['timestamp'],
            'portfolio_value': PORTFOLIO_DATA['portfolio_value'],
            'capital_utilization': PORTFOLIO_DATA['capital_utilization'],
            'average_rorac': PORTFOLIO_DATA['avg_rorac'],
            'diversification_score': PORTFOLIO_DATA['diversification_score']
        })

# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    import traceback
    traceback.print_exc()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Load portfolio on startup
    portfolio = load_portfolio()
    print("✅ Portfolio loaded successfully")
    print(f"   Timestamp: {portfolio['timestamp']}")
    print(f"   Portfolio Value: ${portfolio['portfolio_value']:,.0f}")
    print(f"   Treaties: {portfolio['treaty_count']}")
    print(f"   Capital Utilization: {portfolio['capital_utilization']:.1f}%")
    print(f"\n🚀 Starting Portfolio Agent on http://localhost:5001")
    print(f"   Dashboard: http://localhost:5001/")
    print(f"   With WebSocket support for real-time updates")
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=5001,
        debug=True
    )
