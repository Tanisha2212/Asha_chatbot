import streamlit as st

# Color definitions - Brightened and more balanced color scheme
PURPLE_PRIMARY = "#7D3E81"  # Slightly lighter purple
LIGHT_GREEN = "#89C76F"     # Keep the bright green 
DARK_PURPLE = "#5F3163"     # Lightened background color
LIGHT_PURPLE = "#F0E5F0"    # Light purple for contrast areas
DARK_TEXT = "#121212"       # Nearly black text
LIGHT_TEXT = "#FFFFFF"      # White text
LIGHT_GRAY = "#E0E0E0"      # Light gray for subtle elements
BORDER_COLOR = "#8A5082"    # Border color for elements

# HTML snippets
HEADER_HTML = f"""
<div class="header">
    <img src="https://static.ambitionbox.com/assets/v2/images/rs:fit:200:200:false:false/bG9jYWw6Ly8vbG9nb3Mvb3JpZ2luYWxzL2pvYnNmb3JoZXIuanBn.png" width="60" style="margin-right: 20px;">
    <div>
        <h1 class="app-title">Asha</h1>
        <p style="color:{LIGHT_GREEN}; font-size:1.2rem; margin-top:0;">Your AI Career Assistant</p>
    </div>
</div>
"""

WELCOME_CARD_HTML = """
<div class="welcome-card">
    <h2>Welcome to Asha!</h2>
    <p>I'm your dedicated career assistant focused on women's professional development. Ask me about:</p>
    <ul>
        <li>Career guidance and opportunities</li>
        <li>Professional development resources</li>
        <li>Mentorship programs</li>
        <li>Industry-specific advice</li>
    </ul>
</div>
"""

SIDEBAR_ABOUT_HTML = """
<div class="sidebar-card">
    <h3 style="color: #89C76F;">About Asha</h3>
    <p>Asha is an AI assistant designed to help women navigate their professional journeys with confidence and clarity.</p>
</div>
"""

FOOTER_HTML = """
<div class="footer">
    <p>© 2025 Asha - Women Empowerment Chatbot | Powered by HerKey</p>
</div>
"""

def apply_custom_css():
    """Apply the custom CSS styling to the Streamlit app."""
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: #F5F0F6;
        color: #333333;
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }}
    
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        flex: 1;
    }}
    
    h1, h2, h3 {{
        color: {PURPLE_PRIMARY};
        font-weight: bold;
    }}
    
    .stButton>button {{
        background-color: #7D3E81;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s;
        font-weight: bold;
    }}
    
    .stButton>button:hover {{
        background-color: {LIGHT_GREEN};
        color: {DARK_TEXT};
    }}
    
    .feedback-btn-positive {{
        background-color: {LIGHT_GREEN} !important;
        color: {DARK_TEXT} !important;
    }}
    
    .feedback-btn-negative {{
        background-color: #FF6B6B !important;
        color: white !important;
    }}
    
    .user-message {{
        background-color: white;
        color: #333333;
        border-radius: 15px 15px 0 15px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.05);
    }}
    
    .assistant-message {{
        background-color: white;
        color: #333333;
        border-radius: 15px 15px 15px 0;
        padding: 15px;
        margin-bottom: 10px;
     
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.05);
    }}
    
    .sources {{
        font-size: 0.8rem;
        color: #666666;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid #EBEBEB;
    }}
    
    /* Fix for the chat input background */
    .stChatInput {{
        background-color: white !important;
    }}
    
    .stChatInput>div {{
        background-color: white !important;
    }}
    .stChatInput textarea::placeholder {{
    color: #888888 !important;
    opacity: 1 !important;
}}
    .stChatInput textarea {{
        background-color: white !important;
        color: #333333 !important;
       
        border-radius: 20px !important;
    }}
    
    /* Additional styling for all input elements */
    input, textarea, div[data-baseweb="input"] {{
        background-color: white !important;
    }}
    
    /* Style for the chat input container */
    .element-container:has(.stChatInput) {{
        background-color: white !important;
        border-radius: 20px;
        padding: 5px;
        border: 1px solid #E0E0E0;
    }}
    
    .footer {{
        text-align: center;
        padding: 15px 0;
        color: #666666;
        font-size: 0.8rem;
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(245, 240, 246, 0.9);
        border-top: 1px solid #E0E0E0;
        z-index: 1000;
    }}
    
    .refresh-button {{
        position: absolute;
        top: 20px;
        right: 20px;
    }}
    
    .stats-card {{
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #EBEBEB;
    }}
    
    .stats-value {{
        font-size: 1.5rem;
        font-weight: bold;
        color: {LIGHT_GREEN};
    }}
    
    .stats-label {{
        font-size: 0.8rem;
        color: #666666;
    }}
    
    .welcome-card {{
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 30px;
        border-left: 5px solid {LIGHT_GREEN};
        color: #333333;
    }}
    
    .sidebar-card {{
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #EBEBEB;
    }}
    
    .header {{
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        border-bottom: 2px solid {LIGHT_GREEN};
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }}
    
    .app-title {{
        color: {PURPLE_PRIMARY};
        margin: 0;
        font-size: 2.2rem;
        font-weight: bold;
    }}
    
    .stMarkdown a {{
        color: {PURPLE_PRIMARY};
        text-decoration: none;
        font-weight: bold;
    }}
    
    .stMarkdown a:hover {{
        text-decoration: underline;
    }}
    
    .st-emotion-cache-16txtl3 {{
        padding: 3rem 1rem 1.5rem;
    }}
    
    /* Add padding at the bottom to prevent content from being hidden behind the footer */
    .main {{
        padding-bottom: 60px;
    }}
    
  
    </style>
    """, unsafe_allow_html=True)