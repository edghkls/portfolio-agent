"""
Portfolio Optimization Engine
Calculates RORAC, capital efficiency, and optimization recommendations
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

class PortfolioOptimizer:
    """Optimize reinsurance portfolio allocation"""
    
    def __init__(self, portfolio_data: Dict):
        """Initialize with portfolio data"""
        self.portfolio = portfolio_data
        self.treaties = pd.DataFrame(portfolio_data['treaties'])
    
    def calculate_rorac(self, treaty: Dict) -> float:
        """Calculate Return on Risk-Adjusted Capital"""
        expected_return = treaty['expected_profit']
        capital = treaty['capital_requirement']
        
        if capital == 0:
            return 0
        
        return (expected_return / capital) * 100
    
    def calculate_portfolio_rorac(self) -> float:
        """Calculate portfolio-level RORAC"""
        total_return = self.treaties['expected_profit'].sum()
        total_capital = self.treaties['capital_requirement'].sum()
        
        if total_capital == 0:
            return 0
        
        return (total_return / total_capital) * 100
    
    def identify_optimization_opportunities(self) -> List[Dict]:
        """Identify treaties for optimization"""
        opportunities = []
        
        # Find underperforming treaties
        portfolio_rorac = self.calculate_portfolio_rorac()
        
        for _, treaty in self.treaties.iterrows():
            treaty_rorac = self.calculate_rorac(treaty)
            
            if treaty_rorac < portfolio_rorac * 0.8:  # 20% below average
                opportunities.append({
                    'treaty_id': treaty['treaty_id'],
                    'action': 'Consider reduction or exit',
                    'reason': f'RORAC {treaty_rorac:.1f}% below portfolio average',
                    'priority': 'High' if treaty_rorac < portfolio_rorac * 0.6 else 'Medium',
                    'capital_impact': treaty['capital_requirement'],
                    'premium_impact': treaty['premium'],
                    'expected_profit_improvement': treaty['premium'] * 0.15  # Estimated 15% improvement
                })
        
        # Identify concentration risks
        lob_concentration = self.treaties.groupby('lob')['premium'].sum() / self.treaties['premium'].sum()
        
        for lob, concentration in lob_concentration.items():
            if concentration > 0.4:  # More than 40% in single LOB
                opportunities.append({
                    'treaty_id': f'LOB-{lob}',
                    'action': 'Diversify away from concentration',
                    'reason': f'{lob} represents {concentration*100:.1f}% of portfolio',
                    'priority': 'Medium',
                    'capital_impact': -self.treaties[self.treaties['lob'] == lob]['capital_requirement'].sum() * 0.1,
                    'premium_impact': -self.treaties[self.treaties['lob'] == lob]['premium'].sum() * 0.1,
                    'expected_profit_improvement': self.treaties[self.treaties['lob'] == lob]['premium'].sum() * 0.1 * 0.25
                })
        
        return sorted(opportunities, key=lambda x: {'High': 1, 'Medium': 2, 'Low': 3}[x['priority']])
    
    def optimize_allocation(self, target_rorac: float = None) -> Dict:
        """Recommend optimal portfolio allocation"""
        if target_rorac is None:
            target_rorac = self.calculate_portfolio_rorac() * 1.1  # 10% improvement target
        
        current_rorac = self.calculate_portfolio_rorac()
        
        recommendations = self.identify_optimization_opportunities()
        
        return {
            'current_rorac': round(current_rorac, 2),
            'target_rorac': round(target_rorac, 2),
            'rorac_improvement': round(target_rorac - current_rorac, 2),
            'recommendations': recommendations,
            'estimated_capital_release': round(sum(r.get('capital_impact', 0) for r in recommendations if r.get('capital_impact', 0) < 0), 2),
            'estimated_profit_impact': round(sum(r.get('expected_profit_improvement', 0) for r in recommendations), 2)
        }
    
    def calculate_capital_efficiency(self) -> Dict:
        """Calculate capital efficiency metrics"""
        total_premium = self.treaties['premium'].sum()
        total_capital = self.treaties['capital_requirement'].sum()
        total_profit = self.treaties['expected_profit'].sum()
        
        return {
            'premium_per_capital_unit': round(total_premium / total_capital, 2),
            'profit_per_capital_unit': round(total_profit / total_capital, 2),
            'capital_efficiency_score': round((total_profit / total_capital) * 100, 2),
            'premium_to_capital_ratio': round(total_premium / total_capital, 2)
        }
    
    def get_treaty_ranking(self, metric: str = 'rorac') -> List[Dict]:
        """Rank treaties by specified metric"""
        if metric == 'rorac':
            self.treaties['metric_value'] = self.treaties.apply(
                lambda x: self.calculate_rorac(x), axis=1
            )
        elif metric == 'profit':
            self.treaties['metric_value'] = self.treaties['expected_profit']
        elif metric == 'premium':
            self.treaties['metric_value'] = self.treaties['premium']
        else:
            return []
        
        ranked = self.treaties.nlargest(20, 'metric_value')[['treaty_id', 'lob', 'metric_value']].to_dict('records')
        
        return ranked
