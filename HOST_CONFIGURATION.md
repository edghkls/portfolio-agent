# Portfolio Agent - Host Configuration Guide

## Quick Start

### Windows - Batch File (Easiest)
Double-click to launch:
```
start_portfolio_agent.bat
```

### Windows - PowerShell
```powershell
.\start_portfolio_agent.ps1
```

---

## Access Methods

### Local Access (Same Machine)
```
http://localhost:5000
```
- Only accessible from your machine
- Best for development & testing

### Network Access (Other Machines on LAN)
```
http://<YOUR_MACHINE_IP>:5000
http://<YOUR_MACHINE_NAME>:5000
```

**Find your machine IP:**
```powershell
ipconfig
```
Look for "IPv4 Address" (usually 192.168.x.x or 10.x.x.x)

**Find your machine name:**
```powershell
$env:COMPUTERNAME
```

---

## Configuration

### Change Port
Edit `web_ui/app.py` line 136:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Change 5000 to desired port
```

### Local Only (Disable Network Access)
Edit `web_ui/app.py` line 136:
```python
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)  # Only local access
```

### Production (No Debug Mode)
Edit `web_ui/app.py` line 136:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # Disable debug for production
```

---

## Features & Endpoints

| Feature | URL | Purpose |
|---------|-----|---------|
| Dashboard | `/` | Portfolio overview & key metrics |
| Portfolio | `/portfolio` | Treaty details & filtering |
| Scenarios | `/scenarios` | Monte Carlo & stress testing |
| Recommendations | `/recommendations` | Optimization suggestions |
| Reports | `/reports` | Report generation |

### API Endpoints
```
GET  /api/portfolio           - Full portfolio JSON
GET  /api/portfolio/summary   - Summary metrics
POST /api/analyze-portfolio   - Full analysis
POST /api/scenario/simulate   - Run simulation
GET  /api/recommendations    - Get recommendations
GET  /api/health             - Health check
```

---

## Dashboard Content

### Main Dashboard `/`
- **Portfolio Value**: Total premium across all treaties
- **Capital Utilization**: Percentage of capital in use
- **Average RORAC**: Return on Risk-Adjusted Capital
- **Diversification Score**: Portfolio concentration metric
- **Performance Charts**: LOB & geographic breakdown
- **Top Recommendations**: Priority-ranked optimization suggestions

### Portfolio Page `/portfolio`
- **Filters**: By LOB, Geography, Status
- **Sort Options**: RORAC, Premium, Profit, Loss Ratio
- **Treaty Cards**: Individual treaty metrics & performance

### Scenarios Page `/scenarios`
- **Monte Carlo Simulation**: 1000 iterations with loss distribution
- **Interest Rate Stress**: -500 to +500 basis points
- **Catastrophe Testing**: 100/200/500-year event scenarios
- **Scenario Comparison**: Base/Optimistic/Moderate/Severe cases

### Recommendations Page `/recommendations`
- **Executive Summary**: Key findings & actions
- **Capital Efficiency**: Optimization opportunities
- **Performance Review**: Underperforming treaties
- **Diversification**: Concentration risk mitigation
- **Risk Management**: Catastrophe management improvements

### Reports Page `/reports`
- **Executive Summary**: High-level overview
- **Risk Assessment**: Detailed risk analysis
- **Optimization Report**: Recommended actions
- **Compliance Report**: Regulatory requirements

---

## Portfolio Data

### Sample Data
50 synthetic reinsurance treaties with:
- **Lines of Business** (5 LOBs)
  - Property Catastrophe
  - Casualty
  - Marine & Aviation
  - Financial Lines
  - Specialty
  
- **Geographies** (5 Regions)
  - North America
  - Europe
  - Asia Pacific
  - Latin America
  - Africa/Middle East

- **Treaty Metrics**
  - Premium: $40K - $5M
  - Loss Ratio: 15-75%
  - RORAC: 8-35%
  - Expected Profit: $2K - $1M

---

## Troubleshooting

### Server won't start
```powershell
# Verify Flask installation
python -c "import flask; print(flask.__version__)"

# Reinstall dependencies
pip install -r requirements.txt
```

### ModuleNotFoundError
```powershell
# Set PYTHONPATH
$env:PYTHONPATH = "."
python web_ui/app.py
```

### Port already in use
```powershell
# Find process using port 5000
Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | 
  Foreach-Object {Get-Process -Id $_.OwningProcess}

# Kill the process
Stop-Process -Id <PID> -Force
```

### Network access not working
1. Check firewall allows port 5000
2. Verify using `ipconfig` for correct IP
3. Test connectivity: `ping <machine_name>`

---

## Requirements

- Python 3.11+
- Flask 2.3.3
- NumPy, Pandas, SciPy
- Windows 10+ or PowerShell 5.0+

All dependencies listed in `requirements.txt`

---

## Next Steps

- **Customize Data**: Modify `data_connectors/mock_portfolio.py`
- **Add Analytics**: Update `engines/portfolio_optimizer.py`
- **Deploy to Azure**: Follow [AZURE_DEPLOYMENT.md](./AZURE_DEPLOYMENT.md)
- **Run in Docker**: Use provided `Dockerfile`

---

**Questions?** Check [README.md](./README.md) and [PROJECT_STATUS.md](./PROJECT_STATUS.md)
