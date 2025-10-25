# chart functions to enforce consistent style
import streamlit as st
import missingno as msno
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

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
def crime_type_contribution_by_entity(data):
    """Display crime type contribution by entity involved."""
    st.markdown("### Crime Type Contribution by Entity Involved")

    entities = data['entity_involved'].unique()
    
    if len(entities) <= 3:
        cols = st.columns(len(entities))
    else:
        # For more than 3 entities, use 2 rows
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3] * 2 
    
    for i, entity in enumerate(entities):
        col_index = i % 3 if len(entities) > 3 else i
        
        with cols[col_index]:
            entity_data = get_records_by_entity_type(data, entity)
            
            crime_type_amounts = entity_data.groupby('crime_type')['amount'].sum()
            
            fig = px.pie(
                values=crime_type_amounts.values, 
                names=crime_type_amounts.index,
                title=f"<b>{entity}</b><br><sub>{len(entity_data):,} records</sub>", 
                hole=0.4
            )
            
            fig.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.05,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=9)
                ),
                margin=dict(l=10, r=10, t=80, b=80),
                height=350,
                showlegend=True
            )
            
            fig.update_traces(
                textinfo='percent',
                textposition='inside',
                textfont_size=8
            )
            
            st.plotly_chart(fig, use_container_width=True)
    st.info("""
    💡 **Analysis:**
    - This chart highlights which types of crimes are most frequently reported for each entity involved (Victim, Infraction, Vehicle, Perpetrator).
    - As observed, some types of crimes are only represented by an entity in these records (for example swindle only appears under 'Victim').
    - This suggests that certain entities may be more vulnerable to specific types of crimes, or that cases reported by victims were never pursued further to involve other entities.
    - This highlights the importance of considering the context and relationships between different entities when analyzing crime data.
    """)

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

def overview_metrics(filtered_data):
    """Display overview metrics in a row of columns."""
    st.markdown("#### 📈 Overview Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Records", f"{len(filtered_data):,}")
    with col2:
        regions = filtered_data['Code_region'].nunique()
        st.metric("Regions", f"{regions}")
    with col3:
        departments = filtered_data['Code_department'].nunique()
        st.metric("Departments", f"{departments}")
    with col4:
        years_covered = filtered_data['year'].nunique()
        st.metric("Years Covered", f"{years_covered}")
    with col5:
        crime_types_count = filtered_data['crime_type'].nunique()
        st.metric("Crime Types", f"{crime_types_count}")

