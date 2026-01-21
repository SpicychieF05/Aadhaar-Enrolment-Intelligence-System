"""
Visualization generation module for AEIS
Generates charts as base64-encoded images for frontend display
"""
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import io
import base64
from config import FIGURE_DPI, FIGURE_SIZE, COLOR_PALETTE


# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = FIGURE_DPI


def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string"""
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=FIGURE_DPI)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close(fig)
    return f"data:image/png;base64,{image_base64}"


def plot_daily_enrolments(df, color_theme='default'):
    """
    Plot daily total enrolments over time
    
    Args:
        df: pandas.DataFrame (preprocessed)
        color_theme: Color theme to use
    
    Returns:
        str: Base64 encoded image
    """
    daily = df.groupby('date')['total_enrolments'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    ax.plot(daily['date'], daily['total_enrolments'], 
            color=COLOR_PALETTE['primary'], linewidth=2)
    ax.fill_between(daily['date'], daily['total_enrolments'], 
                     alpha=0.3, color=COLOR_PALETTE['primary'])
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Enrolments', fontsize=12, fontweight='bold')
    ax.set_title('Daily Aadhaar Enrolments - Birbhum District', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    return fig_to_base64(fig)


def plot_age_distribution(df, color_theme='default'):
    """
    Plot age group distribution
    
    Args:
        df: pandas.DataFrame
        color_theme: Color theme
    
    Returns:
        str: Base64 encoded image
    """
    age_totals = {
        '0-5 years': df['age_0_5'].sum(),
        '5-17 years': df['age_5_17'].sum(),
        '18+ years': df['age_18_greater'].sum()
    }
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Bar chart
    colors = [COLOR_PALETTE['primary'], COLOR_PALETTE['accent'], COLOR_PALETTE['secondary']]
    ax1.bar(age_totals.keys(), age_totals.values(), color=colors, alpha=0.8)
    ax1.set_ylabel('Total Enrolments', fontsize=12, fontweight='bold')
    ax1.set_title('Enrolments by Age Group', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Pie chart
    ax2.pie(age_totals.values(), labels=age_totals.keys(), autopct='%1.1f%%',
            colors=colors, startangle=90)
    ax2.set_title('Age Group Percentage Distribution', fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    return fig_to_base64(fig)


def plot_top_pincodes(df, top_n=10, color_theme='default'):
    """
    Plot top pincodes by enrolment volume
    
    Args:
        df: pandas.DataFrame
        top_n: Number of top pincodes to show
        color_theme: Color theme
    
    Returns:
        str: Base64 encoded image
    """
    pincode_totals = df.groupby('pincode')['total_enrolments'].sum().reset_index()
    pincode_totals = pincode_totals.sort_values('total_enrolments', ascending=False).head(top_n)
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    bars = ax.barh(pincode_totals['pincode'].astype(str), 
                   pincode_totals['total_enrolments'],
                   color=COLOR_PALETTE['primary'], alpha=0.8)
    
    ax.set_xlabel('Total Enrolments', fontsize=12, fontweight='bold')
    ax.set_ylabel('Pincode', fontsize=12, fontweight='bold')
    ax.set_title(f'Top {top_n} Pincodes by Enrolment Volume', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='x')
    ax.invert_yaxis()
    
    return fig_to_base64(fig)


def plot_monthly_trend(df, color_theme='default'):
    """
    Plot monthly enrolment trends
    
    Args:
        df: pandas.DataFrame
        color_theme: Color theme
    
    Returns:
        str: Base64 encoded image
    """
    monthly = df.groupby(['year', 'month'])['total_enrolments'].sum().reset_index()
    monthly['period'] = monthly['year'].astype(str) + '-' + monthly['month'].astype(str).str.zfill(2)
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    ax.bar(monthly['period'], monthly['total_enrolments'], 
           color=COLOR_PALETTE['accent'], alpha=0.8)
    
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Enrolments', fontsize=12, fontweight='bold')
    ax.set_title('Monthly Enrolment Trends', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45)
    
    return fig_to_base64(fig)


def plot_day_of_week_pattern(df, color_theme='default'):
    """
    Plot day-of-week enrolment patterns
    
    Args:
        df: pandas.DataFrame
        color_theme: Color theme
    
    Returns:
        str: Base64 encoded image
    """
    dow_pattern = df.groupby('day_of_week')['total_enrolments'].sum()
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_pattern = dow_pattern.reindex(dow_order, fill_value=0)
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    bars = ax.bar(range(len(dow_pattern)), dow_pattern.values, 
                  color=COLOR_PALETTE['primary'], alpha=0.8)
    
    ax.set_xticks(range(len(dow_pattern)))
    ax.set_xticklabels(dow_pattern.index, rotation=45)
    ax.set_ylabel('Total Enrolments', fontsize=12, fontweight='bold')
    ax.set_title('Enrolment Pattern by Day of Week', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    
    return fig_to_base64(fig)


def plot_anomalies(anomaly_data, color_theme='default'):
    """
    Plot anomaly detection results
    
    Args:
        anomaly_data: dict with anomaly detection results
        color_theme: Color theme
    
    Returns:
        str: Base64 encoded image
    """
    zscore_data = pd.DataFrame(anomaly_data['zscore_analysis']['all_days'])
    if zscore_data.empty:
        # Return empty/placeholder chart
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
        return fig_to_base64(fig)
    
    zscore_data['date'] = pd.to_datetime(zscore_data['date'])
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    
    # Plot all points
    ax.scatter(zscore_data['date'], zscore_data['total_enrolments'], 
               c='lightblue', alpha=0.6, s=50, label='Normal')
    
    # Highlight anomalies
    anomalies = zscore_data[zscore_data['is_anomaly']]
    if not anomalies.empty:
        ax.scatter(anomalies['date'], anomalies['total_enrolments'],
                   c='red', alpha=0.8, s=100, marker='X', label='Anomaly')
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Enrolments', fontsize=12, fontweight='bold')
    ax.set_title('Anomaly Detection - Daily Enrolments', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.xticks(rotation=45)
    
    return fig_to_base64(fig)


def plot_age_over_time(df, color_theme='default'):
    """
    Plot stacked area chart of age groups over time
    
    Args:
        df: pandas.DataFrame
        color_theme: Color theme
    
    Returns:
        str: Base64 encoded image
    """
    daily_age = df.groupby('date')[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    
    ax.fill_between(daily_age['date'], 0, daily_age['age_0_5'], 
                     label='0-5 years', color=COLOR_PALETTE['primary'], alpha=0.7)
    ax.fill_between(daily_age['date'], daily_age['age_0_5'], 
                     daily_age['age_0_5'] + daily_age['age_5_17'],
                     label='5-17 years', color=COLOR_PALETTE['accent'], alpha=0.7)
    ax.fill_between(daily_age['date'], 
                     daily_age['age_0_5'] + daily_age['age_5_17'],
                     daily_age['age_0_5'] + daily_age['age_5_17'] + daily_age['age_18_greater'],
                     label='18+ years', color=COLOR_PALETTE['secondary'], alpha=0.7)
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Enrolments', fontsize=12, fontweight='bold')
    ax.set_title('Age Group Distribution Over Time', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    return fig_to_base64(fig)


def generate_all_visualizations(df, anomaly_data=None, color_theme='default'):
    """
    Generate all visualizations for the dashboard
    
    Args:
        df: pandas.DataFrame (preprocessed)
        anomaly_data: Anomaly detection results
        color_theme: Color theme
    
    Returns:
        dict: All visualizations as base64 strings
    """
    visualizations = {
        'daily_enrolments': plot_daily_enrolments(df, color_theme),
        'age_distribution': plot_age_distribution(df, color_theme),
        'top_pincodes': plot_top_pincodes(df, top_n=10, color_theme=color_theme),
        'monthly_trend': plot_monthly_trend(df, color_theme),
        'day_of_week': plot_day_of_week_pattern(df, color_theme),
        'age_over_time': plot_age_over_time(df, color_theme)
    }
    
    if anomaly_data:
        visualizations['anomalies'] = plot_anomalies(anomaly_data, color_theme)
    
    return visualizations
