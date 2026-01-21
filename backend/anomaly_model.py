"""
Explainable anomaly detection module for AEIS
Uses statistical methods (z-score, rolling statistics)
"""
import pandas as pd
import numpy as np
from config import ANOMALY_THRESHOLD, ROLLING_WINDOW


def calculate_zscore_anomalies(df, column='total_enrolments', threshold=ANOMALY_THRESHOLD):
    """
    Detect anomalies using z-score method
    
    Methodology:
    - Calculate mean and standard deviation of daily enrolments
    - Identify days where enrolment deviates by more than threshold standard deviations
    
    Args:
        df: pandas.DataFrame
        column: Column to analyze
        threshold: Z-score threshold
    
    Returns:
        pandas.DataFrame: Data with anomaly flags and scores
    """
    daily = df.groupby('date')[column].sum().reset_index()
    
    # Calculate z-scores
    mean = daily[column].mean()
    std = daily[column].std()
    daily['z_score'] = (daily[column] - mean) / std
    
    # Flag anomalies
    daily['is_anomaly'] = abs(daily['z_score']) > threshold
    daily['anomaly_type'] = daily['z_score'].apply(
        lambda x: 'high' if x > threshold else ('low' if x < -threshold else 'normal')
    )
    
    return daily


def calculate_rolling_anomalies(df, column='total_enrolments', 
                                window=ROLLING_WINDOW, threshold=ANOMALY_THRESHOLD):
    """
    Detect anomalies using rolling window statistics
    
    Methodology:
    - Calculate rolling mean and standard deviation
    - Compare each day to its recent trend
    - Flag significant deviations
    
    Args:
        df: pandas.DataFrame
        column: Column to analyze
        window: Rolling window size (days)
        threshold: Threshold multiplier
    
    Returns:
        pandas.DataFrame: Data with rolling anomaly detection
    """
    daily = df.groupby('date')[column].sum().reset_index()
    daily = daily.sort_values('date')
    
    # Calculate rolling statistics
    daily['rolling_mean'] = daily[column].rolling(window=window, center=True).mean()
    daily['rolling_std'] = daily[column].rolling(window=window, center=True).std()
    
    # Calculate deviation from rolling mean
    daily['deviation'] = abs(daily[column] - daily['rolling_mean'])
    daily['threshold_value'] = daily['rolling_std'] * threshold
    
    # Flag anomalies
    daily['is_rolling_anomaly'] = daily['deviation'] > daily['threshold_value']
    daily['anomaly_severity'] = (daily['deviation'] / daily['threshold_value']).fillna(0)
    
    return daily


def detect_pincode_anomalies(df, threshold_percentile=95):
    """
    Detect anomalous pincodes based on enrolment volume
    
    Methodology:
    - Calculate total enrolments per pincode
    - Identify pincodes above a percentile threshold
    
    Args:
        df: pandas.DataFrame
        threshold_percentile: Percentile threshold
    
    Returns:
        pandas.DataFrame: Pincode-level anomaly analysis
    """
    pincode_totals = df.groupby('pincode')['total_enrolments'].sum().reset_index()
    
    # Calculate threshold
    threshold_value = np.percentile(pincode_totals['total_enrolments'], threshold_percentile)
    
    # Flag high-volume pincodes
    pincode_totals['is_high_volume'] = pincode_totals['total_enrolments'] > threshold_value
    pincode_totals['percentile'] = pincode_totals['total_enrolments'].rank(pct=True) * 100
    
    return pincode_totals.sort_values('total_enrolments', ascending=False)


def detect_temporal_anomalies(df):
    """
    Detect temporal patterns that deviate from expected behavior
    
    Methodology:
    - Compare day-of-week patterns
    - Identify unusual spikes or drops
    
    Args:
        df: pandas.DataFrame
    
    Returns:
        dict: Temporal anomaly analysis
    """
    # Day of week analysis
    dow_pattern = df.groupby('day_of_week')['total_enrolments'].agg(['mean', 'std']).reset_index()
    
    # Month analysis
    month_pattern = df.groupby('month')['total_enrolments'].agg(['mean', 'std']).reset_index()
    
    analysis = {
        'day_of_week_patterns': dow_pattern.to_dict('records'),
        'monthly_patterns': month_pattern.to_dict('records')
    }
    
    return analysis


