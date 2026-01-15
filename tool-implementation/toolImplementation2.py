import os
import anthropic
from dotenv import load_dotenv
load_dotenv()

apikey = os.environ.get('API_KEY')
client = anthropic.Anthropic(api_key=apikey)

tools = [{
  'name':'getWeatherForecast',
  'description':'The tool should help to get the weather details based on city name or location',
  'inputSchema':{
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
  'inputSchema':{
    'type':'object',
    'properties':{
      "location": {
      'type':'string',
      'description':'The city and state, e.g. San Francisco, CA'
    }
    },
  'required':['location']
  }
}
{
  'name':'randomJoke',
  'description':'The tool should help to tell random joke',
  'inputSchema':{
    'type':'object',
  },
  'required':['']
}]


def daily_assistant_agent():
  question = input('Enter the question')
  try:
    messages = client.messages.create(
      max_tokens=6000,
      model='claude-3-5-haiku-20241022',
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
      

  except Exception as e:
    return{f'return as {str(e)}'}
