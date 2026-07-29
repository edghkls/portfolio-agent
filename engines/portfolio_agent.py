"""
AI Agent for Portfolio Optimisation - Handles chat and recommendations
"""

class PortfolioAgent:
    """Intelligent agent that analyzes portfolio and provides insights"""
    
    def __init__(self, portfolio_analyzer):
        self.analyzer = portfolio_analyzer
        self.context = {}
    
    def process_query(self, query, portfolio_data, enhanced_metrics):
        """
        Process user query and return intelligent response
        """
        query_lower = query.lower()
        
        # Extract key entities and intent
        intent = self._detect_intent(query_lower)
        
        # Route to appropriate handler
        if intent == 'top_performers':
            return self._top_performers(portfolio_data)
        elif intent == 'risk_analysis':
            return self._risk_analysis(portfolio_data, enhanced_metrics)
        elif intent == 'health_score':
            return self._portfolio_health(portfolio_data, enhanced_metrics)
        elif intent == 'optimization':
            return self._optimization_recommendations(portfolio_data, enhanced_metrics)
        elif intent == 'alerts':
            return self._get_alerts(portfolio_data, enhanced_metrics)
        elif intent == 'comparison':
            return self._benchmark_comparison(enhanced_metrics)
        elif intent == 'lob_analysis':
            return self._lob_analysis(portfolio_data)
        elif intent == 'geography_analysis':
            return self._geography_analysis(portfolio_data)
        else:
            return self._general_analysis(portfolio_data, enhanced_metrics)
    
    def _detect_intent(self, query):
        """Detect user intent from query"""
        keywords = {
            'top_performers': ['top', 'best', 'perform', 'highest', 'rorac'],
            'risk_analysis': ['risk', 'concentration', 'concentration risk', 'loss'],
            'health_score': ['health', 'score', 'status', 'condition'],
            'optimization': ['optimize', 'recommend', 'suggest', 'strategy', 'strategies'],
            'alerts': ['alert', 'alert', 'warning', 'issue', 'problem'],
            'comparison': ['benchmark', 'compare', 'vs', 'versus'],
            'lob_analysis': ['lob', 'line', 'business', 'casualty', 'marine', 'property', 'financial'],
            'geography_analysis': ['geography', 'region', 'geographic', 'region', 'country', 'area']
        }
        
        for intent, keywords_list in keywords.items():
            if any(kw in query for kw in keywords_list):
                return intent
        
        return 'general'
    
    def _top_performers(self, portfolio_data):
        """Analyze top performing treaties"""
        try:
            # Try both possible field names
            top_treaties = portfolio_data.get('top_treaties', []) or portfolio_data.get('treaties', [])
            
            if not top_treaties:
                return "📊 No treaty data available"
            
            # Sort by RORAC and get top 3
            top_treaties = sorted(top_treaties, key=lambda x: x.get('rorac', 0), reverse=True)[:3]
            
            response = "🏆 **Top Performing Treaties:**\n\n"
            for i, treaty in enumerate(top_treaties, 1):
                treaty_id = treaty.get('treaty_id', treaty.get('id', 'N/A'))
                rorac = treaty.get('rorac', 0)
                premium = treaty.get('premium', 0)
                lob = treaty.get('lob', 'N/A')
                rating = treaty.get('rating', 'N/A')
                status = treaty.get('performance_status', 'Good')
                
                response += f"{i}. **{treaty_id}** (LOB: {lob})\n"
                response += f"   • RORAC: {rorac:.1f}%\n"
                response += f"   • Premium: ${premium/1e6:.2f}M\n"
                response += f"   • Rating: {rating}\n"
                response += f"   • Status: {status}\n\n"
            
            return response
        except Exception as e:
            return f"Error analyzing top performers: {str(e)}"
    
    def _risk_analysis(self, portfolio_data, enhanced_metrics):
        """Analyze portfolio risks"""
        cu = portfolio_data.get('capital_utilization', 0)
        ds = portfolio_data.get('diversification_score', 0)
        cr = enhanced_metrics.get('claims_ratio', 0)
        
        response = "⚠️ **Risk Analysis:**\n\n"
        response += f"**Capital Adequacy:**\n"
        response += f"• Current Utilization: {cu:.1f}%\n"
        response += f"• Status: {'🟢 Optimal' if cu < 90 else '🟡 Monitor' if cu < 110 else '🔴 High'}\n\n"
        
        response += f"**Concentration Risk:**\n"
        response += f"• Diversification Score: {ds:.2f}/1.0\n"
        response += f"• Risk Level: {'🟢 Low' if ds > 0.7 else '🟡 Moderate' if ds > 0.5 else '🔴 High'}\n\n"
        
        response += f"**Claims Experience:**\n"
        response += f"• Claims Ratio: {cr:.1f}%\n"
        response += f"• Trend: {'🟢 Improving' if cr < 50 else '🟡 Monitoring' if cr < 60 else '🔴 Concerning'}\n"
        
        return response
    
    def _portfolio_health(self, portfolio_data, enhanced_metrics):
        """Calculate and explain portfolio health score"""
        cu = portfolio_data.get('capital_utilization', 0)
        ds = portfolio_data.get('diversification_score', 0)
        rorac = portfolio_data.get('average_rorac', 0)
        cr = enhanced_metrics.get('claims_ratio', 0)
        
        # Calculate health score (0-100)
        score = 0
        score += min(100, (90 / cu * 20)) if cu > 0 else 20  # Capital utilization (20 points)
        score += (ds / 1.0 * 20)  # Diversification (20 points)
        score += min(100, (rorac / 200 * 30))  # RORAC (30 points)
        score += min(100, (60 / cr * 30)) if cr > 0 else 30  # Claims ratio (30 points)
        
        score = min(100, score)
        
        health_status = '🟢 Excellent' if score > 80 else '🟡 Good' if score > 60 else '🔴 Needs Attention'
        
        response = f"💊 **Portfolio Health Score: {score:.0f}/100** {health_status}\n\n"
        response += f"**Breakdown:**\n"
        response += f"• Capital Structure: {'✅' if cu < 95 else '⚠️' if cu < 110 else '❌'} {cu:.1f}%\n"
        response += f"• Diversification: {'✅' if ds > 0.7 else '⚠️' if ds > 0.5 else '❌'} {ds:.2f}\n"
        response += f"• Profitability: {'✅' if rorac > 200 else '⚠️' if rorac > 100 else '❌'} {rorac:.1f}%\n"
        response += f"• Claims Control: {'✅' if cr < 50 else '⚠️' if cr < 60 else '❌'} {cr:.1f}%\n"
        
        return response
    
    def _optimization_recommendations(self, portfolio_data, enhanced_metrics):
        """Provide optimization recommendations"""
        response = "🚀 **Optimization Recommendations:**\n\n"
        
        recommendations = []
        
        # Capital optimization
        cu = portfolio_data.get('capital_utilization', 0)
        if cu > 95:
            recommendations.append("1. **Reduce Capital Exposure** - Current utilization is high. Consider reducing premium exposure or increasing capital allocation.")
        elif cu < 70:
            recommendations.append("1. **Increase Capital Deployment** - Underutilized capital. Consider expanding premium writing.")
        
        # Diversification
        ds = portfolio_data.get('diversification_score', 0)
        if ds < 0.65:
            recommendations.append("2. **Improve Diversification** - Portfolio is concentrated. Increase exposure to underrepresented LOBs or geographies.")
        
        # Claims ratio
        cr = enhanced_metrics.get('claims_ratio', 0)
        if cr > 50:
            recommendations.append("3. **Enhance Underwriting** - Claims ratio is elevated. Tighten underwriting standards and improve loss control.")
        
        # RORAC
        rorac = portfolio_data.get('average_rorac', 0)
        if rorac < 150:
            recommendations.append("4. **Repricing Strategy** - RORAC is below target. Review pricing or reduce low-margin business.")
        
        if not recommendations:
            recommendations.append("✅ **Portfolio is well-optimized.** Monitor metrics for changes.")
        
        response += "\n".join(recommendations)
        return response
    
    def _get_alerts(self, portfolio_data, enhanced_metrics):
        """Get current system alerts"""
        from engines.anomaly_detector import AnomalyDetector
        detector = AnomalyDetector()
        alerts = detector.analyze_portfolio(portfolio_data, enhanced_metrics)
        
        response = "🚨 **System Alerts:**\n\n"
        
        if not alerts:
            response += "✅ No active alerts"
            return response
        
        for alert in alerts:
            icon = '🔴' if alert['severity'] == 'danger' else '🟡' if alert['severity'] == 'warning' else '🟢'
            response += f"{icon} {alert['message']}\n"
            if alert.get('recommendation'):
                response += f"   💡 {alert['recommendation']}\n"
            response += "\n"
        
        return response
    
    def _benchmark_comparison(self, enhanced_metrics):
        """Compare against industry benchmarks"""
        response = "📊 **Benchmark Comparison:**\n\n"
        response += "**Your Portfolio vs Industry Standards:**\n\n"
        
        rorac = enhanced_metrics.get('average_rorac', 0)
        response += f"• RORAC: {rorac:.1f}% (Industry Avg: 20-25%)\n"
        response += f"  Status: {'✅ Exceeding' if rorac > 150 else '⚠️ Below Target'}\n\n"
        
        cr = enhanced_metrics.get('claims_ratio', 0)
        response += f"• Claims Ratio: {cr:.1f}% (Industry Avg: 40-50%)\n"
        response += f"  Status: {'✅ Better' if cr < 45 else '⚠️ Higher'}\n\n"
        
        ce = enhanced_metrics.get('capital_efficiency', 0)
        response += f"• Capital Efficiency: ${ce:.0f}K per $1M\n"
        response += f"  Status: {'✅ Efficient' if ce > 500 else '⚠️ Below Avg'}\n"
        
        return response
    
    def _lob_analysis(self, portfolio_data):
        """Analyze by Line of Business"""
        lob_breakdown = portfolio_data.get('lob_breakdown', {})
        
        if not lob_breakdown:
            return "📈 No LOB data available"
        
        response = "📈 **Line of Business Analysis:**\n\n"
        
        total = sum(lob_breakdown.values())
        for lob, value in sorted(lob_breakdown.items(), key=lambda x: x[1], reverse=True):
            percentage = (value / total * 100) if total > 0 else 0
            bar = '█' * int(percentage / 5) + '░' * (20 - int(percentage / 5))
            response += f"{lob}: {bar} {percentage:.1f}% (${value/1e6:.1f}M)\n"
        
        return response
    
    def _geography_analysis(self, portfolio_data):
        """Analyze by Geography"""
        geo_breakdown = portfolio_data.get('geography_breakdown', {})
        
        if not geo_breakdown:
            return "🌍 No geographic data available"
        
        response = "🌍 **Geographic Distribution:**\n\n"
        
        total = sum(geo_breakdown.values())
        for geo, value in sorted(geo_breakdown.items(), key=lambda x: x[1], reverse=True):
            percentage = (value / total * 100) if total > 0 else 0
            bar = '█' * int(percentage / 5) + '░' * (20 - int(percentage / 5))
            response += f"{geo}: {bar} {percentage:.1f}% (${value/1e6:.1f}M)\n"
        
        return response
    
    def _general_analysis(self, portfolio_data, enhanced_metrics):
        """Provide general portfolio overview"""
        response = "📋 **Portfolio Overview:**\n\n"
        
        pv = portfolio_data.get('portfolio_value', 0)
        cu = portfolio_data.get('capital_utilization', 0)
        rorac = portfolio_data.get('average_rorac', portfolio_data.get('avg_rorac', 0))
        ds = portfolio_data.get('diversification_score', 0)
        
        response += f"**Portfolio Value:** ${pv/1e6:.1f}M\n"
        response += f"**Capital Utilization:** {cu:.1f}%\n"
        response += f"**Average RORAC:** {rorac:.1f}%\n"
        response += f"**Diversification Score:** {ds:.2f}/1.0\n\n"
        
        # Count treaties
        treaties = portfolio_data.get('treaties', []) or portfolio_data.get('top_treaties', [])
        treaty_count = len(treaties)
        
        response += "💡 **Quick Insights:**\n"
        response += f"• Portfolio consists of {treaty_count} treaties across 5 lines of business\n"
        
        geo = portfolio_data.get('geography_breakdown', {})
        response += f"• Geographic spread across {len(geo)} regions\n"
        response += f"• Claims ratio: {enhanced_metrics.get('claims_ratio', 0):.1f}%\n"
        
        return response
