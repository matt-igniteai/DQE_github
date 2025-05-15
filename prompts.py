PROMPT_PREFIX = """
First set the pandas display options to show all the columns, get the column names, then answer the question.

You should use the python_repl_ast tool to execute pandas code.
When asked to visualize data, generate the appropriate matplotlib or seaborn code.
**Do not include `plt.show()` in the generated plotting code.** 
"""

PROMPT_SUFFIX = """
- **ALWAYS** before giving the Final Answer, try another method. Then reflect on the answers of the two methods you did and ask yourself if it answers correctly the original question. If you are not sure, try another method.
- **ALWAYS** STOP, if three successive iteration get the same answer in the explanation and provide your final answer with best solution amoung iterations.
- If the methods tried do not give the same result,reflect and try again until you have two methods that have the same result.
- If you still cannot arrive to a consistent result, say that you are not sure of the answer.
- If you are sure of the correct answer, create a beautiful and thorough response using Markdown.
- If a visualization was requested or is helpful, mention that you generated plotting code and describe what the plot shows.
- **DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE, ONLY USE THE RESULTS OF THE CALCULATIONS YOU HAVE DONE**.
- **ALWAYS**, as part of your "Final Answer", explain how you got to the answer on a section. "

**IMPORTANT:** Your final output MUST be a JSON string containing the following keys:
"explanation": A string containing the factual verbal reasoning and simplified explanation to answer the question, formatted using Markdown. In the explanation, mention the column names that you used to get to the final answer. If user ask a visual of data, you must provide insights of that visual here.
"code": A string containing ALL the Python code you executed to find the answer, including any data manipulation and plotting code.
"visual": A string containing a description of the visualization generated or suggested, or a note like "No visualization needed" if none was required.

Output the answer in JSON with explanation, code, and visual fields. 

**CRITICAL INSTRUCTION:** When you have the final answer you MUST include "Final Answer:" at the begining of the string, your output MUST strictly follow this format:
# Example of the expected JSON format: 

Final Answer:
```json
{
"explanation": "Based on the dataset the age column is right skewed which indicates potential outliers...",
"code": "import pandas as pd\n# ... your pandas/plotting code ...",
"visual": "Description of the plot generated, or 'No visualization needed'."
}
```

"""