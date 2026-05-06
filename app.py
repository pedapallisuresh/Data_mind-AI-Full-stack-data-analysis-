import streamlit as st
import pandas as pd
from qa_engine import run_query
from cleaner import clean_data
from analyzer import (
    generate_summary,
    generate_comprehensive_analysis,
    generate_ai_insights,
    generate_data_profiling,
    generate_visualization_suggestions,
    generate_statistical_summary,
    generate_comprehensive_agent_analysis
)

# Initialize session state for DataFrame
if 'df' not in st.session_state:
    st.session_state.df = None
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None

st.set_page_config(page_title="AI Data Assistant", layout="wide")

st.title("📊 AI Data SQL Assistant")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.df = df

    st.subheader("📌 Data Preview")
    st.dataframe(df.head())

    # Data Cleaning Section
    if st.button("Clean Data"):
        with st.spinner("Cleaning data..."):
            st.session_state.cleaned_df = clean_data(df.copy())
        st.success("Data cleaned!")

    # Use cleaned data if available
    data_df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else df

    # Data Analysis Section
    if st.button("Analyze Data"):
        summary = generate_summary(data_df)
        st.subheader("📊 Data Summary")
        st.json(summary)

    # Comprehensive Analysis Section
    if st.button("Generate Comprehensive Analysis"):
        with st.spinner("Analyzing data..."):
            analysis = generate_comprehensive_analysis(data_df)
        
        st.subheader("📈 Comprehensive Analysis")
        
        # Basic Summary
        st.write("### Basic Summary")
        st.json(analysis["Basic Summary"])
        
        # Descriptive Statistics
        if analysis["Descriptive Statistics"]:
            st.write("### Descriptive Statistics")
            for col, stats in analysis["Descriptive Statistics"].items():
                st.write(f"**{col}**: {stats}")
        
        # Correlation Matrix
        if analysis["Correlation Matrix"]:
            st.write("### Correlation Matrix")
            st.json(analysis["Correlation Matrix"])
        
        # Categorical Insights
        if analysis["Categorical Insights"]:
            st.write("### Categorical Insights")
            for col, insights in analysis["Categorical Insights"].items():
                st.write(f"**{col}**: {insights}")
        
        # Outlier Detection
        if analysis["Outlier Detection"]:
            st.write("### Outlier Detection")
            for col, outliers in analysis["Outlier Detection"].items():
                st.write(f"**{col}**: {outliers}")
        
        # Key Insights
        st.write("### Key Insights")
        for insight in analysis["Key Insights"]:
            st.write(f"- {insight}")

    # AI-Powered Insights Section
    if st.button("Generate AI Insights"):
        with st.spinner("Generating AI-powered insights using LLM..."):
            ai_insights = generate_ai_insights(data_df)
        
        st.subheader("🤖 AI-Powered Insights")
        st.write(ai_insights)

    question = st.text_input("Ask a question about your data")

    if question:
        with st.spinner("Generating SQL and fetching result..."):
            sql, answer = run_query(data_df, question)

        st.subheader("🧠 Generated SQL")
        st.code(sql, language="sql")

        st.subheader("📌 Query Result")

        if isinstance(answer, str):
            st.error(answer)
        else:
            st.dataframe(answer)
