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
        return f'${value/1000:.1f}B'
    return f'${value:.1f}M'

# Read data from dataset subfolder
df = pd.read_csv(os.path.join(current_dir, 'dataset', 'finan_sum_gaap.csv'))

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
print("\nDetailed Data Analysis:")
print("Quarter | Revenue | Gross Profit | COGS | Total Height Check")
print("-" * 80)
for i, quarter in enumerate(quarters):
    rev = revenue_data[i]
    gp = gross_profit_data[i]
    cogs = cogs_data[i]
    total_height = cogs + gp
    print(f"{quarter} | {rev:.1f} | {gp:.1f} | {cogs:.1f} | {total_height:.1f} (should equal {rev:.1f})")

# Create the figure
plt.figure(figsize=(12, 6))

# Set y-axis limits with padding for full revenue height
y_max = revenue_data.max()
y_min = 0  # Start from 0 to show full bar height
y_padding = y_max * 0.1  # Add 10% padding
plt.ylim(y_min, y_max + y_padding)

# Create stacked bars
bar_width = 0.4
bottom_bars = plt.bar(x_values, cogs_data, width=bar_width, label='Cost of Goods Sold', color='#f39c12')
top_bars = plt.bar(x_values, gross_profit_data, width=bar_width, bottom=cogs_data, label='Gross Profit', color='#3498db')

plt.title('AMD Revenue Composition', fontsize=14, pad=20)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Amount (Million USD)', fontsize=12)

# Format x-axis
plt.xticks(x_values, quarters, rotation=45)

# Add value labels
for i in x_values:
    # Total revenue label at top
    total = revenue_data[i]
    plt.text(i, total, format_value(total), 
             ha='center', va='bottom')
    
    # COGS label in middle of bottom section
    cogs = cogs_data[i]
    plt.text(i, cogs/2, format_value(cogs), 
             ha='center', va='center', color='white')
    
    # Gross profit label in middle of top section
    gp = gross_profit_data[i]
    plt.text(i, cogs + gp/2, format_value(gp), 
             ha='center', va='center', color='white')

plt.legend(fontsize=10, loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'revenue_composition.png'), dpi=300, bbox_inches='tight')
plt.close()

# 2. Operating Income vs Expenses (Stacked Bar)
plt.figure(figsize=(12, 6))

# Get data
operating_expenses = df[df['metric'] == 'operating_expenses'].set_index('quarter')['value']
operating_income = df[df['metric'] == 'operating_income'].set_index('quarter')['value']

# Create stacked bars
plt.bar(quarters, operating_expenses, width=bar_width, label='Operating Expenses', color='#e67e22')
plt.bar(quarters, operating_income, width=bar_width, bottom=operating_expenses, label='Operating Income', color='#2980b9')

plt.title('AMD Operating Performance', fontsize=14, pad=20)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Amount (Million USD)', fontsize=12)

# Format x-axis
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y Q%q'))
plt.xticks(quarters, rotation=45)

# Add value labels
for quarter in quarters:
    # Total label at top
    total = operating_expenses[quarter] + operating_income[quarter]
    plt.text(quarter, total, format_value(total), 
             ha='center', va='bottom')
    
    # Operating expenses label in middle
    oe = operating_expenses[quarter]
    plt.text(quarter, oe/2, format_value(oe), 
             ha='center', va='center', color='white')
    
    # Operating income label in middle
    oi = operating_income[quarter]
    plt.text(quarter, oe + oi/2, format_value(oi), 
             ha='center', va='center', color='white')

plt.legend(fontsize=10, loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'operating_performance.png'), dpi=300, bbox_inches='tight')
plt.close()

# 1. Revenue Trend
plt.figure(figsize=(12, 6))
revenue_data = df[df['metric'] == 'revenue'].sort_values('quarter')
plt.plot(revenue_data['quarter'], revenue_data['value'], marker='o', linewidth=2, color='#3498db')
plt.title('AMD Quarterly Revenue', fontsize=14, pad=20)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Revenue (Million USD)', fontsize=12)

# Format x-axis
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y Q%q'))
plt.xticks(revenue_data['quarter'], rotation=45)

# Set y-axis limits with padding
y_max = revenue_data['value'].max()
y_min = revenue_data['value'].min()
y_padding = (y_max - y_min) * 0.1  # Add 10% padding
plt.ylim(y_min - y_padding, y_max + y_padding)

# Add value labels
for x, y in zip(revenue_data['quarter'], revenue_data['value']):
    plt.annotate(format_value(y), (x, y), textcoords="offset points", xytext=(0,10), ha='center')

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'revenue.png'), dpi=300, bbox_inches='tight')
plt.close()

