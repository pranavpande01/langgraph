from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]

def chat_node(state:ChatState):
    messages=state['messages']
    response=llm.invoke(messages)
    return {
        'messages':[response]
    }
checkpointer=InMemorySaver()

graph=StateGraph(ChatState)

graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot=graph.compile(checkpointer=checkpointer)


def respond(user_input,thread_id):
    config = {
    "configurable": {
        "thread_id": str(thread_id)
    }
    }
    return chatbot.invoke(
        {'messages':[HumanMessage(content=user_input)]},
        config=config
    )['messages'][-1].content

def load_convo(thread_id):
    config = {
    "configurable": {
        "thread_id": str(thread_id)
    }
    }
    return chatbot.get_state(
                config=config
    ).values['messages']