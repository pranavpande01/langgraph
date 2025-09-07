import uuid

def generate_thread_id():
    return uuid.uuid4()

def load_convo(thread_id,chatbot):

    config = {
    "configurable": {
        "thread_id": thread_id
    }
    }

    return chatbot.get_state(
        config=config
    ).values['messages']