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

# Function to load dataset
def load_dataset(filename):
    try:
        data = pd.read_csv(filename)
        print(f"Dataset '{filename}' loaded successfully.")
        return data
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

# Analyze missing values and return summary
def analyze_missing_values(data):
    missing_summary = data.isnull().sum().to_frame(name="Missing Values")
    missing_summary["% of Total"] = (missing_summary["Missing Values"] / len(data)) * 100
    return missing_summary

# Generate key visualizations
def create_visualizations(data):
    numeric_data = data.select_dtypes(include=["number"])
    
    # Visualization 1: Correlation Matrix
    if numeric_data.shape[1] > 1:
        correlation_matrix = numeric_data.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", cbar=True)
        plt.title("Correlation Matrix")
        plt.savefig("correlation_matrix.png")
        plt.close()

    # Visualization 2: Histogram for all numeric columns
    for column in numeric_data.columns[:1]:  # Focus on 1 key column for speed
        sns.histplot(numeric_data[column], kde=True, bins=30, color='blue')
        plt.title(f"Distribution of {column}")
        plt.savefig(f"distribution_{column}.png")
        plt.close()

    # Visualization 3: Pairplot (subset of columns for performance)
    sns.pairplot(numeric_data.iloc[:, :3])  # Limit pairplot to first 3 columns
    plt.savefig("pairplot.png")
    plt.close()

# Generate a comprehensive prompt
def generate_prompt(data):
    column_info = data.describe(include="all").to_dict()
    missing_values = analyze_missing_values(data).to_dict()
    prompt = f"""
    Analyze the following dataset:
    - Column details: {column_info}
    - Missing values summary: {missing_values}
    Use Python (pandas, seaborn, matplotlib) for the analysis. Suggest patterns, trends, anomalies, and other key findings. Provide insights that can be deduced.
    Also describe all the charts generated.
    Note: Dont give codes instead do the analysis yourself and then provide the necessary values. At the end give a proper narrative. 
    """
    return prompt

# Generate README with detailed insights
def generate_readme(insights):
    with open("README.md", "w") as f:
        f.write("# Automated Dataset Analysis\n\n")
        f.write("## Insights\n")
        f.write(insights)
        f.write("\n\n## Visualizations\n")
        f.write("- Correlation Matrix: correlation_matrix.png\n")
        f.write("- Distribution of Key Numeric Column: distribution_<column>.png\n")
        f.write("- Pairplot: pairplot.png\n")

# Main analysis function
def analyze_dataset(filename):
    try:
        data = load_dataset(filename)
        if data is None:
            return

        # Generate visualizations
        create_visualizations(data)

        # Generate and fetch insights
        prompt = generate_prompt(data)
        insights = fetch_llm_response(prompt)
        print("LLM Analysis:")
        print(insights)

        # Generate README
        generate_readme(insights)

    except Exception as e:
        print(f"Error during analysis: {e}")

# Run the script when called
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run autolysis.py <dataset.csv>")
        sys.exit(1)
    dataset_filename = sys.argv[1]
    analyze_dataset(dataset_filename)


