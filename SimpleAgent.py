import os, json, getpass
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


#Setting up the Client
client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY")
)

#Creating a destination for saved chat history
history = "chat history/chat_history.json"

# On startup either read history or start new
if os.path.exists(history):
    with open(history, "r") as f:
        #if a file exists, use load to deserialize the file
        conversation =json.load(f)
else:
    conversation = [{"role": "system", "content": "Answer like a good chatbot, but try to save API tokens (limit of 150)"}]
    

# Save History function
def save_chat():
    with open(history, "w") as f:
        #using dump to serialize the chat into JSON format
        json.dump(conversation, f, ensure_ascii=False, indent=2)

def response(prompt):
    #appending the users prompt to the conversation array for saving to JSON
    conversation.append({"role": "user", "content" : prompt})

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages= conversation
        
    )

    reply = response.choices[0].message.content

    conversation.append({"role": "assistant", "content" : reply})
    save_chat()
    return (reply)
# #Creating the response
# def response(prompt):
#     response = client.chat.completions.create(
#         model = "gpt-3.5-turbo",
#         messages=[
#             {"role" : "system", "content" : "Answer like a good chatbot, but try to save API tokens (limit of 150)"},
#             {"role" : "user", "content" : prompt}
#         ]
#     )
#     reply = response.choices[0].message.content
#     print("AI: ", reply)



#Creating a loop so the user can keep asking quetions
while True:
    question = input("Enter your question here or type X to cancel: ")
    if question.upper() == "X":
        break
    else:
        answer = response(question)
        print ("AI: ", answer)