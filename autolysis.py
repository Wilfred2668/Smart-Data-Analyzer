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

# Analyze missing values and return summary
def analyze_missing_values(data):
    missing_summary = data.isnull().sum().to_frame(name="Missing Values")
    missing_summary["% of Total"] = (missing_summary["Missing Values"] / len(data)) * 100
    return missing_summary

# Generate key visualizations
def create_visualizations(data):
    image_files = []
    numeric_data = data.select_dtypes(include=["number"])

    # Visualization 1: Correlation Matrix
    if numeric_data.shape[1] > 1:
        correlation_matrix = numeric_data.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", cbar=True)
        filename = "correlation_matrix.png"
        plt.title("Correlation Matrix")
        plt.savefig(filename)
        image_files.append(filename)
        plt.close()

    # Visualization 2: Histogram for Key Numeric Column
    for column in numeric_data.columns[:1]:  # Focus on 1 key column for speed
        sns.histplot(numeric_data[column], kde=True, bins=30, color='blue')
        filename = f"distribution_{column}.png"
        plt.title(f"Distribution of {column}")
        plt.savefig(filename)
        image_files.append(filename)
        plt.close()

    # Visualization 3: Pairplot
    filename = "pairplot.png"
    sns.pairplot(numeric_data.iloc[:, :3])  # Limit pairplot to first 3 columns
    plt.savefig(filename)
    image_files.append(filename)
    plt.close()

    return image_files

# Generate a comprehensive prompt
def generate_prompt(data, image_files):
    column_info = data.describe(include="all").to_dict()
    missing_values = analyze_missing_values(data).to_dict()

    prompt = f"""
    Analyze the following dataset:
    - Column details: {column_info}
    - Missing values summary: {missing_values}
    - Generated visualizations:
        - Correlation Matrix: {image_files[0]}
        - Distribution of Key Numeric Column: {image_files[1]}
        - Pairplot: {image_files[2]}

    Use Python (pandas, seaborn, matplotlib) for the analysis. Suggest patterns, trends, anomalies, and other key findings. Provide insights that can be deduced.
    Also analyse the charts and give insights on those.
    Note: Dont give codes instead do the analysis yourself and then provide the necessary values. At the end give a proper narrative. 
    Make it as detailed and neat as possible. It should be well_structured, should contain proper analysis and proper visualization.
    """
    return prompt

# Generate README with detailed insights and visualizations
def generate_readme(insights, image_files):
    with open("README.md", "w") as f:
        f.write("# Automated Dataset Analysis\n\n")
        f.write("## Insights\n")
        f.write(insights)
        f.write("\n\n## Visualizations\n")
        for image in image_files:
            f.write(f"- {image}\n")
        f.write("\n\n### Embedded Graphs\n")
        for image in image_files:
            f.write(f"![{image}](./{image})\n")

# Main analysis function
def analyze_dataset(filename):
    try:
        data = load_dataset(filename)
        if data is None:
            return

        # Generate visualizations and get file paths
        image_files = create_visualizations(data)

        # Generate and fetch insights
        prompt = generate_prompt(data, image_files)
        insights = fetch_llm_response(prompt)
        print("LLM Analysis:")
        print(insights)

        # Generate README
        generate_readme(insights, image_files)

    except Exception as e:
        print(f"Error during analysis: {e}")

# Run the script when called
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python autolysis.py <dataset.csv>")
        sys.exit(1)
    dataset_filename = sys.argv[1]
    analyze_dataset(dataset_filename)


