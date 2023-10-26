from langchain.chat_models.openai import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.callbacks import StdOutCallbackHandler

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(temperature=0,model="gpt-3.5-turbo-16k",streaming=True,max_tokens=5000)

messages = [
    SystemMessage(
        content="You are a helpful assistant who writes tech stories"
    )
]

handler = StdOutCallbackHandler()

print(chat(messages,callbacks=[handler]))
