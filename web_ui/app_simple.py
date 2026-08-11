"""
Simple Portfolio Dashboard - Working Version
"""

from flask import Flask, render_template, jsonify, request
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from data_connectors.mock_portfolio import MockPortfolioGenerator
    from engines.scenario_analyzer import ScenarioAnalyzer
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")
    MockPortfolioGenerator = None
    ScenarioAnalyzer = None

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'portfolio-secret-key'

# Enable CORS with basic approach
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Global portfolio data
PORTFOLIO_DATA = None
CURRENT_FILTERS = {'lob': None, 'geography': None, 'sort': 'rorac'}

# Simple portfolio generator (fallback if imports fail)
class SimplePortfolioGenerator:
    @staticmethod
    def generate_portfolio():
        """Generate a simple mock portfolio"""
        import random
        random.seed(42)
        
        treaties = []
        lobs = ['Property', 'Casualty', 'Marine', 'Specialty', 'Reinsurance']
        geos = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Africa/ME']
        
        for i in range(50):
            lob = random.choice(lobs)
            geo = random.choice(geos)
            premium = random.uniform(1, 10) * 1e6
            rorac = random.uniform(150, 350)
            loss_ratio = random.uniform(35, 65)
            
            treaties.append({
                'id': f'TR-{lob[:3]}-{i+1:04d}',
                'lob': lob,
                'geography': geo,
                'premium': premium,
                'rorac': rorac,
                'loss_ratio': loss_ratio,
                'expected_profit': premium * (1 - loss_ratio/100) * (rorac/100)
            })
        
        portfolio_value = sum(t['premium'] for t in treaties)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'portfolio_value': portfolio_value,
            'capital_utilization': random.uniform(90, 105),
            'avg_rorac': random.uniform(200, 250),
            'diversification_score': random.uniform(0.7, 0.85),
            'treaties': treaties,
            'treaty_count': len(treaties),
            'lob_breakdown': {lob: sum(t['premium'] for t in treaties if t['lob'] == lob) for lob in lobs},
            'geography_breakdown': {geo: sum(t['premium'] for t in treaties if t['geography'] == geo) for geo in geos}
        }

