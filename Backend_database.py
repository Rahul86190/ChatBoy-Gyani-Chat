from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated,Literal
from pydantic import BaseModel,Field
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import os
load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY2")
llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key

)

class chatbot_State(TypedDict):
    message:Annotated[list[BaseMessage],add_messages]


def Chatbot(state:chatbot_State):
    message=state["message"]
    response=llm.invoke(message)
    return {"message":response}


conn=sqlite3.connect(database="chatbot.db",check_same_thread=False)
checkpointer=SqliteSaver(conn=conn)

graph = StateGraph(chatbot_State)
graph.add_node("Chatbot",Chatbot)

graph.add_edge(START,"Chatbot")
graph.add_edge("Chatbot",END)
chatbot=graph.compile(checkpointer=checkpointer)

all_threads=set()
def retrieve_threads():
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])

    return list(all_threads)