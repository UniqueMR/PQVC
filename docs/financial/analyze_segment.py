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

def format_value(value):
    """Format large numbers with M/B suffix"""
    if value >= 1000:  # Convert to billions if > 1000 million
        return f'${value/1000:.1f}B', 'normal'
    return f'${value:.1f}M', 'small'

# Read segment data
df = pd.read_csv(os.path.join(current_dir, 'dataset', 'finan_sum_segment.csv'))

# Sort quarters
quarters = sorted(df['quarter'].unique())
x_values = range(len(quarters))

# Define colors
revenue_colors = {
    'data_center': '#d35400',    # Most saturated orange
    'client': '#e67e22',         # Saturated orange
    'gaming': '#f39c12',         # Light orange
    'embedded': '#f5b041'        # Lightest orange
}

operating_colors = {
    'data_center': '#d35400',    # Most saturated orange
    'client': '#e67e22',         # Saturated orange
    'gaming': '#f39c12',         # Light orange
    'embedded': '#f5b041'        # Lightest orange
}

# Define colors for margins (more distinct colors)
margin_colors = {
    'data_center': '#d35400',    # Most saturated orange
    'client': '#e67e22',         # Saturated orange
    'gaming': '#f39c12',         # Light orange
    'embedded': '#f5b041'        # Lightest orange
}

# Define marker styles for each segment
marker_styles = {
    'data_center': 'o',          # Circle
    'client': 's',               # Square
    'gaming': '^',               # Triangle
    'embedded': 'D'              # Diamond
}

# 1. Revenue Composition
plt.figure(figsize=(12, 7))
bottom = np.zeros(len(quarters))
segment_revenues = {}

for segment in ['data_center', 'client', 'gaming', 'embedded']:
    segment_data = []
    for quarter in quarters:
        value = df[(df['quarter'] == quarter) & 
                  (df['segment'] == segment) & 
                  (df['metric'] == 'revenue')]['value'].iloc[0]
        segment_data.append(value)
    segment_revenues[segment] = segment_data
    
    plt.bar(x_values, segment_data, bottom=bottom, label=segment.replace('_', ' ').title(),
            color=revenue_colors[segment], width=0.4)
    
    # Add value labels
    for i, value in enumerate(segment_data):
        value_str, size = format_value(value)
        y_pos = bottom[i] + value/2
        plt.text(i, y_pos, value_str,
                ha='center', va='center',
                color='white', fontsize=9)
        bottom[i] += value

# Add total labels
for i in range(len(quarters)):
    total = sum(segment_revenues[segment][i] for segment in revenue_colors.keys())
    value_str, _ = format_value(total)
    plt.text(i, total, value_str,
             ha='center', va='bottom',
             color='black', fontsize=12)

plt.title('AMD Revenue by Segment', fontsize=14, pad=20)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Revenue (Million USD)', fontsize=12)
plt.xticks(x_values, quarters, rotation=45)
plt.legend(fontsize=10, loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'segment_revenue.png'), dpi=300, bbox_inches='tight')
plt.close()

# 2. Operating Income Composition
plt.figure(figsize=(12, 7))
bottom = np.zeros(len(quarters))

for segment in ['data_center', 'client', 'gaming', 'embedded']:
    segment_data = []
    for quarter in quarters:
        value = df[(df['quarter'] == quarter) & 
                  (df['segment'] == segment) & 
                  (df['metric'] == 'operating_income')]['value'].iloc[0]
        segment_data.append(value)
    
    plt.bar(x_values, segment_data, bottom=bottom, label=segment.replace('_', ' ').title(),
            color=operating_colors[segment], width=0.4)
    
    # Add value labels
    for i, value in enumerate(segment_data):
        value_str, size = format_value(value)
        y_pos = bottom[i] + value/2
        if value < 200:  # Small values outside
            plt.text(i + 0.2, y_pos, value_str,
                    ha='left', va='center',
                    color='black', fontsize=9)
        else:  # Larger values inside
            plt.text(i, y_pos, value_str,
                    ha='center', va='center',
                    color='white', fontsize=9)
        bottom[i] += value

# Add total labels
for i in range(len(quarters)):
    total = bottom[i]
    value_str, _ = format_value(total)
    plt.text(i, total, value_str,
             ha='center', va='bottom',
             color='black', fontsize=12)

plt.title('AMD Operating Income by Segment', fontsize=14, pad=20)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Operating Income (Million USD)', fontsize=12)
plt.xticks(x_values, quarters, rotation=45)
plt.legend(fontsize=10, loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'segment_operating_income.png'), dpi=300, bbox_inches='tight')
plt.close()

# 3. Operating Margins
plt.figure(figsize=(12, 7))

segment_margins = {}
for segment in ['data_center', 'client', 'gaming', 'embedded']:
    margins = []
    for quarter in quarters:
        rev = df[(df['quarter'] == quarter) & 
                (df['segment'] == segment) & 
                (df['metric'] == 'revenue')]['value'].iloc[0]
        op_inc = df[(df['quarter'] == quarter) & 
                   (df['segment'] == segment) & 
                   (df['metric'] == 'operating_income')]['value'].iloc[0]
        margin = (op_inc / rev * 100) if rev != 0 else 0
        margins.append(margin)
    
    segment_margins[segment] = margins
    line = plt.plot(x_values, margins, 
                   marker=marker_styles[segment],     # Different marker for each segment
                   markersize=8,                      # Slightly larger markers
                   linewidth=2,
                   label=segment.replace('_', ' ').title(),
                   color=margin_colors[segment])
    
    # Add percentage labels for each point
    for i, margin in enumerate(margins):
        # Alternate label positions above/below for better readability
        if segment in ['data_center', 'gaming']:
            y_offset = 1.5  # Reduced offset due to smaller scale
            va = 'bottom'
        else:
            y_offset = -1.5  # Reduced offset due to smaller scale
            va = 'top'
        
        plt.text(i, margin + y_offset, f'{margin:.1f}%',
                ha='center', va=va,
                color=margin_colors[segment],
                fontsize=9)  # Slightly larger font

plt.title('AMD Operating Margin by Segment', fontsize=14, pad=20)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Operating Margin (%)', fontsize=12)
plt.xticks(x_values, quarters, rotation=45)
plt.legend(fontsize=10, loc='upper right')  # Moved legend to upper right for better visibility
plt.grid(True, alpha=0.3)
plt.ylim(0, 60)  # Changed y-axis limit to 60%

plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'segment_margins.png'), dpi=300, bbox_inches='tight')
plt.close()

print("Segment analysis charts have been generated and saved in the figures folder.") 