"""
Data preprocessing and transformation module for AEIS
"""
import pandas as pd
from datetime import datetime


def parse_dates(df):
    """
    Parse date column to datetime format
    Handles DD-MM-YYYY format from the dataset
    
    Args:
        df: pandas.DataFrame
    
    Returns:
        pandas.DataFrame: DataFrame with parsed dates
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    
    # Remove rows with invalid dates
    df = df.dropna(subset=['date'])
    
    return df


def add_derived_columns(df):
    """
    Add derived columns for analysis
    
    Args:
        df: pandas.DataFrame
    
    Returns:
        pandas.DataFrame: DataFrame with additional columns
    """
    df = df.copy()
    
    # Calculate total enrolments
    df['total_enrolments'] = (
        df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
    )
    
    # Extract time-based features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%B')
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.day_name()
    df['week_of_year'] = df['date'].dt.isocalendar().week
    
    return df


def filter_by_date_range(df, start_date=None, end_date=None):
    """
    Filter dataframe by date range
    
    Args:
        df: pandas.DataFrame
        start_date: Start date (string or datetime)
        end_date: End date (string or datetime)
    
    Returns:
        pandas.DataFrame: Filtered dataframe
    """
    df = df.copy()
    
    if start_date:
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        df = df[df['date'] >= start_date]
    
    if end_date:
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        df = df[df['date'] <= end_date]
    
    return df


def filter_by_pincode(df, pincodes):
    """
    Filter dataframe by pincode(s)
    
    Args:
        df: pandas.DataFrame
        pincodes: Single pincode or list of pincodes
    
    Returns:
        pandas.DataFrame: Filtered dataframe
    """
    if isinstance(pincodes, (int, str)):
        pincodes = [pincodes]
    
    pincodes = [int(p) for p in pincodes]
    return df[df['pincode'].isin(pincodes)]


def filter_by_age_group(df, age_groups):
    """
    Filter to include only specified age groups
    
    Args:
        df: pandas.DataFrame
        age_groups: List of age group column names
    
    Returns:
        pandas.DataFrame: Filtered dataframe
    """
    df = df.copy()
    valid_groups = ['age_0_5', 'age_5_17', 'age_18_greater']
    
    if not age_groups:
        return df
    
    # Ensure requested age groups are valid
    age_groups = [ag for ag in age_groups if ag in valid_groups]
    
    return df


def aggregate_by_time(df, freq='D'):
    """
    Aggregate enrolments by time period
    
    Args:
        df: pandas.DataFrame
        freq: Frequency ('D'=daily, 'W'=weekly, 'M'=monthly)
    
    Returns:
        pandas.DataFrame: Aggregated dataframe
    """
    df = df.copy()
    df = df.set_index('date')
    
    agg_dict = {
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum',
        'total_enrolments': 'sum',
        'pincode': 'nunique',
        'district': 'first'
    }
    
    result = df.resample(freq).agg(agg_dict).reset_index()
    return result


def aggregate_by_pincode(df):
    """
    Aggregate enrolments by pincode
    
    Args:
        df: pandas.DataFrame
    
    Returns:
        pandas.DataFrame: Aggregated by pincode
    """
    agg_dict = {
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum',
        'total_enrolments': 'sum',
        'date': 'count'
    }
    
    result = df.groupby('pincode').agg(agg_dict).reset_index()
    result.rename(columns={'date': 'num_records'}, inplace=True)
    result = result.sort_values('total_enrolments', ascending=False)
    
    return result


def preprocess_data(df):
    """
    Main preprocessing pipeline
    
    Args:
        df: pandas.DataFrame
    
    Returns:
        pandas.DataFrame: Fully preprocessed dataframe
    """
    df = parse_dates(df)
    df = add_derived_columns(df)
    df = df.sort_values('date').reset_index(drop=True)
    
    return df
