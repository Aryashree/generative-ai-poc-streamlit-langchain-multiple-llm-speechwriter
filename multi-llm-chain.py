import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
api_key = st.text_input("Enter your OpenAI API Key", type="password")

if not api_key:
    st.warning("Please enter your OpenAI API key to continue")
    st.stop()

llm1 = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
llm2 = ChatOllama(model="gemma:2b")

title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""You are an experienced speech writer.
    You need to craft an impactful title for a speech 
    on the following topic: {topic}
    Return your response as JSON with the key "title".
    """
)

speech_prompt = PromptTemplate(
    input_variables=["title"],
    template="""You need to write a powerful speech of 350 words
    for the following title: {title}
    Return your response as JSON with the key "speech".
    """
)

first_chain = title_prompt | llm1 | JsonOutputParser() | (lambda result: (st.write(result["title"]), result["title"])[1])
second_chain = speech_prompt | llm2 | JsonOutputParser()
##
#You can also do this instead of lambda
#def display_and_return_title(title):
#    st.write(title)  # Show it
#    return title     # Pass it along

# Instead of: (lambda title: (st.write(title), title)[1])
# Use: display_and_return_title
##
final_chain = first_chain | (lambda title:{"title":title}) | second_chain

st.title("Speech Generator")
topic = st.text_input("Enter the topic:")

if topic:
    response = final_chain.invoke({"topic": topic})
    st.write(response)
