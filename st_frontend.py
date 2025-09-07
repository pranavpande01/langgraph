import streamlit as st
from langgraph_backend import respond,load_convo
from utility import generate_thread_id

####################################################################
#streamlit session state is a dict whose contents donot reset unless page is refreshed

if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
####################################################################
user_input=st.chat_input("type here...")
st.sidebar.title("chatbot")
if st.sidebar.button("new chat"):
    if st.session_state['message_history']!=[]:
        st.session_state['new_chat']=True
        add_thread(st.session_state['thread_id'])
        st.session_state['thread_id']=generate_thread_id()
        st.session_state['message_history']=[]
    else:
        st.session_state['new_chat']=False


st.sidebar.header("my chats")
####################################################################
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#for i in st.session_state['chat_threads']:
#    if st.sidebar.button(str(i)):
#        st.session_state['thread_id']=i
#        [{'role':'user' if isinstance(j,HumanMessage) }for j in load_convo(i)]

####################################################################
if user_input:
    st.session_state['message_history'].append(
        {
            'role':'user',
            'content':user_input
        }
    )
    with st.chat_message("user"):
        st.text(user_input)


    ai_message=respond(user_input,st.session_state['thread_id'])
    st.session_state['message_history'].append(
        {
            'role':'assistant',
            'content':ai_message
        }
    )

    with st.chat_message("assistant"):
        st.text(ai_message)

