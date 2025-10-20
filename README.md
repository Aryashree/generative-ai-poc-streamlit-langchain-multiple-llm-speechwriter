1. Imports and Environment Setup
import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser


os → lets you read environment variables like API keys.

ChatOpenAI → wrapper for OpenAI LLMs using LangChain’s modular interface.

ChatOllama → wrapper for Ollama models (local or cloud-hosted).

streamlit → the UI framework for building the web app.

PromptTemplate → lets you define prompts with variables (like {topic}).

StrOutputParser, JsonOutputParser → parse LLM outputs into Python objects.

Note: langchain_openai and langchain_core are the new modular packages; missing them causes ModuleNotFoundError.

2. Load OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


Reads your OpenAI API key from environment variables (or Streamlit secrets).

Avoids hardcoding sensitive keys.

If missing, you’ll see the error you got earlier about api_key not being set.

3. Initialize LLMs
llm1 = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
llm2 = ChatOllama(model="gemma:2b")


llm1 → OpenAI GPT-4o model for title generation.

llm2 → Ollama Gemma model for speech generation.

Important: Ollama won’t work on Streamlit Cloud unless you host the Ollama API somewhere.

4. Define Prompt Templates
title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""You are an experienced speech writer.
    You need to craft an impactful title for a speech 
    on the following topic: {topic}
    Return your response as JSON with the key "title".
    """
)


Creates a template prompt with a variable topic.

The LLM will fill {topic} dynamically.

Output is expected in JSON so we can parse "title" automatically.

speech_prompt = PromptTemplate(
    input_variables=["title"],
    template="""You need to write a powerful speech of 350 words
    for the following title: {title}
    Return your response as JSON with the key "speech".
    """
)


Similar template, but now input is the title generated earlier.

Asks the LLM to generate structured output (JSON with "speech").

Using JSON output makes chaining easy — you don’t have to manually extract text.

5. Create Chains
first_chain = title_prompt | llm1 | JsonOutputParser() | (lambda result: (st.write(result["title"]), result["title"])[1])


This tries to pipe (|):

title_prompt → generates prompt text with topic.

llm1 → sends prompt to GPT-4o.

JsonOutputParser() → parses JSON response into Python dict.

Lambda → displays the title in Streamlit and passes it along.

⚠️ Problem: lambda inside a LangChain chain breaks execution — LangChain expects Runnables, not plain Python functions.

second_chain = speech_prompt | llm2 | JsonOutputParser()


Similar pipeline for speech generation.

Uses the title as input.

Parses JSON output to get "speech" key.

6. Combine Chains
final_chain = first_chain | (lambda title:{"title":title}) | second_chain


Intends to feed the output of first_chain into second_chain.

The lambda converts the title string to {"title": title} dict (required by the second prompt).

Issue: Again, plain lambda won’t work inside LangChain chaining. Must be handled outside or using a proper Runnable class.

Recommended fix: run the chains sequentially in Python, then pass the result — safer for Streamlit.

7. Streamlit UI
st.title("Speech Generator")
topic = st.text_input("Enter the topic:")

if topic:
    response = final_chain.invoke({"topic": topic})
    st.write(response)


Sets up a text input for the speech topic.

When the user enters a topic, final_chain.invoke({"topic": topic}) triggers the whole pipeline:

Generate title with GPT-4o.

Generate speech with Gemma (Ollama).

The final result is printed in Streamlit.

✅ Key Takeaways

LangChain helps structure multi-step LLM calls (title → speech) and parse JSON automatically.

Ollama model won’t run on Streamlit Cloud unless hosted.

Lambda functions inside a chain break execution — better to handle display and dict conversion outside the chain.

API keys must be set (OPENAI_API_KEY) for OpenAI models.
