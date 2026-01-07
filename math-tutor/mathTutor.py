import os
import anthropic
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get('API_KEY')
mode = '/normal'
converstionHistory = []

def selectMode():
  print('Select an mode to learn math')
  print('1.Solves math problems step-by-step')
  print('2.Explain math concepts')
  print('3.Practice problems')
  print('4.Exit')

def showMenu():
  selectMode()
  user_choice = int(input('Select an mode to start learning'))
  if user_choice == 1:
    mode = 'solve'
  elif user_choice == 2:
    mode ='explain'
  elif user_choice == 3:
    mode = 'practice'
  elif user_choice == 4:
    mode = 'exit'
    print('GoodBye')
  else:
    print('Invalid Choice')

  return mode

def mathTutor(question, mode):
    client = anthropic.Anthropic(api_key=api_key)
    converstionHistory.append({
        'role': 'user',
        'content': question
    })

    messages = client.messages.create(
        max_tokens=6000,
        model='claude-sonnet-4-20250514',
        thinking={
            'type': 'enabled',
            'budget_tokens': 5000
        },
        messages=converstionHistory
    )
    
    thinking_text = None
    response_text = None
    
    for block in messages.content:
        if block.type == 'thinking':
            thinking_text = block.thinking
        elif block.type == 'text':
            response_text = block.text
    
    if response_text:
        converstionHistory.append({
            'role': 'assistant',
            'content': response_text
        })

    return thinking_text, response_text

while True:
  question = input('Ask me question :-')
  if 'mode' in question:
    mode = showMenu()
    question = input('Ask me question :-')
    thinking, response = mathTutor(question, mode=mode)
    print(f'The chatbot is thinking :{thinking}')
    print(f'The answer is {response}')

  elif('exit' in question):
   break
  elif('history' in question):
    for conversation in converstionHistory:
      print(conversation)
  else:
    thinking, response = mathTutor(question, mode=mode)
    print(f'The chatbot is thinking :{thinking}')
    print(f'The answer is {response}')
    
   




  