# === streamlit_app.py ===
import streamlit as st
import requests
import datetime
from utils.config_loader import load_config
import os

BASE_URL = "http://localhost:8000"  # Backend API

st.set_page_config(
    page_title="✈️ Travel Planner AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Enhanced CSS Theme
st.markdown("""
    <style>
        :root {
            --primary: #4A90E2;
            --secondary: #7B68EE;
            --accent: #FF6F61;
            --bg-dark: #1e1e2f;
            --bg-gradient: linear-gradient(135deg, #1e1e2f, #2c3e50);
            --card-gradient: linear-gradient(135deg, #2c3e50, #3b3b5c);
            --text-light: #f0f0f0;
            --text-muted: #aaaaaa;
        }

        html, body, [class*="css"] {
            background: var(--bg-gradient) !important;
            color: var(--text-light);
            font-family: 'Segoe UI', sans-serif;
        }

        .stTextInput input {
            border-radius: 20px;
            padding: 12px 18px;
            border: 1px solid var(--primary);
            background-color: #f9f9f9;
            color: #333;
        }

        .stTextInput input::placeholder {
            color: #666;
            font-style: italic;
        }

        .stButton>button {
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            color: white;
            padding: 12px 25px;
            border-radius: 20px;
            border: none;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background: linear-gradient(45deg, var(--secondary), var(--primary));
            transform: scale(1.03);
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }

        .travel-card {
            background: var(--card-gradient);
            border-radius: 18px;
            padding: 30px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            margin: 20px 0;
            transition: all 0.3s ease-in-out;
        }

        .travel-card:hover {
            background: linear-gradient(135deg, #3b3b5c, #4a4a7f);
            transform: translateY(-2px);
        }

        .title {
            color: var(--primary);
            font-size: 36px;
            font-weight: bold;
        }

        .subtitle {
            color: var(--text-muted);
            font-size: 18px;
            margin-top: -10px;
        }

        .header-text {
            color: var(--text-light);
            font-size: 24px;
            font-weight: bold;
        }

        .divider {
            border-top: 2px dashed var(--primary);
            margin: 20px 0;
        }

        .timestamp {
            font-size: 14px;
            color: var(--text-muted);
            text-align: right;
        }

        .footer-note {
            font-size: 13px;
            text-align: center;
            color: var(--text-muted);
        }
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.image(os.path.join("media", "logo.jpeg"), width=70)
with col2:
    st.markdown("<div class='title'>✈️ Travel Planner AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Plan your perfect trip with elegance and ease</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Prompt Card
st.markdown("""
    <div class='travel-card'>
        <div class='header-text'>Where would you like to go?</div>
        <p class='subtitle'>Let us craft your ideal journey with personalized travel plans and smart budgets.</p>
    </div>
""", unsafe_allow_html=True)

# Load models from config
model_config = load_config()
llm_models = model_config.get("llm", {})
model_options = list(llm_models.keys())
default_model = "ollama-llama3" if "ollama-llama3" in model_options else model_options[0]
selected_model = st.selectbox("Select Model Provider", model_options, index=model_options.index(default_model))

# Input Form
with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input(
        "Enter your travel request",
        placeholder="e.g. Plan a luxury 5-day trip to Bali with spa resorts",
        key="user_input"
    )
    submit_button = st.form_submit_button("Generate Travel Plan ✈️")

# Backend Call
if submit_button and user_input.strip():
    try:
        with st.spinner("🚀 Planning your journey..."):
            payload = {
                "question": user_input,
                "model": selected_model
            }
            response = requests.post(f"{BASE_URL}/query", json=payload)

        if response.status_code == 200:
            result = response.json()
            answer = result.get("answer", "No answer returned.")
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": answer})

            st.markdown(f"""
                <div class='travel-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                        <div class='header-text'>🧽 Your Travel Itinerary</div>
                        <div class='timestamp'>{datetime.datetime.now().strftime('%b %d, %Y at %I:%M %p')}</div>
                    </div>
                    <div class='divider'></div>
                    <div style='margin: 20px 0; line-height: 1.8; color: var(--text-light);'>
                        {answer}
                    </div>
                    <div class='divider'></div>
                    <div class='footer-note'>
                        🛃 Generated by Travel Planner AI. Please confirm local info and prices before you book.
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Optional: Display Graph Image
            if "graph_image" in result and os.path.exists(result["graph_image"]):
                st.image(result["graph_image"], caption="LangGraph Flowchart")

        else:
            st.error("⚠️ The travel agent couldn’t respond. Please try again later.")

    except Exception as e:
        st.error(f"🚨 Error: {str(e)}")