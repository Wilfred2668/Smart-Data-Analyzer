# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas",
#   "numpy",
#   "matplotlib",
#   "seaborn",
#   "requests",
# ]
# ///

import os
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests

# Ensure AIPROXY_TOKEN is set
AIPROXY_TOKEN = os.environ.get("AIPROXY_TOKEN")
if not AIPROXY_TOKEN:
    print("Error: AIPROXY_TOKEN environment variable not set.")
    sys.exit(1)

API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

# Function to interact with the LLM
def fetch_llm_response(prompt, temperature=0.7):
    # Fetch response from GPT-4o-Mini via AI Proxy.
    headers = {
        "Authorization": f"Bearer {AIPROXY_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to load dataset with error handling for different encodings
def load_dataset(filename):
    # Attempt to load dataset with different encodings.
    encodings = [
        "utf-8", "ISO-8859-1", "windows-1252", "utf-16", "utf-32",
        "GB2312", "GBK", "shift_jis", "big5", "macroman", "EUC-JP", "KOI8-R", "windows-1250"
    ]
    for encoding in encodings:
        try:
            data = pd.read_csv(filename, encoding=encoding)
            print(f"Dataset '{filename}' loaded successfully with encoding '{encoding}'.")
            return data
        except UnicodeDecodeError:
            continue
    else:
        print("Error: Could not load file with common encodings.")
        return None

# Analyze missing values and return the result
def analyze_missing_values(data):
    # Analyze and return missing values in the dataset
    missing_values = data.isnull().sum()
    return missing_values

# Perform correlation analysis on numeric columns and visualize
def analyze_correlation(data):
    # Perform correlation analysis on numeric columns
    numeric_data = data.select_dtypes(include=[np.number])
    if numeric_data.shape[1] > 1:
        correlation_matrix = numeric_data.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", cbar=True)
        plt.title("Correlation Matrix of Numeric Features")
        plt.savefig("correlation_matrix.png")
        plt.close()
    else:
        correlation_matrix = None
    return correlation_matrix

# Generate dynamic LLM prompt for analysis
def generate_prompt(data, missing_values, numeric_data):
    # Generate dynamic LLM prompt for analysis.
    prompt = f"""
    Analyze the following dataset:
    - Columns: {data.columns.tolist()}
    - Missing values per column: {missing_values.to_dict()}
    - Summary statistics for numeric columns: {numeric_data.describe().to_dict()}
    Suggest significant analyses, findings, and a possible narrative for this data.
    """
    return prompt

# Generate the final narrative and save it to README.md
def generate_narrative(insights, data, correlation_matrix):
    # Generate the final narrative with insights and visualizations.
    with open("README.md", "w") as f:
        f.write("# Automated Dataset Analysis\n\n")
        f.write("## Summary\n")
        f.write(f"Columns: {data.columns.tolist()}\n")
        f.write(f"Missing Values: {analyze_missing_values(data).to_dict()}\n")
        f.write("## Correlation Matrix\n")
        if correlation_matrix is not None:
            f.write("See correlation_matrix.png for details.\n")
        f.write("## Insights\n")
        f.write(insights)

# Main analysis function
def analyze_dataset(filename):
    # Perform generic analysis and generate insights
    try:
        # Load dataset
        data = load_dataset(filename)
        if data is None:
            return

        # Perform analysis
        missing_values = analyze_missing_values(data)
        numeric_data = data.select_dtypes(include=[np.number])

        # Perform correlation analysis
        correlation_matrix = analyze_correlation(data)

        # Generate dynamic LLM prompt
        prompt = generate_prompt(data, missing_values, numeric_data)

        # Fetch insights from LLM
        insights = fetch_llm_response(prompt)
        print("LLM Analysis:")
        print(insights)

        # Generate final narrative and save to README.md
        generate_narrative(insights, data, correlation_matrix)

    except Exception as e:
        print(f"Error during analysis: {e}")

# Run the script when called
if __name__ == "__main__":
    # Check command-line arguments
    if len(sys.argv) != 2:
        print("Usage: uv run autolysis.py <dataset.csv>")
        sys.exit(1)
    
    dataset_filename = sys.argv[1]
    analyze_dataset(dataset_filename)


