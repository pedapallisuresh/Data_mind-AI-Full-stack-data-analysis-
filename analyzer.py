import pandas as pd
import numpy as np
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration - Support multiple providers
def get_llm_client():
    """Get LLM client based on available API keys"""
    # Try OpenAI first
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        from openai import OpenAI
        return OpenAI(api_key=openai_key), 'openai'
    
    # Try Ollama (local)
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            return None, 'ollama'
    except:
        pass
    
    # Fallback to Tavily
    import openai as tavily_openai
    tavily_openai.api_base = "https://api.tavily.com/v1"
    tavily_openai.api_key = os.getenv('TAVILY_API_KEY')
    return tavily_openai, 'tavily'

def query_llm(prompt, system_prompt="You are a senior data scientist and business analyst.", model="gpt-3.5-turbo"):
    """Query LLM with fallback support"""
    client, provider = get_llm_client()
    
    if provider == 'openai':
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "invalid_api_key" in error_msg.lower():
                return "Error: Invalid or missing OpenAI API key. Please check your .env file and ensure OPENAI_API_KEY is set correctly."
            return f"OpenAI Error: {error_msg}"
    
    elif provider == 'ollama':
        try:
            import requests
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama2",
                    "prompt": f"System: {system_prompt}\n\nUser: {prompt}",
                    "stream": False
                },
                timeout=60
            )
            return response.json().get('response', '').strip()
        except Exception as e:
            return f"Ollama Error: {str(e)}"
    
    else:  # tavily
        try:
            response = client.ChatCompletion.create(
                model="mistralai/Mistral-7B-Instruct-v0.1",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Tavily Error: {str(e)}"

def query_together(prompt, retries=3):
    """Legacy function - uses query_llm instead"""
    return query_llm(prompt)

def generate_summary(df):
    summary = {
        "Total Rows": df.shape[0],
        "Total Columns": df.shape[1],
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
        "Column Names": list(df.columns),
        "Data Types": df.dtypes.astype(str).to_dict()
    }

    return summary

def generate_descriptive_stats(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        return {}
    
    desc_stats = df[numeric_cols].describe().to_dict()
    return desc_stats

def generate_correlation_matrix(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        return {}
    
    corr_matrix = df[numeric_cols].corr().round(2).to_dict()
    return corr_matrix

def generate_categorical_insights(df):
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    insights = {}
    
    for col in categorical_cols:
        value_counts = df[col].value_counts().head(10).to_dict()
        unique_count = df[col].nunique()
        most_common = df[col].mode().iloc[0] if not df[col].mode().empty else None
        
        insights[col] = {
            "Unique Values": unique_count,
            "Most Common Value": most_common,
            "Top 10 Values": value_counts
        }
    
    return insights

def detect_outliers(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers = {}
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        outliers[col] = {
            "Outlier Count": int(outlier_count),
            "Lower Bound": lower_bound,
            "Upper Bound": upper_bound
        }
    
    return outliers

def generate_key_insights(df):
    insights = []
    
    # Check for high missing values
    missing_pct = (df.isnull().sum() / len(df)) * 100
    high_missing_cols = missing_pct[missing_pct > 50].index.tolist()
    if high_missing_cols:
        insights.append(f"Columns with high missing values (>50%): {', '.join(high_missing_cols)}")
    
    # Check for duplicates
    dup_pct = (df.duplicated().sum() / len(df)) * 100
    if dup_pct > 10:
        insights.append(f"High duplicate row percentage: {dup_pct:.2f}%")
    
    # Numeric insights
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        skewness = df[col].skew()
        if abs(skewness) > 1:
            direction = "right-skewed" if skewness > 0 else "left-skewed"
            insights.append(f"Column '{col}' is highly {direction} (skewness: {skewness:.2f})")
    
    # Categorical insights
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols:
        if df[col].nunique() == len(df):
            insights.append(f"Column '{col}' appears to have unique values for each row (potential ID column)")
    
    if not insights:
        insights.append("No significant insights detected. Data appears clean and balanced.")
    
    return insights

def generate_comprehensive_analysis(df):
    analysis = {
        "Basic Summary": generate_summary(df),
        "Descriptive Statistics": generate_descriptive_stats(df),
        "Correlation Matrix": generate_correlation_matrix(df),
        "Categorical Insights": generate_categorical_insights(df),
        "Outlier Detection": detect_outliers(df),
        "Key Insights": generate_key_insights(df)
    }
    
    return analysis

def generate_data_profiling(df):
    """Generate comprehensive data profiling information"""
    profiling = {
        "Data Shape": df.shape,
        "Column Types": df.dtypes.value_counts().to_dict(),
        "Memory Usage (MB)": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
        "Duplicate Rows": int(df.duplicated().sum()),
        "Missing Values Summary": df.isnull().sum().to_dict(),
        "Unique Values Count": df.nunique().to_dict(),
        "Most Frequent Values": {col: df[col].mode().iloc[0] if not df[col].mode().empty else None for col in df.columns}
    }
    return profiling

def generate_visualization_suggestions(df):
    """Generate suggestions for data visualizations"""
    suggestions = []
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    datetime_cols = df.select_dtypes(include=['datetime']).columns

    if len(numeric_cols) > 1:
        suggestions.append("Correlation heatmap for numeric columns")
        suggestions.append("Pair plot for numeric columns")

    if len(numeric_cols) > 0:
        suggestions.append("Histogram for each numeric column")
        suggestions.append("Box plot for outlier detection in numeric columns")

    if len(categorical_cols) > 0:
        suggestions.append("Bar chart for categorical column distributions")
        suggestions.append("Pie chart for categorical value proportions")

    if len(numeric_cols) > 0 and len(categorical_cols) > 0:
        suggestions.append("Box plot grouped by categorical variables")
        suggestions.append("Violin plot for distribution comparison")

    if len(datetime_cols) > 0:
        suggestions.append("Time series plot for datetime columns")
        suggestions.append("Line chart for trend analysis over time")

    if len(numeric_cols) > 0 and len(datetime_cols) > 0:
        suggestions.append("Time series decomposition for seasonal patterns")

    return suggestions

def generate_statistical_summary(df):
    """Generate statistical tests and summaries"""
    stats_summary = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) > 1:
        # Shapiro-Wilk test for normality (simplified)
        normality_tests = {}
        for col in numeric_cols:
            if len(df[col].dropna()) > 3:
                # Simple normality check using skewness and kurtosis
                skewness = df[col].skew()
                kurtosis = df[col].kurtosis()
                normality_tests[col] = {
                    "Skewness": round(skewness, 2),
                    "Kurtosis": round(kurtosis, 2),
                    "Likely Normal": abs(skewness) < 1 and abs(kurtosis) < 1
                }
        stats_summary["Normality Tests"] = normality_tests

    # Basic statistical tests
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        high_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > 0.7:
                    high_corr.append({
                        "Variable 1": corr_matrix.columns[i],
                        "Variable 2": corr_matrix.columns[j],
                        "Correlation": round(corr_matrix.iloc[i, j], 2)
                    })
        stats_summary["High Correlations"] = high_corr

    return stats_summary

def generate_trend_analysis(df):
    """Analyze trends in numeric columns over time if datetime columns exist"""
    trends = {}
    datetime_cols = df.select_dtypes(include=['datetime']).columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(datetime_cols) > 0 and len(numeric_cols) > 0:
        for dt_col in datetime_cols:
            for num_col in numeric_cols:
                try:
                    # Sort by datetime
                    temp_df = df[[dt_col, num_col]].dropna().sort_values(dt_col)

                    if len(temp_df) > 1:
                        # Calculate trend (simple linear regression slope)
                        x = np.arange(len(temp_df))
                        y = temp_df[num_col].values
                        slope = np.polyfit(x, y, 1)[0]

                        # Calculate correlation with time
                        corr = temp_df[dt_col].astype('int64').corr(temp_df[num_col])

                        trends[f"{num_col}_over_{dt_col}"] = {
                            "Trend Slope": round(slope, 4),
                            "Correlation": round(corr, 4),
                            "Direction": "Increasing" if slope > 0 else "Decreasing" if slope < 0 else "Stable",
                            "Strength": "Strong" if abs(corr) > 0.7 else "Moderate" if abs(corr) > 0.3 else "Weak"
                        }
                except Exception as e:
                    trends[f"{num_col}_over_{dt_col}"] = {"Error": str(e)}

    return trends

def generate_anomaly_detection(df):
    """Detect anomalies using statistical methods"""
    anomalies = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        try:
            # Z-score method
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            z_anomalies = (z_scores > 3).sum()

            # IQR method
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            iqr_anomalies = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()

            anomalies[col] = {
                "Z-Score Anomalies": int(z_anomalies),
                "IQR Anomalies": int(iqr_anomalies),
                "Total Anomalies": int(z_anomalies + iqr_anomalies),
                "Anomaly Percentage": round((z_anomalies + iqr_anomalies) / len(df) * 100, 2)
            }
        except Exception as e:
            anomalies[col] = {"Error": str(e)}

    return anomalies

def generate_business_insights(df):
    """Generate business-oriented insights based on data patterns"""
    insights = []

    # Check for data completeness
    completeness = (1 - df.isnull().sum() / len(df)) * 100
    low_completeness = completeness[completeness < 80]
    if len(low_completeness) > 0:
        insights.append(f"Data completeness issues in: {', '.join(low_completeness.index)}. Consider data collection improvements.")

    # Check for potential KPIs
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        # Identify potential metrics
        for col in numeric_cols:
            if 'revenue' in col.lower() or 'sales' in col.lower() or 'profit' in col.lower():
                insights.append(f"'{col}' appears to be a key business metric. Monitor trends and set targets.")
            elif 'cost' in col.lower() or 'expense' in col.lower():
                insights.append(f"'{col}' represents business costs. Analyze cost drivers and optimization opportunities.")

    # Check for customer-related data
    customer_cols = [col for col in df.columns if any(term in col.lower() for term in ['customer', 'client', 'user', 'member'])]
    if customer_cols:
        insights.append(f"Customer data identified in columns: {', '.join(customer_cols)}. Consider customer segmentation and retention analysis.")

    # Check for time-based patterns
    datetime_cols = df.select_dtypes(include=['datetime']).columns
    if len(datetime_cols) > 0:
        insights.append("Time-series data available. Consider trend analysis, seasonality detection, and forecasting models.")

    # Check for categorical data richness
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols:
        if df[col].nunique() > 10:
            insights.append(f"Column '{col}' has high cardinality ({df[col].nunique()} unique values). Consider grouping or feature engineering.")

    return insights

def generate_predictive_potential(df):
    """Assess the predictive modeling potential of the dataset"""
    potential = {
        "Target Variables": [],
        "Feature Candidates": [],
        "Data Quality Score": 0,
        "Modeling Readiness": "Low",
        "Recommended Models": []
    }

    # Identify potential target variables
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if any(term in col.lower() for term in ['target', 'outcome', 'result', 'score', 'rating', 'price', 'value']):
            potential["Target Variables"].append(col)

    # Assess data quality
    completeness_score = ((1 - df.isnull().sum() / len(df)) * 100).mean()
    uniqueness_score = (df.nunique() / len(df) * 100).mean()
    quality_score = (completeness_score + uniqueness_score) / 2
    potential["Data Quality Score"] = round(quality_score, 2)

    # Determine modeling readiness
    if quality_score > 80 and len(df) > 100:
        potential["Modeling Readiness"] = "High"
        potential["Recommended Models"] = ["Linear Regression", "Random Forest", "Gradient Boosting"]
    elif quality_score > 60 and len(df) > 50:
        potential["Modeling Readiness"] = "Medium"
        potential["Recommended Models"] = ["Decision Trees", "Logistic Regression"]
    else:
        potential["Modeling Readiness"] = "Low"
        potential["Recommended Models"] = ["Data preprocessing required first"]

    # Identify feature candidates
    potential["Feature Candidates"] = list(df.select_dtypes(include=[np.number, 'object', 'category']).columns)

    return potential

def generate_comprehensive_agent_analysis(df):
    """Complete agent analysis combining all analysis types"""
    analysis = {
        "Data Profiling": generate_data_profiling(df),
        "Descriptive Statistics": generate_descriptive_stats(df),
        "Correlation Analysis": generate_correlation_matrix(df),
        "Categorical Insights": generate_categorical_insights(df),
        "Outlier Detection": detect_outliers(df),
        "Statistical Summary": generate_statistical_summary(df),
        "Trend Analysis": generate_trend_analysis(df),
        "Anomaly Detection": generate_anomaly_detection(df),
        "Business Insights": generate_business_insights(df),
        "Predictive Potential": generate_predictive_potential(df),
        "Visualization Suggestions": generate_visualization_suggestions(df),
        "Key Insights": generate_key_insights(df)
    }

    return analysis

def generate_ai_insights(df):
    """Generate AI-powered meaningful insights about the data using LLM"""
    try:
        # Prepare a comprehensive summary of the data for the LLM
        summary = generate_summary(df)
        desc_stats = generate_descriptive_stats(df)
        categorical = generate_categorical_insights(df)
        business_insights = generate_business_insights(df)
        predictive_potential = generate_predictive_potential(df)

        # Create a comprehensive prompt
        data_summary = f"""
Dataset Overview:
- Rows: {summary['Total Rows']}, Columns: {summary['Total Columns']}
- Column Names: {', '.join(summary['Column Names'])}
- Data Types: {summary['Data Types']}
- Missing Values: {summary['Missing Values']}
- Duplicate Rows: {summary['Duplicate Rows']}

Descriptive Statistics: {desc_stats}

Categorical Insights: {categorical}

Business Context: {business_insights}

Predictive Potential: {predictive_potential}

As an expert data analyst, provide deep insights about this dataset including:
1. Key patterns and relationships in the data
2. Business implications and actionable recommendations
3. Data quality assessment and improvement suggestions
4. Potential analytical approaches and modeling opportunities
5. Interesting findings that might not be immediately obvious
6. Recommendations for next steps in data analysis
"""

        prompt = f"""You are a senior data scientist and business analyst. Analyze this dataset comprehensively and provide strategic insights.

{data_summary}

Provide 8-12 detailed insights that would be valuable for business decision-making. Structure your response with clear headings and bullet points."""

        output = query_together(prompt)

        if output:
            # Extract the generated text after the prompt
            generated_text = output
            if "Provide 8-12 detailed insights" in generated_text:
                ai_insights = generated_text.split("Provide 8-12 detailed insights")[-1].strip()
            else:
                ai_insights = generated_text.strip()
            return ai_insights

        return "Unable to generate AI insights at this time."

    except Exception as e:
        return f"Error generating AI insights: {str(e)}"
