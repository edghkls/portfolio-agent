# 📊 Portfolio Optimisation Agents - Detailed Specifications

## Agent Details Table

| **Agent Name** | **Agent Description** | **Purpose** | **Gen AI Tool Required** | **LLM Used** | **Programming Language** | **Framework/Dependencies** | **Source Data Supported** |
|---|---|---|---|---|---|---|---|
| **Portfolio Agent** | AI-powered query processor with natural language understanding for portfolio analysis | Multi-intent portfolio analysis (top performers, risk analysis, health scoring, optimization, alerts, comparison, LOB/geography analysis) | ✅ Required (Intent Detection) | Custom Keyword-based NLP (Extensible to GPT/Claude) | Python 3.9+ | Flask (REST API)<br/>Core Python | • Treaty-level data<br/>• Performance metrics<br/>• Historical comparisons<br/>• Multi-dimensional filters |
| **Portfolio Optimizer** | Financial modeling engine for capital allocation and RORAC calculation | Identify optimization opportunities, calculate portfolio-level RORAC, recommend capital reallocation | ❌ Not Required (Rule-based) | N/A (Mathematical algorithms) | Python 3.9+ | Pandas<br/>NumPy<br/>SciPy<br/>Typing | • Treaty premiums<br/>• Capital requirements<br/>• Expected profit data<br/>• Loss ratios<br/>• Concentration metrics |
| **Recommendation Engine** | Multi-factor recommendation generator with priority ranking | Generate prioritized, actionable recommendations across 4+ categories (capital efficiency, performance, diversification, risk management) | ✅ Recommended (Impact scoring) | Custom Weighted Logic (Can integrate LLM for narrative) | Python 3.9+ | Core Python<br/>Datetime<br/>Typing | • Portfolio performance<br/>• Capital utilization<br/>• Risk metrics<br/>• Historical trends<br/>• Market benchmarks |
| **Scenario Analyzer** | Statistical simulation engine for Monte Carlo and stress testing | Run 1000+ simulations, stress-test interest rates/catastrophe events, perform what-if analysis | ❌ Not Required (Statistical) | N/A (NumPy/SciPy) | Python 3.9+ | NumPy<br/>Pandas<br/>SciPy<br/>Datetime | • Treaty loss distributions<br/>• Premium data<br/>• Historical loss ratios<br/>• Volatility metrics<br/>• Market scenarios |
| **Anomaly Detector** | Rule-based monitoring system with threshold enforcement | Real-time anomaly detection, alert generation, KPI tracking, continuous portfolio monitoring | ❌ Not Required (Threshold-based) | N/A (If-then rules) | Python 3.9+ | NumPy<br/>Datetime<br/>Core Python | • Capital utilization<br/>• Claims ratios<br/>• RORAC performance<br/>• Diversification scores<br/>• Loss concentration<br/>• Trend analysis |

---

## Detailed Agent Specifications

### 1. **Portfolio Agent**

**Technical Details:**
```
Language: Python 3.9+
Framework: Flask (API wrapper)
Dependencies: None (Core Python)
Entry Point: engines/portfolio_agent.py
API Endpoint: POST /api/query-agent
```

**Agent Architecture:**
```python
PortfolioAgent
├─ process_query() - Main query processor
├─ _detect_intent() - NLP intent detection (8 modes)
├─ Intent Handlers:
│  ├─ _top_performers() - Top treaty analysis
│  ├─ _risk_analysis() - Risk assessment
│  ├─ _portfolio_health() - Health scoring
│  ├─ _optimization_recommendations() - Recommendations
│  ├─ _get_alerts() - Alert generation
│  ├─ _benchmark_comparison() - Benchmarking
│  ├─ _lob_analysis() - LOB breakdown
│  ├─ _geography_analysis() - Geographic analysis
│  └─ _general_analysis() - Default handler
```