# Simple scenario analyzer (fallback if imports fail)
class SimpleScenarioAnalyzer:
    def __init__(self, portfolio_data):
        self.portfolio = portfolio_data
        self.treaties = portfolio_data.get('treaties', [])
        import random
        random.seed(42)
    
    def run_monte_carlo(self, simulations=1000):
        """Run Monte Carlo simulation"""
        import random
        import statistics
        
        results = []
        for _ in range(simulations):
            total_loss = sum(random.gauss(t['premium'] * (t['loss_ratio']/100), t['premium'] * 0.1) for t in self.treaties)
            results.append(max(0, total_loss))
        
        results.sort()
        total_premium = sum(t['premium'] for t in self.treaties)
        mean_loss = statistics.mean(results)
        mean_profit = total_premium - mean_loss
        
        return {
            'loss_statistics': {
                'mean': mean_loss,
                'std': statistics.stdev(results) if len(results) > 1 else 0,
                'var_95': results[int(len(results) * 0.95)],
                'var_99': results[int(len(results) * 0.99)]
            },
            'profit_statistics': {
                'mean': mean_profit,
                'std': statistics.stdev([total_premium - r for r in results]) if len(results) > 1 else 0,
                'probability_loss': (sum(1 for r in results if r > total_premium) / len(results) * 100) if results else 0
            },
            'simulations': simulations
        }
    
    def stress_test_interest_rates(self, rate_change=50):
        """Stress test for interest rate changes"""
        portfolio_value = self.portfolio.get('portfolio_value', 0)
        rorac_impact = -rate_change / 10000 * 100  # Impact in basis points
        
        # Calculate LOB impacts
        lobs = {}
        for t in self.treaties:
            lob = t.get('lob', 'Unknown')
            if lob not in lobs:
                lobs[lob] = {'count': 0, 'premium': 0}
            lobs[lob]['count'] += 1
            lobs[lob]['premium'] += t['premium']
        
        lob_impacts = {}
        for lob, data in lobs.items():
            impact = data['premium'] * rorac_impact / 100
            lob_impacts[lob] = {
                'capital_impact': impact,
                'pct_change': rorac_impact
            }
        
        total_capital_impact = sum(v['capital_impact'] for v in lob_impacts.values())
        
        return {
            'scenario': f"Interest Rate Change: {'+' if rate_change >= 0 else ''}{rate_change} bps",
            'base_rorac': self.portfolio.get('avg_rorac', 200),
            'stressed_rorac': max(0, self.portfolio.get('avg_rorac', 200) + rorac_impact),
            'rorac_change': rorac_impact,
            'capital_impact': portfolio_value * (rorac_impact / 10000),
            'interest_rate_change_bps': rate_change,
            'total_capital_impact': total_capital_impact,
            'solvency_impact': 'Acceptable' if total_capital_impact > -portfolio_value * 0.2 else 'Critical',
            'lob_impacts': lob_impacts
        }
    
    def catastrophe_stress_test(self, event_type='hurricane', return_period=200):
        """Catastrophe event stress test"""
        portfolio_value = self.portfolio.get('portfolio_value', 0)
        loss_percentage = 100 / return_period
        estimated_loss = portfolio_value * (loss_percentage / 100)
        
        return {
            'event': f"{event_type.title()} ({return_period}-year event)",
            'return_period': return_period,
            'estimated_loss': estimated_loss,
            'portfolio_value': portfolio_value,
            'loss_percentage': loss_percentage,
            'impact_on_capital': estimated_loss * 0.7,
            'exposed_premium': portfolio_value * 0.85,
            'portfolio_impact': loss_percentage,
            'treaties_affected': max(1, int(len(self.treaties) * loss_percentage / 100)),
            'recovery_actions': [
                'Activate reinsurance recovery arrangements',
                'Implement claims triage and prioritization',
                'Engage alternative risk transfer solutions',
                'Accelerate premium collection'
            ]
        }
    
    def scenario_comparison(self):
        """Compare multiple scenarios with correct RORAC calculations"""
        total_premium = sum(t['premium'] for t in self.treaties)
        
        # Define scenarios with expected profits and capital required
        scenarios = [
            {
                'name': 'Base Case',
                'expected_profit': total_premium * 0.40,  # $102.75M
                'capital_required': 50000000,
                'probability': 0.40
            },
            {
                'name': 'Optimistic',
                'expected_profit': total_premium * 0.50,  # $128.44M
                'capital_required': 45000000,
                'probability': 0.25
            },
            {
                'name': 'Moderate Stress',
                'expected_profit': total_premium * 0.25,  # $64.22M
                'capital_required': 52000000,
                'probability': 0.25
            },
            {
                'name': 'Severe Stress',
                'expected_profit': total_premium * 0.10,  # $25.69M
                'capital_required': 60000000,
                'probability': 0.10
            }
        ]
        
        # Calculate RORAC correctly: (Expected Profit / Capital Required) × 100
        for scenario in scenarios:
            scenario['rorac'] = (scenario['expected_profit'] / scenario['capital_required']) * 100
        
        weighted_rorac = sum(s['rorac'] * s['probability'] for s in scenarios)
        weighted_profit = sum(s['expected_profit'] * s['probability'] for s in scenarios)
        
        return {
            'scenarios': scenarios,
            'expected_weighted_outcome': {
                'rorac': weighted_rorac,
                'expected_profit': weighted_profit
            }
        }

def load_portfolio():
    """Load portfolio data"""
    global PORTFOLIO_DATA
    if MockPortfolioGenerator:
        portfolio = MockPortfolioGenerator.generate_portfolio()
    else:
        portfolio = SimplePortfolioGenerator.generate_portfolio()
    PORTFOLIO_DATA = portfolio
    return PORTFOLIO_DATA

# ============ ROUTES ============

