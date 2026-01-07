import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get('API_KEY')
client = anthropic.Anthropic(api_key=api_key)

exit_word = ['quit','exit','stop']
question=''
response=''

converstation_history = []
current_mode = 'normal'

def get_system_prompt(mode):
  mode_prompts = {
    'teacher': 'You are a patient educator. Explain concepts clearly and simply.',
    'coder': 'You are a code-focused assistant. Help with programming questions.',
    'pirate': 'You are a pirate. Talk like a pirate in all your responses (fun!)',
    'shakespeare': 'You are Shakespeare. Speak in old English.',
    'normal': 'You are a standard helpful assistant.'
  }
  return mode_prompts.get(mode, mode_prompts['normal'])

     
def first_chatbot(converstation_history, current_mode='normal'):
  messages = client.messages.create(
    max_tokens=1024,
    model='claude-3-5-haiku-20241022',
    messages=converstation_history,
    system=f'{current_mode}')
  return messages.content[0].text


print("🤖 Welcome to Claude Chatbot!")
print("Type 'quit', 'exit', or 'stop' to end the chat.\n")

while True:
    question=input('You:')
    if(question.startswith('/mode ')):
        current_mode = question.replace('/mode ', '').strip()
        print(f'switched to {current_mode} mode')
        question = input('Ask Question:')

        

    if question.lower() in exit_word:
        print('GoodBye')
        break
    else:
        converstation_history.append({
            'role': 'user',
            'content': question
        })
        response = first_chatbot(converstation_history, current_mode)
        print(response)
        converstation_history.append({
            'role':'assistant',
            'content':response})

    if(question.lower() == 'history'):
        print("\n📜 Conversation History:")
        for index,conv in enumerate(converstation_history,1):
          role = conv['role'].capitalize()
          print(f"{index}. {role}: {conv['content'][:10]}...")        

  
        

