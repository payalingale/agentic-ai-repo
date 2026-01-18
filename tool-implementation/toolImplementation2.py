import os
import anthropic
from dotenv import load_dotenv
import requests
load_dotenv()

apikey = os.environ.get('API_KEY')
client = anthropic.Anthropic(api_key=apikey)

tools = [
{
  'name':'getWeatherForecast',
  'description':'The tool should help to get the weather details based on city name or location',
  'input_schema':{
    'type':'object',
    'properties':{
      "location": {
      'type':'string',
      'description':'The city and state, e.g. San Francisco, CA'
    }
    },
  'required':['location']
  }
 
},
{
  'name':'getCurrentTime',
  'description':'The tool should help to get the current time details based on city name or location',
  'input_schema':{
    'type':'object',
    'properties':{
      "location": {
      'type':'string',
      'description':'The city and state, e.g. San Francisco, CA'
    }
    },
  'required':['location']
  }
},
{
  'name':'getRandomJoke',
  'description':'The tool should help to tell random joke',
  'input_schema':{  
    'type':'object',
    'properties':{} 
  }
}]

def getWeatherForecast():
  print('weather')
def getCurrentTime():
  print('getCurrentTime')
def getRandomJoke():
  print('getRandomJoke')

def process_tools(tool_name,tool_input):
  if tool_name == 'getWeatherForecast':
      getWeatherForecast()
  elif tool_name == 'getCurrentTime':
    getCurrentTime()
  elif tool_name == 'getRandomJoke':
    getRandomJoke()



def daily_assistant_agent():
  question = input('Enter the question:- ')
  try:
    messages = client.messages.create(
      max_tokens=6000,
      model='claude-sonnet-4-5',
      thinking={
        'type':'enabled',
        'budget_tokens':5000
      },
      tools=tools,
      messages=[{
        'role':'user',
        'content':f'Answer the {question} using tools'
      }]
    )
    for block in messages.content:
      if block.type == 'thinking':  # Corrected condition
        print(f"Thinking: {block.thinking}")
      elif block.type == 'text':
        print(f"Response: {block.text}")
      elif block.type == 'tool_use':
        print(f"Tool used: {block.name}")
        print(f"Tool input: {block.input}")
    process_tools(tool_name=block.name,tool_input=block.input)
    return messages.content
  except Exception as e:
    return{f'return as {str(e)}'}


daily_assistant_agent()