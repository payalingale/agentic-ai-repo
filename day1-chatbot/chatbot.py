import anthropic
import os
from dotenv import load_dotenv
load_dotenv()


api_key=os.environ.get('API_KEY')
client = anthropic.Anthropic(api_key=api_key)
conversation_history = []
def chatbot():
  try:
   while(True):
    question = input('Ask question to claude:  ')
    if(question in ['bye' , 'quit' , 'exit']):
      print('Thank you')
      break
    if not question:
      continue
    conversation_history.append({'role':'user','content':question})
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=500,
        messages=conversation_history
    )
    conversation_history.append({'role':'assistant','content':response.content[0].text})
    print(conversation_history)
  except Exception as e:
    print(f"❌ Error: {e}")
    
    

chatbot()