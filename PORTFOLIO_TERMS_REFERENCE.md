# Portfolio Details - Complete Reference Guide

## Local Access

**URL:** `http://localhost:5001/portfolio`

**Files:**
- Frontend: `web_ui/templates/portfolio-dynamic.html`
- Backend: `web_ui/app_simple.py`
- Data Source: `data_connectors/mock_portfolio.py`

---

## Core Treaty Information

### Treaty ID
**Unique identifier/number** assigned to each reinsurance contract for tracking and management purposes.
- Example: `TR-2026-0042`
- Used to reference specific contracts in reports and communications

### LOB (Line of Business)
**Category of insurance coverage** that defines the type of risk being insured.
- Property Catastrophe
- Casualty
- Marine & Aviation
- Financial Lines
- Specialty

### Geography
**Geographic region where the insurance risk is located** - determines regulatory environment and risk profile.
- North America
- Europe
- Asia Pacific
- Latin America
- Africa/Middle East

---

## Financial Metrics

### Premium
**Money received from clients** for providing insurance coverage over the contract period.
- Example: $8.5M received for one-year coverage
- Higher premiums = more revenue from clients
- Represents the top-line income before any claims

### RORAC (Return On Risk-Adjusted Capital)
**Percentage return earned per dollar of capital invested** - measures how efficiently capital is being used.
- Formula: (Profit / Risk-Adjusted Capital) × 100
- Example: 22.5% means earning $0.225 for every $1 of capital allocated
- **Good RORAC: 20%+**
- **Poor RORAC: Below 10%**
- Used to compare profitability between different treaties

### Loss Ratio
**Percentage of premiums paid out as insurance claims** - indicates claim severity and underwriting accuracy.
- Formula: (Claims Paid / Premium Received) × 100
- Example: 45% loss ratio on $8.5M premium = $3.8M in claims paid
- **Excellent: Below 50%** (profitable)
- **Acceptable: 50-70%** (still profitable but higher risk)
- **Warning: 70%+** (paying too much in claims, need to review)

### Expected Profit
**Forecasted earnings after all claims and operational costs** - bottom-line profitability.
- Formula: Premium - Expected Claims - Operating Costs
- Example: $8.5M (Premium) - $3.8M (Claims) - $0.5M (Costs) = $4.2M Profit
- Positive profit means the contract is financially viable
- Used to assess contract attractiveness

---

## Risk & Quality Metrics

### Rating
**Credit/financial strength rating** indicating the likelihood of claims being paid without default.
- **AAA:** Exceptional - virtually no risk
- **AA:** Very Strong - very low risk
- **A:** Strong - low risk
- **BBB:** Adequate - moderate risk
- **BB:** Speculative - higher risk
- **C:** Highly Risky - potential default risk

### Underwriter
**Person or team responsible for** assessing, approving, and managing the insurance contract.
- Evaluates risk
- Sets premium rates
- Monitors contract performance
- Example: John Smith, Mary Johnson

### Performance Status
**Current health/condition of the contract** indicating how well it's performing against expectations.

| Status | Meaning | Action |
|--------|---------|--------|
| **Adequate** | Contract performing as expected - no issues | Monitor regularly |
| **Warning** | Performance declining or risk emerging - needs attention | Review and adjust |
| **Critical** | Serious problems - contract at risk - urgent action needed | Immediate intervention |

---

## Data Categories - Line of Business (LOB)

### 1. Property Catastrophe
**Insurance for major natural disaster coverage** - protects against large-scale catastrophic events.
- Covers: Hurricanes, earthquakes, floods, tornados, wildfires
- Premium Range: High (due to high potential losses)
- Loss Ratio: Variable (depends on natural disaster occurrence)
- Key Metric: Return period of events (1-in-100 year, 1-in-200 year)
- Example: Treaty covers property damage in hurricane-prone areas

### 2. Casualty
**Insurance for accidents, injuries, and legal liability** - covers bodily injury and property damage claims.
- Covers: Auto accidents, workplace injuries, slip & fall, legal liability
- Premium Range: Moderate
- Loss Ratio: More predictable (historical data available)
- Key Metric: Claims per policy, average claim cost
- Example: Liability coverage for commercial businesses

### 3. Marine & Aviation
**Insurance for ships, aircraft, cargo, and maritime risks** - specialized insurance for transportation.
- Covers: Cargo loss/damage, ship collisions, aircraft accidents, piracy
- Premium Range: High (specialized risks)
- Loss Ratio: Volatile (rare but severe events)
- Key Metric: Shipping routes, aircraft types
- Example: Coverage for international cargo shipments