# 2. Operating Expenses
plt.figure(figsize=(12, 6))
expense_data = df[df['metric'] == 'operating_expenses'].sort_values('quarter')
plt.plot(expense_data['quarter'], expense_data['value'], marker='o', linewidth=2, color='#f39c12')
plt.title('AMD Operating Expenses', fontsize=14, pad=20)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Operating Expenses (Million USD)', fontsize=12)

# Format x-axis
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y Q%q'))
plt.xticks(expense_data['quarter'], rotation=45)

# Add value labels
for x, y in zip(expense_data['quarter'], expense_data['value']):
    plt.annotate(format_value(y), (x, y), textcoords="offset points", xytext=(0,10), ha='center')

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'operating_expenses.png'), dpi=300, bbox_inches='tight')
plt.close()

# 3. Net Income
plt.figure(figsize=(12, 6))
income_data = df[df['metric'] == 'net_income'].sort_values('quarter')
plt.plot(income_data['quarter'], income_data['value'], marker='o', linewidth=2, color='#2980b9')
plt.title('AMD Net Income', fontsize=14, pad=20)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Net Income (Million USD)', fontsize=12)

# Format x-axis
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y Q%q'))
plt.xticks(income_data['quarter'], rotation=45)

# Add value labels
for x, y in zip(income_data['quarter'], income_data['value']):
    plt.annotate(format_value(y), (x, y), textcoords="offset points", xytext=(0,10), ha='center')

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'net_income.png'), dpi=300, bbox_inches='tight')
plt.close()

# 4. Gross Profit (absolute value)
plt.figure(figsize=(12, 6))
revenue_data = df[df['metric'] == 'revenue'].set_index('quarter')['value']
expenses_data = df[df['metric'] == 'operating_expenses'].set_index('quarter')['value']
gross_profit = revenue_data - expenses_data

plt.plot(revenue_data.index, gross_profit, marker='o', linewidth=2, color='#3498db')
plt.title('AMD Gross Profit', fontsize=14, pad=20)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Gross Profit (Million USD)', fontsize=12)

# Format x-axis
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y Q%q'))
plt.xticks(revenue_data.index, rotation=45)

# Add value labels
for x, y in zip(revenue_data.index, gross_profit):
    plt.annotate(format_value(y), (x, y), textcoords="offset points", xytext=(0,10), ha='center')

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'gross_profit.png'), dpi=300, bbox_inches='tight')
plt.close()

# 5. Gross Margin
plt.figure(figsize=(12, 6))
margin_data = df[df['metric'] == 'gross_margin'].sort_values('quarter')
plt.plot(margin_data['quarter'], margin_data['value'] * 100, marker='o', linewidth=2, color='#f39c12')
plt.title('AMD Gross Margin', fontsize=14, pad=20)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Gross Margin (%)', fontsize=12)

# Format x-axis
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y Q%q'))
plt.xticks(margin_data['quarter'], rotation=45)

# Add value labels
for x, y in zip(margin_data['quarter'], margin_data['value']):
    plt.annotate(f'{y*100:.1f}%', (x, y*100), textcoords="offset points", xytext=(0,10), ha='center')

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'gross_margin.png'), dpi=300, bbox_inches='tight')
plt.close()

# 6. Operating Margin
plt.figure(figsize=(12, 6))
op_margin_data = df[df['metric'] == 'operating_margin'].sort_values('quarter')
plt.plot(op_margin_data['quarter'], op_margin_data['value'] * 100, marker='o', linewidth=2, color='#e67e22')
plt.title('AMD Operating Margin', fontsize=14, pad=20)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Operating Margin (%)', fontsize=12)

# Format x-axis
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y Q%q'))
plt.xticks(op_margin_data['quarter'], rotation=45)

# Add value labels
for x, y in zip(op_margin_data['quarter'], op_margin_data['value']):
    plt.annotate(f'{y*100:.1f}%', (x, y*100), textcoords="offset points", xytext=(0,10), ha='center')

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'operating_margin.png'), dpi=300, bbox_inches='tight')
plt.close()

# 7. EPS Trend
plt.figure(figsize=(12, 6))
eps_data = df[df['metric'] == 'earnings_per_share'].sort_values('quarter')
plt.plot(eps_data['quarter'], eps_data['value'], marker='o', linewidth=2, color='#2980b9')
plt.title('AMD Earnings Per Share', fontsize=14, pad=20)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('EPS (USD)', fontsize=12)

# Format x-axis
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y Q%q'))
plt.xticks(eps_data['quarter'], rotation=45)

# Add value labels
for x, y in zip(eps_data['quarter'], eps_data['value']):
    plt.annotate(f'${y:.2f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'eps.png'), dpi=300, bbox_inches='tight')
plt.close()

print("All charts have been generated and saved in the figures folder.") 