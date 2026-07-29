# Portfolio Dashboard - KPI (Key Performance Indicator) Implementation

## **Local Access**
**URL:** `http://localhost:5001/`

**Main File:** `web_ui/templates/dashboard.html`

---

## **Complete KPI List - 4 Core + 2 Risk Metrics**

### **1️⃣ PORTFOLIO VALUE**
**Label:** Portfolio Value  
**Unit:** US Dollars (Millions)  
**Display Format:** $XXX.XM (e.g., $236.5M)  

**Definition:** Total monetary value of all reinsurance contracts in the portfolio combined.

**Calculation:** Sum of all treaty premiums in the portfolio

**Formula:**
```
Portfolio Value = SUM(All Treaty Premiums)
```

**Example:** 50 treaties with average premium of $4.73M = $236.5M total

**Use Case:** 
- Understand total portfolio size
- Compare portfolio growth over time
- Assess exposure magnitude

**API Endpoint:** `/api/portfolio/summary`  
**Field Name:** `portfolio_value`  
**Refresh Rate:** Every 60 seconds

---

### **2️⃣ CAPITAL UTILIZATION**
**Label:** Capital Utilization  
**Unit:** Percentage (%)  
**Display Format:** XXX.X% (e.g., 65.2%)  

**Definition:** Percentage of available capital that is currently deployed/allocated across the portfolio.

**Calculation:** 
```
Capital Utilization % = (Capital Allocated / Total Available Capital) × 100
```

**Optimal Range:**
- ✅ 70-95% = Healthy (good balance between deployment and reserves)
- ⚠️ 95-110% = Adequate (high utilization, lower safety margin)
- ❌ >110% = Insufficient (over-leveraged, risky)

**Example:** If $100M capital available and $65.2M is deployed = 65.2% utilization

**Business Implication:**
- Too Low (< 70%): Unused capital, inefficient deployment
- Too High (> 110%): Risk exposure exceeds available capital

**Use Case:**
- Determine if portfolio can absorb major losses
- Decide on new investment opportunities
- Monitor regulatory capital requirements

**API Endpoint:** `/api/portfolio/summary`  
**Field Name:** `capital_utilization`  
**Status Display:**
- Adequate: Green ✅ (if <90%)
- Adequate: Yellow ⚠️ (if 90-110%)
- Insufficient: Red ❌ (if >110%)

---

### **3️⃣ AVERAGE RORAC (Return On Risk-Adjusted Capital)**
**Label:** Average RORAC  
**Unit:** Percentage (%)  
**Display Format:** XX.X% (e.g., 22.5%)  

**Definition:** Average return earned per dollar of risk-adjusted capital invested across all treaties.

**Calculation:**
```
RORAC % = (Total Portfolio Profit / Risk-Adjusted Capital) × 100
```

**Optimal Range:**
- 🌟 20%+ = Excellent (capital working hard)
- ✅ 15-20% = Good (acceptable returns)
- ⚠️ 10-15% = Fair (underperforming)
- ❌ <10% = Poor (capital inefficiency)

**Example:** $10M capital generates $2.25M profit = 22.5% RORAC

**Business Implication:**
- Measures profitability vs. risk taken
- Higher RORAC = more profitable use of capital
- Compare treaties to identify best performers

**Use Case:**
- Portfolio performance assessment
- Capital allocation decisions
- Competitive benchmarking vs. industry
- Bonus/performance evaluations

**API Endpoint:** `/api/portfolio/summary`  
**Field Name:** `average_rorac`  
**Why Important:** Single metric showing both profitability AND risk management

---

### **4️⃣ DIVERSIFICATION SCORE**
**Label:** Diversification Score  
**Unit:** Decimal Scale (0 to 1.0)  
**Display Format:** 0.XX (e.g., 0.78)  

**Definition:** Measure of how well portfolio is spread across different Lines of Business (LOBs) and geographies to reduce concentration risk.

**Calculation:**
```
Diversification Score = 1 - SUM((LOB_Percentage)² + (Geography_Percentage)²)
```

**Interpretation:**
- 🌟 0.8-1.0 = Excellent (well-diversified)
- ✅ 0.6-0.8 = Good (adequate diversification)
- ⚠️ 0.4-0.6 = Fair (some concentration)
- ❌ <0.4 = Poor (highly concentrated)

**Example:** 
- Score 0.78 = Diversified across LOBs and geographies
- Score 0.35 = Heavily concentrated in 1-2 LOBs or regions

