# User asks math questions in natural language
# Claude decides which tool to use
# Your code performs the calculation
# Claude presents the result


import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get('API_KEY')
client = anthropic.Anthropic(api_key=api_key)
conversation_history = []

tools = [{
            "name": "add_numbers",
            "description": "Perform Addition operation ont the numbers given by user",
            "input_schema": {
                "type": "object",
                "properties": {
                    "number1": {
                        "type": "number",
                    },
                    "number2": {
                        "type": "number",
                    }
                },
                "required": ["number1","number2"],
            },
        },
        {
            "name": "subtract_numbers",
            "description": "Perform subtraction operation on the numbers given by user",
            "input_schema": {
                "type": "object",
                "properties": {
                    "number1": {
                        "type": "number",
                    },
                    "number2": {
                        "type": "number",
                    }
                },
                "required": ["number1","number2"],
            },
        },
        {
            "name": "multiply_numbers",
            "description": "Perform Multiplication operation on the numbers given by user",
            "input_schema": {
                "type": "object",
                "properties": {
                    "number1": {
                        "type": "number",
                    },
                    "number2": {
                        "type": "number",
                    }
                },
                "required": ["number1","number2"],
            },
        },
        {
            "name": "divide_numbers",
            "description": "Perform Division operation ",
            "input_schema": {
                "type": "object",
                "properties": {
                    "number1": {
                        "type": "number",
                    },
                    "number2": {
                        "type": "number",
                    }
                },
                "required": ["number1","number2"],
            },
        }]

def process_tool(tool_name,toolInputs):
  if tool_name == 'add_numbers':
    return toolInputs['number1'] + toolInputs['number2']
  elif tool_name == 'subtract_numbers':
    return toolInputs['number1'] - toolInputs['number2']
  elif tool_name == 'multiply_numbers':
    return toolInputs['number1'] * toolInputs['number2']
  elif tool_name == 'divide_numbers':
    if toolInputs['number2'] == 0:
       return "Error: Cannot divide by zero"
    return toolInputs['number1'] / toolInputs['number2']
  else :
      print('tool doesnt exist for the agent needed')


def perform_calculation():
  try:
    while (True):
      question = input('Ask question to claude:- ')
      if question.lower() in ['exit','quit','bye']:
        print('Good bye')
        if not question:
          continue
        break
      conversation_history = [{'role':'user','content':question}]
      response = client.messages.create(
        max_tokens=6000,
          thinking={
                'type': 'enabled',
                'budget_tokens': 5000
            },
        model='claude-sonnet-4-20250514',
        tools=tools,
        messages=conversation_history
      )
      if response.stop_reason=='tool_use':
        conversation_history.append({'role':'user','content':question})
        conversation_history.append({'role':'assistant','content':response.content})
        for block in response.content:
          if block.type == 'tool_use':
            tool_name = block.name
            tool_input = block.input
            tool_id = block.id

            result = process_tool(tool_name,tool_input)

            print(tool_name)
            print(f"   Result: {result}\n")

  except Exception as e:
    print(f"❌ Error: {e}")


perform_calculation()