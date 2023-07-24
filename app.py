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

##PROMPT to - Verify SQL Syntax after SQL chain give a sql Output
prompt_template = f"""
{prompt_text}
Verify the query as per mysql db query syntax
User Input: {{user_input}}
"""

##PROMPT to - Verify Schema after SQL syntax is verified
schema_template = f"""
Validate the query {{correct_query}} as per the below schema and give correct query 
- tables : clients,products,orders
- columns : name, age, city, order_cd, client_name, amount, product_name, product_cd, product_cd, name, description, offer_cd

"""

#Template 1 - prompt for  taking user input and giving sql output
sql_template = PromptTemplate(
    input_variables=["user_input"], template=prompt_template
)

#Template 2 - prompt for  taking output of template 1 and validating syntax
validate_template = PromptTemplate(
    input_variables=["query"], template = 'validate query as per mysql SQL syntax and correct the query : {query}'
)

#Template 3 - prompt for  taking output of template 2 and validating schema
validate_schema_template = PromptTemplate(
    input_variables=["correct_query"], template = schema_template
)


llm = OpenAI(temperature=0.9)
#chain 1 for template 1 
sql_chain = LLMChain(llm=llm, prompt=sql_template,verbose=True)
#chain 2 for template 2
validate_chain = LLMChain(llm=llm, prompt=validate_template,verbose=True)
#chain 3 for template 3
val_schema_chain = LLMChain(llm=llm, prompt=validate_schema_template,verbose=True) 
#Chains instructed to run sequential one after other so that o/p of one is fed to the other as promt variable 
sequence_chain = SimpleSequentialChain(chains=[sql_chain,validate_chain,val_schema_chain], verbose=True)

if prompt:
    response = sequence_chain.run(prompt)
    st.write(response)
    