**Risk Implication:**
- Low score: If one LOB/region performs poorly, entire portfolio suffers
- High score: One LOB failure doesn't destroy portfolio

**Use Case:**
- Monitor portfolio concentration risk
- Identify over-exposure to single LOB/region
- Strategic rebalancing decisions

**API Endpoint:** `/api/portfolio/summary`  
**Field Name:** `diversification_score`  
**Concentration Risk Status:**
- Low: Green ✅ (if score >0.7)
- Moderate: Yellow ⚠️ (if score 0.5-0.7)
- High: Red ❌ (if score <0.5)

---

## **Risk Metrics (Derived from Core KPIs)**

### **5️⃣ CAPITAL ADEQUACY** *(Calculated from Capital Utilization)*
**Status:** Calculated Risk Metric  
**Formula:** IF Capital Utilization < 90% THEN "✅ Adequate" ELSE IF < 110% THEN "⚠️ Adequate" ELSE "❌ Insufficient"

**Definition:** Whether current capital levels are sufficient to cover expected losses and regulatory requirements.

**Display Options:**
- ✅ Adequate (Safe - can absorb losses)
- ⚠️ Adequate (Tight - limited buffer)
- ❌ Insufficient (Risky - needs capital injection)

---

### **6️⃣ CONCENTRATION RISK** *(Calculated from Diversification Score)*
**Status:** Calculated Risk Metric  
**Formula:** IF Diversification Score > 0.7 THEN "✅ Low" ELSE IF > 0.5 THEN "⚠️ Moderate" ELSE "❌ High"

**Definition:** Risk that portfolio is too concentrated in specific LOBs or geographies.

**Display Options:**
- ✅ Low (Well-diversified, low concentration risk)
- ⚠️ Moderate (Acceptable but some concentration)
- ❌ High (Dangerous concentration, rebalance needed)

---

## **Supplementary Visualizations**

### **📊 Portfolio by Line of Business Chart**
- **Type:** Doughnut chart (Chart.js)
- **Data:** Breakdown of portfolio across 5 LOBs:
  - Property Catastrophe
  - Casualty
  - Marine & Aviation
  - Financial Lines
  - Specialty
- **Colors:** Multi-colored segments
- **Use:** Visual identification of LOB concentration

### **🗺️ Geographic Distribution Chart**
- **Type:** Doughnut chart (Chart.js)
- **Data:** Breakdown across 5 regions:
  - North America
  - Europe
  - Asia Pacific
  - Latin America
  - Africa/Middle East
- **Colors:** Multi-colored segments
- **Use:** Visual identification of geographic concentration

---

## **Top 3 Recommendations Section**

**Display:** Ranked by priority and confidence score

**Fields per Recommendation:**
1. **Title** - What to do (e.g., "Increase Property Catastrophe Exposure")
2. **Priority Badge** - High/Medium/Low
   - High: Red 🔴
   - Medium: Yellow 🟡
   - Low: Green 🟢
3. **Description** - Business justification for recommendation
4. **Confidence Score** - 0-100% (how confident system is)

**Example Recommendation:**
```
Title: "Rebalance LOB Mix"
Priority: High
Description: "Current property catastrophe exposure is 35%. 
Recommend increasing to 45% based on market opportunities 
and improved pricing. Expected RORAC increase to 24%."
Confidence: 92%
```

---

## **Live Update Features**

### **⏰ Timestamp Display**
- **Format:** "Last updated: [Date] [Time] IST"
- **Timezone:** Asia/Kolkata (IST - Indian Standard Time)
- **Refresh Rate:** Every 1 second (visual clock)
- **Example:** "Last updated: Jul 15, 2026, 2:35:45 PM IST"

### **🔄 Auto-Refresh Schedule**
- **Portfolio Data:** Every 60 seconds (1 minute)
- **Timestamp:** Every 1 second
- **Manual Refresh:** "Refresh" button for instant update

---

## **KPI Data Sources**

| KPI | Source | Calculation Location |
|-----|--------|----------------------|
| Portfolio Value | Mock Portfolio (50 treaties) | `mock_portfolio.py` |
| Capital Utilization | Portfolio summary metrics | `scenario_analyzer.py` |
| Average RORAC | Treaty RORAC average | `scenario_analyzer.py` |
| Diversification Score | LOB & Geography distribution | `scenario_analyzer.py` |
| Capital Adequacy | Derived from Capital Util. | `dashboard.html` JavaScript |
| Concentration Risk | Derived from Diversification | `dashboard.html` JavaScript |

