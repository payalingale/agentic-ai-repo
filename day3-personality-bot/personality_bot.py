# Build a chatbot where:
# User can switch between 3 personalities (Teacher, Coder, Poet)
# Each personality has unique tone, style, and behavior
# User switches with commands like /teacher, /coder, /poet
# Conversation memory persists across personality changes
# Save proven prompts as reusable templates

import os
import anthropic
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get('API_KEY')
client = anthropic.Anthropic(api_key=api_key)
conversation_history = []


teacher_prompt = f'Act as an teacher who explains the topic to student in very detailed manner and explains with minor details in soft spoken way and answer it in 10 bullet points'

coder_prompt = f'Act as an coder who explains the topic with more examples related to it industry and maintains the style which is more technical and explanation should be in 10 bullet points '

poet_prompt = f'Act as an poet who explains the topic in more delusional way which doesnt have any relation to practical facts but more with imaginary details tone should be more of poetic which includes words which are imaginary explain it in  10 bullet points'

def mode_selection(question):
  mode = question.strip(':')
  if mode.lower() == 'teacher':
    return 'teacher'
  elif mode.lower() == 'coder':
    return 'coder'
  elif mode.lower() == 'poet':
    return 'poet'
  else:
    print('You have entered incorrect mode')

def get_system_prompt(mode):
  if mode == 'teacher':
    return teacher_prompt
  elif mode == 'coder':
    return coder_prompt
  elif mode == 'poet':
    return poet_prompt


def chatbot():
  mode_selected = 'teacher'
  # Welcome message
  print("\n🎭 Multi-Personality Chatbot")
  print("="*50)
  print(f"Starting mode: {mode_selected.title()}\n")
  print("Commands: /teacher, /coder, /poet, /quit\n")
  try:
    while(True):
      print(f'Default mode selected is {mode_selected}')
      question = input('You: ')
      if not question:
                continue
      if question.startswith('/'):
        command = question[1:].lower()
        if command  in ['teacher','coder','poet']:
          mode_selected = command
          print(f'You have selected {mode_selected} mode')
          continue
        if command in ['exit','quit','bye']:
          print('GoodBye')
          break
        else:
          print(f'Unknown command: {command}\n')
          continue
      if question.lower() in ['exit','quit','bye']:
        print('GoodBye')
        break

      conversation_history.append({'role':'user','content':question})
      system_prompt = get_system_prompt(mode_selected)

      response = client.messages.create(
        max_tokens=6000,
        model='claude-opus-4-1-20250805',
        thinking={
                  'type': 'enabled',
                  'budget_tokens': 5000
              },
        system=system_prompt,
        messages=conversation_history
        )
      for block in response.content:
          if block.type == 'text':
            assistant_message = block.text
      conversation_history.append({'role':'assistant','content':assistant_message})
      print(assistant_message)
      
  except Exception as e:
    print(f"❌ Error: {e}")


if __name__ == '__main__':
  chatbot()