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
    fig, ax1 = plt.subplots(figsize=(12, 7))  # Increased height
    
    # Set y-axis limits with padding for full revenue height
    y_max = revenue_data.max()
    y_min = 0  # Start from 0 to show full bar height
    y_padding = y_max * 0.2  # Increase padding to 20% to fit all labels
    ax1.set_ylim(y_min, y_max + y_padding)

    # Create stacked bars
    bar_width = 0.4
    bottom_bars = ax1.bar(x_values, cogs_data, width=bar_width, label='Cost of Goods Sold', color='#a9cce3')  # Light blue
    top_bars = ax1.bar(x_values, gross_profit_data, width=bar_width, bottom=cogs_data, label='Gross Profit', color='#2980b9')  # Saturated blue

    ax1.set_title(f'AMD Revenue Composition ({prefix})', fontsize=14, pad=20)
    ax1.set_xlabel('Quarter', fontsize=12)
    ax1.set_ylabel('Amount (Million USD)', fontsize=12)

    # Format x-axis
    ax1.set_xticks(x_values)
    ax1.set_xticklabels(quarters, rotation=45)

    # Add value labels
    for i in x_values:
        # Total revenue label at top
        total = revenue_data[i]
        value_str, size = format_value(total)
        ax1.text(i, total, value_str, 
                 ha='center', va='bottom', 
                 fontsize=12 if size == 'normal' else 9)
        
        # COGS label in middle of bottom section
        cogs = cogs_data[i]
        value_str, size = format_value(cogs)
        ax1.text(i, cogs/2, value_str, 
                 ha='center', va='center', color='white',
                 fontsize=12 if size == 'normal' else 9)
        
        # Gross profit label in middle of top section
        gp = gross_profit_data[i]
        value_str, size = format_value(gp)
        ax1.text(i, cogs + gp/2, value_str, 
                 ha='center', va='center', color='white',
                 fontsize=12 if size == 'normal' else 9)

    # Add secondary y-axis for margin
    ax2 = ax1.twinx()
    margin_data = df[df['metric'] == 'gross_margin'].sort_values('quarter')['value'].values * 100
    ax2.plot(x_values, margin_data, color='#1a5f96', linestyle='--', marker='o', label='Gross Margin')  # Darkest blue
    ax2.set_ylabel('Margin (%)', fontsize=12)
    
    # Set fixed y-axis range for margin (0-100%)
    ax2.set_ylim(0, 100)

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=10, loc='upper left')

    ax1.grid(True, alpha=0.3)
    plt.subplots_adjust(bottom=0.15)  # Adjust bottom margin
    plt.savefig(os.path.join(figures_dir, f'{prefix}_revenue_composition.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Operating Income vs Expenses (Stacked Bar)
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Get data
    operating_expenses = df[df['metric'] == 'operating_expenses'].sort_values('quarter')['value'].values
    operating_income = df[df['metric'] == 'operating_income'].sort_values('quarter')['value'].values

    # Create stacked bars
    ax1.bar(x_values, operating_expenses, width=bar_width, label='Operating Expenses', color='#d2b4de')  # Light purple
    ax1.bar(x_values, operating_income, width=bar_width, bottom=operating_expenses, label='Operating Income', color='#8e44ad')  # Saturated purple

    # Set y-axis limits with padding
    y_max = (operating_expenses + operating_income).max()
    y_padding = y_max * 0.15
    ax1.set_ylim(0, y_max + y_padding)

    ax1.set_title(f'AMD Operating Performance ({prefix})', fontsize=14, pad=20)
    ax1.set_xlabel('Quarter', fontsize=12)
    ax1.set_ylabel('Amount (Million USD)', fontsize=12)

    # Format x-axis
    ax1.set_xticks(x_values)
    ax1.set_xticklabels(quarters, rotation=45)

    # Add value labels
    for i in x_values:
        # Total label at top
        total = operating_expenses[i] + operating_income[i]
        value_str, size = format_value(total)
        ax1.text(i, total, value_str, 
                 ha='center', va='bottom', 
                 fontsize=12 if size == 'normal' else 9)
        
        # Operating expenses label
        oe = operating_expenses[i]
        value_str, size = format_value(oe)
        ax1.text(i, oe/2, value_str, 
                ha='center', va='center', color='white',
                fontsize=12 if size == 'normal' else 9)
        
        # Operating income label
        oi = operating_income[i]
        value_str, size = format_value(oi)
        if oi < 1000:  # If less than 1B, place text to the right
            ax1.text(i + bar_width/2 + 0.05, oe + oi/2, value_str, 
                    ha='left', va='center', color='black',
                    fontsize=12 if size == 'normal' else 9)
        else:  # Otherwise, place text inside bar
            ax1.text(i, oe + oi/2, value_str, 
                    ha='center', va='center', color='white',
                    fontsize=12 if size == 'normal' else 9)

    # Add secondary y-axis for margins
    ax2 = ax1.twinx()
    
    # Plot operating margin
    op_margin_data = df[df['metric'] == 'operating_margin'].sort_values('quarter')['value'].values * 100
    line1 = ax2.plot(x_values, op_margin_data, color='#6c3483', linestyle='--', marker='o', label='Operating Margin')  # Darkest purple
    
    # Plot operating expense ratio
    expense_ratio_data = df[df['metric'] == 'operating_expense_revenue_ratio'].sort_values('quarter')['value'].values * 100
    line2 = ax2.plot(x_values, expense_ratio_data, color='#884ea0', linestyle='--', marker='s', label='OpEx/Revenue')  # Dark purple
    
    ax2.set_ylabel('Percentage (%)', fontsize=12)
    
    # Set fixed y-axis range for percentages (0-100%)
    ax2.set_ylim(0, 100)

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=10, loc='upper left')

    ax1.grid(True, alpha=0.3)
    plt.subplots_adjust(bottom=0.15)  # Adjust bottom margin
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
        
        # Remove value labels for line charts
            
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