@app.route('/')
def dashboard():
    """Main dashboard"""
    print("\n=== ROUTE: dashboard ===")
    portfolio = load_portfolio()
    print(f"Portfolio loaded, rendering template: dashboard-enhanced.html")
    return render_template('dashboard-enhanced.html')

@app.route('/portfolio')
def portfolio_view():
    """Portfolio details view"""
    load_portfolio()
    return render_template('portfolio-dynamic.html')

@app.route('/scenarios')
def scenarios():
    """Scenarios page"""
    load_portfolio()
    return render_template('scenarios.html')

@app.route('/recommendations')
def recommendations():
    """Recommendations page"""
    load_portfolio()
    return render_template('recommendations.html')

@app.route('/reports')
def reports():
    """Reports page"""
    load_portfolio()
    return render_template('reports.html')

@app.route('/dashboard-enhanced')
def dashboard_enhanced():
    """Enhanced dashboard with new KPIs and charts"""
    load_portfolio()
    return render_template('dashboard-enhanced.html')

@app.route('/portfolio-health')
def portfolio_health():
    """Portfolio Health Executive Dashboard"""
    load_portfolio()
    return render_template('portfolio-health.html')

@app.route('/risk-return-optimization')
def risk_return_optimization():
    """Risk-Return Optimization Dashboard"""
    load_portfolio()
    return render_template('risk-return-optimization.html')

@app.route('/data-aggregation')
def data_aggregation():
    """Data Aggregation Dashboard"""
    load_portfolio()
    return render_template('data-aggregation.html')

@app.route('/deal-impact')
def deal_impact():
    """Deal Impact Assessment Dashboard"""
    load_portfolio()
    return render_template('deal-impact.html')

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
    """Get full portfolio with filters applied"""
    global CURRENT_FILTERS
    
    if PORTFOLIO_DATA is None:
        load_portfolio()
    
    treaties = PORTFOLIO_DATA.get('treaties', [])
    
    # Apply LOB filter
    if CURRENT_FILTERS.get('lob'):
        treaties = [t for t in treaties if t.get('lob') == CURRENT_FILTERS['lob']]
    
    # Apply Geography filter
    if CURRENT_FILTERS.get('geography'):
        treaties = [t for t in treaties if t.get('geography') == CURRENT_FILTERS['geography']]
    
    # Apply sorting
    sort_by = CURRENT_FILTERS.get('sort', 'rorac')
    if sort_by == 'rorac':
        treaties = sorted(treaties, key=lambda t: t.get('rorac', 0), reverse=True)
    elif sort_by == 'premium':
        treaties = sorted(treaties, key=lambda t: t.get('premium', 0), reverse=True)
    elif sort_by == 'profit':
        treaties = sorted(treaties, key=lambda t: t.get('expected_profit', 0), reverse=True)
    elif sort_by == 'loss_ratio':
        treaties = sorted(treaties, key=lambda t: t.get('loss_ratio', 0), reverse=False)
    
    lob_list = sorted(list(set(t.get('lob', '') for t in PORTFOLIO_DATA.get('treaties', []))))
    geo_list = sorted(list(set(t.get('geography', '') for t in PORTFOLIO_DATA.get('treaties', []))))
    
    return jsonify({
        'treaties': treaties,
        'lob_list': lob_list,
        'geography_list': geo_list,
        'treaty_count': len(treaties),
        'total_count': len(PORTFOLIO_DATA.get('treaties', []))
    })

