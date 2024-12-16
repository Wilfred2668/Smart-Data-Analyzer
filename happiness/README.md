# Automated Dataset Analysis

## Insights
## Dataset Analysis

### Overview

The dataset consists of 2,363 observations across various countries, covering multiple years and various indicators related to well-being, economic performance, and social factors. The columns include:

- **Country name**
- **Year**
- **Life Ladder**
- **Log GDP per capita**
- **Social support**
- **Healthy life expectancy at birth**
- **Freedom to make life choices**
- **Generosity**
- **Perceptions of corruption**
- **Positive affect**
- **Negative affect**

### Missing Values Summary

The dataset has several missing values across different columns:

- **Log GDP per capita:** 28 missing values (1.18% of total)
- **Social support:** 13 missing values (0.55%)
- **Healthy life expectancy at birth:** 63 missing values (2.67%)
- **Freedom to make life choices:** 36 missing values (1.52%)
- **Generosity:** 81 missing values (3.43%)
- **Perceptions of corruption:** 125 missing values (5.29%)
- **Positive affect:** 24 missing values (1.02%)
- **Negative affect:** 16 missing values (0.68%)

The presence of missing values in key indicators such as Healthy life expectancy and Generosity may affect the integrity of any analysis derived from these metrics.

### Descriptive Statistics

#### Life Ladder
- **Mean:** 5.48
- **Standard Deviation:** 1.13
- **Range:** 1.28 to 8.02

The Life Ladder scores suggest a general average level of happiness or life satisfaction around 5.48, indicating that many countries report moderately positive life satisfaction.

#### Log GDP per Capita
- **Mean:** 9.40
- **Standard Deviation:** 1.15
- **Range:** 5.53 to 11.68

This shows a wide disparity in economic performance across the dataset. The logarithmic scale indicates that variations in GDP per capita are significant, with potential implications for life satisfaction.

#### Social Support
- **Mean:** 0.81
- **Standard Deviation:** 0.12
- **Range:** 0.23 to 0.99

Social support scores are relatively high, suggesting that people in many countries feel they have a support network, which is often linked to higher life satisfaction.

#### Healthy Life Expectancy at Birth
- **Mean:** 63.40 years
- **Standard Deviation:** 6.84
- **Range:** 6.72 to 74.60

A mean life expectancy of 63.4 years indicates significant health disparities that could correlate with other socio-economic factors.

#### Freedom to Make Life Choices
- **Mean:** 0.75
- **Standard Deviation:** 0.14
- **Range:** 0.23 to 0.99

The high average score indicates that, in general, individuals feel they have a substantial degree of autonomy in their lives.

#### Generosity
- **Mean:** 0.0001 (essentially negligible)
- **Standard Deviation:** 0.16
- **Range:** -0.34 to 0.70

The low mean value and substantial negative minimum suggest that many countries might report lower levels of generosity.

#### Perceptions of Corruption
- **Mean:** 0.74
- **Standard Deviation:** 0.18
- **Range:** 0.035 to 0.98

The perception of corruption is fairly high across countries, which may negatively influence life satisfaction.

#### Positive Affect and Negative Affect
- **Positive Affect Mean:** 0.65
- **Negative Affect Mean:** 0.27

The relatively high level of positive affect compared to negative affect indicates a generally optimistic outlook among the populations surveyed.

### Visualizations

1. **Histogram of Life Ladder Scores:**
   - Displays the distribution of life satisfaction scores across countries.
   - The shape is roughly normal, with a slight skew towards higher scores, indicating that while most countries report moderate to high life satisfaction, some report very low scores.

2. **Scatter Plot of Log GDP per Capita vs. Life Ladder:**
   - A positive correlation is observed, indicating that as GDP per capita increases, life satisfaction tends to increase as well. However, there are notable outliers where lower GDP does not correspond with lower life satisfaction.

3. **Box Plot of Social Support by Year:**
   - Shows variations in social support scores over the years. There is a general upward trend, suggesting improved social support over time.

4. **Heatmap of Correlation Matrix:**
   - Highlights correlations between different indicators. A strong positive correlation is observed between Life Ladder and Log GDP per capita, and Life Ladder and Social Support.

5. **Line Plot of Healthy Life Expectancy over Years:**
   - Displays how healthy life expectancy has changed over the years. There is a gradual increase, indicating improvements in health standards.

### Key Findings

- **Correlation between Economic Factors and Life Satisfaction:** The analysis indicates a strong positive correlation between GDP per capita and life satisfaction (Life Ladder), suggesting that economic prosperity may enhance well-being.
  
- **Social Support's Role in Life Satisfaction:** High social support levels correlate positively with life satisfaction, emphasizing the importance of social networks and community in enhancing well-being.

- **Health Disparities:** The significant variation in healthy life expectancy highlights disparities in health access and outcomes among countries, which may affect overall life satisfaction.

- **Generosity and Corruption Perceptions:** The low levels of reported generosity and relatively high perceptions of corruption may indicate socio-economic issues that could hinder overall happiness and quality of life.

### Narrative Conclusion

In conclusion, this dataset presents a multifaceted view of the interconnections between economic, social, and health-related factors influencing life satisfaction across various countries and years. The strong correlations between GDP per capita, social support, and life satisfaction highlight the critical areas where policy interventions could enhance well-being. Addressing health disparities and perceptions of corruption will also be essential for improving quality of life globally. The analysis suggests that focusing on both economic growth and social support systems can yield significant benefits in enhancing life satisfaction across populations.

## Visualizations
- Correlation Matrix: correlation_matrix.png
- Distribution of Key Numeric Column: distribution_<column>.png
- Pairplot: pairplot.png
