"""
Data Processor Module - CDL Manaus Intelligence Hub
Handles data cleaning, transformation and KPI calculations
Implements Strategic Consultant workflow with rigorous analytics
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Core data processing class implementing the Strategic Consultant workflow.
    Handles data cleaning, validation, and KPI calculations.
    """
    
    def __init__(self):
        """Initialize the DataProcessor with default configurations."""
        self.df: Optional[pd.DataFrame] = None
        self.cleaned_df: Optional[pd.DataFrame] = None
        self.kpis: Dict = {}
        logger.info("DataProcessor initialized")
    
    def load_sample_data(self) -> pd.DataFrame:
        """
        Create sample data simulating CDL Manaus Jan-Nov 2025 billing data.
        
        Returns:
            pd.DataFrame: Sample dataframe with billing information
        """
        data = {
            'Mes': ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', 
                    '2025-06', '2025-07', '2025-08', '2025-09', '2025-10', '2025-11'],
            'Faturamento_Real': [1150000, 1180000, 1220000, 1200000, 1190000, 
                                1250000, 1280000, 1195000, 1215000, 1180000, 1038238],
            'Faturamento_Meta': [1300000, 1300000, 1350000, 1350000, 1400000,
                               1400000, 1450000, 1450000, 1500000, 1500000, 1550000],
            'Top20_Concentracao': [45.2, 44.8, 43.5, 42.1, 41.8,
                                  40.5, 39.8, 38.2, 37.5, 36.8, 35.2],
            'Inadimplencia_Valor': [85000, 92000, 88000, 95000, 103000,
                                   110000, 125000, 132000, 128000, 138000, 145000]
        }
        
        df = pd.DataFrame(data)
        df['Mes'] = pd.to_datetime(df['Mes'])
        self.df = df
        logger.info(f"Sample data loaded: {len(df)} months of data")
        return df
    
    def load_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Load external dataframe for processing.
        
        Args:
            df: DataFrame with required columns
            
        Returns:
            pd.DataFrame: Loaded dataframe
        """
        required_cols = ['Mes', 'Faturamento_Real', 'Faturamento_Meta', 
                        'Top20_Concentracao', 'Inadimplencia_Valor']
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        self.df = df.copy()
        logger.info(f"External data loaded: {len(df)} records")
        return self.df
    
    def clean_data(self) -> pd.DataFrame:
        """
        Stage 1: Data Cleaning - Handle missing values, outliers, and data quality.
        Implements rigorous data validation following consultant standards.
        
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() or load_sample_data() first.")
        
        df_clean = self.df.copy()
        logger.info("Starting data cleaning process")
        
        # Convert date column to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(df_clean['Mes']):
            df_clean['Mes'] = pd.to_datetime(df_clean['Mes'])
            logger.info("Converted 'Mes' column to datetime")
        
        # Sort by month
        df_clean = df_clean.sort_values('Mes').reset_index(drop=True)
        
        # Handle missing values in numeric columns
        numeric_cols = ['Faturamento_Real', 'Faturamento_Meta', 
                       'Top20_Concentracao', 'Inadimplencia_Valor']
        
        for col in numeric_cols:
            missing_count = df_clean[col].isna().sum()
            if missing_count > 0:
                logger.warning(f"Found {missing_count} missing values in {col}")
                # Forward fill for time series data
                df_clean[col] = df_clean[col].fillna(method='ffill')
                # If still NaN (first rows), use backward fill
                df_clean[col] = df_clean[col].fillna(method='bfill')
        
        # Validate non-negative values
        for col in numeric_cols:
            negative_count = (df_clean[col] < 0).sum()
            if negative_count > 0:
                logger.warning(f"Found {negative_count} negative values in {col}, setting to 0")
                df_clean.loc[df_clean[col] < 0, col] = 0
        
        # Detect and log outliers (values > 3 std deviations from mean)
        for col in ['Faturamento_Real', 'Inadimplencia_Valor']:
            mean_val = df_clean[col].mean()
            std_val = df_clean[col].std()
            outliers = df_clean[
                (df_clean[col] > mean_val + 3 * std_val) | 
                (df_clean[col] < mean_val - 3 * std_val)
            ]
            if len(outliers) > 0:
                logger.warning(f"Outliers detected in {col}: {len(outliers)} records")
                for idx, row in outliers.iterrows():
                    logger.info(f"  - {row['Mes'].strftime('%Y-%m')}: {row[col]:,.2f}")
        
        self.cleaned_df = df_clean
        logger.info("Data cleaning completed successfully")
        return df_clean
    
    def calculate_kpis(self) -> Dict:
        """
        Calculate key performance indicators for CDL Manaus.
        
        Returns:
            Dict: Dictionary containing calculated KPIs
        """
        if self.cleaned_df is None:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        df = self.cleaned_df
        
        # 1. Gap de Meta Acumulado
        total_real = df['Faturamento_Real'].sum()
        total_meta = df['Faturamento_Meta'].sum()
        gap_acumulado = ((total_real - total_meta) / total_meta) * 100
        
        # 2. Variação Percentual Mensal
        df['Variacao_Mensal'] = df['Faturamento_Real'].pct_change() * 100
        
        # 3. Taxa Média de Inadimplência
        df['Taxa_Inadimplencia'] = (df['Inadimplencia_Valor'] / df['Faturamento_Real']) * 100
        taxa_media_inadimplencia = df['Taxa_Inadimplencia'].mean()
        taxa_std_inadimplencia = df['Taxa_Inadimplencia'].std()
        
        # 4. Concentração Top 20 (média e tendência)
        concentracao_media = df['Top20_Concentracao'].mean()
        concentracao_tendencia = df['Top20_Concentracao'].iloc[-1] - df['Top20_Concentracao'].iloc[0]
        
        self.kpis = {
            'faturamento_acumulado': total_real,
            'meta_acumulada': total_meta,
            'gap_meta_percentual': gap_acumulado,
            'taxa_inadimplencia_media': taxa_media_inadimplencia,
            'taxa_inadimplencia_std': taxa_std_inadimplencia,
            'concentracao_top20_media': concentracao_media,
            'concentracao_top20_tendencia': concentracao_tendencia,
            'meses_analisados': len(df)
        }
        
        logger.info(f"KPIs calculated: Accumulated Revenue = R$ {total_real:,.2f}")
        logger.info(f"  Gap vs Target: {gap_acumulado:.2f}%")
        logger.info(f"  Average Delinquency Rate: {taxa_media_inadimplencia:.2f}%")
        
        return self.kpis
    
    def get_delinquency_alert(self) -> Tuple[bool, str]:
        """
        Check if current month's delinquency exceeds standard deviation threshold.
        
        Returns:
            Tuple[bool, str]: (alert_triggered, message)
        """
        if self.cleaned_df is None or 'Taxa_Inadimplencia' not in self.cleaned_df.columns:
            return False, "Data not processed"
        
        df = self.cleaned_df
        mean_rate = df['Taxa_Inadimplencia'].mean()
        std_rate = df['Taxa_Inadimplencia'].std()
        current_rate = df['Taxa_Inadimplencia'].iloc[-1]
        threshold = mean_rate + std_rate
        
        if current_rate > threshold:
            message = f"⚠️ ALERTA: Inadimplência atual ({current_rate:.2f}%) excede o limite ({threshold:.2f}%)"
            logger.warning(message)
            return True, message
        else:
            message = f"✓ Inadimplência sob controle: {current_rate:.2f}% (limite: {threshold:.2f}%)"
            return False, message
    
    def simulate_scenario(self, scenario_name: str, changes: Dict) -> Dict:
        """
        Simulate business scenarios with parameter changes.
        
        Args:
            scenario_name: Name of the scenario
            changes: Dictionary with column changes, e.g., {'Inadimplencia_Valor': -0.05}
            
        Returns:
            Dict: Simulated KPIs
        """
        if self.cleaned_df is None:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        logger.info(f"Simulating scenario: {scenario_name}")
        df_scenario = self.cleaned_df.copy()
        
        # Apply changes
        for col, change in changes.items():
            if col in df_scenario.columns:
                if isinstance(change, float) and -1 <= change <= 1:
                    # Treat as percentage change
                    df_scenario[col] = df_scenario[col] * (1 + change)
                    logger.info(f"  Applied {change*100:+.1f}% change to {col}")
                else:
                    # Treat as absolute value
                    df_scenario[col] = change
        
        # Recalculate KPIs with scenario data
        original_df = self.cleaned_df
        self.cleaned_df = df_scenario
        scenario_kpis = self.calculate_kpis()
        self.cleaned_df = original_df  # Restore original
        
        logger.info(f"Scenario '{scenario_name}' completed")
        return scenario_kpis
