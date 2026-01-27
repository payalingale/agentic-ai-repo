import os
from datetime import datetime,timedelta
from dotenv import load_dotenv
import json
import anthropic
load_dotenv()

File_path = os.path.join(os.path.dirname(__file__),'finances.json')
api_key = os.environ.get('API_KEY')
client = anthropic.Anthropic(api_key=api_key)

def process_tool(tool_name,tool_input):
   if tool_name =='log_expense':
    return log_expense(tool_input['amount'],tool_input['category'],tool_input['description'])
   elif tool_name == 'log_income':
      return log_income(tool_input['amount'],tool_input['source'])
   elif tool_name == 'get_monthly_summary':
      return get_monthly_summary()
   elif tool_name == 'check_budget':
      return check_budget()
   elif tool_name == 'get_savings_progress':
      return get_savings_progress()
   elif tool_name == 'set_savings_goal':
      return set_savings_goal(tool_input['target'],tool_input['purpose'])
   else :
      print('tool doesnt exist for the agent needed')
   
def ask_finance_ai(question):  # ← Add parameter
    conversation_history = [
        {"role": "user", "content": question}
    ]
    
    tools_used = []
    
    while True:
        response = client.messages.create(
            max_tokens=6000,
            model='claude-sonnet-4-20250514',
            thinking={
                'type': 'enabled',
                'budget_tokens': 5000
            },
            tools=tools,
            messages=conversation_history  
        )
        
        if response.stop_reason == 'tool_use':
            print("\n🤖 AI is using tools...\n")
            
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tool_id = block.id
                    
                    tools_used.append(tool_name)
                    
                    print(f"Using: {tool_name}")
                    
                    # TODO: Execute the tool
                    tool_result = process_tool(tool_name, tool_input)
                    
                    print(f"   Result: {tool_result}\n")
                    
                    # TODO: Add assistant response to history
                    conversation_history.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    
                    # TODO: Add tool result to history
                    conversation_history.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": str(tool_result)
                        }]
                    })
            
            continue  
        
        # No tool use - extract final answer
        final_text = ""
        for block in response.content:
            if block.type == "text":
                final_text += block.text
        
        return final_text  # ← Return final answer
tools = [
    {
        'name': 'log_expense',
        'description': 'Log a new expense with amount, category, and description',
        'input_schema': {
            'type': 'object',
            'properties': {
                'amount': {
                    'type': 'number',
                    'description': 'Amount spent in dollars'
                },
                'category': {
                    'type': 'string',
                    'description': 'Category: groceries, transport, entertainment, bills, other'
                },
                'description': {
                    'type': 'string',
                    'description': 'What was purchased'
                }
            },
            'required': ['amount', 'category']
        }
    },
    {
        'name': 'log_income',
        'description': 'Log income received',
        'input_schema': {
            'type': 'object',
            'properties': {
                'amount': {
                    'type': 'number',
                    'description': 'Amount received in dollars'
                },
                'source': {
                    'type': 'string',
                    'description': 'Source of income (salary, freelance, gift, etc.)'
                },
                'description': {
                    'type': 'string',
                    'description': 'Description of income'
                }
            },
            'required': ['amount', 'source']
        }
    },
    {
        'name': 'get_monthly_summary',
        'description': 'Get summary of expenses and income for current month',
        'input_schema': {
            'type': 'object',
            'properties': {},
            'required': []
        }
    },
    {
        'name': 'check_budget',
        'description': 'Check if spending is within budget limits',
        'input_schema': {
            'type': 'object',
            'properties': {
                'category': {
                    'type': 'string',
                    'description': 'Optional: check specific category budget'
                }
            },
            'required': []
        }
    },
    {
        'name': 'get_savings_progress',
        'description': 'Check progress toward savings goal',
        'input_schema': {
            'type': 'object',
            'properties': {},
            'required': []
        }
    },
    {
        'name': 'set_savings_goal',
        'description': 'Set or update savings goal',
        'input_schema': {
            'type': 'object',
            'properties': {
                'target': {
                    'type': 'number',
                    'description': 'Target amount to save'
                },
                'purpose': {
                    'type': 'string',
                    'description': 'What you are saving for'
                }
            },
            'required': ['target', 'purpose']
        }
    }
]

