"""
Anomaly Detection Engine for Portfolio Optimisation Agent
Detects unusual portfolio behavior and triggers alerts
"""

import numpy as np
from datetime import datetime

class AnomalyDetector:
    """Detects anomalies in portfolio metrics and generates alerts"""
    
    def __init__(self):
        self.alerts = []
        self.thresholds = {
            'capital_utilization': {'min': 60, 'max': 95},
            'claims_ratio': {'min': 0, 'max': 60},
            'rorac': {'min': 15},
            'diversification': {'min': 0.65},
            'loss_concentration': {'max': 0.4}
        }
    
    def analyze_portfolio(self, portfolio_data, enhanced_metrics):
        """
        Analyze portfolio and detect anomalies
        Returns list of alerts
        """
        self.alerts = []
        
        # Check capital utilization
        cu = portfolio_data.get('capital_utilization', 0)
        if cu > self.thresholds['capital_utilization']['max']:
            self.alerts.append({
                'severity': 'warning',
                'type': 'capital_utilization',
                'message': f'⚠️ Capital Utilization High: {cu:.1f}% (threshold: {self.thresholds["capital_utilization"]["max"]}%)',
                'value': cu,
                'recommendation': 'Consider reducing exposure or increasing capital'
            })
        
        # Check claims ratio
        cr = enhanced_metrics.get('claims_ratio', 0)
        if cr > self.thresholds['claims_ratio']['max']:
            self.alerts.append({
                'severity': 'danger',
                'type': 'claims_ratio',
                'message': f'🚨 Claims Ratio Elevated: {cr:.1f}% (threshold: {self.thresholds["claims_ratio"]["max"]}%)',
                'value': cr,
                'recommendation': 'Review underwriting performance and loss control'
            })
        
        # Check RORAC
        rorac = portfolio_data.get('average_rorac', 0)
        if rorac < self.thresholds['rorac']['min']:
            self.alerts.append({
                'severity': 'warning',
                'type': 'rorac',
                'message': f'⚠️ RORAC Below Target: {rorac:.1f}% (target: {self.thresholds["rorac"]["min"]}%)',
                'value': rorac,
                'recommendation': 'Portfolio profitability is below acceptable levels'
            })
        
        # Check diversification
        ds = portfolio_data.get('diversification_score', 0)
        if ds < self.thresholds['diversification']['min']:
            self.alerts.append({
                'severity': 'warning',
                'type': 'diversification',
                'message': f'⚠️ Concentration Risk: Diversification Score {ds:.2f} (threshold: {self.thresholds["diversification"]["min"]})',
                'value': ds,
                'recommendation': 'Portfolio is not well diversified. Rebalance across LOBs/geographies'
            })
        
        # Analyze LOB concentration
        lob_breakdown = portfolio_data.get('lob_breakdown', {})
        if lob_breakdown:
            total = sum(lob_breakdown.values())
            max_concentration = max(lob_breakdown.values()) / total if total > 0 else 0
            
            if max_concentration > 0.4:
                max_lob = max(lob_breakdown, key=lob_breakdown.get)
                self.alerts.append({
                    'severity': 'warning',
                    'type': 'lob_concentration',
                    'message': f'⚠️ LOB Concentration: {max_lob} represents {max_concentration*100:.1f}% of portfolio',
                    'value': max_concentration,
                    'recommendation': 'Reduce concentration in single LOB'
                })
        
        # Analyze geography concentration
        geo_breakdown = portfolio_data.get('geography_breakdown', {})
        if geo_breakdown:
            total = sum(geo_breakdown.values())
            max_concentration = max(geo_breakdown.values()) / total if total > 0 else 0
            
            if max_concentration > 0.35:
                max_geo = max(geo_breakdown, key=geo_breakdown.get)
                self.alerts.append({
                    'severity': 'warning',
                    'type': 'geo_concentration',
                    'message': f'⚠️ Geography Concentration: {max_geo} represents {max_concentration*100:.1f}% of portfolio',
                    'value': max_concentration,
                    'recommendation': 'Diversify across additional geographies'
                })
        
        # Check for positive indicators
        if cu < 90 and cr < 50 and rorac > 200 and ds > 0.75:
            self.alerts.append({
                'severity': 'success',
                'type': 'portfolio_health',
                'message': '✅ Portfolio Health: Excellent. All metrics within healthy ranges.',
                'value': 1.0,
                'recommendation': 'Maintain current portfolio structure'
            })
        
        return self.alerts
    
    def get_anomalies(self):
        """Return current anomalies/alerts"""
        return self.alerts
    
    def get_severity_count(self):
        """Get count by severity level"""
        return {
            'danger': len([a for a in self.alerts if a['severity'] == 'danger']),
            'warning': len([a for a in self.alerts if a['severity'] == 'warning']),
            'success': len([a for a in self.alerts if a['severity'] == 'success'])
        }
    
    def get_recommendations(self):
        """Get all recommendations from alerts"""
        return [a.get('recommendation', '') for a in self.alerts if a.get('recommendation')]