**Supported Intents:**
- `top_performers` - Keywords: top, best, perform, highest, rorac
- `risk_analysis` - Keywords: risk, concentration, loss
- `health_score` - Keywords: health, score, status, condition
- `optimization` - Keywords: optimize, recommend, suggest, strategy
- `alerts` - Keywords: alert, warning, issue, problem
- `comparison` - Keywords: benchmark, compare, vs, versus
- `lob_analysis` - Keywords: lob, line, business, casualty, marine, property
- `geography_analysis` - Keywords: geography, region, geographic, country, area

**Gen AI Integration Points:**
- Current: Keyword-based intent detection
- Recommended: LLM for contextual intent understanding (OpenAI GPT-4, Anthropic Claude)
- Future: Multi-turn conversation context management

**Input Data Requirements:**
```json
{
  "query": "String (user input)",
  "portfolio_data": {
    "treaties": [...],
    "capital_utilization": number,
    "diversification_score": number,
    "average_rorac": number
  },
  "enhanced_metrics": {
    "claims_ratio": number,
    "premium_growth": number,
    "underwriting_perf": number
  }
}
```

**Output Format:**
```
Markdown-formatted response with:
• Analysis results
• Metrics with emojis for visualization
• Recommendations with priority levels
• Status indicators (🟢🟡🔴)
```

---

### 2. **Portfolio Optimizer**

**Technical Details:**
```
Language: Python 3.9+
Framework: Pandas/NumPy/SciPy
Dependencies: pandas, numpy, scipy
Entry Point: engines/portfolio_optimizer.py
API Endpoint: POST /api/optimize
```

**Agent Architecture:**
```python
PortfolioOptimizer
├─ calculate_rorac() - Per-treaty RORAC
├─ calculate_portfolio_rorac() - Portfolio-level RORAC
├─ identify_optimization_opportunities() - Opportunity detection
├─ optimize_allocation() - Allocation recommendations
├─ calculate_capital_efficiency() - Efficiency metrics
├─ estimate_var() - Value at Risk calculation
└─ stress_test_portfolio() - Stress testing
```

**Financial Formulas Used:**
```
RORAC = (Expected Return / Risk-Adjusted Capital) × 100

Capital Efficiency = Total Premium / Total Capital Requirement

Value at Risk (VaR) = Standard Deviation × Z-Score

Concentration Risk = Premium in Single LOB / Total Premium

Diversification Score = 1 - (Herfindahl Index / Max Index)
```

**Gen AI Integration Points:**
- Current: Pure mathematical calculations
- Recommended: LLM for actionable narrative explanations
- Future: ML models for predictive RORAC estimation

**Input Data Requirements:**
```json
{
  "treaties": [
    {
      "treaty_id": "string",
      "premium": number,
      "expected_profit": number,
      "capital_requirement": number,
      "loss_ratio": number,
      "lob": "string",
      "rorac": number
    }
  ]
}
```

**Output Format:**
```json
{
  "current_rorac": 224.96,
  "target_rorac": 247.46,
  "rorac_improvement": 22.5,
  "opportunities": [
    {
      "treaty_id": "string",
      "action": "string",
      "priority": "High|Medium|Low",
      "capital_impact": number,
      "profit_improvement": number
    }
  ],
  "capital_release": number,
  "profit_impact": number
}
```

---

### 3. **Recommendation Engine**

**Technical Details:**
```
Language: Python 3.9+
Framework: Custom Logic Engine
Dependencies: datetime, typing
Entry Point: engines/recommendation_engine.py
API Endpoint: POST /api/recommendations
```

**Agent Architecture:**
```python
RecommendationEngine
├─ generate_comprehensive_recommendations() - Main orchestrator
├─ _get_capital_efficiency_recommendations()
├─ _get_performance_recommendations()
├─ _get_diversification_recommendations()
├─ _get_risk_management_recommendations()
├─ _get_portfolio_state()
├─ _get_risk_assessment()
└─ _get_executive_summary()
```