#Task 1: File Management Functions (30 min)

def load_finances():
    """Load finances.json file"""
    try:
        if(os.path.exists(File_path)):
            with open (File_path,'r')as f:
                content = f.read()
                if content:
                    json_data =  json.loads(content)
                else:
                    print('File is empty')
            return json_data
    except Exception as e:
        return{f'Error received as str{e}'}

def save_finances(expenses):
    """Save to finances.json file"""
    with open(File_path,'w')as f:
        json.dump(expenses,f,indent=2)
                  
#Task 2: Tool Implementations (60 min)
def log_expense(amount, category, description=""):
   finances = load_finances()
   expenses = {
       'date':str(datetime.now().date()),
      'amount': amount, 'category': category, 'description': description,
      'timestamp':datetime.now().strftime("%H:%M")
   }
   finances['expenses'].append(
       expenses)
   save_finances(finances)


def log_income(amount,source,description=''):
    finances = load_finances()
    incomes = {
    'date':str(datetime.now().date()),
    'amount':amount,
    'source':source,
    'description':description
    }
    finances['income'].append(incomes)
    save_finances(finances)
    print(f'income {finances}')

def set_savings_goal(target,purpose=''):
     finances = load_finances()
     savings = {
    'target':target,
    'purpose':purpose
    }
     finances['savings_goal'].update(savings)
     save_finances(finances)
     print(f'income {finances}')
     print('saving goals')

def get_monthly_summary():
 try:
    finances = load_finances()
    currentDate = datetime.now().date()
    monthlyDates = [str(currentDate - timedelta(days=i)) for i in range(30)]
    monthly_summary ={}

    for expense in finances['expenses']:
     if expense['date'] in monthlyDates:
       cat = expense['category']
       if  cat in monthly_summary:
          monthly_summary[cat] += expense['amount']
       else:
          monthly_summary[cat] = expense['amount']
          
    return monthly_summary
 except Exception as e:
     return {f'Error as str{e}'}

def check_budget():
   finances = load_finances()
   currentDate = datetime.now().date()
   monthlyDate = [str(currentDate-timedelta(days=i)) for i in range(30)]

   total_spend_monthly = 0
   budgetAmt=0
   for expenses in finances['expenses']:
      if expenses['date'] in monthlyDate:
         total_spend_monthly += expenses['amount']
         budgetAmt = finances['budget']['monthly_limit']
   if total_spend_monthly >= budgetAmt:
      return f'spending exceeded :-{total_spend_monthly - budgetAmt}'
   else :
      return f'You still have budget to spend {budgetAmt - total_spend_monthly}'

         
def get_savings_progress():
   finances = load_finances()
   saving_goal = finances['savings_goal']
   percentage = (saving_goal['current']/saving_goal['target'])*100
   return f'You have reached saving {percentage} %'


def main():
    print("💰 Personal Finance AI Agent")
    print("Track expenses, income, and savings goals!\n")
    print("Examples:")
    print("  - I spent 50 dollars on groceries")
    print("  - I earned 500 from freelancing")
    print("  - Show my monthly summary")
    print("  - Am I over budget?")
    print("  - Set savings goal of 2000 for vacation\n")

    while True:
        question = input("You: ").strip()
        
        if question.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        if not question:
            continue
        
        try:
            response = ask_finance_ai(question)
            print(f"\n🤖 AI: {response}\n")
            print("-" * 60 + "\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == '__main__':
    main()


# # print(get_monthly_summary('expenses'))
# print(get_savings_progress())

        
   
