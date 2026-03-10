# Tool name: create_task
# It should accept:

# title (string, required) - task name
# priority (must be "high", "medium", or "low" - use enum!)
# due_date (string, optional) - when it's due
# tags (array of strings, optional) - categories like ["work", "urgent"]
# estimated_hours (number, optional) - how long it takes

# Your task: Write the complete schema!

tool = {
  'name':'create_task',
  'description':'create a task with help of what task to perfomrm how important is the task and what is the deadline of it eg[Go to shopping tomorrow with low priority]',
  'input_schema':{
    'type':'object',
    'properties':{
      'task_name':{
        'type':'string',
         'minLength': 3, # ← NEW: At least 3 characters
        'maxLength': 100,  
        'description':'Plan the action to perform'
      },
      'priority':{
        'type':'string',
        'enum':['high','medium','low'],
        'default':'medium',
        'description':'explain the urgency to perform task'
      },'due_date':{
        'type':'string',
        'pattern': '^\\d{4}-\\d{2}-\\d{2}$',
        'description':'give deadline to finish the task '
      },
      'tags':{
        'type':'array',
        'items': 
        {
        'type': 'string',
        'enum': ['work', 'personal', 'urgent', 'project','coding']
        },
        'description':'explains the type of task to perform [eg create an jira ticket to log the bug for timal project]'
      },
      'estimated_hours':{
        'type':'number',
        'description':'how much time it took to perform the task'
      }
    },
    'required':['task_name','priority']
  }
}