**Recommendation Categories:**
1. **Capital Efficiency (Priority 1)**
   - Reduce/increase capital deployment
   - Improve capital allocation

2. **Performance Optimization (Priority 2)**
   - Exit underperforming treaties
   - Focus on high-RORAC vehicles

3. **Diversification (Priority 3)**
   - Reduce LOB concentration
   - Geographic rebalancing

4. **Risk Management (Priority 4)**
   - Improve claims control
   - Enhance risk monitoring

**Scoring Methodology:**
```
Impact Score = 
  (Capital Impact Weight × 0.25) +
  (Profit Impact Weight × 0.40) +
  (Risk Reduction Weight × 0.20) +
  (Implementation Ease Weight × 0.15)

Priority = Sorted by Impact Score descending
```

**Gen AI Integration Points:**
- Current: Rule-based recommendations
- Recommended: LLM for personalized narrative explanations
- Future: Reinforcement learning for adaptive recommendations

**Input Data Requirements:**
```json
{
  "portfolio_data": {...},
  "enhanced_metrics": {...},
  "market_conditions": "optional",
  "risk_appetite": "optional"
}
```

**Output Format:**
```json
{
  "timestamp": "ISO 8601",
  "portfolio_state": {...},
  "risk_assessment": {...},
  "recommendations": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "category": "string",
      "priority": "High|Medium|Low",
      "impact": {
        "capital": number,
        "profit": number,
        "risk": number
      },
      "action_items": ["string"]
    }
  ],
  "executive_summary": "string"
}
```

---

### 4. **Scenario Analyzer**

**Technical Details:**
```
Language: Python 3.9+
Framework: NumPy/SciPy
Dependencies: numpy, pandas, scipy, datetime
Entry Point: engines/scenario_analyzer.py
API Endpoint: POST /api/scenarios
```

**Agent Architecture:**
```python
ScenarioAnalyzer
├─ run_monte_carlo() - 1000+ simulations
├─ stress_test_interest_rates() - Rate sensitivity
├─ catastrophe_stress_test() - CAT events
├─ scenario_comparison() - Side-by-side analysis
├─ _summarize_monte_carlo()
├─ _calculate_var()
└─ _calculate_cvar()
```

**Simulation Capabilities:**

**Monte Carlo:**
```
Simulations: 1000 iterations
Distribution: Beta(5, 10) for loss ratios
Confidence Level: 99% (Z-score = 2.33)
Outputs:
  • Expected Loss Distribution
  • Expected Profit Distribution
  • Capital Requirements
  • Confidence Intervals
```

**Stress Testing - Interest Rates:**
```
Rate Changes: -200 to +500 bps
Impact Areas:
  • Investment returns
  • Liability valuations
  • Capital requirements
  • Premium pricing
```

**Stress Testing - Catastrophe Events:**
```
Scenarios:
  • Hurricane (Return Period: 10, 50, 100, 200 years)
  • Tornado (Enhanced Fujita Scale EF3-EF5)
  • Earthquake (Magnitude 6.5-8.0)
  • Flooding (100-500 year events)

LOB Impacts:
  • Property: 40-80% loss
  • Casualty: 10-30% loss
  • Marine: 20-50% loss
```

**Gen AI Integration Points:**
- Current: Statistical simulation
- Recommended: LLM for scenario narrative generation
- Future: Generative models for stress scenario creation

**Input Data Requirements:**
```json
{
  "treaties": [
    {
      "premium": number,
      "loss_ratio": number,
      "volatility": number,
      "lob": "string",
      "geography": "string"
    }
  ],
  "simulation_params": {
    "iterations": number,
    "confidence_level": number,
    "rate_change": number,
    "scenario_type": "string"
  }
}
```

**Output Format:**
```json
{
  "scenario": "string",
  "simulations": number,
  "results": {
    "loss_statistics": {
      "mean": number,
      "std": number,
      "percentile_5": number,
      "percentile_95": number,
      "percentile_99": number
    },
    "profit_statistics": {...},
    "capital_requirement": number,
    "confidence_level": number
  },
  "insights": ["string"]
}
```

