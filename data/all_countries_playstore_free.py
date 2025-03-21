import pandas as pd
import os
import ast
import plotly.express as px
import plotly.graph_objects as go


#Number of countries: 12
#Countries: ['us' 'gb' 'be' 'ch' 'de' 'dk' 'es' 'fr' 'it' 'jp' 'no' 'pl']

def explore_file(file_path):
    print(f"\n📂 Exploring file: {os.path.basename(file_path)}")

    # Load the file
    df = pd.read_csv(file_path)

    # Convert to datetime if columns exist
    if 'earliest_date' in df.columns:
        df['earliest_date'] = pd.to_datetime(df['earliest_date'], errors='coerce')
    if 'latest_date' in df.columns:
        df['latest_date'] = pd.to_datetime(df['latest_date'], errors='coerce')

    # Parse 'title' from 'data' column if it exists
    if 'data' in df.columns:
        def parse_title(data_str):
            try:
                return ast.literal_eval(data_str).get('title')
            except Exception:
                return None
        df['title'] = df['data'].apply(parse_title)

    # Display basic info
    print("🔸 Columns:", df.columns.tolist())
    print("🔸 Number of rows:", len(df))
    
    print("\n🔸 Missing values per column:")
    print(df.isnull().sum())

    if 'earliest_date' in df.columns:
        print("\n📅 Earliest date range:", df['earliest_date'].min(), "→", df['earliest_date'].max())
    if 'latest_date' in df.columns:
        print("📅 Latest date range:", df['latest_date'].min(), "→", df['latest_date'].max())

    return df

# Directory containing your raw CSV files
data_dir = r"/Users/basak/Documents/VS Code/EdTech/EdTech/data/raw/PlayStore"

# List all CSV files
files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]

# Display the list
print("Available CSV files:")
for i, file in enumerate(files):
    print(f"{i}: {file}")

# Let user choose
choice = int(input("Enter the number of the file you want to explore: "))
selected_file = os.path.join(data_dir, files[choice])

# Run the explorer
df = explore_file(selected_file)

print("Number of countries:", df['country'].nunique())
print("Countries:", df['country'].unique())

print(df.head())

# Filter the DataFrame for the specific app_id
duolingo_df = df[df['app_id'] == 'com.duolingo']

# Show the result
print(duolingo_df)

print(df['rank'].unique())

# Make sure 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Filter for US on 2017-01-01
filtered = df[(df['country'] == 'us') & (df['date'] == '2017-01-01')]

# Display the result
print(filtered)

# Group by country and date, then count number of rows (apps) per group
grouped = df.groupby(['country', 'date']).size().reset_index(name='app_count')

# Look for groups where app_count is less than 200
missing_data = grouped[grouped['app_count'] < 200]

print("🚨 Days with fewer than 200 apps:")
print(missing_data.sort_values(['country', 'date']))

total_days = len(grouped)
full_days = (grouped['app_count'] == 200).sum()
missing_days = total_days - full_days

print(f"✅ Days with full 200 apps: {full_days} / {total_days}")
print(f"❌ Missing or incomplete days: {missing_days}")

missing_summary = missing_data.groupby('country').size().sort_values(ascending=False)
print("❗ Countries with most missing days:")
print(missing_summary)


# ------------------------------------------------------------------------
# NEW SECTION: Top 3 Apps per Country per Year (Based on #1 Rank Days)
# ------------------------------------------------------------------------
print("\n📊 Top 3 Apps per Country per Year Based on Days at Rank #1")

file_path = r"/Users/basak/Documents/VS Code/EdTech/EdTech/data/processed/app_lookup.csv"

df_lookup = pd.read_csv(file_path)

df_top1 = df[df['rank'] == 1].copy()
df_top1['year'] = df_top1['date'].dt.year
df_top1 = df_top1.drop_duplicates(subset=['country', 'date', 'app_id'])

# Count #1 rank days per app-country-year
rank_counts = (
    df_top1.groupby(['country', 'year', 'app_id'])
    .size()
    .reset_index(name='days_at_1')
)

# Rank within country-year
rank_counts['rank'] = (
    rank_counts
    .groupby(['country', 'year'])['days_at_1']
    .rank(method='first', ascending=False)
)

# Keep top 3
top3 = rank_counts[rank_counts['rank'] <= 3]

# Merge with lookup to get titles
top3 = top3.merge(df_lookup, on='app_id', how='left')

# Use title for labels
top3['label'] = top3['title'].fillna(top3['app_id'])

# Country flag labels
flag_map = {
    'us': '🇺🇸 US', 'gb': '🇬🇧 GB', 'be': '🇧🇪 BE', 'ch': '🇨🇭 CH', 'de': '🇩🇪 DE',
    'dk': '🇩🇰 DK', 'es': '🇪🇸 ES', 'fr': '🇫🇷 FR', 'it': '🇮🇹 IT', 'jp': '🇯🇵 JP',
    'no': '🇳🇴 NO', 'pl': '🇵🇱 PL'
}
top3['country_flag'] = top3['country'].map(flag_map)

# Assign colors per app title
unique_apps = top3['label'].unique()
color_palette = px.colors.qualitative.Set3
color_map = {app: color_palette[i % len(color_palette)] for i, app in enumerate(unique_apps)}

# Sort years
years = sorted(top3['year'].unique())
countries = sorted(top3['country_flag'].unique())

# Build figure
fig = go.Figure()

# Add traces for each year-app combo
for year in years:
    df_year = top3[top3['year'] == year]
    for app in df_year['label'].unique():
        df_app = df_year[df_year['label'] == app]
        fig.add_trace(go.Bar(
            x=df_app['country_flag'],
            y=df_app['days_at_1'],
            name=app,
            marker_color=color_map[app],
            visible=(year == years[0]),
            customdata=df_app['label'],
            hovertemplate="Country: %{x}<br>App: %{customdata}<br>Days at #1: %{y}<extra></extra>"
        ))

# Create slider steps
traces_per_year = len(fig.data) // len(years)
steps = []
for i, year in enumerate(years):
    visibility = [False] * len(fig.data)
    for j in range(traces_per_year):
        visibility[i * traces_per_year + j] = True
    step = dict(
        method="update",
        args=[{"visible": visibility},
              {"title": f"Top 3 Apps per Country in {year} (Days at #1)"}],
        label=str(year)
    )
    steps.append(step)

# Slider control
sliders = [dict(
    active=0,
    currentvalue={"prefix": "Year: "},
    pad={"t": 50},
    steps=steps
)]

# Layout
fig.update_layout(
    sliders=sliders,
    barmode='group',
    title=f"Top 3 Apps per Country in {years[0]} (Days at #1)",
    xaxis_title="Country",
    yaxis_title="Days at Rank #1",
    height=650,
    width=1200,
    legend_title="Applications",
    bargap=0.05,
    bargroupgap=0.02
)

fig.show()

output_path = r"/Users/basak/Documents/VS Code/EdTech/EdTech/graphs/top_apps_by_country_slider.html"

fig.write_html(output_path)

