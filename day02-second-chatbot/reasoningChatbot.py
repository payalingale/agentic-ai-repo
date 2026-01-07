import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

question=input('Ask Question')
api_key  = os.getenv('API_KEY')
client = anthropic.Anthropic(api_key=api_key)
messages = client.messages.create(
  max_tokens=16000,
  model='claude-sonnet-4-5',
  thinking={
    "type":'enabled', 
    'budget_tokens':10000
  },
  messages=[{
    'role':'user',
    'content':f'{question}'
  }]
)

for block in messages.content:
  if block.type == 'thinking':
    print(f'\nThinking Summary: {block.thinking}')
  elif block.type == 'text':
    print(f'\nResponse: {block.text}')

