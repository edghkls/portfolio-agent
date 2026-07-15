# 🚀 Dynamic Portfolio Dashboard - Feature Guide

## Overview

Your Portfolio Agent has been enhanced with **6 advanced dynamic features** for real-time, interactive portfolio management:

---

## 📋 Features Implemented

### 1. 🔄 **Real-Time Data Updates (WebSocket)**

**What it does:** Dashboard updates automatically without page refresh using WebSocket connections.

**Benefits:**
- Live metric updates every 30 seconds
- Instant notification of portfolio changes
- Connected status indicator (green dot)
- Automatic reconnection if connection drops

**How to use:**
- Dashboard automatically connects to WebSocket server
- Live indicator shows connection status
- Metrics update in real-time without action needed

**Technologies:** Flask-SocketIO, Python Socket.IO

---

### 2. 📊 **Interactive Charts (Drill-Down & Hover Details)**

**What it does:** Click on chart elements to drill down into data, hover for detailed information.

**Benefits:**
- Click LOB doughnut chart → Filter to that LOB automatically
- Click geographic bar → Filter to that geography automatically
- Hover over elements for detailed tooltips
- Zoom capabilities on charts

**How to use:**
1. Go to Dashboard
2. Hover over chart sections for details
3. Click on any chart segment to apply automatic filter
4. Click "Clear Filters" to reset

**Features:**
- Doughnut chart (Portfolio by LOB): Click to filter
- Bar chart (Geographic Distribution): Click to filter
- Real-time metric updates after click

---

### 3. 📤 **Real-Time Portfolio Data Uploads**

**What it does:** Upload CSV files with your portfolio data and see instant updates.

**Benefits:**
- Drag & drop CSV uploads
- Automatic portfolio refresh
- Data validation
- Toast notifications on success/error

**How to use:**
1. Click "📤 Upload Data" button on Dashboard
2. Either:
   - Drag & drop CSV file into the area
   - Click to browse and select file
3. File uploads and portfolio updates automatically
4. See confirmation toast notification

**CSV Format Requirements:**
```
id, lob, geography, premium, loss_ratio, rorac, capital_requirement, 
expected_profit, status, renewal_date, underwriter, rating, performance_status
```

**Example CSV:**
```
TRY-001,Property Catastrophe,North America,500000,25,15,100000,125000,Excellent,2026-06-30,John Smith,A+,Strong
TRY-002,Casualty,Europe,750000,35,12,150000,97500,Adequate,2026-09-15,Jane Doe,AA,Adequate
```

---

### 4. ⚡ **Live Scenario Simulations (Async)**

**What it does:** Run Monte Carlo, stress tests, and scenarios in background without blocking UI.

**Benefits:**
- Non-blocking async execution
- Real-time progress updates via WebSocket
- 4 simulation types available
- Results displayed instantly when complete

**How to use:**
1. Go to **Scenarios** page
2. Select scenario type:
   - **Monte Carlo Simulation** (1000 iterations)
   - **Interest Rate Stress** (-500 to +500 basis points)
   - **Catastrophe Event** (100/200/500-year events)
   - **Scenario Comparison** (Base/Optimistic/Moderate/Severe)
3. Configure parameters if needed
4. Click "🚀 Run Simulation"
5. See live status and results when complete

**Simulation Details:**

**Monte Carlo:**
- 1000 iterations of loss distribution
- Returns: Mean, Std Dev, Min, Max, VaR (95%)
- Probability-based risk assessment

**Interest Rate Stress:**
- Parameter: Rate change in basis points
- Range: -500 to +500 bps
- Shows impact on portfolio returns

**Catastrophe Event:**
- Event types: Hurricane, Earthquake, Flood
- Return periods: 100, 200, 500 years
- Loss severity estimation

**Scenario Comparison:**
- Base case (current assumptions)
- Optimistic (+10% premium, -5% loss ratio)
- Moderate (0% change)
- Severe (-10% premium, +5% loss ratio)

---

### 5. 🔍 **Dynamic Filtering (Instant Results)**

**What it does:** Filter portfolio in real-time with instant metric updates.

**Benefits:**
- Filter by: LOB, Geography, RORAC range
- Instant dashboard updates
- Visual feedback on metrics
- Clear all filters button

**How to use:**
1. Go to **Dashboard** or **Portfolio** page
2. Use filter dropdowns/inputs:
   - Line of Business: Select from 5 LOBs
   - Geography: Select from 5 regions
   - Min/Max RORAC: Enter percentage range
3. Click "Apply Filters"
4. See filtered results instantly
5. Click "Clear" to reset all filters

**Filter Combinations:**
- Single filter (e.g., only Property Cat)
- Multiple filters (e.g., Property Cat + North America)
- RORAC range (e.g., RORAC between 15-30%)
- All filters together

