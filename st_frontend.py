import streamlit as st
from langgraph_backend import respond
#streamlit session state is a dict whose contents donot reset unless page is refreshed

if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]


user_input=st.chat_input("type here...")

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

if user_input:
    st.session_state['message_history'].append(
        {
            'role':'user',
            'content':user_input
        }
    )
    with st.chat_message("user"):
        st.text(user_input)


    ai_message=respond(user_input)
    st.session_state['message_history'].append(
        {
            'role':'assistant',
            'content':ai_message
        }
    )

    with st.chat_message("assistant"):
        st.text(ai_message)

