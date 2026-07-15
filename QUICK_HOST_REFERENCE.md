# Portfolio Agent - Quick Host Reference

## 🚀 Launch Commands

### Windows (Easiest)
**Option 1: Batch File**
```bash
start_portfolio_agent.bat
```
Double-click the file or run from CMD

**Option 2: PowerShell**
```powershell
.\start_portfolio_agent.ps1
```

**Option 3: Manual (PowerShell)**
```powershell
cd portfolio-agent
$env:PYTHONPATH = "."
venv\Scripts\Activate.ps1
python web_ui/app.py
```

---

## 🌐 Access URLs

| Host Type | URL | Access From |
|-----------|-----|-------------|
| **Local** | http://localhost:5000 | Same machine only |
| **Network** | http://<YOUR_IP>:5000 | Any machine on LAN |
| **Network** | http://<YOUR_NAME>:5000 | Any machine (if DHCP) |
| **External** | http://PUBLIC_IP:5000 | Internet (if port forwarded) |

---

## 📍 Find Your Host Information

**Windows Command Prompt or PowerShell:**
```powershell
# Machine name
$env:COMPUTERNAME

# IP address
ipconfig

# Full network info
ipconfig /all
```

**Example Output:**
```
YOUR_MACHINE_IP:    192.168.1.100
YOUR_MACHINE_NAME:  LAPTOP-USER
NETWORK_ACCESS:     http://LAPTOP-USER:5000
                    http://192.168.1.100:5000
LOCAL_ACCESS:       http://localhost:5000
```

---

## ✅ Startup Checklist

- [ ] Python 3.11+ installed
- [ ] `cd portfolio-agent` in terminal
- [ ] Run `start_portfolio_agent.bat` or `.ps1`
- [ ] Wait for "Running on http://..."
- [ ] Open http://localhost:5000 in browser
- [ ] Verify all 5 pages load (Dashboard, Portfolio, Scenarios, Recommendations, Reports)

---

## 🔧 Server Status

**Running Successfully When You See:**
```
✅ Portfolio loaded successfully
   Portfolio Value: $67,442,744
   Treaties: 50

🚀 Starting Flask server on http://localhost:5000
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.29.62:5000
 * Debugger PIN: 131-773-109
```

**Stop Server:** Press `CTRL+C` in terminal

---

## 📊 Dashboard Pages

1. **Dashboard** `/` - KPIs & Portfolio Overview
2. **Portfolio** `/portfolio` - Treaty Details & Filtering  
3. **Scenarios** `/scenarios` - Monte Carlo & Stress Tests
4. **Recommendations** `/recommendations` - Optimization Suggestions
5. **Reports** `/reports` - Report Generation

---

## 🌍 Remote Access Setup

**To allow other machines to connect:**

1. **Get your IP:**
   ```powershell
   ipconfig
   ```
   Look for IPv4 Address (e.g., 192.168.1.100)

2. **Start server** (already listening on 0.0.0.0:5000)

3. **Share URL with others:**
   ```
   http://192.168.1.100:5000
   ```

4. **Allow through firewall:**
   - Windows Defender Firewall
   - Allow Python.exe for port 5000
   - Or disable firewall for testing

---

## 🚫 Troubleshooting

| Problem | Solution |
|---------|----------|
| "No module named 'flask'" | Run `pip install -r requirements.txt` |
| "No module named 'data_connectors'" | Set `$env:PYTHONPATH = "."` before running |
| Port 5000 already in use | Change port in `web_ui/app.py` line 136 |
| Can't access from another machine | Check firewall, verify IP, use network IP not localhost |
| Dashboard pages show 404 | Verify static files exist in `web_ui/templates/` |

---

## 📝 Configuration Files

- **Startup Scripts:** `start_portfolio_agent.bat`, `start_portfolio_agent.ps1`
- **Main App:** `web_ui/app.py`
- **Port Config:** Line 136 of `app.py`
- **Dependencies:** `requirements.txt`
- **Detailed Docs:** `HOST_CONFIGURATION.md`

---

## 🎯 Next Steps

1. ✅ Start server with startup script
2. ✅ Open http://localhost:5000
3. ✅ Explore 5 dashboard pages
4. ✅ Test scenario simulations
5. ✅ Review optimization recommendations
6. 📖 See HOST_CONFIGURATION.md for advanced setup