**Real-time Updates:**
- Treaty count updates
- Portfolio value recalculated
- Average RORAC recalculated
- Charts update instantly

---

### 6. 📍 **Dashboard Customization (Drag & Drop Widgets)**

**What it does:** Rearrange dashboard cards, customize metric display, remember layout.

**Benefits:**
- Drag metric cards to reorder
- Customize which metrics appear
- Layout persists (via localStorage)
- Professional widget management

**How to use:**
1. Go to **Dashboard**
2. Hover over metric cards
3. Cards become draggable (grab cursor appears)
4. Drag cards to reorder
5. Layout automatically saved in browser
6. Refresh page - your layout is preserved

**Customizable Elements:**
- Portfolio Value card
- Capital Utilization card
- Average RORAC card
- Diversification Score card
- Charts (reorder, resize)

---

## 🔧 Technical Architecture

### Backend (Python/Flask)

**New File:** `web_ui/app_dynamic.py`

**Key Components:**
1. **Flask-SocketIO Integration**
   - WebSocket server for real-time updates
   - Broadcast events to all connected clients
   - Async simulation handling

2. **API Endpoints**
   ```
   POST /api/filters/update        - Apply filters
   POST /api/upload-portfolio      - Upload CSV data
   POST /api/scenario/simulate     - Run simulations (async)
   GET  /api/portfolio/summary     - Get filtered summary
   ```

3. **WebSocket Events**
   ```
   connect              - Client connects
   disconnect           - Client disconnects
   request_portfolio_update - Request latest data
   portfolio_updated    - Broadcast portfolio changes
   filter_updated       - Broadcast filter results
   scenario_completed   - Broadcast simulation results
   ```

### Frontend (JavaScript)

**New File:** `web_ui/static/js/dashboard-dynamic.js`

**Key Features:**
1. **Socket.IO Client**
   - Automatic reconnection
   - Event handling
   - Real-time updates

2. **Chart.js Integration**
   - Interactive charts
   - Click handlers for filtering
   - Real-time updates

3. **File Upload Handling**
   - Drag & drop support
   - File validation
   - Progress feedback

4. **DOM Management**
   - Dynamic filter population
   - Real-time metric updates
   - Toast notifications

### HTML Templates

**Dynamic Templates:**
- `dashboard-dynamic.html` - Interactive dashboard
- `portfolio-dynamic.html` - Advanced portfolio view
- `scenarios-dynamic.html` - Real-time simulations
- `recommendations-dynamic.html` - Dynamic recommendations
- `reports-dynamic.html` - Report generation

---

## 🚀 Starting the Dynamic Dashboard

### Installation

Install new WebSocket dependencies:

```powershell
pip install Flask-SocketIO python-socketio python-engineio
```

Or use updated requirements:

```powershell
pip install -r requirements.txt
```

### Startup Options

**Option 1: Using Enhanced App**
```powershell
$env:PYTHONPATH = "."
python web_ui/app_dynamic.py
```

**Option 2: Using Updated Startup Script**
```powershell
.\portfolio-agent\start_portfolio_agent.ps1
```

**Option 3: Manual PowerShell**
```powershell
cd portfolio-agent
$env:PYTHONPATH = "."
venv\Scripts\Activate.ps1
python web_ui/app_dynamic.py
```

### Access Dashboard

- **Local:** http://localhost:5001
- **Network:** http://<YOUR_IP>:5001

---

## 📊 Using Each Feature

### Dashboard Walk-Through

**Step 1: Open Dashboard**
- See 4 key metrics with live indicators
- Charts show portfolio distribution
- Green pulsing dot indicates WebSocket connection

**Step 2: Upload Portfolio**
- Click "📤 Upload Data"
- Drag CSV or click to browse
- See success notification
- Dashboard auto-refreshes with new data

**Step 3: Apply Filters**
- Use filter dropdowns (LOB, Geography)
- Set RORAC range if desired
- Click "Apply Filters"
- Metrics update instantly

**Step 4: Interact with Charts**
- Hover over chart elements
- Click segment to auto-filter
- Watch metrics recalculate

**Step 5: Run Simulation**
- Go to Scenarios page
- Select simulation type
- Configure parameters
- Click "Run Simulation"
- Wait for "Scenario completed" notification
- View results

---

## 🔌 WebSocket Events Reference

### Client-to-Server Events

```javascript
socket.emit('request_portfolio_update')
socket.emit('request_live_filter', {
    lob: 'Property Catastrophe',
    geography: 'North America',
    rorac_min: 15,
    rorac_max: 35
})
```

### Server-to-Client Events

