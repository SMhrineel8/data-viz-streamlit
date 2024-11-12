import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Data Visualization Dashboard", layout="wide")

# Title
st.title("📊 Interactive Data Dashboard")

# Generate sample data
def generate_sample_data():
    data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'] * 2,
        'Year': ['2023'] * 6 + ['2024'] * 6,
        'Sales': [4200, 4800, 5200, 4900, 5700, 6000, 
                 4500, 5100, 5800, 5200, 6100, 6400],
        'Customers': [350, 380, 420, 390, 450, 470,
                     380, 410, 440, 420, 480, 510],
        'Category': ['Electronics'] * 3 + ['Clothing'] * 3 + 
                   ['Home Goods'] * 3 + ['Books'] * 3
    }
    return pd.DataFrame(data)

df = generate_sample_data()

# Sidebar filters
st.sidebar.header('Filters')
year_filter = st.sidebar.multiselect('Select Year', options=df['Year'].unique(), default=df['Year'].unique())
category_filter = st.sidebar.multiselect('Select Category', options=df['Category'].unique(), default=df['Category'].unique())

# Filter data
filtered_df = df[df['Year'].isin(year_filter) & df['Category'].isin(category_filter)]

# Create two columns
col1, col2 = st.columns(2)

# Sales Trend Line Chart
with col1:
    st.subheader("Monthly Sales Trend")
    fig_line = px.line(filtered_df, x='Month', y='Sales', color='Year',
                      title='Sales Performance Over Time')
    st.plotly_chart(fig_line, use_container_width=True)

# Category Bar Chart
with col2:
    st.subheader("Sales by Category")
    fig_bar = px.bar(filtered_df.groupby('Category')['Sales'].sum().reset_index(), 
                     x='Category', y='Sales',
                     title='Total Sales by Category')
    st.plotly_chart(fig_bar, use_container_width=True)

# Key Metrics
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    total_sales = filtered_df['Sales'].sum()
    st.metric("Total Sales", f"${total_sales:,.0f}")

with col2:
    avg_sales = filtered_df['Sales'].mean()
    st.metric("Average Monthly Sales", f"${avg_sales:,.0f}")

with col3:
    total_customers = filtered_df['Customers'].sum()
    st.metric("Total Customers", f"{total_customers:,}")

# Correlation Scatter Plot
st.subheader("Sales vs Customers Correlation")
fig_scatter = px.scatter(filtered_df, x='Customers', y='Sales', color='Category',
                        size='Sales', hover_data=['Month', 'Year'],
                        title='Sales vs Number of Customers')
st.plotly_chart(fig_scatter, use_container_width=True)
