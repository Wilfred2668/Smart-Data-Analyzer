# Automated Dataset Analysis  

This project is developed as part of the **IIT Madras Tools in Data Science** course. It implements an automated dataset analysis tool leveraging statistical techniques, data visualizations, and LLM (Large Language Model)-generated insights using **ChatGPT**.

### Problem Description

The detailed problem description can be found [here](https://github.com/sanand0/tools-in-data-science-public/blob/tds-2024-t3/project-2-automated-analysis.md).

---

## How It Works

1. **Input a Dataset**: Provide any `.csv` file as input. The tool dynamically analyzes the dataset to:
   - Identify and summarize missing values.
   - Generate statistical summaries of numeric columns.
   - Perform correlation analysis on numeric features.
   - Suggest actionable insights based on data trends.

2. **AI-Generated Insights**:
   - Uses **ChatGPT (GPT-4o-Mini)** via an AI Proxy to generate a narrative based on the dataset.
   - Provides suggestions for further analysis and improvements.

3. **Visualizations**:
   - Produces a heatmap of correlations between numeric columns.
   - Suggests additional visualizations for deeper analysis.

---

## How to Run the Project

### Prerequisites

- Python version `>=3.11`
- Required dependencies: `pandas`, `numpy`, `matplotlib`, `seaborn`, `requests`
- An active `AIPROXY_TOKEN` to interact with the LLM proxy.

### Steps to Run

#### On PowerShell

1. **Set Environment Variables**:
   ```powershell
   $env:AIPROXY_TOKEN="your_aiproxy_token_here"
   ```

2. **Run the Script**:
   Provide a test `.csv` file as input (e.g., `goodreads.csv`):
   ```powershell
   uv run autolysis.py goodreads.csv
   ```

#### On Command Prompt

1. **Set Environment Variables**:
   ```cmd
   set AIPROXY_TOKEN=your_aiproxy_token_here
   ```

2. **Run the Script**:
   Provide a test `.csv` file as input (e.g., `goodreads.csv`):
   ```cmd
   uv run autolysis.py goodreads.csv
   ```

---

## Output

- A detailed `README.md` file with:
  - Dataset summary
  - Missing values analysis
  - Correlation matrix insights
  - AI-generated narrative with actionable insights
- A `correlation_matrix.png` file visualizing the correlations between numeric columns.

---

## Test Data

You can test the project with the following sample datasets:
1. `goodreads.csv`
2. `happiness.csv`
3. `media.csv`

Ensure the `.csv` files are in the same directory as the script, or provide their full path when running the script.

---

## Developed By

This project was built by **Wilfred Dsouza** as part of the **IIT Madras Tools in Data Science** course and leverages the power of **ChatGPT (GPT-4o-Mini)** for generating insights and narratives.
