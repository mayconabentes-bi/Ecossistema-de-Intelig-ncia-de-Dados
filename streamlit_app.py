"""
CDL Manaus Intelligence Hub - Streamlit Dashboard
Strategic Business Intelligence Platform
Implements Vibe Coding methodology: Strategic Vision + Functional Execution
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_processor import DataProcessor
from src.forecasting import BillingForecaster
from src.bcg_matrix import BCGMatrixAnalyzer
from src.bias_detector import BiasDetector

# Page configuration
st.set_page_config(
    page_title="CDL Manaus Intelligence Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .alert-success {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .alert-danger {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main application entry point."""
    
    # Header
    st.markdown('<h1 class="main-header">📊 CDL Manaus Intelligence Hub</h1>', unsafe_allow_html=True)
    st.markdown("**Strategic Business Intelligence Platform** | Jan-Nov 2025 Data Analysis")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/1f77b4/ffffff?text=CDL+Manaus", use_column_width=True)
        st.title("🎯 Navigation")
        
        page = st.radio(
            "Select Analysis",
            ["📈 Dashboard Overview", "🔮 Revenue Forecast", "📊 BCG Matrix", 
             "⚠️ Bias Detection", "🎮 Scenario Simulator"]
        )
        
        st.markdown("---")
        st.markdown("### 📅 Data Period")
        st.info("January - November 2025")
        
        st.markdown("### 👤 User")
        st.write("CDL Manaus BI Team")
        
        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("[Documentation](https://github.com)")
        st.markdown("[Support](mailto:support@cdlmanaus.com)")
    
    # Initialize data processor
    if 'processor' not in st.session_state:
        st.session_state.processor = DataProcessor()
        st.session_state.processor.load_sample_data()
        st.session_state.processor.clean_data()
        st.session_state.processor.calculate_kpis()
    
    processor = st.session_state.processor
    
    # Route to selected page
    if page == "📈 Dashboard Overview":
        show_dashboard(processor)
    elif page == "🔮 Revenue Forecast":
        show_forecast(processor)
    elif page == "📊 BCG Matrix":
        show_bcg_matrix()
    elif page == "⚠️ Bias Detection":
        show_bias_detection(processor)
    elif page == "🎮 Scenario Simulator":
        show_scenario_simulator(processor)


