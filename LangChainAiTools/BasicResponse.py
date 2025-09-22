# Import relevant functionality
from langchain_openai import ChatOpenAI   
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
load_dotenv()
# Create the agent
memory = MemorySaver()
# Using Langchains OPENAI library, and pulling the API Key from the dotenv file  
model = ChatOpenAI(model="gpt-3.5-turbo") 
#Writing the query and requesting a response
query = "Hi!"
response = model.invoke([{"role": "user", "content": query}])

print(f"Message content: {response.text()}\n")