---

## **API Endpoints for KPIs**

### **GET /api/portfolio/summary**
Returns core KPI data:
```json
{
  "portfolio_value": 236500000,
  "capital_utilization": 65.2,
  "average_rorac": 22.5,
  "diversification_score": 0.78,
  "total_capital": 362300000
}
```

### **GET /api/portfolio/metrics**
Returns chart data:
```json
{
  "lob_breakdown": {
    "Property Catastrophe": 85000000,
    "Casualty": 78000000,
    "Marine & Aviation": 42000000,
    "Financial Lines": 18000000,
    "Specialty": 13500000
  },
  "geography_breakdown": {
    "North America": 94600000,
    "Europe": 56000000,
    "Asia Pacific": 52500000,
    "Latin America": 21400000,
    "Africa/Middle East": 12000000
  }
}
```

### **GET /api/recommendations**
Returns top recommendations:
```json
{
  "recommendations": [
    {
      "title": "Rebalance Portfolio",
      "priority": "High",
      "business_justification": "Increase Property Catastrophe exposure to 45%",
      "confidence_score": 0.92
    }
  ]
}
```

---

## **KPI Performance Targets**

| KPI | Target Range | Warning | Critical |
|-----|--------------|---------|----------|
| Portfolio Value | Growing year-over-year | Declining | Major decline |
| Capital Utilization | 75-95% | <70% or >100% | >110% |
| Average RORAC | 20%+ | 15-20% | <10% |
| Diversification Score | 0.7-1.0 | 0.5-0.7 | <0.5 |
| Capital Adequacy | Adequate ✅ | Adequate ⚠️ | Insufficient ❌ |
| Concentration Risk | Low ✅ | Moderate ⚠️ | High ❌ |

---

## **Real-Time Features**

✅ **Real-time KPI updates** every 60 seconds  
✅ **Live clock display** in IST timezone  
✅ **Interactive charts** with hover information  
✅ **Color-coded risk indicators** (Green/Yellow/Red)  
✅ **One-click refresh button** for immediate update  
✅ **Responsive design** on all devices  

---

## **Dashboard File Structure**

```
web_ui/templates/dashboard.html
├── Navbar (navigation to all pages)
├── Header (title + refresh buttons)
├── 4 KPI Cards
│   ├── Portfolio Value ($XXX.XM)
│   ├── Capital Utilization (X.X%)
│   ├── Average RORAC (X.X%)
│   └── Diversification Score (0.XX)
├── 2 Charts
│   ├── LOB Breakdown (doughnut)
│   └── Geographic Distribution (doughnut)
├── Risk Assessment (2 metrics)
│   ├── Capital Adequacy
│   └── Concentration Risk
├── Top Recommendations (3 items)
└── Auto-refresh logic
```

---

## **Backend Integration**

**Flask Endpoints (app_simple.py):**
```python
@app.route('/api/portfolio/summary')
def get_portfolio_summary():
    # Returns core 4 KPIs
    
@app.route('/api/portfolio/metrics')
def get_portfolio_metrics():
    # Returns chart data (LOB + Geography breakdown)
    
@app.route('/api/recommendations')
def get_recommendations():
    # Returns top 3 recommendations with priority & confidence
```

---

## **KPI Refresh Triggers**

1. **Page Load** - Immediately fetch all KPIs
2. **Auto-Refresh** - Every 60 seconds
3. **Manual Refresh** - User clicks "Refresh" button
4. **Navigation** - When returning to Dashboard from other pages

---

## **Summary**

**Dashboard displays 6 key metrics:**

| # | KPI | Type | Unit | Purpose |
|---|-----|------|------|---------|
| 1 | Portfolio Value | Measurement | $ Millions | Portfolio size |
| 2 | Capital Utilization | Percentage | % | Capital deployment |
| 3 | Average RORAC | Return | % | Profitability efficiency |
| 4 | Diversification Score | Risk | 0-1.0 | Concentration risk |
| 5 | Capital Adequacy | Status | Derived | Safety assessment |
| 6 | Concentration Risk | Status | Derived | Portfolio risk |

**Plus:**
- 2 Interactive charts (LOB & Geography breakdown)
- 3 Top recommendations with confidence scores
- Live timestamp in IST
- Auto-refresh every 60 seconds

**Total Updated:** July 16, 2026  
**Status:** Production Ready ✅
