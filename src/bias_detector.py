"""
Bias Detector Module - CDL Manaus Intelligence Hub
Implements bias detection and logging for analytical rigor
Focuses on Survivorship Bias and Selection Bias in business data
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class BiasDetector:
    """
    Bias detection system for business intelligence data.
    Monitors and alerts about common analytical biases.
    """
    
    def __init__(self):
        """Initialize bias detector."""
        self.bias_log: List[Dict] = []
        self.detection_count = 0
        logger.info("Bias Detector initialized")
    
    def log_bias(self, bias_type: str, severity: str, description: str, 
                 recommendation: str, metadata: Optional[Dict] = None):
        """
        Log a detected bias with details.
        
        Args:
            bias_type: Type of bias (e.g., 'Survivorship', 'Selection')
            severity: Severity level ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')
            description: Description of the bias
            recommendation: Recommended action
            metadata: Additional metadata
        """
        bias_entry = {
            'timestamp': datetime.now().isoformat(),
            'bias_type': bias_type,
            'severity': severity,
            'description': description,
            'recommendation': recommendation,
            'metadata': metadata or {}
        }
        
        self.bias_log.append(bias_entry)
        self.detection_count += 1
        
        # Log with appropriate level
        log_message = f"[{severity}] {bias_type} Bias: {description}"
        if severity in ['HIGH', 'CRITICAL']:
            logger.warning(log_message)
        else:
            logger.info(log_message)
    
    def check_survivorship_bias(self, df: pd.DataFrame, 
                                client_column: str = 'Cliente',
                                status_column: Optional[str] = None) -> Dict:
        """
        Check for survivorship bias in customer/associate data.
        Detects if analysis only includes active clients, ignoring inactive ones.
        
        Args:
            df: DataFrame with client data
            client_column: Name of client identifier column
            status_column: Optional column indicating active/inactive status
            
        Returns:
            Dict: Detection results
        """
        logger.info("Checking for Survivorship Bias")
        
        result = {
            'bias_detected': False,
            'severity': 'LOW',
            'details': {}
        }
        
        # If status column is provided, check for imbalance
        if status_column and status_column in df.columns:
            active_count = (df[status_column] == 'Ativo').sum()
            inactive_count = (df[status_column] == 'Inativo').sum()
            total = len(df)
            
            if total > 0:
                active_pct = (active_count / total) * 100
                inactive_pct = (inactive_count / total) * 100
                
                result['details'] = {
                    'total_clients': total,
                    'active_clients': active_count,
                    'inactive_clients': inactive_count,
                    'active_percentage': active_pct,
                    'inactive_percentage': inactive_pct
                }
                
                # Alert if data heavily skewed toward active clients
                if inactive_count == 0 and active_count > 0:
                    result['bias_detected'] = True
                    result['severity'] = 'HIGH'
                    
                    self.log_bias(
                        bias_type='Survivorship Bias',
                        severity='HIGH',
                        description=f"Dataset contains ONLY active clients ({active_count}). No inactive clients represented.",
                        recommendation="Include historical data from inactive/churned clients to avoid overestimating success metrics.",
                        metadata=result['details']
                    )
                
                elif inactive_pct < 10 and active_count > 50:
                    result['bias_detected'] = True
                    result['severity'] = 'MEDIUM'
                    
                    self.log_bias(
                        bias_type='Survivorship Bias',
                        severity='MEDIUM',
                        description=f"Dataset heavily skewed toward active clients ({active_pct:.1f}% active vs {inactive_pct:.1f}% inactive).",
                        recommendation="Consider including more historical data from churned clients for balanced analysis.",
                        metadata=result['details']
                    )
        
        # Check for missing historical data
        if client_column in df.columns:
            unique_clients = df[client_column].nunique()
            total_records = len(df)
            
            if total_records > 0 and unique_clients > 0:
                avg_records_per_client = total_records / unique_clients
                
                if avg_records_per_client < 3:
                    result['bias_detected'] = True
                    result['severity'] = 'MEDIUM'
                    
                    self.log_bias(
                        bias_type='Survivorship Bias (Data Sparsity)',
                        severity='MEDIUM',
                        description=f"Limited historical data: average {avg_records_per_client:.1f} records per client.",
                        recommendation="Collect more historical data to identify patterns in client lifecycle.",
                        metadata={'avg_records_per_client': avg_records_per_client}
                    )
        
        return result
    
    def check_selection_bias(self, df: pd.DataFrame, 
                            ranking_column: str = 'Top20_Flag',
                            value_column: str = 'Faturamento') -> Dict:
        """
        Check for selection bias in Top 20 or ranking analyses.
        Detects if analysis focuses only on top performers, ignoring the rest.
        
        Args:
            df: DataFrame with ranking/segmentation data
            ranking_column: Column indicating top/bottom segment
            value_column: Column with values being analyzed
            
        Returns:
            Dict: Detection results
        """
        logger.info("Checking for Selection Bias")
        
        result = {
            'bias_detected': False,
            'severity': 'LOW',
            'details': {}
        }
        
        if ranking_column not in df.columns:
            # Create synthetic Top20 flag based on value percentile
            if value_column in df.columns:
                percentile_80 = df[value_column].quantile(0.80)
                top_20_count = (df[value_column] >= percentile_80).sum()
                bottom_80_count = len(df) - top_20_count
                
                result['details'] = {
                    'top_20_count': top_20_count,
                    'bottom_80_count': bottom_80_count,
                    'top_20_value_sum': df[df[value_column] >= percentile_80][value_column].sum(),
                    'total_value_sum': df[value_column].sum()
                }
                
                if result['details']['total_value_sum'] > 0:
                    concentration = (result['details']['top_20_value_sum'] / 
                                   result['details']['total_value_sum']) * 100
                    result['details']['concentration_percentage'] = concentration
                    
                    # Alert on extreme concentration
                    if concentration > 60:
                        result['bias_detected'] = True
                        result['severity'] = 'HIGH'
                        
                        self.log_bias(
                            bias_type='Selection Bias (Concentration Risk)',
                            severity='HIGH',
                            description=f"Top 20% of clients represent {concentration:.1f}% of total revenue. Extreme concentration risk.",
                            recommendation="Diversify client base. Develop strategies to grow mid-tier clients. Monitor Top 20 closely for early warning signs.",
                            metadata=result['details']
                        )
                    
                    elif concentration > 45:
                        result['bias_detected'] = True
                        result['severity'] = 'MEDIUM'
                        
                        self.log_bias(
                            bias_type='Selection Bias (High Concentration)',
                            severity='MEDIUM',
                            description=f"Top 20% of clients represent {concentration:.1f}% of revenue. High concentration detected.",
                            recommendation="Monitor top clients closely. Consider strategies to reduce dependency on few large clients.",
                            metadata=result['details']
                        )
        else:
            # Explicit ranking column exists
            top_count = (df[ranking_column] == True).sum() if df[ranking_column].dtype == bool else \
                       (df[ranking_column] == 1).sum()
            bottom_count = len(df) - top_count
            
            if bottom_count == 0 and top_count > 0:
                result['bias_detected'] = True
                result['severity'] = 'CRITICAL'
                
                self.log_bias(
                    bias_type='Selection Bias',
                    severity='CRITICAL',
                    description=f"Dataset contains ONLY top-ranked clients ({top_count}). No comparison group.",
                    recommendation="Include non-top-tier clients in analysis for proper benchmarking and risk assessment.",
                    metadata={'top_count': top_count}
                )
        
        return result
    
    def check_recency_bias(self, df: pd.DataFrame, date_column: str = 'Mes') -> Dict:
        """
        Check for recency bias - over-weighting recent data.
        
        Args:
            df: DataFrame with time series data
            date_column: Name of date column
            
        Returns:
            Dict: Detection results
        """
        logger.info("Checking for Recency Bias")
        
        result = {
            'bias_detected': False,
            'severity': 'LOW',
            'details': {}
        }
        
        if date_column not in df.columns:
            return result
        
        df_sorted = df.sort_values(date_column)
        date_range = pd.to_datetime(df_sorted[date_column])
        
        if len(date_range) < 2:
            return result
        
        total_days = (date_range.max() - date_range.min()).days
        
        if total_days < 180:  # Less than 6 months of data
            result['bias_detected'] = True
            result['severity'] = 'MEDIUM'
            result['details'] = {
                'data_span_days': total_days,
                'earliest_date': date_range.min().strftime('%Y-%m-%d'),
                'latest_date': date_range.max().strftime('%Y-%m-%d')
            }
            
            self.log_bias(
                bias_type='Recency Bias (Limited History)',
                severity='MEDIUM',
                description=f"Analysis based on only {total_days} days of data. May not capture seasonal patterns or long-term trends.",
                recommendation="Extend data collection period to at least 12 months for robust trend analysis.",
                metadata=result['details']
            )
        
        return result
    
    def run_full_analysis(self, df: pd.DataFrame, 
                         config: Optional[Dict] = None) -> Dict:
        """
        Run all bias checks on a dataset.
        
        Args:
            df: DataFrame to analyze
            config: Optional configuration with column mappings
            
        Returns:
            Dict: Complete bias analysis results
        """
        logger.info("Running full bias analysis")
        
        config = config or {}
        
        results = {
            'survivorship': self.check_survivorship_bias(
                df, 
                client_column=config.get('client_column', 'Cliente'),
                status_column=config.get('status_column')
            ),
            'selection': self.check_selection_bias(
                df,
                ranking_column=config.get('ranking_column', 'Top20_Flag'),
                value_column=config.get('value_column', 'Faturamento')
            ),
            'recency': self.check_recency_bias(
                df,
                date_column=config.get('date_column', 'Mes')
            ),
            'total_biases_detected': self.detection_count,
            'bias_log': self.bias_log
        }
        
        logger.info(f"Bias analysis complete: {self.detection_count} potential biases detected")
        return results
    
    def generate_report(self) -> str:
        """
        Generate formatted bias detection report.
        
        Returns:
            str: Formatted report text
        """
        if not self.bias_log:
            return "✅ No biases detected in the analysis."
        
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║              BIAS DETECTION REPORT - Vigilância                ║
║              Total Biases Detected: {self.detection_count:2d}                       ║
╚════════════════════════════════════════════════════════════════╝

"""
        
        # Group by severity
        by_severity = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': []}
        for entry in self.bias_log:
            severity = entry['severity']
            if severity in by_severity:
                by_severity[severity].append(entry)
        
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            entries = by_severity[severity]
            if not entries:
                continue
            
            icon = '🔴' if severity == 'CRITICAL' else '🟠' if severity == 'HIGH' else '🟡' if severity == 'MEDIUM' else '🟢'
            report += f"\n{icon} {severity} SEVERITY ({len(entries)})\n"
            report += "="*60 + "\n"
            
            for i, entry in enumerate(entries, 1):
                report += f"\n{i}. {entry['bias_type']}\n"
                report += f"   {entry['description']}\n"
                report += f"   💡 Recommendation: {entry['recommendation']}\n"
        
        return report
    
    def get_summary(self) -> Dict:
        """
        Get summary statistics of bias detection.
        
        Returns:
            Dict: Summary statistics
        """
        summary = {
            'total_checks_run': len(self.bias_log),
            'biases_by_type': {},
            'biases_by_severity': {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        }
        
        for entry in self.bias_log:
            bias_type = entry['bias_type']
            severity = entry['severity']
            
            if bias_type not in summary['biases_by_type']:
                summary['biases_by_type'][bias_type] = 0
            summary['biases_by_type'][bias_type] += 1
            
            if severity in summary['biases_by_severity']:
                summary['biases_by_severity'][severity] += 1
        
        return summary
