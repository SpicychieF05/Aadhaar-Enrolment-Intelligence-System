"""
Configuration settings for AEIS Backend
"""
import os

# Data paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
DEFAULT_CSV_PATH = os.path.join(DATA_DIR, 'enrolment_dataset_birbhum.csv')

# Server settings
HOST = '0.0.0.0'
PORT = 5000
DEBUG = False

# CORS settings
CORS_ORIGINS = ['*']

# Analysis settings
ANOMALY_THRESHOLD = 2.5  # Z-score threshold for anomaly detection
ROLLING_WINDOW = 7  # Days for rolling statistics

# Visualization settings
FIGURE_DPI = 100
FIGURE_SIZE = (12, 6)
COLOR_PALETTE = {
    'primary': '#1e3a8a',      # Navy blue
    'secondary': '#475569',     # Dark grey
    'accent': '#2563eb',        # Blue
    'success': '#16a34a',       # Green
    'warning': '#ea580c',       # Orange
    'danger': '#dc2626',        # Red
    'light': '#f1f5f9',        # Light grey
    'white': '#ffffff'
}

# Required columns in dataset
REQUIRED_COLUMNS = [
    'date', 'state', 'district', 'pincode',
    'age_0_5', 'age_5_17', 'age_18_greater'
]

# Age group labels
AGE_GROUPS = {
    'age_0_5': '0-5 years',
    'age_5_17': '5-17 years',
    'age_18_greater': '18+ years'
}
