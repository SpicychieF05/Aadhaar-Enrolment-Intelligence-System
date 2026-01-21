"""
Statistical analysis module for AEIS
Focuses on explainable, interpretable analytics
"""
import pandas as pd
import numpy as np
from scipy import stats


def calculate_summary_statistics(df):
    """
    Calculate basic summary statistics
    
    Args:
        df: pandas.DataFrame
    
    Returns:
        dict: Summary statistics
    """
    summary = {
        'total_enrolments': int(df['total_enrolments'].sum()),
        'age_group_breakdown': {
            'age_0_5': int(df['age_0_5'].sum()),
            'age_5_17': int(df['age_5_17'].sum()),
            'age_18_greater': int(df['age_18_greater'].sum())
        },
        'daily_statistics': {
            'mean': float(df.groupby('date')['total_enrolments'].sum().mean()),
            'median': float(df.groupby('date')['total_enrolments'].sum().median()),
            'std': float(df.groupby('date')['total_enrolments'].sum().std()),
            'min': int(df.groupby('date')['total_enrolments'].sum().min()),
            'max': int(df.groupby('date')['total_enrolments'].sum().max())
        },
        'unique_pincodes': int(df['pincode'].nunique()),
        'date_range': {
            'start': df['date'].min().strftime('%Y-%m-%d'),
            'end': df['date'].max().strftime('%Y-%m-%d'),
            'days': (df['date'].max() - df['date'].min()).days
        }
    }
    
    return summary


def analyze_temporal_trends(df):
    """
    Analyze temporal patterns in enrolments
    
    Args:
        df: pandas.DataFrame
    
    Returns:
        dict: Temporal analysis results
    """
    # Daily trend
    daily = df.groupby('date')['total_enrolments'].sum().reset_index()
    
    # Weekly trend
    weekly = df.groupby(df['date'].dt.to_period('W'))['total_enrolments'].sum()
    
    # Monthly trend
    monthly = df.groupby(['year', 'month'])['total_enrolments'].sum().reset_index()
    
    # Day of week pattern
    dow_pattern = df.groupby('day_of_week')['total_enrolments'].sum()
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_pattern = dow_pattern.reindex(dow_order, fill_value=0)
    
    analysis = {
        'daily_trend': daily.to_dict('records'),
        'monthly_trend': monthly.to_dict('records'),
        'day_of_week_pattern': {
            'days': dow_pattern.index.tolist(),
            'enrolments': dow_pattern.values.tolist()
        },
        'trend_direction': 'increasing' if daily['total_enrolments'].iloc[-1] > daily['total_enrolments'].iloc[0] else 'decreasing'
    }
    
    return analysis


def analyze_geographic_distribution(df):
    """
    Analyze geographic patterns in enrolments
    
    Args:
        df: pandas.DataFrame
    
    Returns:
        dict: Geographic analysis results
    """
    # By pincode
    pincode_dist = df.groupby('pincode').agg({
        'total_enrolments': 'sum',
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum'
    }).reset_index()
    pincode_dist = pincode_dist.sort_values('total_enrolments', ascending=False)
    
    # By district
    district_dist = df.groupby('district').agg({
        'total_enrolments': 'sum',
        'pincode': 'nunique'
    }).reset_index()
    district_dist.rename(columns={'pincode': 'unique_pincodes'}, inplace=True)
    
    analysis = {
        'top_10_pincodes': pincode_dist.head(10).to_dict('records'),
        'district_summary': district_dist.to_dict('records'),
        'pincode_concentration': {
            'top_10_percent': float(pincode_dist.head(10)['total_enrolments'].sum() / pincode_dist['total_enrolments'].sum() * 100)
        }
    }
    
    return analysis


def analyze_age_distribution(df):
    """
    Analyze age group patterns
    
    Args:
        df: pandas.DataFrame
    
    Returns:
        dict: Age distribution analysis
    """
    total = df['total_enrolments'].sum()
    
    age_breakdown = {
        'age_0_5': {
            'count': int(df['age_0_5'].sum()),
            'percentage': float(df['age_0_5'].sum() / total * 100)
        },
        'age_5_17': {
            'count': int(df['age_5_17'].sum()),
            'percentage': float(df['age_5_17'].sum() / total * 100)
        },
        'age_18_greater': {
            'count': int(df['age_18_greater'].sum()),
            'percentage': float(df['age_18_greater'].sum() / total * 100)
        }
    }
    
    # Age distribution over time
    age_over_time = df.groupby('date')[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()
    
    analysis = {
        'overall_breakdown': age_breakdown,
        'temporal_breakdown': age_over_time.to_dict('records')
    }
    
    return analysis


def calculate_correlation_matrix(df):
    """
    Calculate correlations between age groups and time factors
    
    Args:
        df: pandas.DataFrame
    
    Returns:
        dict: Correlation analysis
    """
    # Select numeric columns for correlation
    numeric_cols = ['age_0_5', 'age_5_17', 'age_18_greater', 'total_enrolments', 
                    'month', 'day', 'week_of_year']
    
    corr_matrix = df[numeric_cols].corr()
    
    analysis = {
        'correlation_matrix': corr_matrix.to_dict(),
        'strong_correlations': []
    }
    
    # Find strong correlations (> 0.7 or < -0.7)
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.7:
                analysis['strong_correlations'].append({
                    'var1': corr_matrix.columns[i],
                    'var2': corr_matrix.columns[j],
                    'correlation': float(corr_val)
                })
    
    return analysis


def identify_peak_periods(df):
    """
    Identify peak enrolment periods
    
    Args:
        df: pandas.DataFrame
    
    Returns:
        dict: Peak period analysis
    """
    daily_total = df.groupby('date')['total_enrolments'].sum().reset_index()
    
    # Sort by enrolments
    sorted_days = daily_total.sort_values('total_enrolments', ascending=False)
    
    # Top 10 days
    top_days = sorted_days.head(10)
    
    # Peak month
    monthly = df.groupby(['year', 'month'])['total_enrolments'].sum().reset_index()
    peak_month = monthly.loc[monthly['total_enrolments'].idxmax()]
    
    analysis = {
        'top_10_days': top_days.to_dict('records'),
        'peak_month': {
            'year': int(peak_month['year']),
            'month': int(peak_month['month']),
            'enrolments': int(peak_month['total_enrolments'])
        },
        'average_daily_enrolment': float(daily_total['total_enrolments'].mean())
    }
    
    return analysis


def run_full_analysis(df):
    """
    Run complete statistical analysis
    
    Args:
        df: pandas.DataFrame (preprocessed)
    
    Returns:
        dict: Complete analysis results
    """
    results = {
        'summary': calculate_summary_statistics(df),
        'temporal': analyze_temporal_trends(df),
        'geographic': analyze_geographic_distribution(df),
        'age_distribution': analyze_age_distribution(df),
        'correlations': calculate_correlation_matrix(df),
        'peak_periods': identify_peak_periods(df)
    }
    
    return results
