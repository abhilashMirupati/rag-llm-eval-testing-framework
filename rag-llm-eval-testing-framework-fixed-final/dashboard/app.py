"""
Interactive dashboard for visualizing RAG-LLM evaluation results.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sqlite3
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Constants from environment or defaults
DB_PATH = os.getenv("DB_PATH", "data/results.db")
DASHBOARD_THEME = os.getenv("DASHBOARD_THEME", "light")

@st.cache_data(ttl=600)
def load_data(db_path: str) -> pd.DataFrame:
    """Load evaluation results from SQLite database, with caching."""
    if not os.path.exists(db_path):
        st.error(f"Database not found at {db_path}. Please ensure the path is correct and evaluation data exists.")
        return pd.DataFrame()

    conn = sqlite3.connect(db_path)
    query = "SELECT id, timestamp, model_name, dataset_name, metric_name, score, details FROM results ORDER BY timestamp DESC"
    try:
        df = pd.read_sql_query(query, conn)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    except Exception as e:
        st.error(f"Failed to load data from database: {e}")
        return pd.DataFrame()
    finally:
        conn.close()
    return df

def filter_data(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply user-selected filters to the dataframe."""
    if df.empty:
        return df

    filtered_df = df.copy()
    
    if filters.get("dataset"):
        filtered_df = filtered_df[filtered_df["dataset_name"] == filters["dataset"]]
    
    if filters.get("metric"):
        filtered_df = filtered_df[filtered_df["metric_name"] == filters["metric"]]
    
    if filters.get("model"):
        filtered_df = filtered_df[filtered_df["model_name"] == filters["model"]]
    
    if filters.get("date_range") and len(filters["date_range"]) == 2:
        start_date, end_date = filters["date_range"]
        filtered_df = filtered_df[
            (filtered_df["timestamp"].dt.date >= start_date) &
            (filtered_df["timestamp"].dt.date <= end_date)
        ]
    
    return filtered_df

def plot_metric_trends(df: pd.DataFrame, metric: str) -> go.Figure:
    """Plot metric trends over time for different models."""
    metric_df = df[df["metric_name"] == metric].copy()
    metric_df["date"] = metric_df["timestamp"].dt.date
    
    fig = px.line(
        metric_df,
        x="date",
        y="score",
        color="model_name",
        markers=True,
        title=f"{metric} Trends Over Time"
    )
    fig.update_layout(template=DASHBOARD_THEME)
    return fig

def plot_metric_comparison(df: pd.DataFrame, metrics: list) -> go.Figure:
    """Plot comparison of multiple metrics across models using a box plot."""
    comparison_df = df[df["metric_name"].isin(metrics)]
    
    fig = px.box(
        comparison_df,
        x="model_name",
        y="score",
        color="metric_name",
        title="Metric Comparison Across Models",
    )
    fig.update_layout(template=DASHBOARD_THEME)
    return fig

def generate_pdf_report(df: pd.DataFrame, output_path: str):
    """Generate a PDF report from the filtered evaluation results."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['h1'], alignment=1, spaceAfter=20)
    elements.append(Paragraph("RAG-LLM Evaluation Report", title_style))
    
    elements.append(Paragraph("Summary Statistics", styles['h2']))
    summary = df.groupby('metric_name')['score'].agg(['mean', 'std', 'min', 'max']).reset_index()
    summary.columns = ['Metric', 'Mean', 'Std Dev', 'Min', 'Max']
    summary_table = Table([summary.columns.tolist()] + summary.values.tolist(), colWidths=[2*inch] + [1*inch]*4)
    summary_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey), ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('BOTTOMPADDING', (0,0), (-1,0), 12), ('BACKGROUND', (0,1), (-1,-1), colors.beige), ('GRID', (0,0), (-1,-1), 1, colors.black)]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("Detailed Results", styles['h2']))
    df_display = df[['timestamp', 'model_name', 'dataset_name', 'metric_name', 'score']].copy()
    df_display['timestamp'] = df_display['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    detailed_table = Table([df_display.columns.tolist()] + df_display.values.tolist(), colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
    detailed_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey), ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('BOTTOMPADDING', (0,0), (-1,0), 12), ('GRID', (0,0), (-1,-1), 1, colors.black)]))
    elements.append(detailed_table)
    
    doc.build(elements)

def main():
    """Main function to run the Streamlit dashboard."""
    st.set_page_config(page_title="RAG-LLM Evaluation Dashboard", page_icon="📊", layout="wide")
    st.title("RAG-LLM Evaluation Dashboard")

    df = load_data()
    if df.empty:
        st.warning("No data found to display. Please run an evaluation first.")
        return

    st.sidebar.header("Filters")
    
    datasets = ["All"] + sorted(df["dataset_name"].unique().tolist())
    selected_dataset = st.sidebar.selectbox("Dataset", datasets)
    
    metrics = ["All"] + sorted(df["metric_name"].unique().tolist())
    selected_metric = st.sidebar.selectbox("Metric", metrics)
    
    models = ["All"] + sorted(df["model_name"].unique().tolist())
    selected_model = st.sidebar.selectbox("Model", models)
    
    min_date, max_date = df["timestamp"].min().date(), df["timestamp"].max().date()
    date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    
    filters = {
        "dataset": None if selected_dataset == "All" else selected_dataset,
        "metric": None if selected_metric == "All" else selected_metric,
        "model": None if selected_model == "All" else selected_model,
        "date_range": date_range
    }
    filtered_df = filter_data(df, filters)

    st.header("Visualizations")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Metric Trends")
        if selected_metric != "All":
            st.plotly_chart(plot_metric_trends(filtered_df, selected_metric), use_container_width=True)
        else:
            st.info("Select a specific metric to view trends.")
    
    with col2:
        st.subheader("Metric Comparison")
        default_metrics = metrics[1:4] if len(metrics) > 3 else metrics[1:]
        selected_metrics_comp = st.multiselect("Select metrics to compare", options=metrics[1:], default=default_metrics)
        if selected_metrics_comp:
            st.plotly_chart(plot_metric_comparison(filtered_df, selected_metrics_comp), use_container_width=True)

    st.header("Detailed Results")
    st.dataframe(filtered_df[['timestamp', 'model_name', 'dataset_name', 'metric_name', 'score']].sort_values("timestamp", ascending=False))
    
    st.sidebar.header("Export")
    if st.sidebar.button("Generate PDF Report"):
        pdf_path = "evaluation_report.pdf"
        generate_pdf_report(filtered_df, pdf_path)
        with open(pdf_path, "rb") as f:
            st.sidebar.download_button("Download PDF", f, "evaluation_report.pdf", "application/pdf")

if __name__ == "__main__":
    main()