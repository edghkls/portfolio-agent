"""
Recommendation Engine
Generates prioritized portfolio optimization recommendations
"""

from typing import List, Dict
from datetime import datetime
from engines.portfolio_optimizer import PortfolioOptimizer
from engines.scenario_analyzer import ScenarioAnalyzer

class RecommendationEngine:
    """Generate actionable recommendations for portfolio optimization"""
    
    def __init__(self, portfolio_data: Dict):
        """Initialize with portfolio data"""
        self.portfolio = portfolio_data
        self.optimizer = PortfolioOptimizer(portfolio_data)
        self.analyzer = ScenarioAnalyzer(portfolio_data)
    
    def generate_comprehensive_recommendations(self) -> Dict:
        """Generate all recommendations for portfolio"""
        
        recommendations = []
        
        # 1. Capital Efficiency Recommendations
        recommendations.extend(self._get_capital_efficiency_recommendations())
        
        # 2. Performance-based Recommendations
        recommendations.extend(self._get_performance_recommendations())
        
        # 3. Diversification Recommendations
        recommendations.extend(self._get_diversification_recommendations())
        
        # 4. Risk Management Recommendations
        recommendations.extend(self._get_risk_management_recommendations())
        
        # Sort by priority
        recommendations = sorted(
            recommendations,
            key=lambda x: {'High': 1, 'Medium': 2, 'Low': 3}[x['priority']]
        )
        
        return {
            'timestamp': datetime.now().isoformat(),
            'portfolio_state': self._get_portfolio_state(),
            'risk_assessment': self._get_risk_assessment(),
            'recommendations': recommendations,
            'executive_summary': self._get_executive_summary(recommendations)
        }
    
    def _get_portfolio_state(self) -> Dict:
        """Get current portfolio state"""
        return {
            'portfolio_value': round(self.portfolio['portfolio_value'], 2),
            'total_capital': round(self.portfolio['total_capital'], 2),
            'capital_utilization': round(self.portfolio['capital_utilization'], 2),
            'average_loss_ratio': round(self.portfolio['total_loss_ratio'], 4),
            'expected_profit': round(self.portfolio['expected_profit'], 2),
            'average_rorac': round(self.portfolio['avg_rorac'], 2),
            'treaty_count': self.portfolio['treaty_count'],
            'diversification_score': round(self.portfolio['diversification_score'], 2)
        }
    
    def _get_risk_assessment(self) -> Dict:
        """Get comprehensive risk assessment"""
        return {
            'capital_adequacy': 'Adequate' if self.portfolio['capital_utilization'] < 80 else 'Constrained',
            'capital_utilization_pct': round(self.portfolio['capital_utilization'], 1),
            'concentration_risk': 'Low' if self.portfolio['diversification_score'] > 0.6 else 'Medium' if self.portfolio['diversification_score'] > 0.4 else 'High',
            'performance_outlook': 'Positive' if self.portfolio['avg_rorac'] > 15 else 'Stable' if self.portfolio['avg_rorac'] > 10 else 'Under Pressure',
            'key_risks': [
                'Catastrophe exposure concentration',
                'Casualty line performance deterioration',
                'Interest rate sensitivity',
                'Capital consumption acceleration'
            ]
        }
    
    def _get_capital_efficiency_recommendations(self) -> List[Dict]:
        """Generate capital efficiency recommendations"""
        recommendations = []
        efficiency = self.optimizer.calculate_capital_efficiency()
        
        if efficiency['capital_efficiency_score'] < 12:
            recommendations.append({
                'id': 'CAP-001',
                'title': 'Improve Capital Efficiency',
                'priority': 'High',
                'business_justification': 'Capital efficiency below target threshold',
                'expected_impact': f"Improve RORAC by {min(5, 20 - self.portfolio['avg_rorac']):.1f}%",
                'capital_impact': f"Release ${abs(self.portfolio['total_capital'] * 0.1):,.0f} capital",
                'risk_impact': 'Low - operational improvements only',
                'regulatory_considerations': 'Improves Solvency II ratios',
                'suggested_timeline': 'Q2-Q3 2026',
                'supporting_data': {
                    'current_score': efficiency['capital_efficiency_score'],
                    'target_score': 15.0,
                    'premium_per_capital': efficiency['premium_per_capital_unit']
                },
                'confidence_score': 0.85
            })
        
        return recommendations
    
    def _get_performance_recommendations(self) -> List[Dict]:
        """Generate performance-based recommendations"""
        recommendations = []
        opportunities = self.optimizer.identify_optimization_opportunities()
        
        for opp in opportunities[:3]:  # Top 3 opportunities
            recommendations.append({
                'id': f"PERF-{opportunities.index(opp)+1:03d}",
                'title': f"Review {opp['treaty_id']}",
                'priority': opp['priority'],
                'business_justification': opp['reason'],
                'expected_impact': f"Improve expected profit by ${opp['expected_profit_improvement']:,.0f}",
                'capital_impact': f"Adjust capital by ${opp['capital_impact']:,.0f}",
                'risk_impact': 'Low - treaty-specific adjustment',
                'regulatory_considerations': 'No regulatory impact',
                'suggested_timeline': 'Q3 2026',
                'supporting_data': {
                    'treaty_id': opp['treaty_id'],
                    'premium_impact': opp['premium_impact'],
                    'profit_improvement': opp['expected_profit_improvement']
                },
                'confidence_score': 0.80
            })
        
        return recommendations
    
    def _get_diversification_recommendations(self) -> List[Dict]:
        """Generate diversification recommendations"""
        recommendations = []
        
        if self.portfolio['diversification_score'] < 0.6:
            lob_breakdown = self.portfolio['lob_breakdown']
            max_lob = max(lob_breakdown, key=lob_breakdown.get)
            max_pct = (lob_breakdown[max_lob] / self.portfolio['portfolio_value']) * 100
            
            recommendations.append({
                'id': 'DIV-001',
                'title': 'Improve Portfolio Diversification',
                'priority': 'Medium',
                'business_justification': f'{max_lob} represents {max_pct:.1f}% of portfolio - reduce concentration',
                'expected_impact': 'Improve diversification score by 0.15 points',
                'capital_impact': 'Minimal capital impact',
                'risk_impact': 'Reduces portfolio volatility and concentration risk',
                'regulatory_considerations': 'Better aligns with Pillar 2 requirements',
                'suggested_timeline': 'Q2-Q4 2026',
                'supporting_data': {
                    'current_diversification': self.portfolio['diversification_score'],
                    'target_diversification': 0.75,
                    'concentration_hot_spot': max_lob
                },
                'confidence_score': 0.75
            })
        
        return recommendations
    
    def _get_risk_management_recommendations(self) -> List[Dict]:
        """Generate risk management recommendations"""
        recommendations = []
        
        # Catastrophe scenario analysis
        cat_stress = self.analyzer.catastrophe_stress_test()
        
        recommendations.append({
            'id': 'RISK-001',
            'title': 'Enhance Catastrophe Risk Management',
            'priority': 'High',
            'business_justification': f"Portfolio has ${cat_stress['exposed_premium']:,.0f} catastrophe exposure",
            'expected_impact': f"Better manage potential losses of ${cat_stress['estimated_loss']:,.0f}",
            'capital_impact': f"Ensure ${cat_stress['impact_on_capital']:,.0f} capital available for cat events",
            'risk_impact': 'High - protects against major loss events',
            'regulatory_considerations': 'Aligns with Solvency II catastrophe stress test',
            'suggested_timeline': 'Q1-Q2 2026',
            'supporting_data': {
                'exposed_premium': cat_stress['exposed_premium'],
                'estimated_1_in_200_loss': cat_stress['estimated_loss'],
                'affected_treaties': cat_stress['treaties_affected']
            },
            'confidence_score': 0.90
        })
        
        return recommendations
    
    def _get_executive_summary(self, recommendations: List[Dict]) -> Dict:
        """Generate executive summary"""
        import re
        
        high_priority = sum(1 for r in recommendations if r['priority'] == 'High')
        total_capital_release = sum(
            float(str(r.get('capital_impact', '$0')).replace('$', '').replace(',', '')) 
            for r in recommendations if 'Release' in str(r.get('capital_impact', ''))
        )
        
        # Extract numeric values from expected_impact strings
        total_profit_improvement = 0
        for r in recommendations:
            impact_str = str(r.get('expected_impact', '0'))
            # Extract all numbers from the string
            numbers = re.findall(r'[-+]?\d*\.?\d+', impact_str)
            if numbers:
                # Take the first or largest numeric value found
                total_profit_improvement += float(numbers[0]) * 0.3
        
        return {
            'key_takeaway': f"{high_priority} high-priority actions to improve portfolio performance",
            'total_capital_opportunity': round(total_capital_release, 2),
            'total_profit_improvement': round(total_profit_improvement, 2),
            'recommended_focus_areas': [
                'Capital efficiency optimization',
                'Underperforming treaty review',
                'Portfolio diversification',
                'Catastrophe risk management'
            ],
            'next_steps': [
                'Review high-priority recommendations',
                'Schedule portfolio steering committee',
                'Initiate treaty renewal negotiations',
                'Update capital plan'
            ],
            'approval_required': 'Chief Underwriting Officer + Capital Management',
            'target_implementation': 'Q2-Q3 2026'
        }
