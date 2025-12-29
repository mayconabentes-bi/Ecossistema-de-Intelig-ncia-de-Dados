"""
CDL Manaus Intelligence Hub - Demo Visualization Generator
Creates static visualization of dashboard metrics for documentation
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import sys
sys.path.append('.')

from src.data_processor import DataProcessor
from src.forecasting import BillingForecaster
from src.bcg_matrix import BCGMatrixAnalyzer

# Initialize processor
processor = DataProcessor()
processor.load_sample_data()
processor.clean_data()
kpis = processor.calculate_kpis()
df = processor.cleaned_df

# Create figure with subplots
fig = plt.figure(figsize=(16, 10))
fig.suptitle('CDL Manaus Intelligence Hub - Dashboard Overview', 
             fontsize=20, fontweight='bold', y=0.98)

# Define color scheme
color_primary = '#1f77b4'
color_secondary = '#ff7f0e'
color_success = '#2ca02c'
color_danger = '#d62728'
color_warning = '#ffc107'

# KPI Cards at top
kpi_ax = plt.subplot(4, 4, (1, 4))
kpi_ax.axis('off')

# KPI 1: Accumulated Revenue
kpi1_box = FancyBboxPatch((0, 0.7), 0.23, 0.25, 
                          boxstyle="round,pad=0.01", 
                          linewidth=2, edgecolor=color_primary, 
                          facecolor='#e8f4f8')
kpi_ax.add_patch(kpi1_box)
kpi_ax.text(0.115, 0.88, '💰 Accumulated Revenue', 
           ha='center', va='center', fontsize=10, fontweight='bold')
kpi_ax.text(0.115, 0.80, f'R$ {kpis["faturamento_acumulado"]:,.0f}', 
           ha='center', va='center', fontsize=12, fontweight='bold', color=color_primary)
kpi_ax.text(0.115, 0.73, f'{kpis["gap_meta_percentual"]:.1f}% vs Target', 
           ha='center', va='center', fontsize=8, color=color_danger)

# KPI 2: Target Gap
kpi2_box = FancyBboxPatch((0.26, 0.7), 0.23, 0.25, 
                          boxstyle="round,pad=0.01", 
                          linewidth=2, edgecolor=color_danger, 
                          facecolor='#ffe8e8')
kpi_ax.add_patch(kpi2_box)
kpi_ax.text(0.375, 0.88, '🎯 Target Gap', 
           ha='center', va='center', fontsize=10, fontweight='bold')
kpi_ax.text(0.375, 0.80, f'{kpis["gap_meta_percentual"]:.2f}%', 
           ha='center', va='center', fontsize=12, fontweight='bold', color=color_danger)
kpi_ax.text(0.375, 0.73, 'Below Target', 
           ha='center', va='center', fontsize=8, color=color_danger)

# KPI 3: Delinquency
kpi3_box = FancyBboxPatch((0.52, 0.7), 0.23, 0.25, 
                          boxstyle="round,pad=0.01", 
                          linewidth=2, edgecolor=color_warning, 
                          facecolor='#fff8e8')
kpi_ax.add_patch(kpi3_box)
kpi_ax.text(0.635, 0.88, '📉 Delinquency Rate', 
           ha='center', va='center', fontsize=10, fontweight='bold')
kpi_ax.text(0.635, 0.80, f'{kpis["taxa_inadimplencia_media"]:.2f}%', 
           ha='center', va='center', fontsize=12, fontweight='bold', color=color_warning)
kpi_ax.text(0.635, 0.73, f'±{kpis["taxa_inadimplencia_std"]:.2f}% std', 
           ha='center', va='center', fontsize=8, color='gray')

# KPI 4: Top 20 Concentration
kpi4_box = FancyBboxPatch((0.78, 0.7), 0.23, 0.25, 
                          boxstyle="round,pad=0.01", 
                          linewidth=2, edgecolor=color_secondary, 
                          facecolor='#fff4e8')
kpi_ax.add_patch(kpi4_box)
kpi_ax.text(0.895, 0.88, '👥 Top 20 Concentration', 
           ha='center', va='center', fontsize=10, fontweight='bold')
kpi_ax.text(0.895, 0.80, f'{kpis["concentracao_top20_media"]:.1f}%', 
           ha='center', va='center', fontsize=12, fontweight='bold', color=color_secondary)
kpi_ax.text(0.895, 0.73, f'{kpis["concentracao_top20_tendencia"]:.1f}% trend', 
           ha='center', va='center', fontsize=8, color=color_success if kpis["concentracao_top20_tendencia"] < 0 else color_danger)

# Alert Box
alert_triggered, alert_msg = processor.get_delinquency_alert()
if alert_triggered:
    alert_box = FancyBboxPatch((0, 0.4), 1, 0.15, 
                              boxstyle="round,pad=0.01", 
                              linewidth=2, edgecolor=color_danger, 
                              facecolor='#ffe8e8')
    kpi_ax.add_patch(alert_box)
    kpi_ax.text(0.5, 0.48, '⚠️ ALERTA DE INADIMPLÊNCIA', 
               ha='center', va='center', fontsize=11, fontweight='bold', color=color_danger)
    kpi_ax.text(0.5, 0.43, alert_msg[:60], 
               ha='center', va='center', fontsize=8, color='black')
else:
    alert_box = FancyBboxPatch((0, 0.4), 1, 0.15, 
                              boxstyle="round,pad=0.01", 
                              linewidth=2, edgecolor=color_success, 
                              facecolor='#e8f8e8')
    kpi_ax.add_patch(alert_box)
    kpi_ax.text(0.5, 0.475, '✅ Sistema sob controle', 
               ha='center', va='center', fontsize=11, fontweight='bold', color=color_success)

kpi_ax.set_xlim(0, 1)
kpi_ax.set_ylim(0, 1)

# Chart 1: Revenue vs Target
ax1 = plt.subplot(4, 2, 3)
months = [d.strftime('%b') for d in df['Mes']]
ax1.plot(months, df['Faturamento_Real']/1e6, 'o-', color=color_primary, linewidth=2, 
         markersize=6, label='Real Revenue')
ax1.plot(months, df['Faturamento_Meta']/1e6, '--', color=color_secondary, linewidth=2, 
         label='Target')
ax1.set_title('📊 Revenue vs Target (Jan-Nov 2025)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Revenue (R$ Million)', fontsize=9)
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=45, labelsize=7)
ax1.tick_params(axis='y', labelsize=8)

# Chart 2: Delinquency Monitoring
ax2 = plt.subplot(4, 2, 4)
ax2.bar(months, df['Inadimplencia_Valor']/1000, color=color_danger, alpha=0.7)
mean_val = df['Inadimplencia_Valor'].mean()
std_val = df['Inadimplencia_Valor'].std()
threshold = (mean_val + std_val) / 1000
ax2.axhline(y=threshold, color='red', linestyle='--', linewidth=2, 
           label=f'Alert Threshold (μ+σ): R$ {threshold:.0f}K')
ax2.set_title('📈 Delinquency Monitoring', fontsize=11, fontweight='bold')
ax2.set_ylabel('Delinquency (R$ Thousand)', fontsize=9)
ax2.legend(fontsize=7)
ax2.grid(True, alpha=0.3, axis='y')
ax2.tick_params(axis='x', rotation=45, labelsize=7)
ax2.tick_params(axis='y', labelsize=8)

# Chart 3: BCG Matrix
ax3 = plt.subplot(4, 2, 5)
bcg = BCGMatrixAnalyzer()
bcg.create_sample_product_data()
results = bcg.analyze_portfolio()

colors_bcg = {'💰 Cash Cow': '#32CD32', '🐕 Dog': '#DC143C', 
              '⭐ Star': '#FFD700', '❓ Question Mark': '#FFA500'}
for product, metrics in results.items():
    color = colors_bcg.get(metrics['classification'], 'gray')
    ax3.scatter(metrics['market_share'], metrics['growth_rate'], 
               s=metrics['total_revenue']/50000, color=color, alpha=0.6, 
               edgecolors='black', linewidth=1.5)
    ax3.text(metrics['market_share'], metrics['growth_rate']+0.2, 
            product.replace('_', ' '), fontsize=7, ha='center')

ax3.axhline(y=0, color='gray', linestyle='--', linewidth=1)
ax3.axvline(x=30, color='gray', linestyle='--', linewidth=1)
ax3.set_title('📊 BCG Matrix - Product Portfolio', fontsize=11, fontweight='bold')
ax3.set_xlabel('Market Share (%)', fontsize=9)
ax3.set_ylabel('Growth Rate (%)', fontsize=9)
ax3.grid(True, alpha=0.3)
ax3.tick_params(labelsize=8)

# Chart 4: Forecast Preview
ax4 = plt.subplot(4, 2, 6)
forecaster = BillingForecaster(df)
forecast = forecaster.forecast_billing(periods=1, method='moving_average')

# Plot historical
ax4.plot(range(len(df)), df['Faturamento_Real']/1e6, 'o-', 
        color=color_primary, linewidth=2, label='Historical', markersize=5)

# Plot forecast point
ax4.plot(len(df), forecast['prediction_dezembro']/1e6, '*', 
        color=color_success, markersize=15, label='Forecast Dec 2025')

# Add confidence interval
ci_lower = forecast['confidence_interval_lower'][0]/1e6
ci_upper = forecast['confidence_interval_upper'][0]/1e6
ax4.plot([len(df), len(df)], [ci_lower, ci_upper], 
        color=color_success, linewidth=2, alpha=0.5)
ax4.fill_betweenx([ci_lower, ci_upper], len(df)-0.2, len(df)+0.2, 
                  color=color_success, alpha=0.2, label='95% CI')

ax4.set_title('🔮 Revenue Forecast - December 2025', fontsize=11, fontweight='bold')
ax4.set_xlabel('Month Index', fontsize=9)
ax4.set_ylabel('Revenue (R$ Million)', fontsize=9)
ax4.legend(fontsize=7, loc='best')
ax4.grid(True, alpha=0.3)
ax4.tick_params(labelsize=8)

# Info Panel - Bottom
info_ax = plt.subplot(4, 1, 4)
info_ax.axis('off')

info_text = f"""
📋 SYSTEM INFORMATION

