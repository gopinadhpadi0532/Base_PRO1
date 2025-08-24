# This file is located at: BASEPRO/app/main.py

import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv

# Load environment variables from the .env file in the root directory (BASEPRO)
load_dotenv()

# This is the crucial line. The variable name MUST be `app`.
app = FastAPI()

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

# Define the prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant that answers questions from users."),
        ("user", "{user_input}"),
    ]
)

# Define the output parser
output_parser = StrOutputParser()

# Create the LangChain chain
chain = prompt_template | llm | output_parser

# Define the request body model
class Question(BaseModel):
    text: str

@app.post("/chat")
async def chat(question: Question):
    """
    This endpoint receives a user's question and returns a response from the Gemini model.
    """
    response = chain.invoke({"user_input": question.text})
    return {"response": response}

# Note: The 'if __name__ == "__main__":' block is not strictly necessary when running with uvicorn,
# but it's good practice to keep it for direct execution.
if __name__ == "__main__":
    import uvicorn
    # This will run if you execute `python app/main.py` directly, but we will use the uvicorn command.
    uvicorn.run(app, host="0.0.0.0", port=8000)