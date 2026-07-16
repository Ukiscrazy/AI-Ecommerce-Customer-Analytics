from ai.sql_agent import generate_sql
from ai.query_executor import execute_sql

question = input("Ask a business question: ")

sql = generate_sql(question)

print("\nGenerated SQL:\n")
print(sql)

result = execute_sql(sql)

print("\nQuery Result:\n")
print(result)