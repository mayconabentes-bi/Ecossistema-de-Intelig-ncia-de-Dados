# CDL Manaus Intelligence Hub - Strategic Core

## 🎯 Overview

This implementation provides the core data processing and intelligence system for CDL Manaus, following the **Vibe Coding** methodology: Strategic Vision + Functional Execution.

## 📂 Architecture

```
src/
├── __init__.py           # Package initialization
├── data_processor.py     # Core data cleaning and KPI calculations
├── forecasting.py        # ARIMA time series forecasting
├── bcg_matrix.py         # BCG Matrix product classification
└── bias_detector.py      # Analytical bias detection system

streamlit_app.py          # Main Streamlit dashboard interface
requirements.txt          # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📊 Features

### 1. Data Processing (Strategic Consultant Workflow)
- **Data Cleaning**: Handles missing values, outliers, and data quality issues
- **KPI Calculations**: 
  - Accumulated Revenue (R$ 13,098,238)
  - Target Gap (currently 28%)
  - Monthly variance tracking
  - Delinquency monitoring with std deviation alerts

### 2. Revenue Forecasting
- **ARIMA Model**: Auto-optimized parameters for December 2025 projection
- **Alternative Methods**: Moving average and trend-based forecasts
- **Confidence Intervals**: 95% confidence bounds
- **Model Evaluation**: AIC scoring and stationarity tests

### 3. BCG Matrix Analysis
Automatic product classification:
- ⭐ **Stars**: High growth + High market share
- 💰 **Cash Cows**: Low growth + High market share
- ❓ **Question Marks**: High growth + Low market share
- 🐕 **Dogs**: Low growth + Low market share

Products analyzed:
- Consultas (Queries)
- Certificados (Certificates)
- CDL Saúde (Healthcare)

### 4. Bias Detection (Vigilância)
Monitors and alerts for:
- **Survivorship Bias**: Active vs inactive members
- **Selection Bias**: Top 20 concentration risk
- **Recency Bias**: Limited historical data warnings

Severity levels: CRITICAL, HIGH, MEDIUM, LOW

### 5. Scenario Simulator
Interactive what-if analysis:
- "What if Bemol delinquency drops 5%?"
- Adjust any parameter and see impact
- Side-by-side KPI comparison
- Visual impact analysis

## 📈 Dashboard Pages

### 1. 📈 Dashboard Overview
- Real-time KPI cards
- Revenue vs Target chart
- Delinquency monitoring with alert threshold
- Detailed monthly data table

### 2. 🔮 Revenue Forecast
- Multiple forecasting methods
- December 2025 projection
- Confidence interval visualization
- Model performance metrics

### 3. 📊 BCG Matrix
- Interactive scatter plot with quadrants
- Strategic recommendations per product
- Growth vs market share analysis
- Full portfolio report

### 4. ⚠️ Bias Detection
- Comprehensive bias analysis
- Severity-based alerting
- Detailed recommendations
- Downloadable reports

### 5. 🎮 Scenario Simulator
- Parameter adjustment interface
- Baseline vs scenario comparison
- Visual impact charts
- Strategic insights

## 🔧 Technical Details

### Object-Oriented Design
All modules follow OOP principles:
- **DataProcessor**: Main data handling class
- **BillingForecaster**: Time series forecasting
- **BCGMatrixAnalyzer**: Portfolio analysis
- **BiasDetector**: Quality assurance

### Modular Architecture
- Clean separation of concerns
- Reusable components
- Easy integration with FMI pricing tables
- Extension-ready for future features

### Logging System
Comprehensive logging for:
- Data quality issues
- Outlier detection
- Model performance
- Bias alerts

## 📊 Sample Data

The system includes simulated CDL Manaus data (Jan-Nov 2025):
- Monthly billing: R$ 1.15M - R$ 1.28M
- Total accumulated: R$ 13,098,238
- Top 20 concentration: 35-45%
- Delinquency: R$ 85K - R$ 145K

## 🎓 Business Logic

### Gap Calculation
```
Gap % = ((Real - Target) / Target) × 100
Current: -28% (below target)
```

### Delinquency Alert
```
Alert if: Current > (Mean + Std Deviation)
Visual indicator on dashboard
```

### BCG Thresholds
```
Market Share: 30% (configurable)
Growth Rate: 0% (configurable)
```

### ARIMA Selection
```
Auto-selects best (p,d,q) based on:
- AIC score minimization
- Stationarity tests
- Seasonal patterns
```

## 🔄 Integration Ready

The system is designed for easy integration with:
- **FMI Tables**: Minimum billing price tables
- **ERP Systems**: CSV import via webapp
- **External APIs**: RESTful endpoints (Flask app)
- **Power BI**: Data export capabilities

## 🎯 Vibe Coding Philosophy

This implementation reflects Strategic Consultant thinking:

1. **Start with Why**: Understanding CDL Manaus's 28% gap problem
2. **Data Quality First**: Rigorous cleaning and validation
3. **Bias Awareness**: Active monitoring for analytical blind spots
4. **Actionable Insights**: Every metric tied to business decision
5. **Modular Design**: Easy to maintain and extend

## 📚 Documentation

Each module includes:
- Comprehensive docstrings
- Type hints for clarity
- Usage examples in code
- Logging for observability

## 🚦 Next Steps

To use with real CDL Manaus data:

1. **Replace Sample Data**: Load actual PDF extracts
2. **Configure Parameters**: Adjust thresholds based on business rules
3. **Connect Database**: Link to production data sources
4. **Deploy Dashboard**: Host on cloud platform
5. **Setup Alerts**: Integrate with WhatsApp/Email

## 📞 Support

For questions or issues:
- Review inline code documentation
- Check logging output for diagnostics
- Refer to main project README.md

---

**Built with Strategic Vision • Coded with Functional Excellence**

*CDL Manaus Intelligence Hub - Transforming Data into Decisions*
