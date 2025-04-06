from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from geopy.geocoders import Nominatim
from pydantic import BaseModel, Field
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment. Please check your .env file.")

# Define Agent State
class AgentState(TypedDict):
    """The state of the agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    number_of_steps: int

# Define Weather Tool
geolocator = Nominatim(user_agent="weather-app")

class SearchInput(BaseModel):
    location: str = Field(description="The city and state, e.g., San Francisco")
    date: str = Field(description="the forecasting date for when to get the weather format (yyyy-mm-dd)")

@tool("get_weather_forecast", args_schema=SearchInput, return_direct=True)
def get_weather_forecast(location: str, date: str):
    """Retrieves the weather using Open-Meteo API for a given location (city) and date and summarizes it."""
    location_obj = geolocator.geocode(location)
    if location_obj:
        try:
            response = requests.get(
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={location_obj.latitude}&"
                f"longitude={location_obj.longitude}&"
                f"hourly=temperature_2m&"
                f"start_date={date}&end_date={date}"
            )
            data = response.json()
            hourly_data = list(zip(data["hourly"]["time"], data["hourly"]["temperature_2m"]))

            # Categorize by time
            morning = [temp for time, temp in hourly_data if "06:00" <= time[-5:] <= "11:59"]
            afternoon = [temp for time, temp in hourly_data if "12:00" <= time[-5:] <= "17:59"]
            night = [temp for time, temp in hourly_data if time[-5:] >= "18:00" or time[-5:] < "06:00"]

            def avg(lst): return round(sum(lst) / len(lst), 1) if lst else None

            morning_avg = avg(morning)
            afternoon_avg = avg(afternoon)
            night_avg = avg(night)

            summary = (
                f"🌅 Morning: {morning_avg}°C, "
                f"🌞 Afternoon: {afternoon_avg}°C, "
                f"🌙 Night: {night_avg}°C"
            )

            return summary
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "Location not found"}

# Tools list
tools = [get_weather_forecast]

# Initialize Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=1.0,
    max_output_tokens=300,
    timeout=None,
    max_retries=2,
    google_api_key=api_key,
)

# Bind tools to the model
model = llm.bind_tools(tools)

# Define Nodes
def call_tool(state: AgentState):
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = get_weather_forecast.invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=tool_result,
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}

def call_model(state: AgentState, config: RunnableConfig):
    response = model.invoke(state["messages"], config)
    return {"messages": [response]}

def should_continue(state: AgentState):
    if not state["messages"][-1].tool_calls:
        return "end"
    return "continue"

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("llm", call_model)
workflow.add_node("tools", call_tool)
workflow.set_entry_point("llm")
workflow.add_conditional_edges(
    "llm",
    should_continue,
    {"continue": "tools", "end": END}
)
workflow.add_edge("tools", "llm")
graph = workflow.compile()

# Run the graph
inputs = {"messages": [("user", "How is the weather in Bangalore on 31st of March 2025?")]}

for state in graph.stream(inputs, stream_mode="values"):
    last_message = state["messages"][-1]
    last_message.pretty_print()
