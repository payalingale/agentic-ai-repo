import os
import anthropic
from dotenv import load_dotenv
from datetime import datetime
import random

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get('API_KEY'))

#in memory task
tasks=[]

def create_task():
  
def update_task():
   pass
def assign_task():
   pass
def delete_task():
   pass
def list_tasks():
   pass
def filter_tasks():
   pass
def set_deadline():
   pass
def add_comment():
   pass
def change_priority():
   pass
def mark_complete():
   pass



#tools definitions
tools = [ 
  {
    "name": "create_task",
    "description": (
      "Create a new task with details: [TaskName, Priority, Description, "
      "End Date, Status]. Example: "
      "'Create a task to start the multi-orchestration project with high "
      "priority, due day after tomorrow.'"
    ),
  },
  {
    "name": "update_task",
    "description": (
      "Update an existing task only (do not create a new one). Example: "
      "'Update the deadline of the multi-orchestration project to next "
      "month and set status to InProgress.'"
    ),
  },
  {
    "name": "assign_task",
    "description": (
      "Assign an existing task when its status is To-Do."
    ),
  },
  {
    "name": "delete_task",
    "description": (
      "Delete an existing task in To-Do or InProgress status. Example: "
      "'Delete the multi-orchestration project.'"
    ),
  },
  {
    "name": "list_tasks",
    "description": (
      "Show all tasks without any filters. Use only when user wants to "
      "see everything. Example: 'Show me all tasks.'"
    ),
  },
  {
    "name": "filter_tasks",
    "description": (
      "Filter tasks by status or priority. Example: "
      "'Show tasks with InProgress status.'"
    ),
  },
  {
    "name": "set_deadline",
    "description": (
      "Set or change ONLY the deadline of a task. Use when user only "
      "mentions changing the date. Example: "
      "'Finish the multi-orchestration project on 20th February.'"
    ),
  },
  {
    "name": "add_comment",
    "description": (
      "Add comments or remarks to an existing task or while creating a "
      "new task. Example: 'Add comment: this is a complicated task.'"
    ),
  },
  {
    "name": "change_priority",
    "description": (
      "Update only the priority of an existing task "
      "[high/medium/low]. Example: "
      "'Update the priority of the multi-orchestration project to low.'"
    ),
  },
  {
    "name": "mark_complete",
    "description": (
      "Mark an existing task as completed. Example: "
      "'Mark the multi-orchestration project as complete.'"
    ),
  },
]

def create_empty_task(name, priority, description, status, end_date=None, assignee=None, comments=None):
  if comments is None:      # ← Add this check!
        comments = []
  return {
    'id':len(tasks) + 1,
    'name':name,
    'priority': priority,    # Default value?
     'description': description, # Empty string?
     'end_date': end_date,    # None or empty?
     'status': status,      # Default status?
     'assignee': assignee,    # None or empty?
     'comments': comments,    # Empty list?
     'created_at': datetime.now().strftime('%Y-%m-%d')  # Current timestamp?'
  }