### 4. Financial Lines
**Insurance for financial losses and professional liability** - protects financial institutions and professionals.
- Covers: Directors & Officers liability, professional liability, financial crime, errors & omissions
- Premium Range: Moderate to High
- Loss Ratio: Lower than property (fewer but larger claims)
- Key Metric: Industry type, claim history
- Example: Coverage for bank executives against litigation risk

### 5. Specialty
**Niche/specialized insurance for unique risks** - covers non-standard risks requiring expertise.
- Covers: Cyber attacks, kidnap & ransom, political risk, product recall, event cancellation
- Premium Range: Highly variable
- Loss Ratio: Unpredictable (limited historical data)
- Key Metric: Risk-specific factors
- Example: Coverage for data breach liability

---

## Geographic Regions

### North America
**USA, Canada, Mexico** - Most developed insurance market
- Characteristics: Large premiums, strict regulation, lower loss ratios
- Risk Profile: Well-established, predictable
- Market: Most competitive, highest volume
- Example Treaties: Auto, property, workers compensation

### Europe
**EU countries, UK, Switzerland** - Highly regulated insurance market
- Characteristics: Moderate premiums, strong regulatory oversight, organized market
- Risk Profile: Stable, compliant
- Market: Mature, consolidating
- Example Treaties: Motor, liability, health

### Asia Pacific
**Japan, Australia, Singapore, India, China** - Growing rapidly
- Characteristics: High premiums, emerging risks, regulatory variation
- Risk Profile: Growing but less predictable
- Market: Fastest growing, high potential
- Example Treaties: Natural disaster, cyber, auto

### Latin America
**Brazil, Argentina, Chile, Colombia, Mexico** - Emerging market
- Characteristics: Moderate to high premiums, developing infrastructure, variable regulation
- Risk Profile: Moderate risk, improving
- Market: Growth opportunity
- Example Treaties: Property, casualty, specialty

### Africa/Middle East
**African continent, Saudi Arabia, UAE, Israel** - Specialized market
- Characteristics: Highest premiums, specialized underwriting needed, limited competition
- Risk Profile: Higher risk, requires expertise
- Market: Niche, specialized knowledge required
- Example Treaties: Political risk, property, specialty

---

## Filtering & Sorting Options

### Filter by Line of Business (LOB)
**View only treaties in a specific insurance category.**
- All LOBs (default view)
- Property Catastrophe (disaster coverage)
- Casualty (accident & liability)
- Marine & Aviation (transportation)
- Financial Lines (professional liability)
- Specialty (niche risks)

**Use Case:** Manager wants to review only property catastrophe exposure

### Filter by Geography
**View only treaties serving specific regions.**
- All Geographies (default view)
- North America
- Europe
- Asia Pacific
- Latin America
- Africa/Middle East

**Use Case:** Regional manager analyzing Asia Pacific portfolio

### Sort by RORAC (Highest)
**Rank treaties from highest to lowest return** - identifies best-performing investments.
- 28% RORAC (top)
- 22% RORAC
- 15% RORAC
- 8% RORAC (bottom)

**Use Case:** CFO identifies highest-yield contracts for investment priority

### Sort by Premium (Highest)
**Rank treaties by revenue size** - identifies largest income-generating contracts.
- $15M premium (top)
- $12M premium
- $8M premium
- $2M premium (bottom)

**Use Case:** Revenue manager focuses on biggest income sources

### Sort by Expected Profit (Highest)
**Rank by forecast earnings** - identifies most profitable contracts.
- $4.5M profit (top)
- $3.2M profit
- $1.8M profit
- -$0.5M loss (bottom)

**Use Case:** Profitability analysis for portfolio optimization

### Sort by Loss Ratio (Lowest)
**Identify treaties with lowest claims payouts** - highlights healthiest contracts.
- 30% loss ratio (excellent)
- 50% loss ratio (good)
- 70% loss ratio (concerning)
- 85% loss ratio (critical)

**Use Case:** Risk manager identifies underwriting issues in high-loss contracts

---

## Example Treaty Breakdown

### Treaty Details:
```
Treaty ID:          TR-2026-0042
Line of Business:   Property Catastrophe
Geography:          Asia Pacific
Premium:            $8.5M
RORAC:              22.5%
Loss Ratio:         45%
Expected Profit:    $4.2M
Rating:             AA
Underwriter:        John Smith
Performance Status: Adequate
```