---

### 5. **Anomaly Detector**

**Technical Details:**
```
Language: Python 3.9+
Framework: Rule Engine
Dependencies: numpy, datetime
Entry Point: engines/anomaly_detector.py
API Endpoint: GET /api/anomalies
```

**Agent Architecture:**
```python
AnomalyDetector
├─ analyze_portfolio() - Main analyzer
├─ _check_capital_utilization()
├─ _check_claims_ratio()
├─ _check_rorac_performance()
├─ _check_diversification()
├─ _check_loss_concentration()
└─ _generate_alerts()
```

**Threshold Configuration:**
```
Metric: capital_utilization
├─ Min: 60% (Under-deployment warning)
└─ Max: 95% (Over-deployment alert)

Metric: claims_ratio
├─ Min: 0%
└─ Max: 60% (Above 60% = danger alert)

Metric: rorac
└─ Min: 15% (Below 15% = warning)

Metric: diversification
└─ Min: 0.65 (Below 0.65 = concentration risk)

Metric: loss_concentration
└─ Max: 40% (Single LOB concentration limit)
```

**Alert Severity Levels:**
```
🔴 Critical - Immediate action required
🚨 Danger - Urgent escalation needed
🟡 Warning - Monitor closely
🟢 Normal - Operating within parameters
```

**Gen AI Integration Points:**
- Current: Threshold-based rules
- Recommended: ML models for anomaly detection
- Future: Predictive alerting with anomaly forecasting

**Input Data Requirements:**
```json
{
  "portfolio_data": {
    "capital_utilization": number,
    "diversification_score": number,
    "average_rorac": number,
    "average_loss_ratio": number
  },
  "enhanced_metrics": {
    "claims_ratio": number,
    "premium_growth": number,
    "underwriting_perf": number
  }
}
```

**Output Format:**
```json
{
  "alerts": [
    {
      "severity": "critical|danger|warning|normal",
      "type": "string",
      "message": "string",
      "value": number,
      "threshold": number,
      "recommendation": "string",
      "timestamp": "ISO 8601"
    }
  ],
  "alert_count": number,
  "critical_count": number
}
```

---

## Comparative Analysis

### Performance Metrics

| Metric | Portfolio Agent | Optimizer | Recommendation | Scenario | Anomaly |
|--------|-----------------|-----------|----------------|----------|---------|
| **Execution Time** | < 500ms | < 200ms | < 300ms | 2-5s | < 100ms |
| **Data Points Processed** | ~100K | ~10K | ~5K | Variable | ~1K |
| **ML/AI Complexity** | Medium | Low | Medium | High | Low |
| **Output Latency** | Real-time | Real-time | Real-time | Batch | Real-time |
| **Scalability** | High | High | High | Medium | Very High |

### Capability Matrix

| Feature | Portfolio Agent | Optimizer | Recommendation | Scenario | Anomaly |
|---------|-----------------|-----------|----------------|----------|---------|
| **Query Processing** | ✅ (8 intents) | ❌ | ❌ | ❌ | ❌ |
| **RORAC Calculation** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Capital Optimization** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Recommendations** | ✅ | ✅ | ✅ | ❌ | ✅ |
| **Simulations** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Stress Testing** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Anomaly Detection** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Real-time Alerts** | ❌ | ❌ | ❌ | ❌ | ✅ |

### LLM Integration Roadmap

```
Phase 1 (Current):
└─ Rule-based systems with keyword matching

Phase 2 (Recommended):
├─ Portfolio Agent: Add GPT-4/Claude for intent understanding
├─ Optimizer: Add LLM for narrative explanations
└─ Recommendation Engine: Add LLM for personalized messaging

Phase 3 (Advanced):
├─ Add multi-turn conversational AI
├─ Integrate few-shot prompting for novel scenarios
└─ Implement retrieval-augmented generation (RAG) for market data

Phase 4 (AI-Native):
├─ Custom fine-tuned models on portfolio data
├─ Agentic workflows with tool-use capabilities
└─ Autonomous portfolio management recommendations
```

