#step1:log daily activity
import os
import anthropic
from dotenv import load_dotenv
import json
from datetime import datetime
load_dotenv()

api_key = os.environ.get('API_KEY')
client = anthropic.Anthropic(api_key=api_key)
Log_activity_file = os.path.join(os.path.dirname(__file__), 'activity.json')


def userActivities():
  try:
    now = datetime.now()
    currentDate = str(now.date())
    print(currentDate)
    print(type(currentDate))
    activity = input('Enter activity :-')
    durationMin = int(input('Enter the duration for activity you performed:- '))
    notes = input('Add notes if you like :- ')
    timestamp = input('when did u do the activity:- ')
    
    # Return as a list to allow multiple activities per day
    return {
      currentDate: [
        {
          'activity': activity,
          'duration': durationMin,
          'notes': notes,
          'timestamp': timestamp
        }
      ]
    }
  except Exception as e:
    return {f'The exception is ${str(e)}'}

def loadJson(activityData):
    try:
      existing_data = {}
      if os.path.exists(Log_activity_file):
        with open(Log_activity_file, 'r') as f:
          content = f.read()
          if content:
            existing_data = json.loads(content)
      # Append activities instead of replacing
      for date,activities in activityData.items():
        if date in existing_data:
          existing_data[date].extend(activities)
        else:
          existing_data[date]=activities
      return existing_data
    except Exception as e:
      print(f'Error loading JSON: {str(e)}')
      return activityData

def saveToJson(activityData):
  try:
    existing_data = loadJson(activityData)
    with open(Log_activity_file, 'w') as f:
      json.dump(existing_data, f, indent=2)
    print(f'Activity saved successfully to {Log_activity_file}')
  except Exception as e:
    print(f'The exception is {str(e)}')

def weeklyProgress(activityData):
     """
    What this function must do:
    1. Get last 7 days of dates
    2. Load productivity_log.json
    3. For each activity, calculate:
       - Total minutes this week
       - Number of days worked on it
    4. Return formatted summary
    """
last7dayData = datetime.now-7()


def main():
  # userData = userActivities()
  loadJson(userData)
  # saveToJson(userData)



if __name__ == '__main__':
  main()