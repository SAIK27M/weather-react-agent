import streamlit as st
from main import graph  # make sure main.py is in the same folder

st.set_page_config(page_title="🌤️ Weather Assistant", page_icon="⛅", layout="centered")

st.title("🌤️ Weather Forecast Assistant")
st.markdown("Ask about the weather in any city for a specific date.")

# Get user input
user_query = st.text_input("Enter your query", placeholder="e.g. What's the weather in Paris on 2025-04-10?")

# Button to submit
if st.button("Get Forecast"):
    if user_query:
        with st.spinner("🤖 Thinking..."):
            try:
                # Prepare input
                inputs = {"messages": [("user", user_query)]}

                # Stream the LangGraph response
                for state in graph.stream(inputs, stream_mode="values"):
                    last_message = state["messages"][-1]
                    # st.markdown("### 🤖 Assistant")
                    if isinstance(last_message.content, dict):
                        st.json(last_message.content)
                    else:
                        st.write(last_message.content)
            except Exception as e:
                st.error(f" Error: {str(e)}")
    else:
        st.warning("Please enter a valid query.")