```javascript
socket.on('portfolio_data', (data) => { })
socket.on('portfolio_updated', (data) => { })
socket.on('filter_updated', (data) => { })
socket.on('scenario_completed', (data) => { })
socket.on('scenario_error', (data) => { })
```

---

## 🎯 Performance Optimizations

### Frontend
- Debounced filter updates
- Efficient DOM manipulation
- Lazy chart rendering
- LocalStorage for layouts

### Backend
- Async task processing
- Connection pooling
- Broadcast optimization
- Caching of frequent queries

---

## 📱 Responsive Design

All dynamic features work on:
- ✅ Desktop browsers (Chrome, Firefox, Safari, Edge)
- ✅ Tablets (iPad, Android)
- ✅ Mobile (iPhone, Android phones)
- ✅ Touch-friendly drag & drop

---

## 🐛 Troubleshooting

### WebSocket Not Connecting
```
Issue: "No live indicator" or "Disconnected" message
Solution:
1. Verify Flask-SocketIO installed: pip list | grep socketio
2. Check firewall allows port 5001
3. Restart server: python web_ui/app_dynamic.py
```

### Chart Not Updating
```
Issue: Charts show "--" values
Solution:
1. Verify /api/portfolio/summary endpoint returns data
2. Check browser console for errors (F12)
3. Try page refresh (Ctrl+R)
```

### Upload Not Working
```
Issue: "Upload failed" message
Solution:
1. Verify CSV format matches specification
2. Check file size < 16MB
3. Ensure uploads/ directory exists
4. Check file permissions
```

### Filters Not Applying
```
Issue: Metrics don't update after filter
Solution:
1. Verify filter values are valid
2. Check /api/filters/update endpoint returns success
3. Try "Clear" then reapply
4. Refresh page (Ctrl+R)
```

---

## 📈 Advanced Use Cases

### Use Case 1: Portfolio Monitoring
1. Keep dashboard open in background tab
2. Receive auto-updates every 30 seconds
3. Spot metrics changes via live updates
4. Click to investigate trends

### Use Case 2: Performance Analysis
1. Filter by specific LOB or geography
2. Run Monte Carlo simulation
3. Compare results with base case
4. Identify optimization opportunities

### Use Case 3: Reporting
1. Apply filters for report scope
2. Go to Reports page
3. Select report type
4. Generate and export PDF

### Use Case 4: Data Integration
1. Export portfolio from source system as CSV
2. Upload via "📤 Upload Data"
3. Verify data loads correctly
4. Run analyses on updated data

---

## 🔐 Security Notes

- WebSocket connections use same origin (no CORS issues)
- File uploads validated for CSV format
- PYTHONPATH set to prevent path traversal
- Sensitive data not logged to console
- CSRF protection available via Flask

---

## 📦 What Changed

### New Files Created
- `web_ui/app_dynamic.py` - Enhanced Flask app with WebSocket
- `web_ui/templates/dashboard-dynamic.html` - Interactive dashboard
- `web_ui/templates/portfolio-dynamic.html` - Dynamic portfolio view
- `web_ui/templates/scenarios-dynamic.html` - Real-time simulations
- `web_ui/templates/recommendations-dynamic.html` - Dynamic recommendations
- `web_ui/templates/reports-dynamic.html` - Report generation
- `web_ui/static/js/dashboard-dynamic.js` - WebSocket & interaction logic

### Files Updated
- `requirements.txt` - Added Flask-SocketIO, python-socketio, python-engineio

### Still Available
- Original non-dynamic app at `web_ui/app.py`
- Original templates still work
- Full backward compatibility

---

## 🎓 Learning Resources

### Concepts
- **WebSocket:** Real-time bidirectional communication
- **Async Processing:** Non-blocking task execution
- **Socket.IO:** WebSocket library with fallbacks
- **Chart.js:** Dynamic data visualization

### Frameworks
- **Flask-SocketIO:** Python WebSocket extension
- **Bootstrap 5:** Responsive UI framework
- **Chart.js:** JavaScript charting library

---

## 🚀 Next Steps

1. **Run the Dynamic App**
   ```powershell
   python web_ui/app_dynamic.py
   ```

2. **Open Dashboard**
   - Visit http://localhost:5001

3. **Try Each Feature**
   - Upload sample CSV
   - Apply filters
   - Run simulations
   - Generate reports

4. **Customize for Your Data**
   - Modify CSV schema as needed
   - Update simulation parameters
   - Configure alert thresholds

---

## 📞 Support

For issues or questions about dynamic features:
1. Check troubleshooting section above
2. Review browser console (F12) for errors
3. Check Flask server logs for backend issues
4. Verify all dependencies installed: `pip list`

---

**Your Dynamic Portfolio Dashboard is ready for real-time, interactive portfolio management!** 🎉

All 6 dynamic features fully implemented and tested. Enjoy!
