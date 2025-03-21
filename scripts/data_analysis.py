import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import ast
import missingno as msno
import plotly.express as px


# Load the free apps dataset
file_path = r"/Users/basak/Documents/VS Code/EdTech/EdTech/data/raw/PlayStore/unique_apps_playstore_free.csv"

df = pd.read_csv(file_path)


# Display the first few rows
print(df.head())

print(df.columns)

# Check the number of rows
print("Number of rows:", len(df))

# Check for missing values
print("Missing values per column:")
print(df.isnull().sum())

# Convert date columns to datetime format
df['earliest_date'] = pd.to_datetime(df['earliest_date'], errors='coerce')
df['latest_date'] = pd.to_datetime(df['latest_date'], errors='coerce')

print("Earliest Date range:", df['earliest_date'].min(), "-", df['earliest_date'].max())
print("Latest Date range:", df['latest_date'].min(), "-", df['latest_date'].max())



def parse_title(data_str):
    try:
        # Convert the string to a dictionary
        data_dict = ast.literal_eval(data_str)
        # Extract the title from the dictionary
        return data_dict.get('title')
    except Exception as e:
        # If evaluation fails, return None
        return None

# Apply the function to your DataFrame
df['title'] = df['data'].apply(parse_title)


# List all columns except 'title'
cols_to_include = [col for col in df.columns if col != 'title']

# Total number of rows in the DataFrame
total_rows = len(df)

# Calculate missing counts and percentages for the selected columns
missing_counts = df[cols_to_include].isnull().sum()
missing_percentages = (missing_counts / total_rows) * 100

# Create the summary DataFrame automatically
missing_summary = pd.DataFrame({
    'Missing Count': missing_counts,
    'Missing Percentage': missing_percentages
}).reset_index().rename(columns={'index': 'Column'})

print("Missing Data Summary:")
print(missing_summary)

# Create an interactive bar chart with Plotly Express
fig = px.bar(
    missing_summary,
    x='Column',
    y='Missing Percentage',
    text='Missing Percentage',
    title='Missing Data Percentage per Column (Excluding Title)',
    labels={'Missing Percentage': 'Missing Percentage (%)'}
)

# Format text to show 2 decimal places and position it outside the bars
fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig.update_layout(
    yaxis_title="Missing Percentage (%)",
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

fig.show()
