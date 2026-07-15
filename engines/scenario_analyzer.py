"""
Scenario Analysis Engine
Monte Carlo simulations, stress testing, and what-if analysis
"""

import numpy as np
import pandas as pd
from typing import Dict, List
from datetime import datetime

class ScenarioAnalyzer:
    """Perform scenario analysis on reinsurance portfolio"""
    
    def __init__(self, portfolio_data: Dict):
        """Initialize with portfolio data"""
        self.portfolio = portfolio_data
        self.treaties = pd.DataFrame(portfolio_data['treaties'])
    
    def run_monte_carlo(self, simulations: int = 1000) -> Dict:
        """Run Monte Carlo simulation for portfolio outcomes"""
        results = {
            'expected_loss': [],
            'expected_profit': [],
            'capital_required': []
        }
        
        for _ in range(simulations):
            # Simulate loss ratios based on historical distribution
            simulated_loss_ratio = np.random.beta(
                a=5,  # Shape parameter
                b=10,  # Shape parameter (higher b = lower average loss ratio)
                size=len(self.treaties)
            ) * 0.8  # Cap at 80% loss ratio
            
            simulated_losses = self.treaties['premium'].values * simulated_loss_ratio
            simulated_profit = (self.treaties['premium'].values - simulated_losses)
            
            results['expected_loss'].append(simulated_losses.sum())
            results['expected_profit'].append(simulated_profit.sum())
            results['capital_required'].append(simulated_profit.std() * 2.33)  # 99% confidence
        
        return self._summarize_monte_carlo(results)
    
    def _summarize_monte_carlo(self, results: Dict) -> Dict:
        """Summarize Monte Carlo results"""
        return {
            'loss_statistics': {
                'mean': round(np.mean(results['expected_loss']), 2),
                'std': round(np.std(results['expected_loss']), 2),
                'percentile_5': round(np.percentile(results['expected_loss'], 5), 2),
                'percentile_95': round(np.percentile(results['expected_loss'], 95), 2),
                'var_99': round(np.percentile(results['expected_loss'], 99), 2),
            },
            'profit_statistics': {
                'mean': round(np.mean(results['expected_profit']), 2),
                'std': round(np.std(results['expected_profit']), 2),
                'percentile_5': round(np.percentile(results['expected_profit'], 5), 2),
                'percentile_95': round(np.percentile(results['expected_profit'], 95), 2),
                'probability_loss': round(sum(1 for x in results['expected_profit'] if x < 0) / len(results['expected_profit']) * 100, 2)
            }
        }
    
    def stress_test_interest_rates(self, rate_change: float) -> Dict:
        """Simulate interest rate change impact"""
        """
        Simulate interest rate impact on:
        - Bond portfolio values (if any)
        - Discount rates for liabilities
        - Equity valuations
        """
        
        # Estimate impact based on LOB sensitivity
        interest_rate_sensitivity = {
            'Property Catastrophe': 0.15,
            'Casualty': 0.25,  # More sensitive due to longer tails
            'Marine & Aviation': 0.12,
            'Financial Lines': 0.20,
            'Specialty': 0.18
        }
        
        impact = {}
        total_capital_impact = 0
        
        for lob in self.treaties['lob'].unique():
            lob_treaties = self.treaties[self.treaties['lob'] == lob]
            sensitivity = interest_rate_sensitivity.get(lob, 0.15)
            
            lob_capital = lob_treaties['capital_requirement'].sum()
            capital_impact = lob_capital * sensitivity * rate_change / 100
            total_capital_impact += capital_impact
            
            impact[lob] = {
                'capital_impact': round(capital_impact, 2),
                'pct_change': round((capital_impact / lob_capital) * 100, 2)
            }
        
        return {
            'scenario': f'{rate_change:+.0f} bps interest rate change',
            'lob_impacts': impact,
            'total_capital_impact': round(total_capital_impact, 2),
            'solvency_impact': 'Positive' if total_capital_impact > 0 else 'Negative'
        }
    
    def catastrophe_stress_test(self, event_type: str = 'hurricane', return_period: int = 200) -> Dict:
        """Simulate catastrophe event impact"""
        cat_exposure = self.treaties[self.treaties['cat_exposed'] == True]
        
        # Estimate losses based on return period
        # Simplified: 1-in-200 year event causes 20% loss on exposed premium
        loss_severity = 0.20 if return_period == 200 else 0.50
        
        exposed_premium = cat_exposure['premium'].sum()
        estimated_loss = exposed_premium * loss_severity
        
        return {
            'event': f'{event_type.title()} - {return_period}-year return period',
            'exposed_premium': round(exposed_premium, 2),
            'estimated_loss': round(estimated_loss, 2),
            'impact_on_capital': round(estimated_loss * 0.9, 2),  # 90% of loss affects capital
            'portfolio_impact': round((estimated_loss / self.portfolio['portfolio_value']) * 100, 2),
            'treaties_affected': len(cat_exposure),
            'recovery_actions': [
                'Activate retrocession coverage',
                'Review capital adequacy',
                'Consider capital raise',
                'Adjust underwriting guidelines'
            ]
        }
    
    def scenario_comparison(self) -> Dict:
        """Compare outcomes across multiple scenarios"""
        base_case = {
            'name': 'Base Case',
            'description': 'Current portfolio, no major changes',
            'expected_profit': self.portfolio['portfolio_value'] * 0.25 - sum(t['incurred_loss'] for t in self.portfolio['treaties']),
            'capital_required': self.portfolio['total_capital'],
            'rorac': self.portfolio['avg_rorac'],
            'probability': 0.50
        }
        
        optimistic_case = {
            'name': 'Optimistic Case',
            'description': 'Better loss experience, market improvements',
            'expected_profit': base_case['expected_profit'] * 1.3,
            'capital_required': base_case['capital_required'] * 0.9,
            'rorac': base_case['rorac'] * 1.25,
            'probability': 0.25
        }
        
        stress_case = {
            'name': 'Moderate Stress',
            'description': 'Elevated losses, market volatility',
            'expected_profit': base_case['expected_profit'] * 0.6,
            'capital_required': base_case['capital_required'] * 1.15,
            'rorac': base_case['rorac'] * 0.65,
            'probability': 0.20
        }
        
        severe_case = {
            'name': 'Severe Stress',
            'description': 'Major catastrophe event, severe losses',
            'expected_profit': base_case['expected_profit'] * -0.5,
            'capital_required': base_case['capital_required'] * 2.0,
            'rorac': -25,
            'probability': 0.05
        }
        
        scenarios = [base_case, optimistic_case, stress_case, severe_case]
        
        return {
            'timestamp': datetime.now().isoformat(),
            'scenarios': scenarios,
            'expected_weighted_outcome': {
                'profit': round(sum(s['expected_profit'] * s['probability'] for s in scenarios), 2),
                'capital': round(sum(s['capital_required'] * s['probability'] for s in scenarios), 2),
                'rorac': round(sum(s['rorac'] * s['probability'] for s in scenarios), 2)
            }
        }
