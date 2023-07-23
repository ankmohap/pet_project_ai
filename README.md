# pet_project_ai

Use the sql file to create the list of tables.
Preferrably we are using mysql db to test our code.
Idea is to use a llm chain to convert user queries NLP to actual sql queries with sytantical and semantical validations
Demo - 

![image](https://github.com/ankmohap/pet_project_ai/assets/43520996/cb4bbf88-501b-4378-833b-08535eb12058)



Few Key Observations - 

SQLDatabase chains - we cannot decouple just sql generation and exclude SQL executions 
Agents - Agents can be used to self-rectify the code but it needs a db to try and see if sql works correctly 
Sequentialchains - As of now best way to create three templates - 
 - one for query generation
 - one for syntax validation
 - one for semantic validation
and produce the final output
