import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get('API_KEY')
client = anthropic.Anthropic(api_key=api_key)

exit_word = ['quit','exit','stop']


def first_chatbot(question):
  messages = client.messages.create(
    max_tokens=1024,
    model='claude-3-5-haiku-20241022',
    system='You are an helpfull teacher answer precisely',
    messages=[{
      'role':'user',
      'content':f'''{question}'''
    }])
  return messages.content[0].text

answer = ''
# for i in range(1,100):
#   question = input('You:')
  



print("🤖 Welcome to Claude Chatbot!")
print("Type 'quit', 'exit', or 'stop' to end the chat.\n")

while True:
    question = input('You:')
    if question.lower() in exit_word:
        print('GoodBye')
        break
    else:
        answer = first_chatbot(question=question)
        print(answer)




