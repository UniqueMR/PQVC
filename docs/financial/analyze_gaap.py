import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from matplotlib.dates import DateFormatter, date2num
from datetime import timedelta, datetime

# Set style
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid")
sns.set_palette("husl")

# Get current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Create figures directory if it doesn't exist
figures_dir = os.path.join(current_dir, 'figures')
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)

def format_value(value):
    """Format large numbers with M/B suffix"""
    if value >= 1000:  # Convert to billions if > 1000 million
        return f'${value/1000:.1f}B', 'normal'
    return f'${value:.1f}M', 'small'

def generate_charts(df, prefix):
    """Generate all charts for a given dataset with specified prefix for filenames"""
    
    # Create a mapping of quarters to ensure proper order
    quarters = sorted(df['quarter'].unique())
    quarter_to_idx = {q: i for i, q in enumerate(quarters)}
    df['x_value'] = df['quarter'].map(quarter_to_idx)

    # Get data and calculate COGS
    x_values = range(len(quarters))
    revenue_data = df[df['metric'] == 'revenue'].sort_values('quarter')['value'].values
    gross_profit_data = df[df['metric'] == 'gross_profit'].sort_values('quarter')['value'].values
    cogs_data = revenue_data - gross_profit_data

    # Print diagnostic information
    print(f"\nDetailed Data Analysis ({prefix}):")
    print("Quarter | Revenue | Gross Profit | COGS | Total Height Check")
    print("-" * 80)
    for i, quarter in enumerate(quarters):
        rev = revenue_data[i]
        gp = gross_profit_data[i]
        cogs = cogs_data[i]
        total_height = cogs + gp
        print(f"{quarter} | {rev:.1f} | {gp:.1f} | {cogs:.1f} | {total_height:.1f} (should equal {rev:.1f})")

    # 1. Revenue Composition (Stacked Bar)
    plt.figure(figsize=(12, 6))
    
    # Set y-axis limits with padding for full revenue height
    y_max = revenue_data.max()
    y_min = 0  # Start from 0 to show full bar height
    y_padding = y_max * 0.1  # Add 10% padding
    plt.ylim(y_min, y_max + y_padding)

    # Create stacked bars
    bar_width = 0.4
    bottom_bars = plt.bar(x_values, cogs_data, width=bar_width, label='Cost of Goods Sold', color='#a9cce3')  # Light blue
    top_bars = plt.bar(x_values, gross_profit_data, width=bar_width, bottom=cogs_data, label='Gross Profit', color='#2980b9')  # Saturated blue

    plt.title(f'AMD Revenue Composition ({prefix})', fontsize=14, pad=20)
    plt.xlabel('Quarter', fontsize=12)
    plt.ylabel('Amount (Million USD)', fontsize=12)

    # Format x-axis
    plt.xticks(x_values, quarters, rotation=45)

    # Add value labels
    for i in x_values:
        # Total revenue label at top
        total = revenue_data[i]
        value_str, size = format_value(total)
        plt.text(i, total, value_str, 
                 ha='center', va='bottom', 
                 fontsize=12 if size == 'normal' else 9)
        
        # COGS label in middle of bottom section
        cogs = cogs_data[i]
        value_str, size = format_value(cogs)
        plt.text(i, cogs/2, value_str, 
                 ha='center', va='center', color='white',
                 fontsize=12 if size == 'normal' else 9)
        
        # Gross profit label in middle of top section
        gp = gross_profit_data[i]
        value_str, size = format_value(gp)
        plt.text(i, cogs + gp/2, value_str, 
                 ha='center', va='center', color='white',
                 fontsize=12 if size == 'normal' else 9)

    plt.legend(fontsize=10, loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, f'{prefix}_revenue_composition.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Operating Income vs Expenses (Stacked Bar)
    plt.figure(figsize=(12, 6))

    # Get data
    operating_expenses = df[df['metric'] == 'operating_expenses'].sort_values('quarter')['value'].values
    operating_income = df[df['metric'] == 'operating_income'].sort_values('quarter')['value'].values

    # Calculate the height threshold for text placement (e.g., 200M)
    height_threshold = 200

    # Create stacked bars
    plt.bar(x_values, operating_expenses, width=bar_width, label='Operating Expenses', color='#d2b4de')  # Light purple
    plt.bar(x_values, operating_income, width=bar_width, bottom=operating_expenses, label='Operating Income', color='#8e44ad')  # Saturated purple

    plt.title(f'AMD Operating Performance ({prefix})', fontsize=14, pad=20)
    plt.xlabel('Quarter', fontsize=12)
    plt.ylabel('Amount (Million USD)', fontsize=12)

    # Format x-axis
    plt.xticks(x_values, quarters, rotation=45)

    # Add value labels
    for i in x_values:
        # Total label at top
        total = operating_expenses[i] + operating_income[i]
        value_str, size = format_value(total)
        plt.text(i, total, value_str, 
                 ha='center', va='bottom', 
                 fontsize=12 if size == 'normal' else 9)
        
        # Operating expenses label
        oe = operating_expenses[i]
        value_str, size = format_value(oe)
        if oe < height_threshold:  # If bar is too small, place text to the right
            plt.text(i + bar_width/2 + 0.1, oe/2, value_str, 
                    ha='left', va='center', color='black',
                    fontsize=12 if size == 'normal' else 9)
        else:  # Otherwise, place text inside bar
            plt.text(i, oe/2, value_str, 
                    ha='center', va='center', color='white',
                    fontsize=12 if size == 'normal' else 9)
        
        # Operating income label
        oi = operating_income[i]
        value_str, size = format_value(oi)
        if oi < height_threshold:  # If bar is too small, place text to the right
            plt.text(i + bar_width/2 + 0.1, oe + oi/2, value_str, 
                    ha='left', va='center', color='black',
                    fontsize=12 if size == 'normal' else 9)
        else:  # Otherwise, place text inside bar
            plt.text(i, oe + oi/2, value_str, 
                    ha='center', va='center', color='white',
                    fontsize=12 if size == 'normal' else 9)

    plt.legend(fontsize=10, loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, f'{prefix}_operating_performance.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Generate individual metric charts
    metrics_config = [
        ('revenue', 'AMD Quarterly Revenue', 'Revenue (Million USD)', '#3498db'),
        ('operating_expenses', 'AMD Operating Expenses', 'Operating Expenses (Million USD)', '#f39c12'),
        ('net_income', 'AMD Net Income', 'Net Income (Million USD)', '#2980b9'),
        ('gross_margin', 'AMD Gross Margin', 'Gross Margin (%)', '#f39c12'),
        ('operating_margin', 'AMD Operating Margin', 'Operating Margin (%)', '#e67e22'),
        ('earnings_per_share', 'AMD Earnings Per Share', 'EPS (USD)', '#2980b9')
    ]

    for metric, title, ylabel, color in metrics_config:
        plt.figure(figsize=(12, 6))
        metric_data = df[df['metric'] == metric].sort_values('quarter')
        
        # Handle percentage values
        if 'margin' in metric:
            y_values = metric_data['value'] * 100
            value_format = lambda x: f'{x:.1f}%'
        elif metric == 'earnings_per_share':
            y_values = metric_data['value']
            value_format = lambda x: f'${x:.2f}'
        else:
            y_values = metric_data['value']
            value_format = format_value
            
        plt.plot(metric_data['quarter'], y_values, marker='o', linewidth=2, color=color)
        plt.title(f'{title} ({prefix})', fontsize=14, pad=20)
        plt.xlabel('Quarter', fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        
        # Format x-axis
        plt.xticks(metric_data['quarter'], rotation=45)
        
        # Add value labels
        for x, y in zip(metric_data['quarter'], y_values):
            plt.annotate(value_format(y), (x, y), textcoords="offset points", xytext=(0,10), ha='center')
            
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, f'{prefix}_{metric}.png'), dpi=300, bbox_inches='tight')
        plt.close()

# Read and process GAAP data
gaap_df = pd.read_csv(os.path.join(current_dir, 'dataset', 'finan_sum_gaap.csv'))
generate_charts(gaap_df, 'gaap')

# Read and process non-GAAP data
nongaap_df = pd.read_csv(os.path.join(current_dir, 'dataset', 'finan_sum_nongaap.csv'))
generate_charts(nongaap_df, 'nongaap')

print("\nAll charts have been generated and saved in the figures folder.") 