def entity_distribution(filtered_data):
    """Display entity type distribution with chart selection."""
    st.markdown("#### 📋 Entity Type Distribution of Records")
    
    entity_counts = filtered_data['entity_involved'].value_counts()
    
    # Check if there's only one entity type after filtering
    if len(entity_counts) <= 1:
        if len(entity_counts) == 1:
            entity_name = entity_counts.index[0]
            entity_count = entity_counts.iloc[0]
            st.info(f"📊 All {entity_count:,} records are of type: **{entity_name}**")
        else:
            st.warning("⚠️ No entity data available with current filters.")
        return
    
    # Only show chart options if we have multiple entities
    chart_type = st.radio("Chart Type", ["Bar Chart", "Donut Chart"], horizontal=True)
    
    if chart_type == "Bar Chart":
        fig = px.bar(x=entity_counts.index, y=entity_counts.values, color=entity_counts.index,
                    title="Records by Entity Type")
        fig.update_layout(xaxis_title="Entity Type", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)
    else:  # Donut Chart
        fig = px.pie(values=entity_counts.values, names=entity_counts.index,
                    title="Records by Entity Type", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    st.info("""
    💡 **Analysis:**
    - This chart shows the distribution of records across different entity types (Victim, Infraction, Vehicle, Perpetrator).
    - A higher count for a specific entity type may indicate that this group is more frequently involved in reported offences, or that certain types of crimes are more likely to be reported by or against that entity.
    - Over the years, Victims consistently represent the majority of records, highlighting their central role in crime reporting.
    """)

def map_records_by_region(filtered_data):
    """Display records by region using Folium with proper DOM-TOM handling."""
    st.markdown("#### 🗺️ Records by Region")
    
    # Check if coordinate columns exist in filtered data
    if 'Region_lat' not in filtered_data.columns or 'Region_lon' not in filtered_data.columns:
        st.error("Geographic coordinate data is missing from the filtered dataset.")
        return
    
    # Remove rows with missing coordinates BEFORE grouping
    filtered_data_with_coords = filtered_data.dropna(subset=['Region_lat', 'Region_lon', 'Region_name'])
    
    if len(filtered_data_with_coords) == 0:
        st.warning("No data with valid coordinates found after filtering.")
        return
    
    # Group by region and preserve coordinates
    dept_data = filtered_data_with_coords.groupby(['Region_name']).agg({
        'amount': 'sum',
        'Region_lat': 'first',  # Take first coordinate value for each region
        'Region_lon': 'first'   # Take first coordinate value for each region
    }).reset_index()
    
    # Rename columns for clarity
    dept_data = dept_data.rename(columns={
        'Region_lat': 'latitude',
        'Region_lon': 'longitude'
    })
    
    # Map selection
    map_choice = st.radio(
        "Select Map View", 
        ["All Territories", "Zoom on Metropolitan France"], 
        horizontal=True
    )
    
    if map_choice == "All Territories":
        zoom_start = 2
    else:
        zoom_start = 6
        
    m = folium.Map(
        location=[46.6034, 1.8883],
        zoom_start=zoom_start, 
        tiles='OpenStreetMap'
    )       
    
    # Add circles to the map
    if len(dept_data) > 0:
        max_amount = dept_data['amount'].max()
        
        for _, row in dept_data.iterrows():
            size = 10 + (row['amount'] / max_amount) * (40)
            
            # Color based on amount (violet scale)
            color_intensity = (row['amount'] / max_amount)
            color = f"rgba({int(221 - 83 * color_intensity)}, {int(160 - 160 * color_intensity)}, {int(221 - 89 * color_intensity)}, 0.8)"
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=size,
                popup=folium.Popup(
                    f"<b>{row['Region_name']}</b><br>"
                    f"Amount: {row['amount']:,.0f}<br>"
                    f"Coordinates: {row['latitude']:.2f}, {row['longitude']:.2f}",
                    max_width=200
                ),
                tooltip=f"{row['Region_name']}: {row['amount']:,.0f}",
                color='pink',
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(m)
    
    st_folium(m, width=700, height=500)
    
    # Show top regions
    if len(dept_data) > 0:
        st.markdown("#### 📊 Top Regions by Amount")
        col1, col2, col3, col4, col5 = st.columns(5)
        top_regions = dept_data.nlargest(5, 'amount')
        for i, (_, row) in enumerate(top_regions.iterrows(), 1):
            if i <= 5:  # Safety check
                with eval(f"col{i}"):
                    st.write(f"**{row['Region_name']}**:")
                    st.write(f"{row['amount']:,.0f}")

    st.info("""
    💡 **Analysis:**
    - This map visualizes the distribution of reported offences across French regions.
    - Larger circles indicate regions with higher amounts of reported offences.
    - Urban regions, particularly in metropolitan France, tend to have larger circles, reflecting higher reporting activity likely due to population density.
    """)

def crime_rate_analysis(filtered_data):
    """Display crime rate analysis for all entity types."""
    st.markdown("#### 🚨 Crime Rate Analysis")
    
    if len(filtered_data) == 0:
        st.warning("⚠️ No data available with current filters for crime rate analysis.")
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_rate = filtered_data['rate_per_1000'].mean()
        st.metric("Average Crime Rate", f"{avg_rate:.2f} per 1,000")
    with col2:
        max_rate = filtered_data['rate_per_1000'].max()
        st.metric("Highest Crime Rate", f"{max_rate:.2f} per 1,000")
    with col3:
        median_rate = filtered_data['rate_per_1000'].median()
        st.metric("Median Crime Rate", f"{median_rate:.2f} per 1,000")

    # Histogram
    st.markdown("**Crime Rate Distribution:**")
    bins = st.slider("Number of bins", 10, 100, 30)
    fig_hist = px.histogram(
        filtered_data, 
        x='rate_per_1000', 
        nbins=bins,
        title="Distribution of Crime Rates (All Entities)", 
        color_discrete_sequence=['steelblue'],
        labels={'rate_per_1000': 'Crime Rate per 1,000 inhabitants'}
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    st.info("""
    💡 **Analysis:**
    - This section analyzes the crime rates (per 1,000 inhabitants) across all entity types and filtered records.
    - The average, highest, and median crime rates provide insights into the overall crime situation.
    - The histogram illustrates the distribution of crime rates, helping identify common rate ranges and potential outliers.
    - Although the majority seems to be of lower rates, there are outliers with significantly higher rates, indicating areas or
             entities with elevated crime reporting. It can be caused by smaller populations or active police/judicial systems.
    """)

def geographic_insights(filtered_data):
    """Display geographic insights with department rankings."""
    st.markdown("#### 🗺️ Geographic Insights")
    
    if len(filtered_data) == 0:
        st.warning("⚠️ No data available with current filters for geographic analysis.")
        return
    
    view_type = st.radio("View", ["Top 10 Departments", "Bottom 10 Departments", "All Departments"], horizontal=True)

    dept_stats = filtered_data.groupby('Department_name')['rate_per_1000'].mean().sort_values(ascending=False)
    
    if view_type == "Top 10 Departments":
        display_data = dept_stats.head(10)
    elif view_type == "Bottom 10 Departments":
        display_data = dept_stats.tail(10)
    else:
        display_data = dept_stats

    fig_geo = px.bar(
        x=display_data.index, 
        y=display_data.values,
        color=display_data.values,
        color_continuous_scale='Reds',
        title=f"{view_type} by Average Deposition Rate"
    )
    
    fig_geo.update_layout(
        xaxis_title="Department Name", 
        yaxis_title="Average Deposition Rate per 1,000",
        showlegend=False
    )
    fig_geo.update_xaxes(tickangle=45) 
    st.plotly_chart(fig_geo, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📈 Highest Rate:**")
        if len(display_data) > 0:
            top_dept = display_data.index[0]
            top_rate = display_data.iloc[0]
            st.write(f"• {top_dept}: {top_rate:.2f} per 1,000")
    
    with col2:
        st.markdown("**📉 Lowest Rate:**")
        if len(display_data) > 0:
            bottom_dept = display_data.index[-1]
            bottom_rate = display_data.iloc[-1]
            st.write(f"• {bottom_dept}: {bottom_rate:.2f} per 1,000")
    
    st.info("""
    💡 **Analysis:**
    - This chart ranks departments based on their average deposition rates (per 1,000 inhabitants) across all entity types.
    - Higher rates indicate more active judicial/police reporting activity in that department.
    - Rates include all crime types and entity perspectives (victims, suspects, vehicles, etc.).
    - Small departments may show higher rates due to population size effects.
    """)

def temporal_trends(data):
    """Display temporal trends analysis."""
    st.markdown("#### 📅 Temporal Trends (regardless of filter)")
    yearly_trends = data.groupby(['year', 'crime_type']).size().reset_index(name='count')
    yearly_trends['amount'] = data.groupby(['year', 'crime_type'])['amount'].sum().values

    # Entity selector for trend
    crime_selector = st.multiselect(
        "Select crime types to show trends",
        yearly_trends['crime_type'].unique(),
        default=yearly_trends['crime_type'].unique().tolist()
    )

    if crime_selector:
        trend_data = yearly_trends[yearly_trends['crime_type'].isin(crime_selector)]
        fig_trend = px.line(trend_data, x='year', y='amount', color='crime_type',
                            title="Temporal Trends by Crime Type")
        st.plotly_chart(fig_trend, use_container_width=True)
    st.info("""
    💡 **Analysis:**
    - This line chart illustrates temporal trends in reported offences across different crime types over the years.
    - Users can select specific crime types to visualize their trends.
    - Observing these trends helps identify whether certain crimes are increasing, decreasing, or remaining stable over time.
    - The trends seem relatively stable overall, with some fluctuations in specific crime types.
    """)

def data_quality(filtered_data):
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

def crime_rate_by_population(filtered_data):
    """Display crime rate analysis in relation to population size for infractions."""
    if 'Infraction' not in filtered_data['entity_involved'].values:
        st.warning("⚠️ No infraction data available with current filters for crime rate analysis.")
        return
    
    infraction_data = get_records_by_entity_type(filtered_data, 'Infraction')
    st.markdown("#### 🚨 Crime Rate Analysis")
    
    dept_analysis = infraction_data.groupby('Department_name').agg({
        'amount': 'sum',           # Total crimes in department
        'population': 'first',     # Population (should be same for each dept)
        'rate_per_1000': 'mean'    # Average crime rate
    }).reset_index()
    
    # Key metrics based on department-level data
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_rate = dept_analysis['rate_per_1000'].mean()
        st.metric("Average Crime Rate", f"{avg_rate:.2f} per 1,000")
    with col2:
        max_rate = dept_analysis['rate_per_1000'].max()
        max_dept = dept_analysis.loc[dept_analysis['rate_per_1000'].idxmax(), 'Department_name']
        st.metric("Highest Crime Rate", f"{max_rate:.2f} per 1,000", delta=max_dept)
    with col3:
        median_rate = dept_analysis['rate_per_1000'].median()
        st.metric("Median Crime Rate", f"{median_rate:.2f} per 1,000")
    
    
    fig_scatter = px.scatter(
        dept_analysis,
        x='population',
        y='rate_per_1000',
        size='amount',
        hover_name='Department_name',
        hover_data={
            'population': ':,.0f',
            'amount': ':,.0f',
            'rate_per_1000': ':.2f'
        },
        title="Crime Rate vs Population Size by Department",
        labels={
            'population': 'Population',
            'rate_per_1000': 'Crime Rate (per 1,000 inhabitants)',
            'amount': 'Total Crimes'
        },
        log_x=True,  # Log scale for better visualization
        size_max=50,
        color='rate_per_1000',
        color_continuous_scale='Reds'
    )
    
    fig_scatter.update_layout(
        xaxis_title="Population (log scale)",
        yaxis_title="Crime Rate (per 1,000 inhabitants)",
        showlegend=False
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Add explanation
    st.info("""
    💡 **How to read this chart:**
    - **X-axis**: Department population (logarithmic scale)
    - **Y-axis**: Crime rate per 1,000 inhabitants
    - **Circle size**: Total number of crimes
    - **Color intensity**: Higher crime rate = darker red
    
    **Key insight**: Large populations don't necessarily mean high crime rates!
    """)

def show_kpis(data):
    """Display comprehensive interactive key performance indicators."""
    st.markdown("### 📊 Key Performance Indicators")
    st.write("Explore key metrics and visualizations to understand reported offences in France.")
    st.write("---")
    crime_type_contribution_by_entity(data)
    st.write("---")
    filtered_data = create_filters(data)
    data_quality(filtered_data)
    st.write("---")
    # Show different sections
    overview_metrics(filtered_data)
    st.write("---")
    entity_distribution(filtered_data)
    st.write("---")
    map_records_by_region(filtered_data)
    st.write("---")
    crime_rate_analysis(filtered_data)
    st.write("---")
    geographic_insights(filtered_data) 
    st.write("---") 
    crime_rate_by_population(filtered_data)
    st.write("---")
    temporal_trends(data)

# --------------------------------------------------------------
# Regional comparison visualization functions
# --------------------------------------------------------------

def region_selection(data):
    """Create region selection and return filtered data."""
    st.markdown("#### 🔧 Region Selection")
    regions = ['All'] + list(data['Region_name'].unique())
    selected_region = st.selectbox("Select Region", regions)
    
    if selected_region != 'All':
        region_data = data[data['Region_name'] == selected_region]
        st.write(f"📊 Showing data for region: **{selected_region}** ({len(region_data):,} records)")
    else:
        region_data = data.copy()
        st.write(f"📊 Showing data for all regions ({len(region_data):,} records)")

    return region_data

def show_deep_drives(data):
    region_data = region_selection(data)
