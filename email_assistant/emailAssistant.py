
import os
import anthropic
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get('API_KEY')
client = anthropic.Anthropic(api_key=api_key)

tools = [{
  'name':'adjust_tone',
  'description':'The tone should be updated as per client need',
  'input_schema':{
    'type':'object',
    'properties':{
      'email':{
      'type':'string',
      'description':'original email text'},
      'tone':{
      'type':'string',
      'description':'adjust the tone based on customer need'
    }
    },
    'required':['email','tone']
  },
  
}]

def process_tools(tool_name,tool_input):
  if tool_name == 'adjust_tone':
    return tool_adjust_tone(tool_input['email'],tool_input['tone'])
  

def tool_adjust_tone(email, tone):
    prompt = f'Rewrite an existing email with proper subject and body with modifying the body of {email} based on {tone} expected by customer'
    conversation_history=[{
   'role':'user',
   'content':prompt
  }]
    response = client.messages.create(
     max_tokens=6000,
     model='claude-sonnet-4-20250514',
     thinking={
      'type':'enabled',
      'budget_tokens':4096
     },
     messages=conversation_history
    )
    return response.content

def draft_email_simple(description):
 prompt = f'Draft an email with proper subject line which also contains the body and in proper structure it should also address someone and the email should be drafted based on {description} '

 conversation_history=[{
   'role':'user',
   'content':prompt
  }]
 response = client.messages.create(
     max_tokens=6000,
     model='claude-sonnet-4-20250514',
     thinking={
      'type':'enabled',
      'budget_tokens':4096
     },
     messages=conversation_history
    )
 return response.content

def format_email_display(email):
  print("\n" + "="*60)
  print("📧 DRAFTED EMAIL")
  print("="*60)
  for block in email:
    if block.type == 'text':
      print(f'{block.text}')
  print("="*60 + "\n")

def ask_assistant_with_tools(question, current_email=None):
     # 1. Create conversation history
    conversation_history = [{
       'role':'user',
       'content':question
    }]
    while True:
      response = client.messages.create(
       max_tokens=6000,
       model='claude-sonnet-4-20250514',
       thinking={
          'type':'enabled',
          'budget_tokens':4096
       },
       tools=tools,
       messages=conversation_history
    )
      used_tool = False
      for block in response.content:
        if getattr(block, 'stop_reason', None) == 'tool_use':
          tool_name = block.tool_name 
          tool_input = block.tool_input
          tool_id = block.tool_id
          if tool_name == 'adjust_tone':
            tool_result = process_tools(tool_name, tool_input)
            used_tool = True
          
      if used_tool:
        conversation_history.append({'role':'assisant','result' :response.content})

        conversation_history.append({
          'role':'user',
          'content':[
            {
              'type':'tool_result',
              'tool_use_id':tool_id,
              'content': str(tool_result)
            }
          ]
        })
       # Add tool result
        conversation_history.append({
                          'role':'user',
                          'content':[{
                              'type':'tool_result',
                              'tool_use_id':tool_id,
                              'content':str(tool_result)
                          }]
                      })
        continue
      return response.content

def main():
  print('Welcome to Email Assistant')
  print('_'*40)
  current_email = None
  while True:
   if current_email is None:
    print('\n What email do you need?')
    description = input('Describe the email').strip()

    if description in ['exit','quit']:
      print('GoodBye')
      break

    if not description:
      continue

    print('\n Drafting email')
    email_content = draft_email_simple(description)
    format_email_display(email_content)

    for email in email_content:
      if email.type == 'text':
        current_email = email.text
        break
   # Mode 2: Options menu
   print('\n Options:')
   print("  'adjust [formal/casual/warm/direct]' - Change tone")
   print("  'new' - Draft new email")
   print("  'quit' - Exit")

   command = input('\nCommand..').strip()
   valid_tones = ['warm','formal','direct','casual']
   if command == 'quit':
    print('\n👋 Goodbye!')
    break     
   elif command == 'new':
      current_email = None
      continue
   elif command.startswith('adjust '):
       tone = command.replace('adjust ', '').strip()
       valid_tones = ['warm', 'formal', 'direct', 'casual']
            
       if tone not in valid_tones:
         print(f"❌ Invalid tone. Choose from: {', '.join(valid_tones)}")
         continue

  question = f'Adjust the email {command} tone:\n\n for {current_email}'
  adjusted_content = ask_assistant_with_tools(question)
  
  format_email_display(adjusted_content)
  for block in adjusted_content:
    if block.type == 'text':
     current_email = block.text
     break
    else:
      print("❌ Unknown command")


if __name__ == '__main__':
    main()