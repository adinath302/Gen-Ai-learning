from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
# to setup the behavior(context for the A), Represents input or questions coming from the user, Represents the output or response returned by the chat model.

from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
load_dotenv()

model = init_chat_model(
   model = "gemini-3.6-flash",
   model_provider="google_genai",
)

print("choose your Ai mode")
print("press 1 for Angry mode")
print("press 2 for funny mode")
print("press 3 for sad mode")

choice = int(input('tell your response :- '))

if choice == 1:
     mode = "You are Deeply provoked, furious, or filled with righteous anger AI agent. You respond aggressively and impatiently."

elif choice == 2:
     mode = "You are a very funny AI agent. You respond with humor and jokes."
elif choice == 3:
     mode = "You are an sad Ai agent."

# here to gone store the chat history so that the chatbot can keep the history and ans according to that.( short term memory )
messages=[
SystemMessage(content="mode"),
]

# here we created a loop so that it will act as a real chabot till i enter 0 to "break" stop it .
print("---------------------- Welcome type 0 to exit the application --------------")
while True:

     prompt = input('You : ')

     # here to save the prompt to the messages list
     messages.append(HumanMessage(content=prompt))
     if prompt == "0":
          break
     response = model.invoke(messages)
     # here to save the response to the messages list

     messages.append(AIMessage(content=response.text))
     print("AI : ",response.text) 

print(messages)