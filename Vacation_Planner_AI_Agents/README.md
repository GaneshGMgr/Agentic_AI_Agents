# 🧠✈️ Agentic AI-Based Vacation Planner

## 📝 Brief

This is a simple AI-based **vacation planner** powered by **Agentic AI** concepts using langgraph. The goal is to build an intelligent assistant that can help users plan their vacations end-to-end using real-time data and smart planning capabilities.

---

## 🛠️ What We Are Building

1. 🌤️ Real-time weather information (OpenWeatherMap API)
2. 🗺️ Attractions and activities finder (Google Places / Foursquare)
3. 🏨 Hotel cost estimation
4. 💱 Currency conversion (Exchange Rate API)
5. 📅 Itinerary planning with day-wise suggestions
6. 💰 Total expense calculation
7. 🧾 Generate a final summary (trip brief + recommendations)

---

## 📚 Resources

- [OpenAI API](https://platform.openai.com/)
- [OpenWeatherMap API](https://home.openweathermap.org/api_keys)
- [Google Map(Places) API](https://console.cloud.google.com/projectselector2/apis/dashboard?inv=1&invt=Ab2OmQ&supportedpurview=project)
- [Foursquare Places API](https://foursquare.com/developers/home)
- [ExchangeRate API](https://app.exchangerate-api.com/keys/added)
- [Groq Cloud API](https://console.groq.com/keys)

---

## ⚙️ Setup Instructions

1. **Initialize the environment with UV (a fast Python package manager):**

   ```bash
   uv init
   ```

2. **List available Python versions (optional):**

   ```bash
   uv python list
   ```

3. **Install Python 3.11.12 via UV:**

   ```bash
   uv python install cpython-3.11.12
   ```

4. **Create a virtual environment:**

   ```bash
   uv venv -p cpython-3.11.12 .venv
   ```

5. **Activate the virtual environment (Windows):**

   ```bash
   .venv\Scripts\activate
   ```

6. **Check installed packages:**

   ```bash
   uv pip list
   ```

7. **Install dependencies:**

   ```bash
   uv pip install -r requirements.txt
   or
   uv pip freeze > requirements.lock.txt
   ```

8. **Save your folder structure for reference:**
   ```bash
   tree /F > folder_structure.txt
   ```
9. **Run your Streamlit frontend app:**

   ```bash
   streamlit run streamlit_app.py
   ```

10. **Run your FastAPI backend server:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

---

## 📌 Notes

- Make sure you have all required **API keys** stored securely (e.g., in a `.env` file).
- This project may use **agent-based planning**, meaning multiple AI components (agents) work together to complete tasks like booking, planning, and summarizing.
- The project is modular and allows you to expand on each task using different APIs or models.

---

## ✅ Goals

- Make vacation planning as seamless as talking to a human travel agent.
- Use multiple tools and agents to collaborate and gather real-time, personalized info.
- Make it fun, useful, and intuitive for users!

---

## Some API KEY required

OPENAI_API_KEY="" # API key for OpenAI (ChatGPT, GPT-4, etc.)
GROQ_API_KEY="" # API key for Groq (if available – not always public or free)
GOOGLE_API_KEY="" # API key to access models from Google AI Studio
GPLACES_API_KEY="" # API key to fetch real-time places from Google Maps
FOURSQUARE_API_KEY="" # Alternative to Google Places API – for place search
TAVILAY_API_KEY="" # API for real-time information from the internet (check service availability)
OPENWEATHERMAP_API_KEY="" # API for current weather information
EXCHANGE_RATE_API_KEY="" # API to get currency exchange rates

Happy building! 🌍🧳🚀
