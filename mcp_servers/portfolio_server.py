"""
MCP Portfolio Data Server
Provides portfolio data through Model Context Protocol
"""

import json
from data_connectors.mock_portfolio import MockPortfolioGenerator

class PortfolioDataServer:
    """MCP server for portfolio data access"""
    
    def __init__(self):
        self.portfolio = MockPortfolioGenerator.generate_portfolio()
    
    def get_portfolio_summary(self):
        """Get portfolio summary"""
        return {
            'portfolio_value': self.portfolio['portfolio_value'],
            'capital_utilization': self.portfolio['capital_utilization'],
            'avg_rorac': self.portfolio['avg_rorac'],
            'treaty_count': self.portfolio['treaty_count'],
            'lob_breakdown': self.portfolio['lob_breakdown']
        }
    
    def get_treaties(self, lob=None, geography=None):
        """Get treaties filtered by LOB or geography"""
        treaties = self.portfolio['treaties']
        
        if lob:
            treaties = [t for t in treaties if t['lob'] == lob]
        if geography:
            treaties = [t for t in treaties if t['geography'] == geography]
        
        return treaties
    
    def get_treaty(self, treaty_id):
        """Get single treaty by ID"""
        for treaty in self.portfolio['treaties']:
            if treaty['treaty_id'] == treaty_id:
                return treaty
        return None
    
    def get_lob_breakdown(self):
        """Get portfolio breakdown by LOB"""
        return self.portfolio['lob_breakdown']
    
    def get_geographic_breakdown(self):
        """Get portfolio breakdown by geography"""
        return self.portfolio['geography_breakdown']

# Initialize server
server = PortfolioDataServer()
