"""
Data loading and validation module for AEIS
"""
import pandas as pd
import os
from datetime import datetime
from config import REQUIRED_COLUMNS, DEFAULT_CSV_PATH


def validate_columns(df):
    """Validate that all required columns are present"""
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    return True


def load_data(file_path=None):
    """
    Load enrolment data from CSV file
    
    Args:
        file_path: Path to CSV file (optional, uses default if not provided)
    
    Returns:
        pandas.DataFrame: Loaded and validated data
    """
    if file_path is None:
        file_path = DEFAULT_CSV_PATH
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    # Load CSV
    df = pd.read_csv(file_path)
    
    # Validate columns
    validate_columns(df)
    
    return df


def get_data_info(df):
    """
    Get summary information about the dataset
    
    Args:
        df: pandas.DataFrame
    
    Returns:
        dict: Summary statistics and metadata
    """
    info = {
        'total_records': len(df),
        'columns': list(df.columns),
        'date_range': {
            'start': df['date'].min() if 'date' in df.columns else None,
            'end': df['date'].max() if 'date' in df.columns else None
        },
        'districts': df['district'].unique().tolist() if 'district' in df.columns else [],
        'pincodes_count': df['pincode'].nunique() if 'pincode' in df.columns else 0,
        'missing_values': df.isnull().sum().to_dict()
    }
    return info


def validate_uploaded_file(file_path):
    """
    Validate an uploaded CSV file
    
    Args:
        file_path: Path to uploaded file
    
    Returns:
        tuple: (success: bool, message: str, data: DataFrame or None)
    """
    try:
        df = load_data(file_path)
        info = get_data_info(df)
        return True, "File validated successfully", df, info
    except Exception as e:
        return False, f"Validation error: {str(e)}", None, None
