import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid")

# Get current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Create figures directory if it doesn't exist
figures_dir = os.path.join(current_dir, 'figures')
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)

def format_value(value, is_eps=False):
    """Format numbers with appropriate suffix"""
    if is_eps:
        return f'${value:.2f}'
    if value >= 1000:
        return f'${value/1000:.1f}B'
    return f'${value:.0f}M'

def generate_profit_chart(df, prefix):
    """Generate profit metrics chart for given dataset"""
    # Sort quarters and prepare data
    quarters = sorted(df['quarter'].unique())
    x_values = np.arange(len(quarters))

    # Set up colors (using same color with different saturations)
    base_color = '#27ae60'  # Dark green for GAAP, Light green for non-GAAP
    colors = {
        'income': base_color,          # More saturated
        'eps': f'{base_color}80'       # Less saturated (adding alpha)
    }

    # Create figure with dual y-axes
    fig, ax1 = plt.subplots(figsize=(12, 7))
    ax2 = ax1.twinx()

    # Width of each bar
    bar_width = 0.35
    bar_positions = {
        'income': x_values - bar_width/2,
        'eps': x_values + bar_width/2
    }

    # Get sorted data
    income_data = df[df['metric'] == 'net_income'].sort_values('quarter')['value'].values
    eps_data = df[df['metric'] == 'earnings_per_share'].sort_values('quarter')['value'].values

    # Net Income bars (left y-axis)
    income_bars = ax1.bar(bar_positions['income'], income_data, 
                         bar_width, label='Net Income',
                         color=colors['income'])
    
    # Add value labels for income
    for i, value in enumerate(income_data):
        ax1.text(bar_positions['income'][i], value,
                format_value(value),
                ha='center', va='bottom',
                color=colors['income'],
                fontsize=9)
    
    # EPS bars (right y-axis)
    eps_bars = ax2.bar(bar_positions['eps'], eps_data,
                      bar_width, label='EPS',
                      color=colors['eps'])
    
    # Add value labels for EPS
    for i, value in enumerate(eps_data):
        ax2.text(bar_positions['eps'][i], value,
                format_value(value, True),
                ha='center', va='bottom',
                color=colors['eps'],
                fontsize=9)

    # Customize axes
    title_prefix = 'GAAP' if prefix == 'gaap' else 'Non-GAAP'
    ax1.set_title(f'AMD {title_prefix} Net Income and Earnings Per Share', fontsize=14, pad=20)
    ax1.set_xlabel('Quarter', fontsize=12)
    ax1.set_ylabel('Net Income (Million USD)', fontsize=12)
    ax2.set_ylabel('Earnings Per Share (USD)', fontsize=12)

    # Set x-ticks
    plt.xticks(x_values, quarters, rotation=45)

    # Add some padding to y-axes
    ax1.set_ylim(0, max(income_data) * 1.15)
    ax2.set_ylim(0, max(eps_data) * 1.15)

    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, 
              loc='upper left', fontsize=10)

    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, f'{prefix}_profit_metrics.png'), dpi=300, bbox_inches='tight')
    plt.close()

# Read data
gaap_df = pd.read_csv(os.path.join(current_dir, 'dataset', 'finan_sum_gaap.csv'))
nongaap_df = pd.read_csv(os.path.join(current_dir, 'dataset', 'finan_sum_nongaap.csv'))

# Generate charts for both datasets
generate_profit_chart(gaap_df, 'gaap')
generate_profit_chart(nongaap_df, 'nongaap')

print("Profit metrics charts have been generated and saved in the figures folder.") 