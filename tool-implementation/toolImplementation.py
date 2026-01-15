import os
import anthropic
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get('API_KEY')
model ='claude-sonnet-4-20250514'
Calculatortools=[
        {
            "name": "calculate",
            "description": "Calculate or solve the problem with given values",
            "input_schema": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "convert the string and check for numbers and operator",
                    }
                },
                "required": ["data"],
            },
        }
]
PythonCodetool=[
        {
            "name": "PythonComplier",
            "description": "Run the python program and give the output",
            "input_schema": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Check the code go line by line and execute it",
                    }
                },
                "required": ["code"],
            },
        }
]

searchWikiTool=[
        {
            "name": "Search",
            "description": "Go through wikipedia and respond to question ",
            "input_schema": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "It will be a sentence or word eg:Explain photosynthesis",
                    }
                },
                "required": ["keyword"],
            },
        }
]

tools = Calculatortools + PythonCodetool + searchWikiTool



client = anthropic.Anthropic(api_key=api_key)

def toolImplementation():
  question = input('Enter the question')

  messages = client.messages.create(
  max_tokens=6000,
  thinking={
    'type':'enabled',
    'budget_tokens':5000
  },
  model='claude-sonnet-4-20250514',
  tools=tools,
  messages=[{
    'role':'user',
    'content':f'Answer {question} using tools if needed'
  }]
)
  for block in messages.content:
    if block.type == 'thinking' and not 'thinking_text':
      thinking_text = block.thinking
    if block.text != '':
      text = block.text
    return thinking_text
        
  

text,tool_used,stop_reason = toolImplementation()
print(f'The claude is thinking {text}')
print(f'The tool used to solve problem is {tool_used} tool')

