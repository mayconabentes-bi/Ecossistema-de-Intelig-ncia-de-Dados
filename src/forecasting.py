"""
Forecasting Module - CDL Manaus Intelligence Hub
Implements time series forecasting using ARIMA for revenue projection
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
import warnings

# Suppress ARIMA convergence warnings for cleaner output
warnings.filterwarnings('ignore')

try:
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.stattools import adfuller
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    logging.warning("statsmodels not installed. Forecasting will use simple methods.")

logger = logging.getLogger(__name__)


class BillingForecaster:
    """
    Time series forecasting for billing data using ARIMA methodology.
    Implements strategic forecasting for December 2025 revenue projection.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize forecaster with historical billing data.
        
        Args:
            data: DataFrame with 'Mes' and 'Faturamento_Real' columns
        """
        if 'Mes' not in data.columns or 'Faturamento_Real' not in data.columns:
            raise ValueError("Data must contain 'Mes' and 'Faturamento_Real' columns")
        
        self.data = data.copy()
        self.data = self.data.sort_values('Mes')
        self.model = None
        self.forecast_result = None
        logger.info(f"BillingForecaster initialized with {len(data)} data points")
    
    def check_stationarity(self) -> Tuple[bool, float]:
        """
        Check if the time series is stationary using Augmented Dickey-Fuller test.
        
        Returns:
            Tuple[bool, float]: (is_stationary, p_value)
        """
        if not STATSMODELS_AVAILABLE:
            return False, 1.0
        
        series = self.data['Faturamento_Real'].values
        result = adfuller(series)
        p_value = result[1]
        is_stationary = p_value < 0.05
        
        logger.info(f"Stationarity test: p-value = {p_value:.4f}, stationary = {is_stationary}")
        return is_stationary, p_value
    
    def forecast_billing(self, periods: int = 1, method: str = 'arima') -> Dict:
        """
        Forecast billing for future periods using specified method.
        
        Args:
            periods: Number of periods to forecast (default: 1 for December)
            method: Forecasting method - 'arima', 'moving_average', or 'trend'
            
        Returns:
            Dict: Forecast results with predictions and confidence intervals
        """
        logger.info(f"Starting forecast for {periods} period(s) using {method} method")
        
        if method == 'arima' and STATSMODELS_AVAILABLE:
            return self._forecast_arima(periods)
        elif method == 'moving_average':
            return self._forecast_moving_average(periods)
        elif method == 'trend':
            return self._forecast_trend(periods)
        else:
            logger.warning(f"Method '{method}' not available, falling back to moving average")
            return self._forecast_moving_average(periods)
    
    def _forecast_arima(self, periods: int) -> Dict:
        """
        Forecast using ARIMA model.
        Auto-determines best (p,d,q) parameters.
        
        Args:
            periods: Number of periods to forecast
            
        Returns:
            Dict: Forecast results
        """
        series = self.data['Faturamento_Real'].values
        
        # Auto-determine parameters based on data characteristics
        # For monthly billing data, common patterns:
        # p (AR terms): 1-2, d (differencing): 0-1, q (MA terms): 1-2
        
        # Check if differencing is needed
        is_stationary, _ = self.check_stationarity()
        d = 0 if is_stationary else 1
        
        # Try different parameter combinations and select best AIC
        best_aic = np.inf
        best_order = (1, d, 1)
        
        for p in range(0, 3):
            for q in range(0, 3):
                try:
                    model = ARIMA(series, order=(p, d, q))
                    fitted_model = model.fit()
                    if fitted_model.aic < best_aic:
                        best_aic = fitted_model.aic
                        best_order = (p, d, q)
                except:
                    continue
        
        logger.info(f"Best ARIMA order: {best_order} (AIC: {best_aic:.2f})")
        
        # Fit final model
        try:
            model = ARIMA(series, order=best_order)
            self.model = model.fit()
            
            # Generate forecast
            forecast = self.model.forecast(steps=periods)
            forecast_conf = self.model.get_forecast(steps=periods)
            conf_int = forecast_conf.conf_int()
            
            # Calculate historical mean for baseline comparison
            historical_mean = series.mean()
            
            # Extract confidence intervals safely
            ci_lower, ci_upper = self._extract_confidence_intervals(conf_int)
            
            # Build result
            result = {
                'method': 'ARIMA',
                'order': best_order,
                'aic': best_aic,
                'forecast_periods': periods,
                'predictions': forecast.tolist(),
                'prediction_dezembro': float(forecast[0]) if periods >= 1 else None,
                'confidence_interval_lower': ci_lower,
                'confidence_interval_upper': ci_upper,
                'historical_mean': float(historical_mean),
                'model_summary': str(self.model.summary())
            }
            
            logger.info(f"ARIMA forecast complete: December 2025 = R$ {result['prediction_dezembro']:,.2f}")
            return result
            
        except Exception as e:
            logger.error(f"ARIMA modeling failed: {str(e)}")
            logger.warning("Falling back to moving average method")
            return self._forecast_moving_average(periods)
    
    def _forecast_moving_average(self, periods: int, window: int = 3) -> Dict:
        """
        Forecast using simple moving average.
        
        Args:
            periods: Number of periods to forecast
            window: Moving average window size
            
        Returns:
            Dict: Forecast results
        """
        series = self.data['Faturamento_Real'].values
        
        # Calculate moving average of last 'window' periods
        ma = np.mean(series[-window:])
        
        # For multiple periods, use the same MA value (naive forecast)
        predictions = [ma] * periods
        
        # Estimate confidence interval based on historical standard deviation
        std = np.std(series[-window:])
        conf_lower = [ma - 1.96 * std] * periods
        conf_upper = [ma + 1.96 * std] * periods
        
        result = {
            'method': 'Moving Average',
            'window': window,
            'forecast_periods': periods,
            'predictions': predictions,
            'prediction_dezembro': predictions[0],
            'confidence_interval_lower': conf_lower,
            'confidence_interval_upper': conf_upper,
            'historical_mean': float(np.mean(series))
        }
        
        logger.info(f"Moving average forecast: December 2025 = R$ {result['prediction_dezembro']:,.2f}")
        return result
    
    def _forecast_trend(self, periods: int) -> Dict:
        """
        Forecast using linear trend extrapolation.
        
        Args:
            periods: Number of periods to forecast
            
        Returns:
            Dict: Forecast results
        """
        series = self.data['Faturamento_Real'].values
        n = len(series)
        
        # Fit linear trend: y = a + b*x
        x = np.arange(n)
        coeffs = np.polyfit(x, series, 1)
        trend = np.poly1d(coeffs)
        
        # Predict future periods
        future_x = np.arange(n, n + periods)
        predictions = trend(future_x).tolist()
        
        # Estimate confidence interval from residuals
        fitted_values = trend(x)
        residuals = series - fitted_values
        std_residual = np.std(residuals)
        
        conf_lower = [p - 1.96 * std_residual for p in predictions]
        conf_upper = [p + 1.96 * std_residual for p in predictions]
        
        result = {
            'method': 'Linear Trend',
            'trend_coefficients': coeffs.tolist(),
            'forecast_periods': periods,
            'predictions': predictions,
            'prediction_dezembro': predictions[0],
            'confidence_interval_lower': conf_lower,
            'confidence_interval_upper': conf_upper,
            'historical_mean': float(np.mean(series))
        }
        
        logger.info(f"Trend forecast: December 2025 = R$ {result['prediction_dezembro']:,.2f}")
        return result
    
    def _extract_confidence_intervals(self, conf_int) -> Tuple[List[float], List[float]]:
        """
        Safely extract confidence interval bounds from various formats.
        
        Args:
            conf_int: Confidence interval object (DataFrame, ndarray, etc.)
            
        Returns:
            Tuple of (lower_bounds, upper_bounds) as lists
        """
        try:
            if hasattr(conf_int, 'iloc'):
                # DataFrame format
                ci_lower = conf_int.iloc[:, 0].tolist()
                ci_upper = conf_int.iloc[:, 1].tolist()
            elif hasattr(conf_int, 'shape') and len(conf_int.shape) == 2:
                # NumPy array format
                ci_lower = conf_int[:, 0].tolist()
                ci_upper = conf_int[:, 1].tolist()
            else:
                # Fallback for unexpected formats
                ci_lower = [float(conf_int[0, 0])]
                ci_upper = [float(conf_int[0, 1])]
            return ci_lower, ci_upper
        except Exception as e:
            logger.warning(f"Error extracting confidence intervals: {e}. Using default values.")
            # Return empty confidence intervals as fallback
            return [0.0], [0.0]
    
    def get_forecast_summary(self) -> str:
        """
        Generate a human-readable summary of the forecast.
        
        Returns:
            str: Formatted summary text
        """
        if self.forecast_result is None:
            return "No forecast available. Run forecast_billing() first."
        
        pred = self.forecast_result['prediction_dezembro']
        method = self.forecast_result['method']
        hist_mean = self.forecast_result['historical_mean']
        
        var_percent = ((pred - hist_mean) / hist_mean) * 100
        
        summary = f"""
        Forecast Summary - December 2025
        ================================
        Method: {method}
        Predicted Revenue: R$ {pred:,.2f}
        Historical Average: R$ {hist_mean:,.2f}
        Variance from Average: {var_percent:+.2f}%
        
        Confidence Interval (95%):
        Lower Bound: R$ {self.forecast_result['confidence_interval_lower'][0]:,.2f}
        Upper Bound: R$ {self.forecast_result['confidence_interval_upper'][0]:,.2f}
        """
        
        return summary
