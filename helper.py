import streamlit as st
import pandas as pd
import os
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_deepseek import ChatDeepSeek # Assuming deepseek-python provides this
from langchain_core.messages import HumanMessage, AIMessage
import re # For parsing agent output
import json # Import json
import tabulate


def load_data(uploaded_file):
    """Loads data from an uploaded file into a pandas DataFrame."""
    try:
        # Assuming CSV for simplicity, could add more formats
        # Use pandas read_csv with error handling
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        return f"Error loading file: {e}"

def get_llm(llm_name):
    """Initializes and returns the chosen LLM."""
    if llm_name == "OpenAI":
        api_key = st.secrets.get("OAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        # Use gpt-4o or gpt-4-turbo for better performance with agents
        return ChatOpenAI(model="gpt-4o", api_key=api_key, temperature=0)
    elif llm_name == "Google Gemini":
        api_key = st.secrets.get("GEM_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        # Use a suitable Gemini model
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17", google_api_key=api_key, temperature=0)
    elif llm_name == "DeepSeek":
        api_key = st.secrets.get("DEEP_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables.")
        # Use a suitable DeepSeek model
        return ChatDeepSeek(model="deepseek-coder", api_key=api_key, temperature=0) # deepseek-coder or deepseek-chat
    else:
        raise ValueError(f"Unknown LLM: {llm_name}")

def run_dataframe_agent(df, llm_name, query, prefix, suffix):
    """
    Runs the LangChain Pandas DataFrame agent with the given query and LLM.
    Expects and parses a JSON output from the agent.
    """
    try:
        llm = get_llm(llm_name)

        # Create the agent
        # We use handle_parsing_errors=True to make it more robust
        agent = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True, # Keep verbose to help debug
            agent_executor_kwargs={"handle_parsing_errors": True},
            allow_dangerous_code=True,
            # Include necessary tools if needed, but python_repl_ast is default
        )

        # Construct the full prompt
        # Pass df_head to the prefix for context
        full_prompt = f"{prefix}\n\n{query}\n\n{suffix}"

        # Run the agent
        # The agent's final output should be the JSON string as per the suffix prompt
        response = agent.invoke({"input": full_prompt})
        output_text = response.get('output', str(response)) # Get the output string

        # --- Parsing the JSON output ---
        # Look for the JSON block indicated by ```json ... ```
        json_match = re.search(r"```json\n(.*?)\n```", output_text, re.DOTALL)
        # json_match = json.loads(output_text)


        if not json_match:
            # If no JSON block is found, it means the LLM failed to follow instructions
            return {
                "error": "LLM failed to produce the expected JSON output format.",
                "raw_output": output_text # Include raw output for debugging
            }

        json_string = json_match.group(1).strip()

        try:
            # Parse the JSON string
            parsed_output = json.loads(json_string)

            # Validate keys
            required_keys = ["explanation", "code", "visual"]
            if not all(key in parsed_output for key in required_keys):
                 return {
                    "error": f"JSON output is missing required keys. Expected {required_keys}.",
                    "raw_output": output_text,
                    "parsed_json_attempt": parsed_output # Show what was parsed
                 }


            return {
                "code": parsed_output.get("code", "No code provided in JSON."),
                "visualization_info": parsed_output.get("visual", "No visualization info provided in JSON."),
                "explanation": parsed_output.get("explanation", "No explanation provided in JSON."),
                "raw_output": output_text # Include raw output for debugging
            }

        except json.JSONDecodeError as e:
            # If parsing fails even after finding a block
            return {
                "error": f"Failed to parse JSON output: {e}",
                "raw_output": output_text, # Show the raw output
                "json_string_attempt": json_string # Show the string that failed to parse
            }


    except ValueError as ve:
        # Handle errors during LLM initialization (e.g., missing API key)
        return {"error": str(ve)}
    except Exception as e:
        # Catch other potential errors during agent execution
        return {"error": f"An error occurred during agent execution: {e}", "raw_output": str(e)} # Include error details