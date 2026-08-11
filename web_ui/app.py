"""
Dynamic Portfolio Optimisation Agent - Flask Web Application
Serves portfolio monitoring, optimization, and recommendation interface
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
from data_connectors.mock_portfolio import MockPortfolioGenerator
from engines.portfolio_optimizer import PortfolioOptimizer
from engines.scenario_analyzer import ScenarioAnalyzer
from engines.recommendation_engine import RecommendationEngine

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize portfolio data
PORTFOLIO_DATA = None

def load_portfolio():
    """Load or generate portfolio data"""
    global PORTFOLIO_DATA
    if PORTFOLIO_DATA is None:
        PORTFOLIO_DATA = MockPortfolioGenerator.generate_portfolio()
    return PORTFOLIO_DATA

# Routes
@app.route('/')
def dashboard():
    """Main dashboard"""
    portfolio = load_portfolio()
    return render_template('dashboard-enhanced.html', portfolio=portfolio)

@app.route('/portfolio')
def portfolio_view():
    """Portfolio details view"""
    portfolio = load_portfolio()
    return render_template('portfolio.html', portfolio=portfolio)

@app.route('/scenarios')
def scenarios_view():
    """Scenario analysis view"""
    return render_template('scenarios.html')

@app.route('/recommendations')
def recommendations_view():
    """Recommendations view"""
    return render_template('recommendations.html')

@app.route('/reports')
def reports_view():
    """Reports view"""
    return render_template('reports.html')

# API Endpoints
@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """Get portfolio data"""
    portfolio = load_portfolio()
    return jsonify(portfolio)

@app.route('/api/portfolio/summary', methods=['GET'])
def get_portfolio_summary():
    """Get portfolio summary metrics"""
    portfolio = load_portfolio()
    return jsonify({
        'portfolio_value': portfolio['portfolio_value'],
        'total_capital': portfolio['total_capital'],
        'capital_utilization': portfolio['capital_utilization'],
        'total_loss_ratio': portfolio['total_loss_ratio'],
        'expected_profit': portfolio['expected_profit'],
        'avg_rorac': portfolio['avg_rorac'],
        'diversification_score': portfolio['diversification_score'],
        'treaty_count': portfolio['treaty_count']
    })

@app.route('/api/portfolio/metrics', methods=['GET'])
def get_portfolio_metrics():
    """Get detailed portfolio metrics"""
    portfolio = load_portfolio()
    optimizer = PortfolioOptimizer(portfolio)
    
    return jsonify({
        'rorac': round(optimizer.calculate_portfolio_rorac(), 2),
        'capital_efficiency': optimizer.calculate_capital_efficiency(),
        'top_treaties': optimizer.get_treaty_ranking('rorac')[:10],
        'lob_breakdown': portfolio['lob_breakdown'],
        'geography_breakdown': portfolio['geography_breakdown'],
        'performance_distribution': portfolio['performance_distribution']
    })

@app.route('/api/analyze-portfolio', methods=['POST'])
def analyze_portfolio():
    """Comprehensive portfolio analysis"""
    portfolio = load_portfolio()
    optimizer = PortfolioOptimizer(portfolio)
    
    return jsonify({
        'portfolio_state': {
            'portfolio_value': portfolio['portfolio_value'],
            'capital_utilization': portfolio['capital_utilization'],
            'avg_rorac': optimizer.calculate_portfolio_rorac()
        },
        'optimization_opportunities': optimizer.identify_optimization_opportunities()[:5],
        'capital_efficiency': optimizer.calculate_capital_efficiency(),
        'treaty_rankings': optimizer.get_treaty_ranking('rorac')[:10]
    })

@app.route('/api/scenario/simulate', methods=['POST'])
def run_scenario_simulation():
    """Run scenario analysis"""
    portfolio = load_portfolio()
    analyzer = ScenarioAnalyzer(portfolio)
    
    data = request.json or {}
    
    if data.get('simulation_type') == 'monte_carlo':
        simulations = data.get('simulations', 1000)
        return jsonify(analyzer.run_monte_carlo(simulations))
    
    elif data.get('simulation_type') == 'interest_rate':
        rate_change = data.get('rate_change', 50)  # basis points
        return jsonify(analyzer.stress_test_interest_rates(rate_change / 100))
    
    elif data.get('simulation_type') == 'catastrophe':
        event_type = data.get('event_type', 'hurricane')
        return_period = data.get('return_period', 200)
        return jsonify(analyzer.catastrophe_stress_test(event_type, return_period))
    
    else:
        return jsonify(analyzer.scenario_comparison())

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get portfolio recommendations"""
    portfolio = load_portfolio()
    engine = RecommendationEngine(portfolio)
    
    return jsonify(engine.generate_comprehensive_recommendations())

@app.route('/api/recommendations/portfolio-optimization', methods=['GET'])
def get_optimization_recommendations():
    """Get portfolio optimization recommendations"""
    portfolio = load_portfolio()
    optimizer = PortfolioOptimizer(portfolio)
    
    return jsonify(optimizer.optimize_allocation())

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'environment': os.getenv('AZURE_ENV', 'local')
    })

@app.route('/api/data/treaties', methods=['GET'])
def get_treaties():
    """Get all treaties data"""
    portfolio = load_portfolio()
    
    lob_filter = request.args.get('lob')
    geography_filter = request.args.get('geography')
    
    treaties = portfolio['treaties']
    
    if lob_filter:
        treaties = [t for t in treaties if t['lob'] == lob_filter]
    
    if geography_filter:
        treaties = [t for t in treaties if t['geography'] == geography_filter]
    
    return jsonify(treaties)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Load portfolio on startup
    load_portfolio()
    print("✅ Portfolio loaded successfully")
    print(f"   Timestamp: {PORTFOLIO_DATA['timestamp']}")
    print(f"   Portfolio Value: ${PORTFOLIO_DATA['portfolio_value']:,.0f}")
    print(f"   Treaties: {PORTFOLIO_DATA['treaty_count']}")
    print(f"   Capital Utilization: {PORTFOLIO_DATA['capital_utilization']:.1f}%")
    print(f"\n🚀 Starting Flask server on http://localhost:5001")
    
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5001)),
        debug=True if os.getenv('AZURE_ENV') != 'production' else False
    )