@app.route('/api/filters/update', methods=['POST'])
def update_filters():
    """Update filter state"""
    global CURRENT_FILTERS
    try:
        data = request.get_json()
        
        # Update filters
        if 'lob' in data:
            CURRENT_FILTERS['lob'] = data['lob'] if data['lob'] else None
        if 'geography' in data:
            CURRENT_FILTERS['geography'] = data['geography'] if data['geography'] else None
        if 'sort' in data:
            CURRENT_FILTERS['sort'] = data['sort'] if data['sort'] else 'rorac'
        
        return jsonify({'status': 'ok', 'current_filters': CURRENT_FILTERS})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        
        # Initialize scenario analyzer (use fallback if import failed)
        if ScenarioAnalyzer:
            analyzer = ScenarioAnalyzer(PORTFOLIO_DATA)
        else:
            analyzer = SimpleScenarioAnalyzer(PORTFOLIO_DATA)
        
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
            results = comparison
        else:
            return jsonify({'error': f'Unknown simulation type: {simulation_type}'}), 400
        
        return jsonify(results)
    except Exception as e:
        import traceback
        print(f"ERROR in simulate_scenario: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio/enhanced', methods=['GET'])
def get_portfolio_enhanced():
    """Get enhanced KPIs for advanced dashboard"""
    try:
        if PORTFOLIO_DATA is None:
            load_portfolio()
        
        analyzer = ScenarioAnalyzer(PORTFOLIO_DATA)
        enhanced_metrics = analyzer.calculate_enhanced_metrics()
        
        return jsonify(enhanced_metrics)
    except Exception as e:
        import traceback
        print(f"ERROR in get_portfolio_enhanced: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-portfolio', methods=['POST'])
def analyze_portfolio():
    """Analyze portfolio and return optimization opportunities"""
    try:
        if PORTFOLIO_DATA is None:
            load_portfolio()
        
        analyzer = ScenarioAnalyzer(PORTFOLIO_DATA)
        enhanced = analyzer.calculate_enhanced_metrics()
        summary = PORTFOLIO_DATA
        
        # Get actual metrics for priority determination
        risk_concentration = enhanced.get('risk_concentration_index', 24)
        capital_util = enhanced.get('capital_utilization', 93)
        loss_ratio = enhanced.get('claims_ratio', 43.6)
        
        # Determine priority based on actual metrics
        concentration_priority = 'High' if risk_concentration > 30 else 'Medium' if risk_concentration > 20 else 'Low'
        capital_priority = 'High' if capital_util > 100 else 'Medium' if capital_util > 95 else 'Low'
        claims_priority = 'High' if loss_ratio > 65 else 'Medium' if loss_ratio > 55 else 'Low'
        
        # Identify optimization opportunities
        opportunities = [
            {
                'action': 'Rebalance Concentration Risk',
                'reason': f"Risk concentration at {risk_concentration:.1f}%. Diversify into underweighted LOBs to reduce below 20%.",
                'potential_impact': '$2.5M capital optimization',
                'priority': concentration_priority
            },
            {
                'action': 'Expand High-Performing Geographies',
                'reason': 'North America showing strongest profitability. Increase market share by 15-20% in this region.',
                'potential_impact': '$3.1M additional profit',
                'priority': 'Medium'
            },
            {
                'action': 'Optimize Claims Experience',
                'reason': f'Current loss ratio at {loss_ratio:.1f}%. Target improvement to 40% through better underwriting selection.',
                'potential_impact': '$1.8M profit improvement',
                'priority': claims_priority
            },
            {
                'action': 'Deploy Additional Capital',
                'reason': f"Capital utilization at {capital_util:.1f}%. Maintain optimal level (75-95%) while exploring higher-RORAC opportunities.",
                'potential_impact': '$500K efficiency gain',
                'priority': capital_priority
            }
        ]
        
        return jsonify({
            'optimization_opportunities': opportunities,
            'portfolio_health': 'Strong',
            'recommendation_count': len(opportunities)
        })
    except Exception as e:
        import traceback
        print(f"ERROR in analyze_portfolio: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'optimization_opportunities': []}), 500

# ============ WEBSOCKET EVENTS DISABLED ============
# Using basic Flask instead of WebSocket for simplicity

# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

# ============ AI AGENT ROUTES ============

@app.route('/chat')
def chat():
    """AI Agent Chat Interface"""
    load_portfolio()
    return render_template('agent-chat.html')

@app.route('/api/agent/chat', methods=['POST'])
def agent_chat():
    """Chat API endpoint for AI Agent"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'response': 'Please enter a message.'}), 400
        
        if PORTFOLIO_DATA is None:
            load_portfolio()
        
        # Try to use full agent, fallback to simple responses
        try:
            from engines.portfolio_agent import PortfolioAgent
            analyzer = ScenarioAnalyzer(PORTFOLIO_DATA) if ScenarioAnalyzer else None
            
            if analyzer and PortfolioAgent:
                agent = PortfolioAgent(analyzer)
                response = agent.process_query(user_message, PORTFOLIO_DATA, {})
            else:
                response = generate_fallback_response(user_message)
        except:
            response = generate_fallback_response(user_message)
        
        return jsonify({'response': response})
    except Exception as e:
        import traceback
        print(f"ERROR in agent_chat: {str(e)}")
        traceback.print_exc()
        return jsonify({'response': 'Unable to process your query at this time. Please try again.'}), 500

def generate_fallback_response(user_message):
    """Generate fallback responses for common portfolio queries"""
    if PORTFOLIO_DATA is None:
        return "Portfolio data is loading. Please try again in a moment."
    
    message_lower = user_message.lower()
    
    # Portfolio overview
    if 'top' in message_lower and 'performing' in message_lower:
        treaties = PORTFOLIO_DATA.get('treaties', [])
        top = sorted(treaties, key=lambda x: x.get('rorac', 0), reverse=True)[:5]
        summary = "Top 5 Performing Treaties:\n"
        for t in top:
            summary += f"• {t['id']}: RORAC {t.get('rorac', 0):.1f}%, Premium ${t.get('premium', 0)/1e6:.1f}M\n"
        return summary
    
    # Health score
    if 'health' in message_lower:
        portfolio_value = PORTFOLIO_DATA.get('portfolio_value', 0)
        capital_util = PORTFOLIO_DATA.get('capital_utilization', 0)
        rorac = PORTFOLIO_DATA.get('avg_rorac', 0)
        health_status = "Healthy 🟢" if capital_util < 100 and rorac > 150 else "Monitor 🟡" if capital_util < 110 else "Review ⚠️"
        return f"📊 Portfolio Health Score: {health_status}\n• Portfolio Value: ${portfolio_value/1e6:.1f}M\n• Capital Utilization: {capital_util:.1f}%\n• Average RORAC: {rorac:.1f}%"
    
    # Risk analysis
    if 'risk' in message_lower and 'analyz' in message_lower:
        diversif = PORTFOLIO_DATA.get('diversification_score', 0)
        lobs = PORTFOLIO_DATA.get('lob_breakdown', {})
        max_lob = max(lobs.items(), key=lambda x: x[1]) if lobs else ('Unknown', 0)
        risk_level = "Low" if diversif > 0.8 else "Medium" if diversif > 0.7 else "High"
        return f"⚠️ Risk Assessment:\n• Overall Risk Level: {risk_level}\n• Diversification Score: {diversif:.2f}/1.0\n• Largest LOB: {max_lob[0]} (${max_lob[1]/1e6:.1f}M)"
    
    # Current alerts
    if 'alert' in message_lower:
        capital_util = PORTFOLIO_DATA.get('capital_utilization', 0)
        alerts = []
        if capital_util > 100:
            alerts.append("⚠️ Capital utilization exceeds 100%")
        if capital_util < 75:
            alerts.append("💡 Consider deploying additional capital")
        diversif = PORTFOLIO_DATA.get('diversification_score', 0)
        if diversif < 0.7:
            alerts.append("🎯 Portfolio concentration is high - consider diversifying")
        if not alerts:
            alerts.append("✅ No critical alerts")
        return "🚨 Current Alerts:\n" + "\n".join(alerts)
    
    # Optimization strategies
    if 'optim' in message_lower and 'strateg' in message_lower:
        return "🚀 Optimization Strategies:\n1. Rebalance underperforming LOBs\n2. Deploy capital to high-RORAC treaties\n3. Diversify geographic concentration\n4. Review Marine segment for premium optimization\n5. Consider hedging strategies for volatile lines"
    
    # Benchmarks
    if 'benchmark' in message_lower:
        rorac = PORTFOLIO_DATA.get('avg_rorac', 200)
        industry_rorac = 220
        status = "Above" if rorac >= industry_rorac else "Below"
        return f"📈 Benchmark Comparison:\n• Your RORAC: {rorac:.1f}%\n• Industry Benchmark: {industry_rorac}%\n• Status: {status} industry average\n• Recommendation: Focus on premium quality and underwriting discipline"
    
    # Default helpful response
    return "👋 I can help you with:\n• Top performing treaties\n• Portfolio health score\n• Risk analysis\n• Current alerts\n• Optimization strategies\n• Benchmark comparisons\n\nWhat would you like to explore?"

@app.route('/api/portfolio/alerts', methods=['GET'])
def get_alerts():
    """Get portfolio alerts and anomalies"""
    try:
        from engines.anomaly_detector import AnomalyDetector
        
        if PORTFOLIO_DATA is None:
            load_portfolio()
        
        # Get enhanced metrics
        analyzer = ScenarioAnalyzer(PORTFOLIO_DATA)
        enhanced_metrics = analyzer.calculate_enhanced_metrics()
        
        # Detect anomalies
        detector = AnomalyDetector()
        alerts = detector.analyze_portfolio(PORTFOLIO_DATA, enhanced_metrics)
        
        # Format alerts for frontend
        formatted_alerts = []
        for alert in alerts:
            formatted_alerts.append({
                'message': alert['message'],
                'severity': alert['severity'],
                'type': alert['type']
            })
        
        return jsonify({
            'alerts': formatted_alerts,
            'severity_count': detector.get_severity_count()
        })
    except Exception as e:
        import traceback
        print(f"ERROR in get_alerts: {str(e)}")
        traceback.print_exc()
        return jsonify({'alerts': [], 'severity_count': {'danger': 0, 'warning': 0, 'success': 0}}), 200

# ==================== ADVANCED ANALYTICS ENDPOINTS ====================

@app.route('/data-aggregation')
def data_aggregation_view():
    """Data aggregation and normalization view"""
    load_portfolio()
    return render_template('data-aggregation.html')

@app.route('/portfolio-health')
def portfolio_health_view():
    """Portfolio health and composition analysis"""
    load_portfolio()
    return render_template('portfolio-health.html')

@app.route('/risk-return-optimization')
def risk_return_view():
    """Risk-return optimization analysis"""
    load_portfolio()
    return render_template('risk-return-optimization.html')

@app.route('/deal-impact')
def deal_impact_view():
    """Deal impact assessment"""
    load_portfolio()
    return render_template('deal-impact.html')

@app.route('/api/aggregated-portfolio', methods=['GET'])
def get_aggregated_portfolio():
    """Get aggregated and normalized portfolio data"""
    try:
        if PORTFOLIO_DATA is None:
            load_portfolio()
        
        treaties = PORTFOLIO_DATA.get('treaties', [])
        
        # Aggregate by Line of Business
        lob_data = {}
        for lob in ['Property', 'Casualty', 'Marine', 'Specialty', 'Reinsurance']:
            lob_treaties = [t for t in treaties if t.get('lob') == lob]
            total_premium = sum(t.get('premium', 0) for t in lob_treaties)
            avg_rorac = sum(t.get('rorac', 0) for t in lob_treaties) / len(lob_treaties) if lob_treaties else 0
            avg_loss_ratio = sum(t.get('loss_ratio', 0) for t in lob_treaties) / len(lob_treaties) if lob_treaties else 0
            
            lob_data[lob] = {
                'treaty_count': len(lob_treaties),
                'total_premium': total_premium,
                'avg_rorac': avg_rorac,
                'avg_loss_ratio': avg_loss_ratio,
                'combined_ratio': avg_loss_ratio + 15,  # expense ratio estimate
                'return_on_capital': (total_premium * (1 - avg_loss_ratio/100)) / (total_premium / 10) * 100 if total_premium > 0 else 0
            }
        
        # Aggregate by Geography
        geo_data = {}
        for geo in ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Africa/ME']:
            geo_treaties = [t for t in treaties if t.get('geography') == geo]
            total_premium = sum(t.get('premium', 0) for t in geo_treaties)
            avg_rorac = sum(t.get('rorac', 0) for t in geo_treaties) / len(geo_treaties) if geo_treaties else 0
            
            geo_data[geo] = {
                'treaty_count': len(geo_treaties),
                'total_premium': total_premium,
                'avg_rorac': avg_rorac,
                'exposure_concentration': (total_premium / PORTFOLIO_DATA.get('portfolio_value', 1)) * 100
            }
        
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'total_portfolio_value': PORTFOLIO_DATA.get('portfolio_value', 0),
            'total_treaties': len(treaties),
            'lob_aggregation': lob_data,
            'geography_aggregation': geo_data,
            'capital_allocation': {
                'total_capital': PORTFOLIO_DATA.get('portfolio_value', 0) * 0.25,
                'utilized_capital': PORTFOLIO_DATA.get('portfolio_value', 0) * (PORTFOLIO_DATA.get('capital_utilization', 90) / 100),
                'available_capital': PORTFOLIO_DATA.get('portfolio_value', 0) * (1 - PORTFOLIO_DATA.get('capital_utilization', 90) / 100)
            }
        })
    except Exception as e:
        import traceback
        print(f"ERROR in get_aggregated_portfolio: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio-health', methods=['GET'])
def get_portfolio_health():
    """Get portfolio health metrics and analysis"""
    try:
        if PORTFOLIO_DATA is None:
            load_portfolio()
        
        treaties = PORTFOLIO_DATA.get('treaties', [])
        
        # Calculate portfolio metrics
        total_premium = PORTFOLIO_DATA.get('portfolio_value', 0)
        avg_loss_ratio = sum(t.get('loss_ratio', 0) for t in treaties) / len(treaties) if treaties else 0
        combined_ratio = avg_loss_ratio + 12  # expense ratio
        avg_rorac = PORTFOLIO_DATA.get('avg_rorac', 200)
        
        # Health status determination
        health_score = 100
        if combined_ratio > 100:
            health_score -= (combined_ratio - 100) * 2
        if PORTFOLIO_DATA.get('capital_utilization', 90) > 100:
            health_score -= 20
        
        health_status = 'Excellent' if health_score > 80 else 'Good' if health_score > 60 else 'Fair' if health_score > 40 else 'Poor'
        
        # Premium mix analysis
        lob_breakdown = {}
        for lob in ['Property', 'Casualty', 'Marine', 'Specialty', 'Reinsurance']:
            lob_premium = sum(t.get('premium', 0) for t in treaties if t.get('lob') == lob)
            lob_breakdown[lob] = (lob_premium / total_premium * 100) if total_premium > 0 else 0
        
        return jsonify({
            'health_score': max(0, health_score),
            'health_status': health_status,
            'combined_ratio': combined_ratio,
            'expected_loss_ratio': avg_loss_ratio,
            'return_on_capital': avg_rorac,
            'premium_mix': lob_breakdown,
            'capital_utilization': PORTFOLIO_DATA.get('capital_utilization', 90),
            'diversification_score': PORTFOLIO_DATA.get('diversification_score', 0.76),
            'key_risks': [
                {'risk': 'Concentration Risk', 'level': 'Medium', 'description': 'Casualty segment represents 25% of premium'},
                {'risk': 'Catastrophe Exposure', 'level': 'Medium', 'description': 'Property segment CAT exposure at historical average'},
                {'risk': 'Capital Utilization', 'level': 'High' if PORTFOLIO_DATA.get('capital_utilization', 90) > 95 else 'Medium', 'description': 'Capital deployment efficiency acceptable'}
            ]
        })
    except Exception as e:
        import traceback
        print(f"ERROR in get_portfolio_health: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/risk-return-analysis', methods=['GET'])
def get_risk_return_analysis():
    """Get risk-return optimization analysis"""
    try:
        if PORTFOLIO_DATA is None:
            load_portfolio()
        
        treaties = PORTFOLIO_DATA.get('treaties', [])
        
        # Analyze each LOB segment
        segments = {}
        for lob in ['Property', 'Casualty', 'Marine', 'Specialty', 'Reinsurance']:
            lob_treaties = [t for t in treaties if t.get('lob') == lob]
            if not lob_treaties:
                continue
            
            total_premium = sum(t.get('premium', 0) for t in lob_treaties)
            avg_rorac = sum(t.get('rorac', 0) for t in lob_treaties) / len(lob_treaties)
            avg_loss_ratio = sum(t.get('loss_ratio', 0) for t in lob_treaties) / len(lob_treaties)
            capital_required = total_premium / 10  # simplified capital model
            
            segments[lob] = {
                'expected_return': avg_rorac,
                'capital_usage': (capital_required / PORTFOLIO_DATA.get('portfolio_value', 1)) * 100,
                'tail_risk_load': 5 + (avg_loss_ratio / 10),  # simplified tail risk
                'diversification_value': 1.0 if lob != 'Property' else 0.85,
                'efficiency_score': (avg_rorac / 100) - (avg_loss_ratio / 100),
                'recommendation': 'Maintain' if avg_rorac > 200 else 'Review' if avg_rorac > 150 else 'Reduce'
            }
        
        return jsonify({
            'segments': segments,
            'efficient_frontier': {
                'min_return': min(s['expected_return'] for s in segments.values()) if segments else 0,
                'max_return': max(s['expected_return'] for s in segments.values()) if segments else 0,
                'portfolio_return': PORTFOLIO_DATA.get('avg_rorac', 200),
                'portfolio_risk': 100 - (PORTFOLIO_DATA.get('diversification_score', 0.76) * 100)
            }
        })
    except Exception as e:
        import traceback
        print(f"ERROR in get_risk_return_analysis: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/deal-impact-assessment', methods=['POST'])
def assess_deal_impact():
    """Assess impact of new deals on portfolio"""
    try:
        data = request.get_json()
        
        # Deal parameters
        deal_premium = data.get('premium', 5000000)
        deal_rorac = data.get('rorac', 200)
        deal_lob = data.get('lob', 'Property')
        deal_capital_req = deal_premium / 10
        
        if PORTFOLIO_DATA is None:
            load_portfolio()
        
        current_portfolio_value = PORTFOLIO_DATA.get('portfolio_value', 0)
        current_capital_util = PORTFOLIO_DATA.get('capital_utilization', 90)
        current_rorac = PORTFOLIO_DATA.get('avg_rorac', 200)
        
        # Calculate impact
        new_portfolio_value = current_portfolio_value + deal_premium
        new_capital_util = ((current_portfolio_value * current_capital_util / 100) + deal_capital_req) / (new_portfolio_value * 0.25) * 100
        new_rorac = ((current_portfolio_value * current_rorac) + (deal_premium * deal_rorac)) / new_portfolio_value
        
        impact_assessment = {
            'deal_premium': deal_premium,
            'deal_rorac': deal_rorac,
            'deal_lob': deal_lob,
            'standalone_metrics': {
                'premium': deal_premium,
                'rorac': deal_rorac,
                'capital_required': deal_capital_req
            },
            'portfolio_impact': {
                'portfolio_value_change': deal_premium,
                'portfolio_value_pct_change': (deal_premium / current_portfolio_value) * 100,
                'capital_utilization_change': new_capital_util - current_capital_util,
                'rorac_change': new_rorac - current_rorac,
                'new_portfolio_rorac': new_rorac,
                'new_capital_utilization': new_capital_util
            },
            'recommendation': 'Accept' if new_rorac > 200 and new_capital_util < 100 else 'Review' if new_rorac > 150 else 'Decline',
            'rationale': 'Attractive returns with good capital efficiency' if new_rorac > 200 else 'Moderate returns, acceptable capital impact' if new_rorac > 150 else 'Below target returns'
        }
        
        return jsonify(impact_assessment)
    except Exception as e:
        import traceback
        print(f"ERROR in assess_deal_impact: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

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
    print(f"   Real-time updates via API polling")
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
