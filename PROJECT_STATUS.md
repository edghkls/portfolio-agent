# Dynamic Portfolio Optimisation Agent Configuration

## Project Status
✅ **Phase 1 Complete - Quick Start MVP Ready**

## What's Included

### ✅ Core Components
1. **Mock Portfolio System** - 50+ synthetic reinsurance treaties with realistic data
2. **Portfolio Optimizer Engine** - RORAC calculations, capital efficiency analysis
3. **Scenario Analysis Engine** - Monte Carlo, stress testing, what-if analysis
4. **Recommendation Engine** - Prioritized portfolio optimization actions
5. **Flask Web UI** - Professional dashboard with 5+ pages
6. **MCP Server Framework** - Portfolio data server ready for expansion

### ✅ Features
- Real-time portfolio monitoring
- RORAC and capital efficiency metrics
- Monte Carlo simulations (1000+ scenarios)
- Interest rate stress testing
- Catastrophe scenario analysis
- Concentration risk detection
- Diversification recommendations
- Executive-ready reports

### ✅ Cloud Ready
- Azure deployment templates
- Docker containerization
- Azure Container Instances ready
- Azure App Service compatible
- Fully scalable architecture

## Quick Start

### Local Development (Windows)
```powershell
# Navigate to project directory
cd c:\Users\m107\OneDrive - Capgemini\Desktop\MCP\portfolio-agent

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python web_ui/app.py

# Access dashboard
# http://localhost:5000
```

### Azure Deployment
```bash
# See AZURE_DEPLOYMENT.md for complete instructions

# Quick deploy:
az login
az group create --name portfolio-agent-rg --location eastus
docker build -t portfolio-agent:latest .
# ... push to Azure Container Registry ...
# ... deploy using ARM template ...
```

## API Endpoints

### Portfolio Data
- `GET /api/portfolio` - Complete portfolio data
- `GET /api/portfolio/summary` - Summary metrics
- `GET /api/portfolio/metrics` - Detailed metrics
- `GET /api/data/treaties` - Treaty list with filters

### Analysis
- `POST /api/analyze-portfolio` - Full portfolio analysis
- `POST /api/scenario/simulate` - Run scenarios
- `GET /api/recommendations` - Optimization recommendations

### System
- `GET /api/health` - Health check
- `GET /` - Main dashboard

## File Structure

```
portfolio-agent/
├── web_ui/
│   ├── app.py                      # Flask application
│   └── templates/                  # HTML pages
│       ├── dashboard.html          # Main dashboard
│       ├── portfolio.html          # Portfolio details
│       ├── scenarios.html          # Scenario analysis
│       └── recommendations.html    # Recommendations
├── engines/
│   ├── portfolio_optimizer.py      # RORAC, optimization
│   ├── scenario_analyzer.py        # Monte Carlo, stress tests
│   └── recommendation_engine.py    # Recommendation generation
├── mcp_servers/
│   └── portfolio_server.py         # MCP data server
├── data_connectors/
│   └── mock_portfolio.py           # Mock data generator
├── Dockerfile                      # Container image
├── azure-deploy.json               # Azure ARM template
├── requirements.txt                # Python dependencies
└── README.md                       # Documentation
```

## Technology Stack

- **Backend**: Python 3.11, Flask 2.3
- **Frontend**: HTML5, Bootstrap 5, Chart.js
- **Data**: NumPy, Pandas, SciPy
- **Cloud**: Microsoft Azure
- **Container**: Docker
- **Protocol**: Model Context Protocol (MCP)

## Key Metrics & Features

### Portfolio Metrics
- Portfolio Value: Tracks total exposure
- Capital Utilization: Monitors capital efficiency
- Average RORAC: Return on Risk-Adjusted Capital
- Diversification Score: Portfolio balance (0-1 scale)
- Loss Ratio: Incurred losses / Premium

### Optimization Engines
- **RORAC Calculation**: (Expected Profit / Capital Required) × 100
- **Capital Efficiency**: Premium per Capital Unit, Profit per Capital Unit
- **Portfolio Optimization**: Identify underperforming treaties, diversification opportunities
- **Concentration Analysis**: Detect over-exposure to LOBs or geographies

### Scenario Simulations
- **Monte Carlo**: 1000+ iterations with beta distribution loss simulation
- **Interest Rate Stress**: -500 to +500 bps sensitivity analysis
- **Catastrophe Events**: 100-year to 500-year return period events
- **Comparison Analysis**: Base case vs optimistic/stress cases

### Recommendation Types
1. **Capital Efficiency** - Improve capital utilization
2. **Performance** - Review underperforming treaties
3. **Diversification** - Reduce concentration risks
4. **Risk Management** - Enhance catastrophe management

## Next Steps (Future Phases)

### Phase 2: Full Integration (4-6 weeks)
- Real Bloomberg market data
- RMS/AIR catastrophe model integration
- SQL database backend
- Advanced UI with more visualizations
- User authentication & multi-tenant support

### Phase 3: Enterprise Features (8+ weeks)
- Regulatory compliance reporting
- Solvency II capital calculations
- Real-time portfolio alerts
- Advanced ML-based recommendations
- Integration with underwriting systems

## Support & Documentation

- **README.md** - Project overview
- **AZURE_DEPLOYMENT.md** - Cloud deployment guide
- **Code Comments** - Inline documentation
- **API Documentation** - Endpoint descriptions

## Team Notes

- Mock data is realistic but synthetic
- All calculations use standard reinsurance formulas
- Confidence scores indicate recommendation reliability
- Designed for executive-level decision making
- Fully AWS/Azure/GCP compatible

---

**Status**: Ready for demonstration and testing
**Last Updated**: July 2026
**Version**: 1.0 (MVP)
