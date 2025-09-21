import os, json, getpass
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

#client set by getting the API key from Env
client = OpenAI(
    api_key=os.getenv("OPEN_AI_KEY")
)

#Chat History Destination
history = "chat history/Underground_path.json"

#Checking for file when running the chatbot or creating the file if one doesnt already exist
if os.path.exists(history):
    with open(history, "r") as f:
        conversation = json.load(f)
else:
    conversation = [{"role": "system", "content": "You are a london underground assistant bot with the main focus on helping commuters find routes and diversions using the map given, but try to save API tokens (limit of 150)"}]

#Function to save history
def save_history():
    with open(history, "w") as f:
        json.dump(conversation, f, ensure_ascii=False, indent=2)


file_destination = "undergroundMap.jpg"

def load_file(file:str) -> str:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            full = f.read()
    else:
        print("Unable to locate file")
    return full

def response(prompt):
    #appending the users prompt to the conversation array for saving to JSON
    conversation.append({"role": "user", "content" : prompt})

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages= conversation
        
    )

    reply = response.choices[0].message.content

    conversation.append({"role": "assistant", "content" : reply})
    save_history()
    return (reply)

# Ask the original question once
question = input("Please tell the virtual assistant where abouts you are and where you would like to go: ")

if question.upper() != "X":
    answer = response(question)
    print("AI:", answer)

    # Keep looping with a shorter follow-up prompt
    while True:
        follow_up = input("How else can I help? (press X to quit): ")
        if follow_up.upper() == "X":
            break
        else:
            answer = response(follow_up)
            print("AI:", answer)