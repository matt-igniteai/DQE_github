PROMPT_PREFIX = """
First set the pandas display options to show all the columns, get the column names, then answer the question.

You should use the python_repl_ast tool to execute pandas code.
When asked to visualize data, generate the appropriate matplotlib or seaborn code.
**ALWAYS** visualize graphs in ONE figure with multiple axes. DO NOT add multiple figures.
**Do not include `plt.show()` in the generated plotting code.** 
**ALWAYS** provide comprehensive explanation.
"""

PROMPT_SUFFIX = """
- **ALWAYS** before giving the Final Answer, try another method. Then reflect on the answers of the two methods you did and ask yourself if it answers correctly the original question. If you are not sure, try another method.
- **ALWAYS** STOP, if three successive iteration get the same answer in the explanation and provide your final answer with best solution amoung iterations.
- If the methods tried do not give the same result,reflect and try again until you have two methods that have the same result.
- If you still cannot arrive to a consistent result, say that you are not sure of the answer.
- If you are sure of the correct answer, create a beautiful and thorough response using Markdown.
- If a visualization was requested or is helpful, mention that you generated plotting code and describe what the plot shows.
- **ALWAYS**, as part of your "Final Answer".

**IMPORTANT:** Your final output MUST be a JSON string containing the following keys:
"explanation": A string of comprehensive verbal response to answer user's question, formatted using Markdown. 
"code": A string containing ALL the Python code you executed to find the answer, including any data manipulation and plotting code.
"visual": A string containing a description of the visualization generated or suggested, or a note like "No visualization needed" if none was required.

Output the answer in JSON with explanation, code, and visual fields. 

**CRITICAL INSTRUCTION:** When you have the final answer you MUST include "Final Answer:" at the begining of the string, your output MUST strictly follow this format:
# Example of the expected JSON format: 

Final Answer:
```json
{
"explanation": "Your response to user's question",
"code": "import pandas as pd\n# ... your pandas/plotting code ...",
"visual": "Description of the plot generated, or 'No visualization needed'."
}
```

"""