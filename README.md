# 🌦️ ReAct Agent: Weather Forecast Assistant

This project is a smart, conversational **Weather Forecast Assistant** built using **LangChain**, **LangGraph**, **Google Gemini (GenAI)**, and the **Open-Meteo API**. It uses the **ReAct (Reason + Act)** framework to combine reasoning with real-time tool usage, mimicking how a human assistant would retrieve and summarize weather data.

---

## 🚀 Features

- 🌍 Understands natural language queries like:
  > *"What will the weather be in Bangalore on March 31st, 2025?"*

- 🔧 Uses tool calling to fetch real-time weather forecasts

- 🧠 Uses LLMs for intelligent summarization and reasoning

- 📅 Categorizes temperatures into:
  - 🌅 Morning
  - 🌞 Afternoon
  - 🌙 Night

- 🤖 Powered by a **ReAct Agent**, combining LLM reasoning with tool usage

---

## 🧠 What is a ReAct Agent?

**ReAct** (Reason + Act) agents allow an LLM to:
- Think step-by-step through a problem
- Decide when to use a tool (API, database, etc.)
- Use the result to make an informed response

This makes the system highly interactive and intelligent, perfect for real-world applications like weather forecasting, document Q&A, search assistants, etc.

---

## 🛠 Tech Stack

| Technology        | Purpose                        |
|-------------------|--------------------------------|
| `LangChain`       | LLM orchestration and tools    |
| `LangGraph`       | Agent workflow and control flow|
| `Gemini 2.0 Flash`| LLM reasoning (Google GenAI)   |
| `Open-Meteo API`  | Weather forecast data          |
| `Geopy`           | Geolocation (lat/lon lookup)   |
| `Python`          | Backend & agent development    |

---

## 📦 Installation

```bash
git clone https://github.com/SAIK27M/weather-react-agent.git
cd weather-react-agent
pip install -r requirements.txt


Create a .env file in the root directory:
GEMINI_API_KEY=your_google_gemini_api_key

▶️ Run the Project:
streamlit run app.py

