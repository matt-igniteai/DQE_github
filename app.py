import streamlit as st
import pandas as pd
from helper import load_data, run_dataframe_agent
from prompts import PROMPT_PREFIX, PROMPT_SUFFIX
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt # Import matplotlib
import seaborn as sns # Import seaborn, as agent might use it
import io # To potentially capture stdout/stderr from exec
import sys # To potentially capture stdout/stderr from exec

load_dotenv(".env") # Load environment variables

# --- Company Branding Configuration ---
# Replace with your company's actual colors (using hex codes)
COMPANY_PRIMARY_COLOR = "#000000" # Example: A shade of blue
COMPANY_SECONDARY_COLOR = "#F0F2F6" # Example: A light grey for backgrounds
COMPANY_TEXT_COLOR = "#333333" # Example: Dark grey/black for text
COMPANY_ACCENT_COLOR = "#007BFF" # Example: For links or highlights

# Replace with the path to your company logo image file
# Make sure the logo file is in a place accessible to your app
LOGO_PATH = "images/IGNITE-AI-PARTNERS-LOGO-HOT-ORANGE-No-Margin-300x84.png"


# --- Streamlit App Configuration ---
st.set_page_config(layout="wide", page_title="Chat and Manipulate your Dataset")


# --- Inject Custom CSS for Branding ---
st.markdown(
    f"""
    <style>
    /* General body text color */
    body {{
        color: {COMPANY_TEXT_COLOR};
    }}

    /* Main app background color */
    div.stApp {{
        background-color: #FFFFFF; /* White background for main content */
        color: {COMPANY_TEXT_COLOR};
    }}

    /* Sidebar background color */
    div[data-testid="stSidebar"] > div:first-child {{
        background-color: {COMPANY_SECONDARY_COLOR}; /* Use a lighter background for sidebar */
        color: {COMPANY_TEXT_COLOR};
    }}

    /* Titles and Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: {COMPANY_PRIMARY_COLOR};
    }}

    /* Primary button styling */
    .stButton button {{
        background-color: {COMPANY_PRIMARY_COLOR};
        color: white; /* Text color for buttons, usually white or a contrasting light color */
        border-radius: 5px;
        border-color: {COMPANY_PRIMARY_COLOR};
    }}

    .stButton button:hover {{
        background-color: {COMPANY_PRIMARY_COLOR}CC; /* Slightly darker on hover */
        border-color: {COMPANY_PRIMARY_COLOR}CC;
    }}

    /* Links */
    a {{
        color: {COMPANY_ACCENT_COLOR};
    }}

    /* You can add more specific CSS here to style other elements */
    /* e.g., st.selectbox, st.text_input, st.dataframe headers, etc. */

    </style>
    """,
    unsafe_allow_html=True
)

# --- Add Company Logo to Sidebar ---
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)
else:
    st.sidebar.warning(f"Logo file not found at {LOGO_PATH}. Please update LOGO_PATH.")




st.title("💻 Chat and Manipulate your Dataset")
st.markdown("""
* Upload your dataset (CSV), 
* Choose an LLM, 
* Ask questions in natural language.\n
Your Data Scientist will generate and execute code to answer your questions. 
Provide the code, potentially suggest visualizations, and you will get a clear 
explanation in a structured JSON format.
""")

# --- Session State Initialization ---
if 'df' not in st.session_state:
    st.session_state.df = None
if 'results' not in st.session_state:
    st.session_state.results = None
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'llm_name' not in st.session_state:
    st.session_state.llm_name = "OpenAI" # Default LLM

# --- File Upload ---
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Check if a new file is uploaded or if the session state df is from a different file
    if st.session_state.df is None or getattr(st.session_state, '_uploaded_file_name', None) != uploaded_file.name:
        with st.spinner("Loading data..."):
            df = load_data(uploaded_file)
            if isinstance(df, pd.DataFrame):
                st.session_state.df = df
                st.session_state._uploaded_file_name = uploaded_file.name # Store file name
                st.session_state.results = None # Clear previous results
                st.success("Data loaded successfully!")
                st.sidebar.write("Data Preview:")
                st.sidebar.dataframe(df.head())
            else:
                st.error(df) # Display error message from load_data
                st.session_state.df = None # Ensure df is None on error
    else:
        st.sidebar.info(f"Using already loaded file: {uploaded_file.name}")
        st.sidebar.write("Data Preview:")
        st.sidebar.dataframe(st.session_state.df.head())