Data Period: January - November 2025 (11 months)
Total Records: {len(df)}
Total Revenue: R$ {kpis['faturamento_acumulado']:,.2f}
Target Gap: {kpis['gap_meta_percentual']:.2f}%
Average Delinquency: {kpis['taxa_inadimplencia_media']:.2f}%

BCG Product Classification:
• Consultas: Cash Cow (50.1% share, -1.1% growth) - Maximize profits
• Certificados: Dog (29.3% share, -1.1% growth) - Reevaluate strategy  
• CDL Saúde: Dog (20.6% share, -0.7% growth) - Consider repositioning

Forecast December 2025: R$ {forecast['prediction_dezembro']:,.2f} (Moving Average method)
Confidence Interval: R$ {forecast['confidence_interval_lower'][0]:,.2f} - R$ {forecast['confidence_interval_upper'][0]:,.2f}

✅ All modules operational • 🎯 Strategic insights ready • ⚠️ Alerts active
"""

info_ax.text(0.05, 0.95, info_text, fontsize=8, verticalalignment='top', 
            family='monospace', bbox=dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.8))

plt.tight_layout()
plt.savefig('/tmp/cdl_manaus_dashboard_demo.png', dpi=150, bbox_inches='tight')
print("✓ Dashboard visualization saved to /tmp/cdl_manaus_dashboard_demo.png")
print(f"\nKey Metrics:")
print(f"  Revenue: R$ {kpis['faturamento_acumulado']:,.2f}")
print(f"  Gap: {kpis['gap_meta_percentual']:.2f}%")
print(f"  Delinquency: {kpis['taxa_inadimplencia_media']:.2f}%")
print(f"  Forecast Dec: R$ {forecast['prediction_dezembro']:,.2f}")
