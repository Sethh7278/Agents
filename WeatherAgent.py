from langchain_openai import ChatOpenAI   
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
load_dotenv()

# Adding memory


model = ChatOpenAI(model="gpt-3.5-turbo")


# Creating Search Tool
search = TavilySearch(max_results=2)

tools=[search]
# Adding memory checkpointer
agent_executor = create_react_agent(model, tools)

model_with_tools = model.bind_tools(tools)


# Asking the user for the location they would like to know the weather in
location = input("Please enter the your location to find out the weather: ")
input_message = {"role": "user", "content": "Search for the weather in " + location}

# Calling the agent with the message and location
response = agent_executor.invoke({"messages": [input_message]})

# # Using langsmith Trace to see whats going on under the hood
# for message in response["messages"]:
#     message.pretty_print()

# Streaming Messages
for step in agent_executor.stream({"messages": [input_message]}, stream_mode="values"):
    step["messages"][-1].pretty_print()
    