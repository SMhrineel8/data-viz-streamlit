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
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1E3D59;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
    .upload-section {
        text-align: center;
        padding: 2rem;
        border-radius: 1rem;
        background: #f8f9fa;
        margin-bottom: 2rem;
    }
    .button-style {
        background-color: #1E3D59;
        color: white;
        padding: 0.5rem 2rem;
        border-radius: 0.3rem;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">Data Visualization App</h1>', unsafe_allow_html=True)

# Initialize session state for reset functionality
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'df' not in st.session_state:
    st.session_state.df = None

def reset_app():
    st.session_state.uploaded_file = None
    st.session_state.df = None

# Upload section
st.markdown('<h2 class="upload-section">Upload Your File</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    uploaded_file = st.file_uploader("Choose an Excel or CSV file", 
                                   type=['xlsx', 'csv'],
                                   help="Upload your data file in Excel or CSV format")

if uploaded_file is not None:
    try:
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
            
            # Create visualizations
            tab1, tab2, tab3 = st.tabs(["📈 Line Chart", "📊 Bar Chart", "🔄 Scatter Plot"])
            
            with tab1:
                fig_line = px.line(df, x=x_axis, y=y_axis, title=f'{y_axis} over {x_axis}')
                st.plotly_chart(fig_line, use_container_width=True)
                
            with tab2:
                fig_bar = px.bar(df, x=x_axis, y=y_axis, title=f'{y_axis} by {x_axis}')
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with tab3:
                fig_scatter = px.scatter(df, x=x_axis, y=y_axis, title=f'{y_axis} vs {x_axis}')
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Download buttons for visualizations
            def get_image_download_link(fig, filename, text):
                img = fig.to_image(format="png")
                btn = st.download_button(
                    label=text,
                    data=img,
                    file_name=filename,
                    mime="image/png"
                )
                return btn
            
            st.subheader("Download Visualizations")
            col1, col2, col3 = st.columns(3)
            with col1:
                get_image_download_link(fig_line, "line_chart.png", "📥 Download Line Chart")
            with col2:
                get_image_download_link(fig_bar, "bar_chart.png", "📥 Download Bar Chart")
            with col3:
                get_image_download_link(fig_scatter, "scatter_plot.png", "📥 Download Scatter Plot")
                
        else:
            st.warning("No numeric columns found in the dataset for visualization")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        
# Reset button
col1, col2, col3 = st.columns([4,1,4])
with col2:
    if st.button("🔄 Reset", type="primary", use_container_width=True):
        reset_app()
        st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        Made with ❤️ using Streamlit
    </div>
""", unsafe_allow_html=True)
