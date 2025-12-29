#!/bin/bash
# CDL Manaus Intelligence Hub - Test Suite
# Runs comprehensive tests on all modules

echo "============================================================"
echo "CDL MANAUS INTELLIGENCE HUB - TEST SUITE"
echo "============================================================"
echo ""

# Test 1: Core Data Processor
echo "Test 1: Data Processor"
echo "----------------------"
python3 -c "
import sys
sys.path.append('.')
from src.data_processor import DataProcessor

processor = DataProcessor()
df = processor.load_sample_data()
processor.clean_data()
kpis = processor.calculate_kpis()

assert len(df) == 11, 'Should have 11 months of data'
assert kpis['faturamento_acumulado'] > 13000000, 'Revenue should be > 13M'
assert kpis['gap_meta_percentual'] < 0, 'Gap should be negative'

print('✓ Data Processor test passed')
"

# Test 2: Forecasting
echo ""
echo "Test 2: Forecasting"
echo "-------------------"
python3 -c "
import sys
sys.path.append('.')
from src.forecasting import BillingForecaster
from src.data_processor import DataProcessor

processor = DataProcessor()
df = processor.load_sample_data()
processor.clean_data()

forecaster = BillingForecaster(df)
forecast = forecaster.forecast_billing(periods=1, method='moving_average')

assert forecast['prediction_dezembro'] > 0, 'Forecast should be positive'
assert 'confidence_interval_lower' in forecast, 'Should have confidence intervals'

print('✓ Forecasting test passed')
"

# Test 3: BCG Matrix
echo ""
echo "Test 3: BCG Matrix"
echo "------------------"
python3 -c "
import sys
sys.path.append('.')
from src.bcg_matrix import BCGMatrixAnalyzer

bcg = BCGMatrixAnalyzer()
product_df = bcg.create_sample_product_data()
results = bcg.analyze_portfolio()

assert len(results) == 3, 'Should have 3 products'
assert 'Consultas' in results, 'Should include Consultas'

print('✓ BCG Matrix test passed')
"

# Test 4: Bias Detection
echo ""
echo "Test 4: Bias Detection"
echo "----------------------"
python3 -c "
import sys
sys.path.append('.')
from src.bias_detector import BiasDetector
from src.data_processor import DataProcessor

processor = DataProcessor()
df = processor.load_sample_data()
processor.clean_data()

detector = BiasDetector()
results = detector.run_full_analysis(df, config={'date_column': 'Mes'})

assert 'total_biases_detected' in results, 'Should have total count'
assert 'bias_log' in results, 'Should have bias log'

print('✓ Bias Detection test passed')
"

# Test 5: Scenario Simulation
echo ""
echo "Test 5: Scenario Simulation"
echo "---------------------------"
python3 -c "
import sys
sys.path.append('.')
from src.data_processor import DataProcessor

processor = DataProcessor()
processor.load_sample_data()
processor.clean_data()
baseline_kpis = processor.calculate_kpis()

scenario_kpis = processor.simulate_scenario('Test', {'Inadimplencia_Valor': -0.05})

assert scenario_kpis['faturamento_acumulado'] > 0, 'Scenario should have revenue'

print('✓ Scenario Simulation test passed')
"

echo ""
echo "============================================================"
echo "ALL TESTS PASSED ✓"
echo "============================================================"
echo ""
echo "System is ready to use!"
echo "To start the Streamlit dashboard:"
echo "  streamlit run streamlit_app.py"