# --- LLM Selection ---
st.sidebar.header("LLM Selection")
st.session_state.llm_name = st.sidebar.selectbox(
    "Choose an LLM:",
    ("OpenAI", "Google Gemini", "DeepSeek"),
    index=("OpenAI", "Google Gemini", "DeepSeek").index(st.session_state.llm_name)
)
st.sidebar.markdown("Make sure you have the corresponding API key in your `.env` file.")

# --- Query Input ---
st.header("🧑‍🔬 Ask a Question about the Data")
query = st.text_area(
    "Enter your natural language query here:",
    value=st.session_state.query,
    height=100,
    placeholder="e.g., How many orders were placed last month? Show me the average price by category. What are the columns?"
)
st.session_state.query = query # Update session state with current text area value

# --- Process Button ---
if st.button("Process Query"):
    if st.session_state.df is None:
        st.warning("Please upload a dataset first.")
    elif not st.session_state.query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner(f"Processing query with {st.session_state.llm_name}..."):
            results = run_dataframe_agent(
                st.session_state.df,
                st.session_state.llm_name,
                st.session_state.query,
                PROMPT_PREFIX,
                PROMPT_SUFFIX
            )
            st.session_state.results = results # Store results in session state

# --- Display Results ---
if st.session_state.results:
    st.header("Results")
    results = st.session_state.results

    if "error" in results:
        st.error(f"Error: {results['error']}")
        # Optionally display raw output if available in the error dict
        if 'raw_output' in results:
             with st.expander("View Raw Agent Output (for debugging)"):
                 st.text(results['raw_output'])
        if 'json_string_attempt' in results:
             with st.expander("View JSON String Attempt (for debugging)"):
                 st.text(results['json_string_attempt'])
        if 'parsed_json_attempt' in results:
             with st.expander("View Parsed JSON Attempt (for debugging)"):
                 st.json(results['parsed_json_attempt'])

    else:
        # Display Code
        st.subheader("Generated Code")
        generated_code = results.get('code', 'N/A')
        st.code(generated_code, language='python')

       # Display Visualization
        st.subheader("Visualization")
        visual_info = results.get('visualization_info', 'No visualization info provided in JSON.')
        st.info(visual_info) # Display the description from the JSON

        # --- Attempt to execute plotting code and display plot ---
        # Check if the generated code looks like it contains plotting commands
        # This is a heuristic check
        if generated_code != 'N/A' and ('plt.' in generated_code or 'sns.' in generated_code or '.plot(' in generated_code):
            st.write("Attempting to render plot...")
            try:
                # Prepare the execution environment
                # Make df, plt, sns, pd available to the executed code
                exec_scope = {
                    'df': st.session_state.df,
                    'plt': plt,
                    'sns': sns,
                    'pd': pd # Include pandas just in case
                }

                # Execute the generated code
                # We can capture stdout/stderr if needed for debugging exec issues
                # old_stdout = sys.stdout
                # redirect_output = io.StringIO()
                # sys.stdout = redirect_output

                # Remove plt.show() if it exists, as it interferes with Streamlit
                code_to_execute = generated_code.replace("plt.show()", "")

                exec(code_to_execute, exec_scope)

                # sys.stdout = old_stdout # Restore stdout

                # Check if a figure was created
                if plt.gcf().get_axes(): # Check if the current figure has any axes (meaning something was plotted)
                    st.pyplot(plt.gcf()) # Display the figure in Streamlit
                else:
                    st.warning("Plotting code executed, but no figure was generated or captured.")

            except Exception as e:
                st.error(f"Error executing plotting code: {e}")
                # Optionally display captured output
                # st.text("Captured Output:\n" + redirect_output.getvalue())
            finally:
                # Close all figures to free up memory and prevent them from showing up unexpectedly
                plt.close('all')
        else:
            st.info("No plotting code detected or required for this query.")


        # Display Verbal Explanation
        st.subheader("Verbal Explanation")
        # Access the 'explanation' key from the parsed JSON
        st.markdown(results.get('explanation', 'No explanation provided in JSON.')) # Use markdown to render formatting

        # Optional: Display raw output for debugging
        with st.expander("View Raw Agent Output"):
            st.text(results.get('raw_output', 'N/A'))