### What This Means:

| Field | Value | Interpretation |
|-------|-------|-----------------|
| Treaty ID | TR-2026-0042 | This is contract #42 from 2026 |
| LOB | Property Catastrophe | Covers major disasters (hurricanes, earthquakes) |
| Geography | Asia Pacific | Serves customers in Japan, Australia, Singapore, India |
| Premium | $8.5M | Received $8.5M from clients for this coverage |
| RORAC | 22.5% | Earning 22.5% return on invested capital = EXCELLENT |
| Loss Ratio | 45% | Paying out 45% of premium as claims = GOOD (profitable) |
| Expected Profit | $4.2M | Forecast profit = $4.2M (Premium - Claims - Costs) |
| Rating | AA | Very Strong financial rating = LOW DEFAULT RISK |
| Underwriter | John Smith | John is responsible for managing this contract |
| Status | Adequate | Contract is performing as expected = NO ISSUES |

---

## Why These Metrics Matter

### RORAC (Return On Risk-Adjusted Capital)
- **Why:** Measures how efficiently capital is being deployed
- **Good:** 20%+ = capital is working hard, generating strong returns
- **Poor:** Below 10% = capital underutilized, consider reallocating
- **Action:** Move capital from low RORAC to high RORAC treaties

### Loss Ratio
- **Why:** Indicates underwriting quality and claim experience
- **Excellent:** Below 50% = underwriting is accurate, clients are good risks
- **Warning:** 70%+ = either prices are too low OR clients are riskier than expected
- **Action:** Increase premiums or tighten underwriting standards for high-ratio contracts

### Rating (Credit Quality)
- **Why:** Predicts likelihood of being able to pay claims when due
- **Strong (AA):** Unlikely to default, safe
- **Weak (C):** May default on claims, risky
- **Action:** Avoid concentrating portfolio in low-rated counterparties

### Performance Status
- **Why:** Early warning indicator of contract health
- **Adequate:** No intervention needed, monitor normally
- **Warning:** Problems emerging, needs review and adjustment
- **Critical:** Urgent action required to prevent major loss
- **Action:** Critical treaties require immediate management attention

### Premium Size
- **Why:** Indicates concentration risk and strategic importance
- **High Premium:** Large exposure, significant revenue, requires careful management
- **Low Premium:** Minor exposure, limited financial impact
- **Action:** Diversify portfolio - avoid over-concentration in few large treaties

---

## Key Insights for Portfolio Management

### Portfolio Health Check:
1. **Are we earning good RORAC?** (Target: 20%+)
2. **Are loss ratios acceptable?** (Target: Below 60%)
3. **Any critical performance treaties?** (Action: Address immediately)
4. **Is portfolio well-diversified?** (Check across LOBs and geographies)

### Optimization Opportunities:
- Rebalance capital from low-RORAC to high-RORAC treaties
- Review treaties with high loss ratios (45%+)
- Increase premiums on underperforming contracts
- Diversify away from concentrated LOBs or regions
- Phase out critical-status treaties

### Risk Monitoring:
- Watch for trends in loss ratios increasing
- Monitor concentration risk (too many in one LOB/region)
- Track underwriter performance
- Review status changes (Adequate → Warning → Critical)

---

## Quick Reference - Healthy Portfolio Ranges

| Metric | Excellent | Acceptable | Warning |
|--------|-----------|-----------|---------|
| RORAC | 20%+ | 15-20% | Below 15% |
| Loss Ratio | 30-50% | 50-70% | Above 70% |
| Rating | AA-AAA | A-BBB | BB-C |
| % Adequate Status | 85%+ | 70-85% | Below 70% |
| Profit Margin | 40%+ | 25-40% | Below 25% |

---

## File Locations for Reference

**Frontend Code:** `web_ui/templates/portfolio-dynamic.html` (400+ lines, filtering & display logic)

**Backend API:** `web_ui/app_simple.py` (Flask endpoint `/api/portfolio` returns treaty data)

**Data Generator:** `data_connectors/mock_portfolio.py` (Creates 50 synthetic treaties)

**Main App:** `web_ui/app_simple.py` (Port 5001, serves all dashboard pages)

---

**Last Updated:** July 15, 2026  
**Portfolio Agent Version:** 1.0  
**Status:** Production Ready