def show_dashboard(processor: DataProcessor):
    """Display main dashboard with KPIs and visualizations."""
    
    st.header("📈 Dashboard Overview")
    st.markdown("Real-time view of key performance indicators")
    
    # KPI Cards
    kpis = processor.kpis
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Accumulated Revenue",
            f"R$ {kpis['faturamento_acumulado']:,.2f}",
            delta=f"{kpis['gap_meta_percentual']:.2f}% vs Target"
        )
    
    with col2:
        st.metric(
            "🎯 Target Gap",
            f"{kpis['gap_meta_percentual']:.2f}%",
            delta="Below Target" if kpis['gap_meta_percentual'] < 0 else "Above Target"
        )
    
    with col3:
        st.metric(
            "📉 Delinquency Rate",
            f"{kpis['taxa_inadimplencia_media']:.2f}%",
            delta=f"±{kpis['taxa_inadimplencia_std']:.2f}%"
        )
    
    with col4:
        st.metric(
            "👥 Top 20 Concentration",
            f"{kpis['concentracao_top20_media']:.1f}%",
            delta=f"{kpis['concentracao_top20_tendencia']:.1f}% trend"
        )
    
    st.markdown("---")
    
    # Delinquency Alert
    alert_triggered, alert_message = processor.get_delinquency_alert()
    if alert_triggered:
        st.markdown(f'<div class="alert-box alert-danger">🚨 {alert_message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-box alert-success">✅ {alert_message}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Revenue vs Target")
        df = processor.cleaned_df
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Mes'], y=df['Faturamento_Real'],
            name='Real Revenue',
            line=dict(color='#1f77b4', width=3),
            mode='lines+markers'
        ))
        fig.add_trace(go.Scatter(
            x=df['Mes'], y=df['Faturamento_Meta'],
            name='Target',
            line=dict(color='#ff7f0e', width=2, dash='dash'),
            mode='lines'
        ))
        
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Revenue (R$)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Delinquency Monitoring")
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['Mes'], y=df['Inadimplencia_Valor'],
            name='Delinquency Value',
            marker_color='#d62728'
        ))
        
        # Add standard deviation threshold line
        mean_val = df['Inadimplencia_Valor'].mean()
        std_val = df['Inadimplencia_Valor'].std()
        threshold = mean_val + std_val
        
        fig.add_hline(
            y=threshold,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Alert Threshold (μ+σ): R$ {threshold:,.0f}"
        )
        
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Delinquency (R$)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Data Table
    st.markdown("---")
    st.subheader("📋 Detailed Monthly Data")
    
    display_df = df.copy()
    display_df['Mes'] = display_df['Mes'].dt.strftime('%Y-%m')
    display_df['Gap (%)'] = ((display_df['Faturamento_Real'] - display_df['Faturamento_Meta']) / 
                              display_df['Faturamento_Meta'] * 100)
    
    st.dataframe(
        display_df[['Mes', 'Faturamento_Real', 'Faturamento_Meta', 'Gap (%)', 
                   'Top20_Concentracao', 'Inadimplencia_Valor']].style.format({
            'Faturamento_Real': 'R$ {:,.2f}',
            'Faturamento_Meta': 'R$ {:,.2f}',
            'Gap (%)': '{:+.2f}%',
            'Top20_Concentracao': '{:.1f}%',
            'Inadimplencia_Valor': 'R$ {:,.2f}'
        }),
        use_container_width=True
    )


def show_forecast(processor: DataProcessor):
    """Display revenue forecasting page."""
    
    st.header("🔮 Revenue Forecast - December 2025")
    st.markdown("Time series forecasting using ARIMA and statistical methods")
    
    # Forecasting options
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("⚙️ Settings")
        method = st.selectbox(
            "Forecasting Method",
            ["arima", "moving_average", "trend"],
            format_func=lambda x: {
                "arima": "📈 ARIMA (Advanced)",
                "moving_average": "📊 Moving Average",
                "trend": "📉 Linear Trend"
            }[x]
        )
        
        periods = st.slider("Forecast Periods", 1, 6, 1)
        
        if st.button("🚀 Generate Forecast", type="primary"):
            st.session_state.forecast_run = True
    
    with col2:
        if 'forecast_run' in st.session_state and st.session_state.forecast_run:
            with st.spinner("Calculating forecast..."):
                df = processor.cleaned_df
                forecaster = BillingForecaster(df)
                forecast_result = forecaster.forecast_billing(periods=periods, method=method)
                
                # Display results
                st.success("✅ Forecast completed successfully!")
                
                # Key metrics
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric(
                        "December 2025 Forecast",
                        f"R$ {forecast_result['prediction_dezembro']:,.2f}"
                    )
                
                with col_b:
                    st.metric(
                        "Historical Average",
                        f"R$ {forecast_result['historical_mean']:,.2f}"
                    )
                
                with col_c:
                    variance = ((forecast_result['prediction_dezembro'] - forecast_result['historical_mean']) / 
                               forecast_result['historical_mean'] * 100)
                    st.metric(
                        "Variance from Average",
                        f"{variance:+.2f}%"
                    )
                
                # Confidence interval
                st.markdown("---")
                st.subheader("📊 Forecast Visualization")
                
                # Create visualization
                fig = go.Figure()
                
                # Historical data
                fig.add_trace(go.Scatter(
                    x=df['Mes'],
                    y=df['Faturamento_Real'],
                    name='Historical',
                    line=dict(color='#1f77b4', width=3),
                    mode='lines+markers'
                ))
                
                # Forecast
                last_date = df['Mes'].max()
                forecast_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=periods, freq='MS')
                
                fig.add_trace(go.Scatter(
                    x=forecast_dates,
                    y=forecast_result['predictions'],
                    name='Forecast',
                    line=dict(color='#2ca02c', width=3, dash='dash'),
                    mode='lines+markers'
                ))
                
                # Confidence interval
                fig.add_trace(go.Scatter(
                    x=forecast_dates,
                    y=forecast_result['confidence_interval_upper'],
                    name='Upper CI (95%)',
                    line=dict(color='rgba(44, 160, 44, 0.2)', width=0),
                    showlegend=False
                ))
                
                fig.add_trace(go.Scatter(
                    x=forecast_dates,
                    y=forecast_result['confidence_interval_lower'],
                    name='Confidence Interval',
                    line=dict(color='rgba(44, 160, 44, 0.2)', width=0),
                    fill='tonexty',
                    fillcolor='rgba(44, 160, 44, 0.2)'
                ))
                
                fig.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Revenue (R$)",
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Model details
                st.markdown("---")
                st.subheader("📋 Forecast Details")
                
                details_col1, details_col2 = st.columns(2)
                
                with details_col1:
                    st.write("**Method:**", forecast_result['method'])
                    if 'order' in forecast_result:
                        st.write("**ARIMA Order (p,d,q):**", forecast_result['order'])
                    if 'aic' in forecast_result:
                        st.write("**AIC Score:**", f"{forecast_result['aic']:.2f}")
                
                with details_col2:
                    st.write("**December 2025 Forecast:**", f"R$ {forecast_result['prediction_dezembro']:,.2f}")
                    st.write("**95% CI Lower:**", f"R$ {forecast_result['confidence_interval_lower'][0]:,.2f}")
                    st.write("**95% CI Upper:**", f"R$ {forecast_result['confidence_interval_upper'][0]:,.2f}")
        else:
            st.info("👈 Configure settings and click 'Generate Forecast' to begin")