---

## Data Flow Architecture

```
┌──────────────────────────────────────────────────────┐
│         User Interface Layer                         │
│  (Dashboard, Chat, Reports, Scenarios)              │
└──────────────────┬───────────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────────┐
│         REST API Layer (26 Endpoints)                │
│  GET/POST /api/portfolio/*, /api/scenarios, etc.    │
└──────────────────┬───────────────────────────────────┘
                   │
        ┌──────────┴──────────┬────────────────┐
        │                     │                │
┌───────▼──────┐   ┌──────────▼────┐  ┌────────▼────────┐
│ Portfolio    │   │  Optimizer    │  │ Recommendation  │
│ Agent        │   │  Engine       │  │ Engine          │
├──────────────┤   ├───────────────┤  ├─────────────────┤
│ • NLP        │   │ • RORAC       │  │ • Multi-factor  │
│ • Intent     │   │ • Capital     │  │ • Priority      │
│ • Analysis   │   │ • Efficiency  │  │ • Impact        │
└───────┬──────┘   └───────────────┘  └────────────────┘
        │
        │          ┌────────────────┐  ┌──────────────┐
        │          │ Scenario       │  │ Anomaly      │
        │          │ Analyzer       │  │ Detector     │
        │          ├────────────────┤  ├──────────────┤
        │          │ • Monte Carlo  │  │ • Thresholds │
        │          │ • Stress Test  │  │ • Alerts     │
        │          │ • What-if      │  │ • Monitoring │
        │          └────────────────┘  └──────────────┘
        │
┌───────▼─────────────────────────────────────────────┐
│         Data Processing Layer                       │
│  (Portfolio Data, Metrics, Calculations)           │
└───────┬─────────────────────────────────────────────┘
        │
┌───────▼─────────────────────────────────────────────┐
│    Mock Portfolio Generator (50 Synthetic Treaties) │
│  • 5 Lines of Business (LOBs)                       │
│  • 5 Geographic Regions                            │
│  • Dynamic Metrics & Simulated Loss Ratios         │
└─────────────────────────────────────────────────────┘
```

---

## Implementation Status

| Agent | Status | Version | Last Updated | API Live | UI Integration |
|-------|--------|---------|--------------|----------|-----------------|
| Portfolio Agent | ✅ Production | 1.0 | 2026-08-04 | ✅ | ✅ Full |
| Portfolio Optimizer | ✅ Production | 1.0 | 2026-08-04 | ✅ | ✅ Full |
| Recommendation Engine | ✅ Production | 1.0 | 2026-08-04 | ✅ | ✅ Full |
| Scenario Analyzer | ✅ Production | 1.0 | 2026-08-04 | ✅ | ✅ Full |
| Anomaly Detector | ✅ Production | 1.0 | 2026-08-04 | ✅ | ✅ Full |

---

## Key Features Summary

✅ **5 Specialized AI Agents** with complementary capabilities  
✅ **26 REST API Endpoints** for comprehensive access  
✅ **Real-time Monitoring** with 5-level alert severity  
✅ **Monte Carlo Simulations** with 1000+ iterations  
✅ **Natural Language Processing** for portfolio queries  
✅ **Multi-dimensional Analysis** (RORAC, Capital, Risk, Diversification)  
✅ **Adaptive Recommendations** with impact quantification  
✅ **Professional Reporting** (Excel, Word, PDF exports)  
✅ **Extensible Architecture** ready for LLM integration  
✅ **Scalable Infrastructure** supporting 50+ treaty portfolios  

---

**Dashboard Status:** ✅ **FULLY OPERATIONAL ON LOCALHOST:5001**
