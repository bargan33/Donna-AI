import openai
import json
import os

with open('keys/gpt_api_key.txt', 'r') as file:
    openai.api_key = file.read().strip()


def get_candidate_cv(json_file_path, name):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        candidates = data['candidates']
        for candidate in candidates:
            if candidate['full_name'] == name:
                return candidate['cv']
    return None


def chat_api_call(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation,
        max_tokens=250,
        temperature=1,
    )
    return response


def append_to_file(file_path, role, content):
    message = {"role": role, "content": content}
    with open(file_path, 'a') as f:
        f.write(json.dumps(message) + '\n')


def clear_file(file_path):
    with open(file_path, 'w') as f:
        f.truncate(0)


def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def add_message_to_conversation(role, content):
    print(os.getcwd())
    with open("src/chat_conversation.txt", "r") as file:
        conversation = json.load(file)

    conversation.append({"role": role, "content": content})

    with open("chat_conversation.txt", "w") as file:
        json.dump(conversation, file)


CHAT_SYSTEM_CONTEXT = '''
You are a recruitment assistant in an IT company. You will be given the candidate's CV or other relevant information.
Your job is to answer questions about the candidate.
'''
