import streamlit as st
import pandas as pd
from langchain.chat_models import ChatOpenAI
import tempfile
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from dotenv import load_dotenv
import os
import tabulate
import pandas as pd
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
# Import create_csv_agent from langchain_experimental.agents instead of langchain.agents
from langchain_experimental.agents import create_csv_agent 
from langchain.agents.agent_types import AgentType

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API")
# Title for the Streamlit app
st.title("AI-powered CSV Query Tool")

dtype = {
    'column_name_1': 'str',  # Specify the column data type
    'column_name_2': 'float',
    # Add more columns here as necessary
}

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
    # agent = create_csv_agent(llm_model, path=csv_paths, verbose=True, allow_dangerous_code=True, pandas_kwargs={'encoding': 'latin-1'})
    print("path: ", csv_paths)
    csv_agent = create_csv_agent(
        ChatOpenAI(temperature=0.7, model="gpt-4o", openai_api_key=OPENAI_API_KEY),
        csv_paths,
        verbose=True,
        stop=["\nObservation:"],
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors=True,
        allow_dangerous_code=True,
        pandas_kwargs={
            'na_filter': False,  # Disable filtering of missing values
            'low_memory': False,
            'encoding': 'latin-1'
            }
    )

    # Input box for asking questions related to the CSV data
    st.subheader("Ask a Question about the CSV Data")
    user_query = st.text_area("Enter your question:")

    # Query the agent and display the result when the user inputs a query
    if st.button("Ask"):
        if user_query:
            # Invoke the agent with the user's query
            response = csv_agent.run(user_query)
            
            # Display the response
            st.write("### Answer:")
            st.write(response)
        else:
            st.write("Please enter a question to get an answer.")
else:
    st.write("Please upload CSV files to begin querying.")
