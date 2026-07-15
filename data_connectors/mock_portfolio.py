"""
Mock Portfolio Data Generator
Generates realistic reinsurance portfolio data for testing and development
"""

import json
import random
from datetime import datetime, timedelta
import pandas as pd

class MockPortfolioGenerator:
    """Generate mock reinsurance portfolio data"""
    
    LOB_PARAMS = {
        'Property Catastrophe': {
            'premium_range': (100_000, 5_000_000),
            'loss_ratio_range': (0.15, 0.45),
            'cat_exposure': True,
            'count': 15
        },
        'Casualty': {
            'premium_range': (50_000, 1_000_000),
            'loss_ratio_range': (0.50, 0.75),
            'cat_exposure': False,
            'count': 12
        },
        'Marine & Aviation': {
            'premium_range': (75_000, 2_000_000),
            'loss_ratio_range': (0.30, 0.60),
            'cat_exposure': True,
            'count': 10
        },
        'Financial Lines': {
            'premium_range': (40_000, 800_000),
            'loss_ratio_range': (0.20, 0.50),
            'cat_exposure': False,
            'count': 8
        },
        'Specialty': {
            'premium_range': (60_000, 1_500_000),
            'loss_ratio_range': (0.25, 0.55),
            'cat_exposure': False,
            'count': 5
        }
    }
    
    GEOGRAPHIES = [
        'North America', 'Europe', 'Asia Pacific', 'Latin America', 'Africa/Middle East'
    ]
    
    TREATY_TYPES = ['Quota Share', 'Excess of Loss', 'Proportional', 'Cat XL', 'Stop Loss']
    
    @staticmethod
    def generate_portfolio(treaty_count=50):
        """Generate complete mock portfolio"""
        treaties = []
        
        for lob, params in MockPortfolioGenerator.LOB_PARAMS.items():
            for i in range(params['count']):
                treaty = MockPortfolioGenerator.generate_treaty(
                    lob=lob,
                    treaty_id=f"TR-{lob[0:3]}-{i+1:04d}",
                    params=params
                )
                treaties.append(treaty)
        
        return MockPortfolioGenerator._create_portfolio_summary(treaties)
    
    @staticmethod
    def generate_treaty(lob, treaty_id, params):
        """Generate single treaty data"""
        premium = random.uniform(params['premium_range'][0], params['premium_range'][1])
        loss_ratio = random.uniform(params['loss_ratio_range'][0], params['loss_ratio_range'][1])
        
        return {
            'treaty_id': treaty_id,
            'lob': lob,
            'geography': random.choice(MockPortfolioGenerator.GEOGRAPHIES),
            'treaty_type': random.choice(MockPortfolioGenerator.TREATY_TYPES),
            'premium': round(premium, 2),
            'incurred_loss': round(premium * loss_ratio, 2),
            'earned_premium': round(premium * random.uniform(0.6, 1.0), 2),
            'loss_ratio': round(loss_ratio, 4),
            'ceded_premium': round(premium * random.uniform(0.3, 0.8), 2),
            'capital_requirement': round(premium * random.uniform(0.15, 0.35), 2),
            'expected_profit': round(premium * (1 - loss_ratio) * random.uniform(0.7, 1.2), 2),
            'rorac': round(((premium - (premium * loss_ratio)) / (premium * 0.25)) * 100, 2),
            'cat_exposed': params['cat_exposure'],
            'concentration_score': round(random.uniform(0.1, 0.9), 2),
            'renewal_date': (datetime.now() + timedelta(days=random.randint(1, 180))).strftime('%Y-%m-%d'),
            'underwriter': f"UW-{random.randint(1, 20):03d}",
            'rating': random.choice(['AAA', 'AA', 'A', 'BBB', 'BB']),
            'performance_status': random.choice(['Excellent', 'Good', 'Adequate', 'Watch', 'Poor'])
        }
    
    @staticmethod
    def _create_portfolio_summary(treaties):
        """Create portfolio-level summary metrics"""
        df = pd.DataFrame(treaties)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'portfolio_value': round(df['premium'].sum(), 2),
            'total_loss_ratio': round(df['incurred_loss'].sum() / df['premium'].sum(), 4),
            'total_capital': round(df['capital_requirement'].sum(), 2),
            'capital_utilization': round((df['capital_requirement'].sum() / (df['premium'].sum() * 0.25)) * 100, 2),
            'expected_profit': round(df['expected_profit'].sum(), 2),
            'avg_rorac': round(df['rorac'].mean(), 2),
            'diversification_score': round(1 - (df.groupby('lob')['premium'].sum().std() / df['premium'].sum()), 2),
            'treaties': treaties,
            'treaty_count': len(treaties),
            'lob_breakdown': df.groupby('lob')['premium'].sum().to_dict(),
            'geography_breakdown': df.groupby('geography')['premium'].sum().to_dict(),
            'performance_distribution': df['performance_status'].value_counts().to_dict()
        }

if __name__ == '__main__':
    # Generate and save sample portfolio
    portfolio = MockPortfolioGenerator.generate_portfolio()
    
    with open('mock_portfolio.json', 'w') as f:
        json.dump(portfolio, f, indent=2)
    
    print(f"✅ Generated mock portfolio with {portfolio['treaty_count']} treaties")
    print(f"   Portfolio Value: ${portfolio['portfolio_value']:,.0f}")
    print(f"   Capital Utilization: {portfolio['capital_utilization']:.1f}%")
    print(f"   Average RORAC: {portfolio['avg_rorac']:.1f}%")
