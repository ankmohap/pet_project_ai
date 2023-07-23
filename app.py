import openai
import mysql.connector
import os
import sqlparse
from open_key import api_key
os.environ['OPENAI_API_KEY'] = api_key
openai.api_key = api_key
# List of tables and columns (customize this based on your database schema)
tables = {
    "ai_stg.client": ["name", "age", "city"],
    "ai_stg.orders": ["order_cd", "client_name", "amount","product_name","product_cd"],
    "ai_stg.products": ["product_cd","name","description","offer_cd"]
}
import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain


# Generate the prompt based on the provided tables and columns
def generate_prompt(tables):
    prompt = "You can query data from the following tables:\n"
    for table, columns in tables.items():
        columns_str = ", ".join(columns)
        prompt += f"- {table} with columns: {columns_str}\n"
    prompt += "Please write a natural language query using these tables and columns to get the data you need."
    return prompt

def text_to_sql(user_input, tables):
    prompt = generate_prompt(tables)
    user_prompt= f"{prompt}\nUser Input: {user_input}",
    return user_prompt

st.title("Super Query interface")
prompt = st.text_input("Write your query here")
prompt_text = generate_prompt(tables)
prompt_template = f"""
{prompt_text}
Verify the query as per mysql db query syntax
User Input: {{user_input}}
"""

sql_template = PromptTemplate(
    input_variables=["user_input"], template=prompt_template
)
validate_template = PromptTemplate(
    input_variables=["query"], template = 'validate query as per mysql SQL syntax and correct it {query}'
)


llm = OpenAI(temperature=0.9)
sql_chain = LLMChain(llm=llm, prompt=sql_template,verbose=True)
validate_chain = LLMChain(llm=llm, prompt=validate_template,verbose=True)
sequence_chain = SimpleSequentialChain(chains=[sql_chain,validate_chain], verbose=True)

if prompt:
    response = sequence_chain.run(prompt)
    st.write(response)
    
