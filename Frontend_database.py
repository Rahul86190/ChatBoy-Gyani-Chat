import streamlit as st
from Backend_database import chatbot,retrieve_threads
from langchain_core.messages import HumanMessage

import uuid    #to generate dynamic thread everytime

def generate_dynamic_thread():
    thread_id=uuid.uuid4()
    return thread_id

def new_chat():
    thread_id=generate_dynamic_thread()
    st.session_state["thread_id"]=thread_id
    add_thread_id(st.session_state["thread_id"])
    st.session_state["message_history"]=[]

def add_thread_id(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config={"configurable":{"thread_id":thread_id}}).values["message"]

# CONFIG={"configurable":{"thread_id":st.session_state["thread_id"]}}

if "message_history" not in st.session_state:
    st.session_state["message_history"]=[]

if "thread_id" not in st.session_state:
    st.session_state["thread_id"]=generate_dynamic_thread()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"]=retrieve_threads()

add_thread_id(st.session_state["thread_id"])



st.sidebar.title("CHATBOY")
if st.sidebar.button("NEW CHAT"):
    new_chat()
st.sidebar.header("My conversations")

for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"]=thread_id
        messages=load_conversation(thread_id)


        temp_message=[]

        for msg in messages:
            if isinstance(msg,HumanMessage):
                role="user"
            else:
                role="assistent"
            temp_message.append({"role":role,"content":msg.content})
        st.session_state["message_history"]=temp_message







for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input=st.chat_input("Type Here")


if user_input:
    st.session_state["message_history"].append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.write(user_input)

    CONFIG={"configurable":{"thread_id":st.session_state["thread_id"]}}


    with st.chat_message("assistant"):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {"message":[HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            )
        )



    st.session_state["message_history"].append({"role":"assistent","content":ai_message})