# chart functions to enforce consistent style
import streamlit as st
import missingno as msno
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import plotly.express as px

# --------------------------------------------------------------
# Intermediate visualization functions
# --------------------------------------------------------------
def get_records_by_entity_type(data, entity_type: str) -> pd.DataFrame:
    """Filter data by 'entity' type."""
    return data[data['entity_involved'] == entity_type]

def get_records_by_crime_type(data, crime_type: str) -> pd.DataFrame:
    """Filter data by 'crime_type'."""
    return data[data['crime_type'] == crime_type]

# --------------------------------------------------------------
# Data preparation visualization functions
# --------------------------------------------------------------
def show_missing_data(data):
    """Display missing data matrix using missingno."""
    st.markdown("### Missing Data Visualization")
    fig, ax = plt.subplots(figsize=(10, 4))
    msno.matrix(data, ax=ax)
    st.pyplot(fig)

def show_duplicates(data):
    """Display number of duplicate rows."""
    st.markdown("### Duplicate Rows")
    num_duplicates = data.duplicated().sum()
    st.write(f"Number of duplicate rows: {num_duplicates}")
    if num_duplicates > 0:
        st.dataframe(data[data.duplicated()])

# --------------------------------------------------------------
# Overview visualization functions
# --------------------------------------------------------------
def create_filters(data):
    """Create interactive filters and return filtered data."""
    st.markdown("#### 🔧 Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        entity_types = ['All'] + list(data['entity_involved'].unique())
        selected_entity = st.selectbox("Entity Type", entity_types)
    
    with col2:
        min_year, max_year = int(data['year'].min()), int(data['year'].max())
        year_range = st.slider("Year Range", min_year, max_year, (min_year, max_year))
    
    with col3:
        crime_types = ['All'] + list(data['crime_type'].unique())
        selected_crime = st.selectbox("Crime Type", crime_types)
    
    # Apply filters
    filtered_data = data.copy()
    if selected_entity != 'All':
        filtered_data = get_records_by_entity_type(filtered_data, selected_entity)
    
    filtered_data = filtered_data[
        (filtered_data['year'] >= year_range[0]) & 
        (filtered_data['year'] <= year_range[1])
    ]
    
    if selected_crime != 'All':
        filtered_data = get_records_by_crime_type(filtered_data, selected_crime)
    
    # Show filter impact
    if len(filtered_data) != len(data):
        st.info(f"📊 Showing {len(filtered_data):,} records (filtered from {len(data):,})")
    
    return filtered_data

def show_overview_metrics(filtered_data):
    """Display overview metrics in a row of columns."""
    st.markdown("#### 📈 Overview Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Records", f"{len(filtered_data):,}")
    with col2:
        regions = filtered_data['Code_region'].nunique()
        st.metric("Regions", f"{regions}")
    with col3:
        departments = filtered_data['Code_departement'].nunique()
        st.metric("Departments", f"{departments}")
    with col4:
        years_covered = filtered_data['year'].nunique()
        st.metric("Years Covered", f"{years_covered}")
    with col5:
        crime_types_count = filtered_data['crime_type'].nunique()
        st.metric("Crime Types", f"{crime_types_count}")

def show_entity_distribution(filtered_data):
    """Display entity type distribution with chart selection."""
    st.markdown("#### 📋 Entity Type Distribution")
    
    chart_type = st.radio("Chart Type", ["Bar Chart", "Donut Chart"], horizontal=True)
    entity_counts = filtered_data['entity_involved'].value_counts()
    
    if chart_type == "Bar Chart":
        fig = px.bar(x=entity_counts.index, y=entity_counts.values, color=entity_counts.index,
                    title="Records by Entity Type")
        fig.update_layout(xaxis_title="Entity Type", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)
    else:  # Donut Chart
        fig = px.pie(values=entity_counts.values, names=entity_counts.index,
                    title="Records by Entity Type", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

def show_crime_rate_analysis(filtered_data):
    """Display crime rate analysis for infractions only."""
    if 'Infraction' not in filtered_data['entity_involved'].values:
        return
    
    infraction_data = get_records_by_entity_type(filtered_data, 'Infraction')
    st.markdown("#### 🚨 Crime Rate Analysis")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_rate = infraction_data['rate_per_1000'].mean()
        st.metric("Average Crime Rate", f"{avg_rate:.2f} per 1,000")
    with col2:
        max_rate = infraction_data['rate_per_1000'].max()
        st.metric("Highest Crime Rate", f"{max_rate:.2f} per 1,000")
    with col3:
        median_rate = infraction_data['rate_per_1000'].median()
        st.metric("Median Crime Rate", f"{median_rate:.2f} per 1,000")
    
    # Histogram
    st.markdown("**Crime Rate Distribution:**")
    bins = st.slider("Number of bins", 10, 100, 100)
    fig_hist = px.histogram(infraction_data, x='rate_per_1000', nbins=bins,
                           title="Distribution of Crime Rates", 
                           color_discrete_sequence=['steelblue'])
    st.plotly_chart(fig_hist, use_container_width=True)

def show_geographic_insights(data):
    """Display geographic insights with department rankings."""
    st.markdown("#### 🗺️ Geographic Insights")
    
    view_type = st.radio("View", ["Top 10 Departments", "Bottom 10 Departments", "All Departments"], horizontal=True)
    dept_stats = get_records_by_entity_type(data, 'Infraction').groupby('Code_departement')['rate_per_1000'].mean().sort_values(ascending=False)
    
    if view_type == "Top 10 Departments":
        display_data = dept_stats.head(10)
    elif view_type == "Bottom 10 Departments":
        display_data = dept_stats.tail(10)
    else:
        display_data = dept_stats

    # Map department codes to names
    dept_code_to_name = data[['Code_departement', 'Departement_name']].drop_duplicates().set_index('Code_departement')['Departement_name'].to_dict()
    dept_names = [dept_code_to_name.get(code, code) for code in display_data.index]

    fig_geo = px.bar(x=dept_names, y=display_data.values, 
                    title=f"{view_type} by Average Crime Rate")
    fig_geo.update_layout(xaxis_title="Department Name", yaxis_title="Average Rate per 1,000")
    fig_geo.update_xaxes(tickangle=45) 
    st.plotly_chart(fig_geo, use_container_width=True)

def show_temporal_trends(data):
    """Display temporal trends analysis."""
    st.markdown("#### 📅 Temporal Trends")
    yearly_trends = data.groupby(['year', 'crime_type']).size().reset_index(name='count')
    yearly_trends['amount'] = data.groupby(['year', 'crime_type'])['amount'].sum().values

    # Entity selector for trend
    crime_selector = st.multiselect(
        "Select crime types to show trends",
        yearly_trends['crime_type'].unique(),
        default=yearly_trends['crime_type'].unique()[:4]
    )

    if crime_selector:
        trend_data = yearly_trends[yearly_trends['crime_type'].isin(crime_selector)]
        fig_trend = px.line(trend_data, x='year', y='amount', color='crime_type',
                            title="Temporal Trends by Crime Type")
        st.plotly_chart(fig_trend, use_container_width=True)

def show_data_quality(filtered_data):
    """Display data quality information in an expandable section."""
    with st.expander("✅ Data Quality Details", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            missing_by_col = filtered_data.isnull().sum()
            if missing_by_col.sum() > 0:
                st.write("**Missing Values by Column:**")
                st.dataframe(missing_by_col[missing_by_col > 0])
            else:
                st.success("No missing values!")
                
        with col2:
            duplicates = filtered_data.duplicated().sum()
            st.metric("Duplicates", f"{duplicates:,}")
            if duplicates > 0:
                if st.button("Show duplicate rows"):
                    st.dataframe(filtered_data[filtered_data.duplicated()])

def show_kpis(data):
    """Display comprehensive interactive key performance indicators."""
    st.markdown("### 📊 Key Performance Indicators")
    
    # Create filters and get filtered data
    filtered_data = create_filters(data)
    
    # Show different sections
    show_overview_metrics(filtered_data)
    show_entity_distribution(filtered_data)
    show_crime_rate_analysis(filtered_data)
    show_geographic_insights(data)  
    show_temporal_trends(data)      
    show_data_quality(filtered_data)