def show_bcg_matrix():
    """Display BCG Matrix analysis page."""
    
    st.header("📊 BCG Matrix - Product Portfolio Analysis")
    st.markdown("Strategic classification: Stars, Cash Cows, Question Marks, and Dogs")
    
    # Initialize BCG analyzer
    if 'bcg_analyzer' not in st.session_state:
        st.session_state.bcg_analyzer = BCGMatrixAnalyzer()
        st.session_state.bcg_analyzer.create_sample_product_data()
        st.session_state.bcg_analyzed = False
    
    analyzer = st.session_state.bcg_analyzer
    
    # Configuration
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("⚙️ Configuration")
        
        share_threshold = st.slider(
            "Market Share Threshold (%)",
            min_value=20.0,
            max_value=40.0,
            value=30.0,
            step=1.0
        )
        
        growth_threshold = st.slider(
            "Growth Rate Threshold (%)",
            min_value=-5.0,
            max_value=10.0,
            value=0.0,
            step=0.5
        )
        
        if st.button("📊 Analyze Portfolio", type="primary"):
            st.session_state.bcg_analyzed = True
    
    with col2:
        if st.session_state.bcg_analyzed:
            with st.spinner("Analyzing product portfolio..."):
                results = analyzer.analyze_portfolio(share_threshold, growth_threshold)
                
                st.success("✅ BCG Matrix analysis completed!")
                
                # Create BCG Matrix scatter plot
                st.subheader("🎯 BCG Matrix Visualization")
                
                products = []
                market_shares = []
                growth_rates = []
                classifications = []
                revenues = []
                
                for product, metrics in results.items():
                    products.append(product.replace('_', ' '))
                    market_shares.append(metrics['market_share'])
                    growth_rates.append(metrics['growth_rate'])
                    classifications.append(metrics['classification'])
                    revenues.append(metrics['total_revenue'])
                
                # Create scatter plot
                fig = go.Figure()
                
                # Color mapping for classifications
                color_map = {
                    '⭐ Star': '#FFD700',
                    '💰 Cash Cow': '#32CD32',
                    '❓ Question Mark': '#FFA500',
                    '🐕 Dog': '#DC143C'
                }
                
                for classification in set(classifications):
                    mask = [c == classification for c in classifications]
                    fig.add_trace(go.Scatter(
                        x=[ms for ms, m in zip(market_shares, mask) if m],
                        y=[gr for gr, m in zip(growth_rates, mask) if m],
                        mode='markers+text',
                        name=classification,
                        text=[p for p, m in zip(products, mask) if m],
                        textposition='top center',
                        marker=dict(
                            size=[r/50000 for r, m in zip(revenues, mask) if m],  # Size by revenue
                            color=color_map.get(classification, '#888888'),
                            line=dict(color='white', width=2)
                        ),
                        hovertemplate='<b>%{text}</b><br>Market Share: %{x:.1f}%<br>Growth: %{y:+.2f}%<extra></extra>'
                    ))
                
                # Add threshold lines
                fig.add_hline(y=growth_threshold, line_dash="dash", line_color="gray", 
                             annotation_text="Growth Threshold")
                fig.add_vline(x=share_threshold, line_dash="dash", line_color="gray",
                             annotation_text="Share Threshold")
                
                # Add quadrant labels
                fig.add_annotation(x=share_threshold+10, y=growth_threshold+3, text="⭐ STARS", 
                                  showarrow=False, font=dict(size=14, color="gray"))
                fig.add_annotation(x=share_threshold+10, y=growth_threshold-3, text="💰 CASH COWS",
                                  showarrow=False, font=dict(size=14, color="gray"))
                fig.add_annotation(x=share_threshold-10, y=growth_threshold+3, text="❓ QUESTION MARKS",
                                  showarrow=False, font=dict(size=14, color="gray"))
                fig.add_annotation(x=share_threshold-10, y=growth_threshold-3, text="🐕 DOGS",
                                  showarrow=False, font=dict(size=14, color="gray"))
                
                fig.update_layout(
                    xaxis_title="Relative Market Share (%)",
                    yaxis_title="Growth Rate (%)",
                    hovermode='closest',
                    height=600,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed results
                st.markdown("---")
                st.subheader("📋 Product Analysis Details")
                
                for product, metrics in results.items():
                    with st.expander(f"{product.replace('_', ' ')} - {metrics['classification']}"):
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            st.metric("Market Share", f"{metrics['market_share']:.2f}%")
                            st.metric("Total Revenue", f"R$ {metrics['total_revenue']:,.2f}")
                        
                        with col_b:
                            st.metric("Growth Rate", f"{metrics['growth_rate']:+.2f}%")
                            st.metric("Avg Monthly", f"R$ {metrics['avg_monthly_revenue']:,.2f}")
                        
                        with col_c:
                            st.metric("First Month", f"R$ {metrics['first_month']:,.2f}")
                            st.metric("Last Month", f"R$ {metrics['last_month']:,.2f}")
                        
                        # Recommendations
                        recommendations = analyzer.get_recommendations()[product]
                        st.markdown("**📋 Strategic Recommendations:**")
                        for rec in recommendations:
                            st.markdown(f"- {rec}")
                
                # Full report
                st.markdown("---")
                if st.button("📄 Generate Full Report"):
                    report = analyzer.generate_report()
                    st.text_area("BCG Matrix Report", report, height=400)
        
        else:
            st.info("👈 Configure thresholds and click 'Analyze Portfolio' to begin")


def show_bias_detection(processor: DataProcessor):
    """Display bias detection analysis page."""
    
    st.header("⚠️ Bias Detection - Analytical Vigilance")
    st.markdown("Monitoring for Survivorship Bias, Selection Bias, and other analytical blind spots")
    
    if st.button("🔍 Run Bias Analysis", type="primary"):
        with st.spinner("Analyzing data for potential biases..."):
            detector = BiasDetector()
            df = processor.cleaned_df
            
            # Run full analysis
            results = detector.run_full_analysis(df, config={'date_column': 'Mes'})
            
            # Display results
            st.success(f"✅ Analysis complete: {results['total_biases_detected']} potential biases detected")
            
            # Summary cards
            col1, col2, col3 = st.columns(3)
            
            with col1:
                survivorship_detected = results['survivorship']['bias_detected']
                st.metric(
                    "Survivorship Bias",
                    "Detected" if survivorship_detected else "Clear",
                    delta=results['survivorship']['severity'] if survivorship_detected else "OK"
                )
            
            with col2:
                selection_detected = results['selection']['bias_detected']
                st.metric(
                    "Selection Bias",
                    "Detected" if selection_detected else "Clear",
                    delta=results['selection']['severity'] if selection_detected else "OK"
                )
            
            with col3:
                recency_detected = results['recency']['bias_detected']
                st.metric(
                    "Recency Bias",
                    "Detected" if recency_detected else "Clear",
                    delta=results['recency']['severity'] if recency_detected else "OK"
                )
            
            # Detailed report
            st.markdown("---")
            st.subheader("📊 Detailed Bias Report")
            
            if results['total_biases_detected'] > 0:
                report = detector.generate_report()
                st.text_area("Bias Detection Report", report, height=400)
                
                # Download report
                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name=f"bias_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            else:
                st.success("✅ No significant biases detected in the current analysis!")
                st.info("""
                **Best Practices Applied:**
                - Comprehensive historical data coverage
                - Balanced representation of all client segments
                - No extreme concentration risks identified
                """)
            
            # Visualization of bias log
            if results['bias_log']:
                st.markdown("---")
                st.subheader("📈 Bias Detection Timeline")
                
                bias_df = pd.DataFrame(results['bias_log'])
                bias_df['timestamp'] = pd.to_datetime(bias_df['timestamp'])
                
                fig = px.scatter(
                    bias_df,
                    x='timestamp',
                    y='bias_type',
                    color='severity',
                    size=[1]*len(bias_df),
                    title="Detected Biases Over Time",
                    color_discrete_map={
                        'CRITICAL': '#DC143C',
                        'HIGH': '#FFA500',
                        'MEDIUM': '#FFD700',
                        'LOW': '#32CD32'
                    }
                )
                
                st.plotly_chart(fig, use_container_width=True)


def show_scenario_simulator(processor: DataProcessor):
    """Display scenario simulation page."""
    
    st.header("🎮 Scenario Simulator")
    st.markdown("What-if analysis: Simulate business scenarios and see impact on KPIs")
    
    st.info("💡 Example: 'What if Bemol's delinquency drops by 5%?'")
    
    # Scenario configuration
    st.subheader("⚙️ Configure Scenario")
    
    scenario_name = st.text_input("Scenario Name", "Bemol Delinquency Reduction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Parameter to Change:**")
        parameter = st.selectbox(
            "Select Parameter",
            ["Inadimplencia_Valor", "Faturamento_Real", "Top20_Concentracao"]
        )
    
    with col2:
        st.markdown("**Change Amount:**")
        change_type = st.radio("Change Type", ["Percentage", "Absolute Value"])
        
        if change_type == "Percentage":
            change_value = st.slider(
                "Percentage Change (%)",
                min_value=-50.0,
                max_value=50.0,
                value=-5.0,
                step=1.0
            ) / 100
        else:
            change_value = st.number_input(
                "Absolute Change (R$)",
                min_value=-500000.0,
                max_value=500000.0,
                value=-10000.0,
                step=1000.0
            )
    
    if st.button("🚀 Run Simulation", type="primary"):
        with st.spinner("Running scenario simulation..."):
            # Run scenario
            changes = {parameter: change_value}
            scenario_kpis = processor.simulate_scenario(scenario_name, changes)
            
            # Compare with baseline
            baseline_kpis = processor.kpis
            
            st.success(f"✅ Scenario '{scenario_name}' completed!")
            
            # Comparison table
            st.markdown("---")
            st.subheader("📊 KPI Comparison: Baseline vs Scenario")
            
            comparison_data = {
                'KPI': [
                    'Accumulated Revenue',
                    'Target Gap (%)',
                    'Avg Delinquency Rate (%)',
                    'Top 20 Concentration (%)'
                ],
                'Baseline': [
                    f"R$ {baseline_kpis['faturamento_acumulado']:,.2f}",
                    f"{baseline_kpis['gap_meta_percentual']:.2f}%",
                    f"{baseline_kpis['taxa_inadimplencia_media']:.2f}%",
                    f"{baseline_kpis['concentracao_top20_media']:.1f}%"
                ],
                'Scenario': [
                    f"R$ {scenario_kpis['faturamento_acumulado']:,.2f}",
                    f"{scenario_kpis['gap_meta_percentual']:.2f}%",
                    f"{scenario_kpis['taxa_inadimplencia_media']:.2f}%",
                    f"{scenario_kpis['concentracao_top20_media']:.1f}%"
                ],
                'Difference': [
                    f"R$ {scenario_kpis['faturamento_acumulado'] - baseline_kpis['faturamento_acumulado']:+,.2f}",
                    f"{scenario_kpis['gap_meta_percentual'] - baseline_kpis['gap_meta_percentual']:+.2f} pp",
                    f"{scenario_kpis['taxa_inadimplencia_media'] - baseline_kpis['taxa_inadimplencia_media']:+.2f} pp",
                    f"{scenario_kpis['concentracao_top20_media'] - baseline_kpis['concentracao_top20_media']:+.1f} pp"
                ]
            }
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True)
            
            # Visual comparison
            st.markdown("---")
            st.subheader("📈 Visual Impact Analysis")
            
            # Bar chart comparison
            metrics_to_plot = ['Accumulated Revenue', 'Avg Delinquency Rate (%)']
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Baseline',
                x=['Revenue', 'Delinquency'],
                y=[baseline_kpis['faturamento_acumulado'], baseline_kpis['taxa_inadimplencia_media']],
                text=[f"R$ {baseline_kpis['faturamento_acumulado']:,.0f}", 
                      f"{baseline_kpis['taxa_inadimplencia_media']:.2f}%"],
                textposition='auto'
            ))
            
            fig.add_trace(go.Bar(
                name='Scenario',
                x=['Revenue', 'Delinquency'],
                y=[scenario_kpis['faturamento_acumulado'], scenario_kpis['taxa_inadimplencia_media']],
                text=[f"R$ {scenario_kpis['faturamento_acumulado']:,.0f}",
                      f"{scenario_kpis['taxa_inadimplencia_media']:.2f}%"],
                textposition='auto'
            ))
            
            fig.update_layout(
                title=f"Impact of Scenario: {scenario_name}",
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Insights
            st.markdown("---")
            st.subheader("💡 Insights")
            
            revenue_diff = scenario_kpis['faturamento_acumulado'] - baseline_kpis['faturamento_acumulado']
            delinq_diff = scenario_kpis['taxa_inadimplencia_media'] - baseline_kpis['taxa_inadimplencia_media']
            
            if revenue_diff > 0:
                st.success(f"✅ Revenue impact: +R$ {revenue_diff:,.2f} ({(revenue_diff/baseline_kpis['faturamento_acumulado']*100):+.2f}%)")
            elif revenue_diff < 0:
                st.warning(f"⚠️ Revenue impact: -R$ {abs(revenue_diff):,.2f} ({(revenue_diff/baseline_kpis['faturamento_acumulado']*100):+.2f}%)")
            else:
                st.info("ℹ️ No revenue impact from this scenario")
            
            if delinq_diff < 0:
                st.success(f"✅ Delinquency improvement: {delinq_diff:.2f} percentage points")
            elif delinq_diff > 0:
                st.warning(f"⚠️ Delinquency worsening: +{delinq_diff:.2f} percentage points")
            else:
                st.info("ℹ️ No delinquency impact from this scenario")


if __name__ == "__main__":
    main()