def explain_anomaly(anomaly_row, analysis_type='zscore'):
    """
    Generate human-readable explanation for detected anomaly
    
    Args:
        anomaly_row: pandas.Series with anomaly data
        analysis_type: Type of analysis used
    
    Returns:
        str: Explanation text
    """
    if analysis_type == 'zscore':
        if anomaly_row.get('anomaly_type') == 'high':
            explanation = (
                f"On {anomaly_row['date']}, enrolments ({int(anomaly_row['total_enrolments'])}) "
                f"were significantly higher than average (z-score: {anomaly_row['z_score']:.2f}). "
                f"This is {abs(anomaly_row['z_score']):.1f} standard deviations above the mean."
            )
        elif anomaly_row.get('anomaly_type') == 'low':
            explanation = (
                f"On {anomaly_row['date']}, enrolments ({int(anomaly_row['total_enrolments'])}) "
                f"were significantly lower than average (z-score: {anomaly_row['z_score']:.2f}). "
                f"This is {abs(anomaly_row['z_score']):.1f} standard deviations below the mean."
            )
        else:
            explanation = "No significant anomaly detected."
    
    elif analysis_type == 'rolling':
        explanation = (
            f"On {anomaly_row['date']}, enrolments deviated significantly from the "
            f"recent {ROLLING_WINDOW}-day trend (severity: {anomaly_row.get('anomaly_severity', 0):.2f})."
        )
    
    else:
        explanation = "Anomaly detected based on statistical analysis."
    
    return explanation


def run_anomaly_detection(df):
    """
    Run complete anomaly detection pipeline
    
    Args:
        df: pandas.DataFrame (preprocessed)
    
    Returns:
        dict: Anomaly detection results with explanations
    """
    # Z-score based detection
    zscore_anomalies = calculate_zscore_anomalies(df)
    zscore_flagged = zscore_anomalies[zscore_anomalies['is_anomaly']]
    
    # Rolling window detection
    rolling_anomalies = calculate_rolling_anomalies(df)
    rolling_flagged = rolling_anomalies[rolling_anomalies['is_rolling_anomaly']]
    
    # Pincode anomalies
    pincode_anomalies = detect_pincode_anomalies(df)
    
    # Temporal anomalies
    temporal_anomalies = detect_temporal_anomalies(df)
    
    # Generate explanations for top anomalies
    top_zscore = zscore_flagged.nlargest(5, 'z_score') if not zscore_flagged.empty else pd.DataFrame()
    explanations = []
    for _, row in top_zscore.iterrows():
        explanations.append({
            'date': row['date'].strftime('%Y-%m-%d'),
            'enrolments': int(row['total_enrolments']),
            'explanation': explain_anomaly(row, 'zscore')
        })
    
    results = {
        'zscore_analysis': {
            'all_days': zscore_anomalies.to_dict('records'),
            'anomalies_found': int(zscore_flagged.shape[0]),
            'flagged_days': zscore_flagged.to_dict('records')
        },
        'rolling_analysis': {
            'all_days': rolling_anomalies.to_dict('records'),
            'anomalies_found': int(rolling_flagged.shape[0]),
            'flagged_days': rolling_flagged.to_dict('records')
        },
        'pincode_analysis': {
            'high_volume_pincodes': pincode_anomalies[pincode_anomalies['is_high_volume']].to_dict('records'),
            'top_10_pincodes': pincode_anomalies.head(10).to_dict('records')
        },
        'temporal_analysis': temporal_anomalies,
        'explanations': explanations,
        'methodology': {
            'zscore_threshold': ANOMALY_THRESHOLD,
            'rolling_window_days': ROLLING_WINDOW,
            'description': (
                'Anomaly detection uses statistical methods: '
                '1) Z-score analysis identifies days that deviate significantly from overall mean. '
                '2) Rolling window analysis compares each day to recent trends. '
                '3) All methods are explainable and transparent.'
            )
        }
    }
    
    return results
