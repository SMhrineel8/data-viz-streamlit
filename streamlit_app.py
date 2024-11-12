import streamlit as st
import pandas as pd
import plotly.express as px
import io
import base64

# Page config
st.set_page_config(page_title="Data Visualization App", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2C3E50;
        padding: 2rem;
        background: linear-gradient(135deg, #E3F2FD, #BBDEFB, #90CAF9);
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .upload-section {
        text-align: center;
        padding: 3rem;
        border-radius: 1rem;
        background: linear-gradient(45deg, #E8F5E9, #C8E6C9, #A5D6A7);
        margin: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        background-color: #2196F3;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">Data Visualization App</h1>', unsafe_allow_html=True)

# Initialize session state
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'df' not in st.session_state:
    st.session_state.df = None

def reset_app():
    st.session_state.uploaded_file = None
    st.session_state.df = None

# Only show upload section if no file is uploaded
if st.session_state.df is None:
    # Upload section with gradient background
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose an Excel or CSV file", 
                                   type=['xlsx', 'csv'],
                                   help="Drag and drop or click to browse")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Show reset button at top when file is uploaded
    col1, col2, col3 = st.columns([4,1,4])
    with col2:
        if st.button("🔄 Reset", type="primary", use_container_width=True):
            reset_app()
            st.experimental_rerun()

if uploaded_file is not None:
    try:
        # Read the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.session_state.df = df
        
        # Data Preview Section
        st.subheader("Data Preview")
        st.dataframe(df.head(), use_container_width=True)
        
        # Visualization Section
        st.subheader("Visualizations")
        
        # Select columns for visualization
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                x_axis = st.selectbox('Select X-axis', df.columns)
            with col2:
                y_axis = st.selectbox('Select Y-axis', numeric_cols)
            
            # Create visualizations with custom colors
            tab1, tab2, tab3 = st.tabs(["📈 Line Chart", "📊 Bar Chart", "🔄 Scatter Plot"])
            
            color_sequence = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD']
            
            with tab1:
                fig_line = px.line(df, x=x_axis, y=y_axis, 
                                 title=f'{y_axis} over {x_axis}',
                                 color_discrete_sequence=color_sequence)
                st.plotly_chart(fig_line, use_container_width=True)
                
            with tab2:
                fig_bar = px.bar(df, x=x_axis, y=y_axis, 
                                title=f'{y_axis} by {x_axis}',
                                color_discrete_sequence=color_sequence)
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with tab3:
                fig_scatter = px.scatter(df, x=x_axis, y=y_axis, 
                                       title=f'{y_axis} vs {x_axis}',
                                       color_discrete_sequence=color_sequence)
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Download buttons for visualizations
            st.subheader("Download Visualizations")
            col1, col2, col3 = st.columns(3)
            
            # Using native plotly save
            for fig in [fig_line, fig_bar, fig_scatter]:
                fig.write_image("temp.png")
            
            with col1:
                with open("temp.png", "rb") as file:
                    btn = st.download_button(
                        label="📥 Download Line Chart",
                        data=file,
                        file_name="line_chart.png",
                        mime="image/png"
                    )
            with col2:
                with open("temp.png", "rb") as file:
                    btn = st.download_button(
                        label="📥 Download Bar Chart",
                        data=file,
                        file_name="bar_chart.png",
                        mime="image/png"
                    )
            with col3:
                with open("temp.png", "rb") as file:
                    btn = st.download_button(
                        label="📥 Download Scatter Plot",
                        data=file,
                        file_name="scatter_plot.png",
                        mime="image/png"
                    )
                
        else:
            st.warning("No numeric columns found in the dataset for visualization")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Update requirements.txt with:
# streamlit
# pandas
# plotly
# openpyxl
# kaleido
