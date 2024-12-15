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
    print("Error: Could not load file with common encodings.")
    return None

# Analyze missing values and return the result
def analyze_missing_values(data):
    missing_values = data.isnull().sum()
    missing_percentage = (missing_values / len(data)) * 100
    return pd.DataFrame({"Missing Values": missing_values, "% of Total": missing_percentage})

# Perform correlation analysis and visualize
def analyze_correlation(data):
    numeric_data = data.select_dtypes(include=[np.number])
    if numeric_data.shape[1] > 1:
        correlation_matrix = numeric_data.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", cbar=True)
        plt.title("Correlation Matrix of Numeric Features")
        plt.savefig("correlation_matrix.png")
        plt.close()
        return correlation_matrix
    return None

# Streamlined visualizations

def create_visualizations(data):
    numeric_data = data.select_dtypes(include=[np.number])
    categorical_data = data.select_dtypes(exclude=[np.number])

    # Correlation matrix
    if numeric_data.shape[1] > 1:
        sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.savefig("correlation_heatmap.png")
        plt.close()

    # Distribution plot for a key numeric column
    if not numeric_data.empty:
        key_numeric_column = numeric_data.columns[0]
        sns.histplot(numeric_data[key_numeric_column], kde=True, bins=30, color='blue')
        plt.title(f"Distribution of {key_numeric_column}")
        plt.xlabel(key_numeric_column)
        plt.ylabel("Frequency")
        plt.savefig(f"distribution_{key_numeric_column}.png")
        plt.close()

    # Box plot for numeric vs categorical
    if not categorical_data.empty and not numeric_data.empty:
        cat_col = categorical_data.columns[0]
        num_col = numeric_data.columns[0]
        sns.boxplot(x=cat_col, y=num_col, data=data)
        plt.title(f"Box Plot of {num_col} by {cat_col}")
        plt.savefig(f"boxplot_{num_col}_by_{cat_col}.png")
        plt.close()

    # Bar plot for a categorical column
    if not categorical_data.empty:
        cat_col = categorical_data.columns[0]
        sns.countplot(x=cat_col, data=data)
        plt.title(f"Bar Plot of {cat_col}")
        plt.savefig(f"barplot_{cat_col}.png")
        plt.close()

# Efficient data summarization
def summarize_data(data):
    numeric_data = data.select_dtypes(include=[np.number])
    categorical_data = data.select_dtypes(exclude=[np.number])
    return {
        "numeric_summary": numeric_data.describe().to_dict(),
        "categorical_summary": categorical_data.describe(include='all').to_dict(),
    }

# Generate dynamic LLM prompt
def generate_prompt(data, missing_values, numeric_summary):
    prompt = f"""
    Analyze the following dataset:
    - Columns: {data.columns.tolist()}
    - Missing values per column: {missing_values.to_dict()}
    - Summary statistics for numeric columns: {numeric_summary}
    Suggest significant analyses, findings, and a possible narrative for this data.
    """
    return prompt

# Generate README with detailed analysis
def generate_narrative(insights, data, correlation_matrix):
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
    try:
        data = load_dataset(filename)
        if data is None:
            return

        missing_values = analyze_missing_values(data)
        numeric_data = data.select_dtypes(include=[np.number])

        correlation_matrix = analyze_correlation(data)
        create_visualizations(data)

        summary = summarize_data(data)

        prompt = generate_prompt(data, missing_values, summary['numeric_summary'])
        insights = fetch_llm_response(prompt)
        print("LLM Analysis:")
        print(insights)

        generate_narrative(insights, data, correlation_matrix)

    except Exception as e:
        print(f"Error during analysis: {e}")

# Run the script when called
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run autolysis.py <dataset.csv>")
        sys.exit(1)
    dataset_filename = sys.argv[1]
    analyze_dataset(dataset_filename)


