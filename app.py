import streamlit as st
import pandas as pd
from langchain.chat_models import ChatOpenAI
import tempfile
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the ChatOpenAI model
llm_model = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)

# Title for the Streamlit app
st.title("AI-powered CSV Query Tool")

# Upload CSV files through Streamlit
st.subheader("Upload your CSV Files")
uploaded_files = st.file_uploader("Upload CSV files", accept_multiple_files=True, type=["csv"])

# Check if the user has uploaded the CSV files
if uploaded_files:
    # Inform the user that the agent is being created
    st.write("Creating the CSV agent using the uploaded files...")

    # Save the uploaded files to temporary paths
    csv_paths = []
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            csv_paths.append(temp_file.name)

    # Create the CSV agent using LangChain's agent toolkit
    agent = create_csv_agent(llm_model, path=csv_paths, verbose=True, allow_dangerous_code=True)

    # Input box for asking questions related to the CSV data
    st.subheader("Ask a Question About Your Inventory Data")
    user_query = st.text_input("Enter your question:")

    # Query the agent and display the result when the user inputs a query
    if st.button("Ask"):
        if user_query:
            # Invoke the agent with the user's query
            response = agent.invoke(user_query)
            
            # Display the response
            st.write("### Answer:")
            st.write(response)
        else:
            st.write("Please enter a question to get an answer.")
else:
    st.write("Please upload CSV files to begin querying.")
