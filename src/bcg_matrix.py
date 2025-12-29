"""
BCG Matrix Module - CDL Manaus Intelligence Hub
Implements Boston Consulting Group Matrix for product portfolio analysis
Classifies products into Stars, Cash Cows, Question Marks, and Dogs
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class BCGMatrixAnalyzer:
    """
    BCG Matrix analyzer for product portfolio classification.
    Classifies products based on market share (real billing) vs growth rate.
    """
    
    # Product categories for CDL Manaus
    PRODUCT_CATEGORIES = ['Consultas', 'Certificados', 'CDL Saúde']
    
    def __init__(self):
        """Initialize BCG Matrix analyzer."""
        self.products_df: Optional[pd.DataFrame] = None
        self.classifications: Dict = {}
        logger.info("BCG Matrix Analyzer initialized")
    
    def create_sample_product_data(self) -> pd.DataFrame:
        """
        Create sample product data for CDL Manaus (Jan-Nov 2025).
        
        Returns:
            pd.DataFrame: Sample product billing data
        """
        data = {
            'Mes': pd.date_range(start='2025-01', end='2025-11', freq='MS'),
            'Consultas': [580000, 595000, 610000, 600000, 595000, 625000, 
                         640000, 597500, 607500, 590000, 519119],
            'Certificados': [340000, 348000, 356000, 352000, 349000, 365000,
                           374000, 349250, 355250, 345000, 303539],
            'CDL_Saude': [230000, 237000, 254000, 248000, 246000, 260000,
                         266000, 248250, 252250, 245000, 215580]
        }
        
        df = pd.DataFrame(data)
        self.products_df = df
        logger.info(f"Sample product data created: {len(df)} months, {len(self.PRODUCT_CATEGORIES)} products")
        return df
    
    def load_product_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Load external product dataframe.
        
        Args:
            df: DataFrame with 'Mes' column and product columns
            
        Returns:
            pd.DataFrame: Loaded dataframe
        """
        if 'Mes' not in df.columns:
            raise ValueError("DataFrame must contain 'Mes' column")
        
        self.products_df = df.copy()
        logger.info(f"Product data loaded: {len(df)} records")
        return self.products_df
    
    def calculate_growth_rate(self, series: pd.Series) -> float:
        """
        Calculate growth rate for a time series.
        Uses CAGR (Compound Annual Growth Rate) method.
        
        Args:
            series: Time series of product revenues
            
        Returns:
            float: Growth rate as percentage
        """
        if len(series) < 2:
            return 0.0
        
        # Remove any zero or negative values for log calculation
        series_clean = series[series > 0]
        if len(series_clean) < 2:
            return 0.0
        
        # CAGR formula: ((End Value / Start Value) ^ (1 / Number of Periods)) - 1
        start_value = series_clean.iloc[0]
        end_value = series_clean.iloc[-1]
        n_periods = len(series_clean) - 1
        
        if start_value <= 0:
            return 0.0
        
        growth_rate = ((end_value / start_value) ** (1 / n_periods) - 1) * 100
        return growth_rate
    
    def calculate_market_share(self, series: pd.Series, total_market: pd.Series) -> float:
        """
        Calculate relative market share for a product.
        
        Args:
            series: Product revenue series
            total_market: Total market revenue series
            
        Returns:
            float: Market share as percentage
        """
        total_product = series.sum()
        total_market_sum = total_market.sum()
        
        if total_market_sum == 0:
            return 0.0
        
        market_share = (total_product / total_market_sum) * 100
        return market_share
    
    def classify_bcg(self, market_share: float, growth_rate: float, 
                     share_threshold: float = 30.0, growth_threshold: float = 0.0) -> str:
        """
        Classify product into BCG quadrant.
        
        Args:
            market_share: Relative market share (%)
            growth_rate: Growth rate (%)
            share_threshold: Threshold for high/low market share
            growth_threshold: Threshold for high/low growth
            
        Returns:
            str: BCG classification (Star, Cash Cow, Question Mark, Dog)
        """
        high_share = market_share >= share_threshold
        high_growth = growth_rate >= growth_threshold
        
        if high_share and high_growth:
            return "⭐ Star"
        elif high_share and not high_growth:
            return "💰 Cash Cow"
        elif not high_share and high_growth:
            return "❓ Question Mark"
        else:
            return "🐕 Dog"
    
    def analyze_portfolio(self, share_threshold: float = 30.0, 
                         growth_threshold: float = 0.0) -> Dict:
        """
        Perform complete BCG Matrix analysis on product portfolio.
        
        Args:
            share_threshold: Market share threshold for classification
            growth_threshold: Growth rate threshold for classification
            
        Returns:
            Dict: Analysis results with classifications
        """
        if self.products_df is None:
            raise ValueError("No product data loaded. Call load_product_data() or create_sample_product_data() first.")
        
        df = self.products_df
        results = {}
        
        # Calculate total market (sum of all products)
        product_cols = [col for col in df.columns if col != 'Mes']
        df['Total_Market'] = df[product_cols].sum(axis=1)
        
        logger.info("Starting BCG Matrix analysis")
        
        for product in product_cols:
            if product == 'Total_Market':
                continue
            
            # Calculate metrics
            growth_rate = self.calculate_growth_rate(df[product])
            market_share = self.calculate_market_share(df[product], df['Total_Market'])
            classification = self.classify_bcg(market_share, growth_rate, 
                                              share_threshold, growth_threshold)
            
            # Total revenue
            total_revenue = df[product].sum()
            avg_revenue = df[product].mean()
            
            results[product] = {
                'growth_rate': growth_rate,
                'market_share': market_share,
                'classification': classification,
                'total_revenue': total_revenue,
                'avg_monthly_revenue': avg_revenue,
                'first_month': df[product].iloc[0],
                'last_month': df[product].iloc[-1]
            }
            
            logger.info(f"{product}: {classification} (Share: {market_share:.1f}%, Growth: {growth_rate:+.2f}%)")
        
        self.classifications = results
        return results
    
    def get_recommendations(self) -> Dict[str, List[str]]:
        """
        Generate strategic recommendations based on BCG classifications.
        
        Returns:
            Dict: Recommendations by product
        """
        if not self.classifications:
            return {}
        
        recommendations = {}
        
        for product, metrics in self.classifications.items():
            classification = metrics['classification']
            recs = []
            
            if "Star" in classification:
                recs = [
                    "🎯 INVESTIR: Produto com alto crescimento e participação",
                    "Aumentar capacidade operacional",
                    "Manter qualidade do serviço",
                    "Proteger market share contra concorrentes"
                ]
            elif "Cash Cow" in classification:
                recs = [
                    "💵 COLHER: Maximizar lucros com investimento mínimo",
                    "Otimizar processos para reduzir custos",
                    "Usar caixa gerado para financiar Stars/Question Marks",
                    "Manter produto estável sem grandes inovações"
                ]
            elif "Question Mark" in classification:
                recs = [
                    "🤔 ANALISAR: Produto com crescimento mas baixa participação",
                    "Avaliar potencial de mercado",
                    "Decidir: investir para tornar Star ou desinvestir",
                    "Testar campanhas de marketing direcionadas"
                ]
            else:  # Dog
                recs = [
                    "⚠️ REAVALIAR: Produto com baixo crescimento e participação",
                    "Considerar descontinuação ou venda",
                    "Reduzir investimentos ao mínimo",
                    "Explorar nicho específico ou reformular produto"
                ]
            
            recommendations[product] = recs
        
        return recommendations
    
    def generate_report(self) -> str:
        """
        Generate formatted BCG Matrix report.
        
        Returns:
            str: Formatted report text
        """
        if not self.classifications:
            return "No analysis available. Run analyze_portfolio() first."
        
        report = """
╔════════════════════════════════════════════════════════════════╗
║          BCG MATRIX - CDL Manaus Product Portfolio            ║
╚════════════════════════════════════════════════════════════════╝

"""
        
        # Sort by market share (descending)
        sorted_products = sorted(self.classifications.items(), 
                               key=lambda x: x[1]['market_share'], 
                               reverse=True)
        
        for product, metrics in sorted_products:
            report += f"\n{'='*60}\n"
            report += f"PRODUTO: {product.replace('_', ' ').upper()}\n"
            report += f"{'='*60}\n"
            report += f"Classificação: {metrics['classification']}\n"
            report += f"Market Share: {metrics['market_share']:.2f}%\n"
            report += f"Taxa de Crescimento: {metrics['growth_rate']:+.2f}%\n"
            report += f"Receita Total (Jan-Nov): R$ {metrics['total_revenue']:,.2f}\n"
            report += f"Receita Média Mensal: R$ {metrics['avg_monthly_revenue']:,.2f}\n"
            
            # Get recommendations
            recs = self.get_recommendations()[product]
            report += f"\n📋 RECOMENDAÇÕES ESTRATÉGICAS:\n"
            for i, rec in enumerate(recs, 1):
                report += f"   {i}. {rec}\n"
        
        # Add summary
        report += f"\n{'='*60}\n"
        report += "RESUMO DO PORTFÓLIO\n"
        report += f"{'='*60}\n"
        
        by_classification = {}
        for product, metrics in self.classifications.items():
            classification = metrics['classification']
            if classification not in by_classification:
                by_classification[classification] = []
            by_classification[classification].append(product)
        
        for classification, products in by_classification.items():
            report += f"{classification}: {', '.join(products)}\n"
        
        return report
