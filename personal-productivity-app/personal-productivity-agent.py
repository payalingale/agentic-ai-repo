#step1:log daily activity
import os
import anthropic
from dotenv import load_dotenv
import json
from datetime import datetime,timedelta

load_dotenv()

api_key = os.environ.get('API_KEY')
client = anthropic.Anthropic(api_key=api_key)
Log_activity_file = os.path.join(os.path.dirname(__file__), 'activity.json')
tools =[{
  'name':'addActivity',
  'description':'Log a new productivity activity with name, duration, and optional notes',
    'input_schema':{
    'type':'object',
    'properties':{
      'activity_name': {
                    'type': 'string',
                    'description': 'Name of the activity (e.g., "Coding", "Reading", "Exercise")'
                },
      'duration_minutes': {
                    'type': 'integer',
                    'description': 'Duration in minutes'
                },
      'notes': {
                    'type': 'string',
                    'description': 'Optional notes about the activity'
                }
    },
  'required':['activity_name', 'duration_minutes','notes']
    }
},
{'name': 'get_weekly_summary',
        'description': 'Get a summary of all activities for the past 7 days',
        'input_schema': {
            'type': 'object',
            'properties': {},
            'required': []
        }
}
    ,
    {
        'name': 'get_activity_stats',
        'description': 'Get detailed statistics for a specific activity',
        'input_schema': {
            'type': 'object',
            'properties': {
                'activity_name': {
                    'type': 'string',
                    'description': 'Name of the activity to analyze'
                }
            },
            'required': ['activity_name']
        }
        }]

def process_tool(tool_name,tool_input):
  """Execute the appropriate tool"""
  print(f"🔧 Executing tool: {tool_name}")
  print(f"   Input: {tool_input}")
  if tool_name=='addActivity':
      return userActivities(
            activity_name=tool_input['activity_name'],
            duration_minutes=tool_input['duration_minutes'],
            notes=tool_input.get('notes', '')
        )
  elif tool_name == 'get_weekly_summary':
     return weeklyProgress()
  elif tool_name == 'get_activity_stats':
        return get_activity_stats(tool_input['activity_name'])
  else:
     return {"error": f"Unknown tool: {tool_name}"}
    

def userActivities(activity_name, duration_minutes, notes=""):
  try:
    now = datetime.now()
    currentDate = str(now.date())   
    # Return as a list to allow multiple activities per day
    activityData = {
     currentDate: [
        {
          'activityName': activity_name,
          'durationInMin': duration_minutes,
          'notes': notes,
          'timestamp': now.strftime('%H:%M')
        }
      ]
    }
    result = saveToJson(activityData)
    return {
            "status": "success",
            "activity": activity_name,
            "duration": duration_minutes,
            "date": currentDate,
            "message": f"Logged {duration_minutes} minutes of {activity_name}"
        }
  except Exception as e:
    return {f'The exception is ${str(e)}'}

def loadJson():
    try:
      existing_data = {}
      if os.path.exists(Log_activity_file):
        with open(Log_activity_file, 'r') as f:
          content = f.read()
          if content:
            existing_data = json.loads(content)
      return existing_data
    except Exception as e:
      print(f'Error loading JSON: {str(e)}')

def saveToJson(activityData):
  try:
    existing_data = loadJson()
    for date,activities in activityData.items():
        if date in existing_data:
          existing_data[date].extend(activities)
        else:
          existing_data[date]=activities
    with open(Log_activity_file, 'w') as f:
      json.dump(existing_data, f, indent=2)
    print(f'Activity saved successfully to {Log_activity_file}')
  except Exception as e:
    print(f'The exception is {str(e)}')


def weeklyProgress():
  try:
    activityData = loadJson()
    date = datetime.now().date()
    weeklyDates = [str(date - timedelta(days=i)) for i in range(7)]
    summary = {
            'total_activities': 0,
            'total_minutes': 0,
            'activities_breakdown': {},
            'days_logged': 0
        }
    days_with_data = set()
    for date,activities in activityData.items():
     if date in weeklyDates:
      for activity in activities:
         name = activity['activityName']
         duration = activity['durationInMin']
         if name in summary['activities_breakdown']:
          summary[name] += duration
         else:
          summary[name]=duration
    summary['days_logged'] = len(days_with_data)
    return summary
  except Exception as e:
     return {"error": str(e)}

def get_activity_stats(activity_name):
    """Get stats for a specific activity - FIXED!"""
    try:
        activityData = loadJson()  # ← Load the data!
        date = datetime.now().date()
        weeklyDates = [str(date - timedelta(days=i)) for i in range(7)]
        
        stats = {
            'activity': activity_name,
            'total_minutes': 0,
            'days_practiced': 0,
            'sessions': []
        }
        
        for date_key, activities in activityData.items():
            if date_key in weeklyDates:
                day_found = False
                for activity in activities:
                    if activity['activityName'].lower() == activity_name.lower():
                        stats['total_minutes'] += activity['durationInMin']
                        stats['sessions'].append({
                            'date': date_key,
                            'duration': activity['durationInMin'],
                            'notes': activity.get('notes', '')
                        })
                        day_found = True
                
                if day_found:
                    stats['days_practiced'] += 1
        
        return stats
    except Exception as e:
        return {"error": str(e)}


def ask_ai_assistant(question):
    """Ask Claude about your productivity data"""
    
    conversation_history = [
        {"role": "user", "content": question}
    ]
    
    tools_used = []
    
    while True:
        response = client.messages.create(
            max_tokens=4096,
            thinking={
                'type': 'enabled',
                'budget_tokens': 3000
            },
            model='claude-sonnet-4-20250514',
            tools=tools,
            messages=conversation_history
        )
        
        # Check if Claude wants to use a tool
        if response.stop_reason == "tool_use":
            print("\n🤖 AI is analyzing your data...\n")
            
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tool_id = block.id
                    
                    tools_used.append(tool_name)
                    
                    print(f"📊 Using: {tool_name}")
                    
                    # Execute the tool
                    tool_result = process_tool(tool_name, tool_input)
                    
                    print(f"   Result: {tool_result}\n")
                    
                    # Add to conversation
                    conversation_history.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    conversation_history.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": str(tool_result)
                        }]
                    })
            
            continue
        
        # Extract final response
        final_text = ""
        for block in response.content:
            if block.type == "text":
                final_text += block.text
        
        return final_text



def main():
    print("🤖 AI Productivity Assistant")
    print("Ask me to log activities or analyze your productivity!\n")
    print("Examples:")
    print("  - Log 120 minutes of coding")
    print("  - Show my weekly summary")
    print("  - How much time did I spend on exercise?")
    print("  - What's my most productive activity?\n")
    
    while True:
        question = input("\nYou: ").strip()
        
        if question.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        if not question:
            continue
        
        try:
            response = ask_ai_assistant(question)
            print(f"\n🤖 AI: {response}\n")
            print("-" * 60)
        except Exception as e:
            print(f"❌ Error: {e}\n")



if __name__ == '__main__':
  main()