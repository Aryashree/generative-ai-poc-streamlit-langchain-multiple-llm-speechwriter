import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Initialize models
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

api_key = st.text_input("Enter your OpenAI API Key", type="password")

if not api_key:
    st.warning("Please enter your OpenAI API key to continue")
    st.stop()

llm1 = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
llm2 = ChatOllama(model="gemma:2b")

# Prompts
title_prompt = PromptTemplate(
    input_variables=["topic"],
    template=(
        "You are an experienced speech writer.\n"
        "Craft an impactful title for a speech on the following topic: {topic}\n"
        "Return your response as JSON with the key 'title'."
    )
)

speech_prompt = PromptTemplate(
    input_variables=["title"],
    template=(
        "You need to write a powerful 350-word speech for the following title: {title}.\n"
        "Return your response as JSON with the key 'speech'."
    )
)

# Chains
title_chain = title_prompt | llm1 | JsonOutputParser()
speech_chain = speech_prompt | llm2 | JsonOutputParser()

# Streamlit UI
st.title("🎤 Speech Generator")

topic = st.text_input("Enter a topic for your speech:")

if topic:
    # Step 1: Generate title
    title_response = title_chain.invoke({"topic": topic})
    title = title_response.get("title", "Untitled Speech")
    st.subheader("Generated Title")
    st.write(title)

    # Step 2: Generate speech using the title
    speech_response = speech_chain.invoke({"title": title})
    speech = speech_response.get("speech", "No speech generated.")
    
    st.subheader("Generated Speech")
    st.write(speech)
