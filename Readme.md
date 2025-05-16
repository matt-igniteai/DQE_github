# Data Quality Enrichment (DQE) - AI-Powered Data Analysis Tool

DQE is an agentic AI solution designed to simplify data analysis and visualization through natural language interactions. It allows users to upload CSV datasets and ask questions in plain English, receiving answers with supporting code, visualizations, and explanations.

## Features

- **Natural Language Processing**: Ask questions about your data in plain English
- **Automatic Field Mapping**: AI agent intelligently maps your questions to dataset fields
- **Iterative Refinement**: System evaluates and refines results until they meet your expectations
- **Comprehensive Outputs**: Provides:
  - Executable Python code used for analysis
  - Data visualizations
  - Clear verbal explanations of results
- **Multi-Model Support**: Choose from different AI models provider for analysis

## Web App Usage

1. Access the demo at: [https://dqe-demo-ignite-ai-partners.streamlit.app/](https://dqe-demo-ignite-ai-partners.streamlit.app/)
2. From the left navigation pane:
   - Upload your dataset (.CSV format)
   - Select your preferred AI model
3. Type your question in the input box
4. Click "Process Query"
5. View results including:
   - Generated Python code
   - Data visualizations
   - Detailed explanation

## Local Installation

Follow these steps to run DQE on your local machine:

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/matt-igniteai/DQE_github.git
   cd <repository-directory>
   ```

2. Set up API keys:
   ```bash
   mkdir .streamlit
   touch .streamlit/secrets.toml
   ```
   Edit `.streamlit/secrets.toml` to include your API keys:
   ```toml
   OAI_API_KEY = "your_openai_api_key_here"
   GEM_API_KEY = "your_gemini_api_key_here"
   DEEP_API_KEY = "your_deepseek_api_key_here"
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

6. Access the app at `http://localhost:8501` in your browser

### Sample Datasets
The repository includes sample datasets in the `data/` directory that you can use for testing.
