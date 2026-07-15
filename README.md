# Dynamic Portfolio Optimisation Agent (MCP-Enabled)

A real-time reinsurance portfolio optimization platform powered by AI, MCP servers, and advanced analytics.

## 🎯 Features

- **Real-Time Portfolio Monitoring** - Track exposure, capital utilization, performance metrics
- **Dynamic Optimization** - RORAC calculations, capital efficiency, risk-adjusted returns
- **Scenario Analysis** - Monte Carlo simulations, stress testing, what-if analysis
- **Recommendation Engine** - Prioritized actions with business justification
- **MCP Integration** - Modular data sources (portfolio, market, catastrophe, regulatory)
- **Executive Dashboard** - Professional, data-driven interface for leadership

## 📋 Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Portfolio Optimisation Agent (AI)               │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Optimization │  │  Scenario    │  │ Recommendation
│  │    Engine    │  │   Engine     │  │    Engine     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         ↓                 ↓                  ↓           │
├─────────────────────────────────────────────────────────┤
│                   MCP Data Servers                       │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Portfolio   │  │   Market     │  │ Catastrophe  │  │
│  │   Server     │  │   Server     │  │   Server     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         ↓                 ↓                  ↓           │
├─────────────────────────────────────────────────────────┤
│              Data Sources (Mock / Real)                  │
│                                                           │
│  Portfolio DB │ Market Data │ RMS/AIR │ Regulatory    │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│         Web UI (Flask/React) - Azure Cloud              │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Local Development
```bash
# Clone and setup
git clone <repo>
cd portfolio-agent
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run locally
python web_ui/app.py
# Visit: http://localhost:5000
```

### Azure Deployment
```bash
# Build & deploy to Azure
az login
az acr build --registry <registry-name> --image portfolio-agent:latest .
az container create --resource-group <rg> --name portfolio-agent \
  --image <registry>.azurecr.io/portfolio-agent:latest \
  --ports 5000 --cpu 2 --memory 4 \
  --environment-variables AZURE_ENV=production
```

## 📊 Key Endpoints

### Web UI
- **Dashboard**: `/` - Portfolio overview & health
- **Portfolio**: `/portfolio` - Treaty details & performance
- **Scenarios**: `/scenarios` - Simulation & stress testing
- **Recommendations**: `/recommendations` - Optimization actions
- **Reports**: `/reports` - Executive summaries

### API Endpoints
- `POST /api/analyze-portfolio` - Full portfolio analysis
- `POST /api/scenario/simulate` - Run scenario analysis
- `GET /api/recommendations` - Get current recommendations
- `GET /api/portfolio/metrics` - Portfolio metrics
- `GET /api/health` - System health check

## 📁 Project Structure

```
portfolio-agent/
├── mcp_servers/               # MCP Server implementations
│   ├── portfolio_server.py    # Portfolio data server
│   ├── market_server.py       # Market data server
│   └── catastrophe_server.py  # Cat model server
├── engines/                   # Optimization & analysis engines
│   ├── portfolio_optimizer.py # RORAC, optimization logic
│   ├── scenario_analyzer.py   # Monte Carlo, stress testing
│   └── recommendation_engine.py
├── web_ui/
│   ├── app.py                 # Flask application
│   ├── templates/             # HTML templates
│   └── static/                # CSS, JS, assets
├── data_connectors/           # Data source connectors
│   └── mock_portfolio.py      # Mock data generator
├── config/                    # Configuration files
│   ├── mcp_config.json
│   ├── azure_config.json
│   └── portfolio_config.json
├── Dockerfile                 # Azure container image
├── azure-deploy.json          # ARM template for Azure
└── requirements.txt           # Python dependencies
```

## 🔑 Key Capabilities

### Portfolio Monitoring
- Real-time exposure tracking
- Capital consumption monitoring
- Performance analytics
- Concentration risk detection

### Optimization
- RORAC calculations
- Risk-adjusted return maximization
- Capital allocation optimization
- Treaty recommendation engine

### Scenario Analysis
- Monte Carlo simulations
- Interest rate scenarios
- Catastrophe stress tests
- Regulatory stress testing

### Reporting
- Executive summary reports
- Portfolio health dashboards
- Recommendation reports
- Compliance documentation

## 🔐 Security & Compliance

- Azure Managed Identity for auth
- Encryption at rest & in transit
- Role-based access control
- Audit logging
- Solvency II compliance ready

## 📈 Technologies

- **Backend**: Python 3.11+, Flask
- **Frontend**: HTML5, Bootstrap 5, Chart.js
- **Cloud**: Microsoft Azure (App Service, Container Instances)
- **Database**: Azure SQL / Cosmos DB
- **Optimization**: NumPy, SciPy, Pandas
- **MCP**: Model Context Protocol servers

## 📝 Configuration

### Azure Setup
1. Create Azure Resource Group
2. Create Azure Container Registry
3. Create Azure App Service or Container Instance
4. Set environment variables in Azure Portal
5. Deploy using Docker or direct deployment

### Local Setup
- Copy `config/portfolio_config_sample.json` to `config/portfolio_config.json`
- Update with your settings
- Run Flask development server

## 🤝 Contributing

- Create feature branches from `develop`
- Follow existing code patterns
- Add tests for new features
- Create pull requests for review

## 📄 License

Proprietary - Reinsurance Portfolio Optimization

## 🆘 Support

For issues, questions, or feature requests:
- Create GitHub issue
- Contact: portfolio-team@company.com

---

**Built with ❤️ for Reinsurance Portfolio Management**
