import os
from openai import OpenAI
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt: str) -> str:
    """
    Calls the LLM with a constrained prompt.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        #model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a cautious analytical assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
