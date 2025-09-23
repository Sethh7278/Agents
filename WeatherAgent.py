from langchain_openai import ChatOpenAI   
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
load_dotenv()


memory = MemorySaver()

model = ChatOpenAI(model="gpt-3.5-turbo")


# Creating Search Tool
search = TavilySearch(max_results=2)

tools=[search]

agent_executor = create_react_agent(model, tools)

model_with_tools = model.bind_tools(tools)



location = input("Please enter the your location to find out the weather: ")
input_message = {f"role": "user", "content": "Search for the weather in " + location}
response = agent_executor.invoke({"messages": [input_message]})

for message in response["messages"]:
    message.pretty_print()