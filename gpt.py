
import openai
from openai import OpenAI
from api_keys import openai_key

client = OpenAI(api_key=openai_key)

conversation_history = [
    { 
        "role": "system", 
        "content": (
            """
            You are an old sea man. Never break character.
            You speak an old tongue.
            You speak in short precise sentences.
            Do not return any sentence structure.
            """
        )
    },
]

def add_system_message(message):
    global conversation_history
    conversation_history.append({ "role": "system", "content": message })

def add_user_message(user_input):
    global conversation_history
    conversation_history.append({ "role": "user", "content": user_input })


def generate_fish_message():
    global conversation_history

    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation_history,
        temperature=1,
        stream=True
    )

    msg = ''
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content is not None and len(content):
            msg += content
            yield content

    # Add assistant reply to history
    conversation_history.append({"role": "assistant", "content": msg })

    return msg
