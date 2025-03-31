import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
df = pd.read_csv('cpu_benchmark.csv')

# Define brand colors with appropriate saturation (more muted, academic style)
brand_colors = {
    'AMD': '#E69F00',  # Muted orange
    'INTEL': '#56B4E9',  # Light blue
    'APPLE': '#999999',  # Gray
    'Qualcomm': '#D55E00'  # Muted red
}

# Create the figure and axis
plt.figure(figsize=(15, 8))

# Create bars with reduced width
bars = plt.bar(range(len(df)), df['cpu mark'], width=0.6)  # Reduced width from default 0.8 to 0.6

# Create legend handles
legend_elements = [plt.Rectangle((0,0),1,1, facecolor=color, label=brand) 
                  for brand, color in brand_colors.items()]

# Customize the bars with brand colors
for i, bar in enumerate(bars):
    brand = df['product'].iloc[i].strip()
    bar.set_color(brand_colors.get(brand, '#CCCCCC'))  # Default to light gray if brand not found

# Customize the plot
plt.title('CPU Benchmark Scores by Processor', pad=20)
plt.xlabel('Processor')
plt.ylabel('CPU Mark Score')
plt.xticks(range(len(df)), df['type '], rotation=45, ha='right')  # Note the space after 'type'
plt.grid(True, axis='y', linestyle='--', alpha=0.3)  # Reduced grid opacity

# Add rank labels on top of each bar
for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'Rank: {df["rank"].iloc[i]}',
             ha='center', va='bottom')

# Add legend
plt.legend(handles=legend_elements, loc='upper right', title='Manufacturer')

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the plot
plt.savefig('cpu_benchmark.png', dpi=300, bbox_inches='tight')
plt.close() 