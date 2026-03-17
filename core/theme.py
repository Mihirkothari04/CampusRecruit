import streamlit as st

def apply_theme():
    """Injects custom CSS to upgrade the Streamlit application UI."""
    custom_css = """
    <style>
        /* Import Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Global Typography and Backgrounds */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Sidebar Styling - Glassmorphism attempt */
        [data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.8) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255,255,255,0.05);
        }

        /* Buttons Styling (Primary) */
        button[kind="primary"] {
            background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.4), 0 2px 4px -1px rgba(99, 102, 241, 0.2) !important;
            transition: all 0.3s ease !important;
            font-weight: 500 !important;
        }
        button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.5), 0 4px 6px -2px rgba(99, 102, 241, 0.3) !important;
        }

        /* Buttons Styling (Secondary/Default) */
        button[kind="secondary"] {
            background-color: rgba(30, 41, 59, 0.6) !important;
            color: #F8FAFC !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            transition: all 0.3s ease !important;
        }
        button[kind="secondary"]:hover {
            border-color: #6366F1 !important;
            color: #6366F1 !important;
        }

        /* Metric Cards / Standard Cards - Glassmorphism */
        div[data-testid="stMetric"], div[data-testid="stContainer"] {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1rem;
            backdrop-filter: blur(8px);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        /* Make containers look slightly elevated */
        div[data-testid="stContainer"]:hover {
            border-color: rgba(99, 102, 241, 0.3);
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.2);
        }
        
        /* Metric Text Coloring */
        div[data-testid="stMetricValue"] {
            color: #E2E8F0 !important;
            font-weight: 700 !important;
            font-size: 2.2rem !important;
        }
        div[data-testid="stMetricLabel"] {
            color: #94A3B8 !important;
            font-size: 0.9rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Headers and Typography */
        h1, h2, h3 {
            background: linear-gradient(135deg, #F8FAFC 0%, #94A3B8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }
        
        /* Progress Bars styling */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 100%) !important;
            border-radius: 10px;
        }

        /* Expander headers */
        .streamlit-expanderHeader {
            background-color: transparent !important;
            border-bottom: 1px solid rgba(255,255,255,0.05) !important;
            font-weight: 500 !important;
        }
        
        /* Dataframes styling */
        [data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        /* Status/Toast popups */
        .stToast {
            background-color: #1E293B !important;
            border: 1px solid #6366F1 !important;
            color: white !important;
        }
        
        /* Inputs styling */
        input, select, textarea {
            background-color: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border-radius: 6px !important;
        }
        input:focus, select:focus, textarea:focus {
            border-color: #6366F1 !important;
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
