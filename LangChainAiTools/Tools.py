from langchain_openai import ChatOpenAI   
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
load_dotenv()


#Creating the Agent
memory = MemorySaver()

model = ChatOpenAI(model="gpt-3.5-turbo")
# Using Tavily to allow the agent to search the web
search = TavilySearch(max_results=2)
#Tools used
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Giving the model knowledge of the tools
model_with_tools = model.bind_tools(tools)

# Using the Search to find out the weather 
query = "Search for the Weather in Oxford, England"

response = model_with_tools.invoke([{"role": "user", "content": query}])

print(f"Message Content: {response.text()}\n")
print(f"Tools Used: {response.tool_calls}")