Tools=[
{
'name': 'create_task',
'description': 'create an task when new task needs to be created with details as [TaskName,Priority,Description of task,End Date,Status]
for eg [create an task to start multi-orchestration project wtih priority as high and will be able to finish by day after tomorrow]'
},
{
'name': 'update_task',
'description': 'Update the existing task only dont create an new one when asked for update this should work for updating the existing created task update task will work as for eg[update the deadline of multi-orchestration project to next month and update the status to InProgress] '
},
{
'name': 'assign_task',
'description': 'Task will be assigned when the task is already created and its in To-Do state '
}
{
'name':'delete_task',
'description':'Delete task will be used to delete the existing task which are in_progress status or to_do status for eg[Delete the multi-orchestration project]'
}
{
'name':'list_tasks',
'description':'show me all task without filter Use ONLY when user wants to see everything. Example: "Show me all tasks"'
}
{
'name':'filter_tasks',
'description':'Filter the task which are already added in list based on status or priority eg[give me list of task for In_progress status]'
}
{
'name':'set_deadline',
'description':'Sets or changes ONLY the deadline of a task. Use when user ONLY mentions changing the date, nothing else. eg[Finish the multi-orchestration project on 20th February]'
}
{
'name':'add_comment',
'description':'Add the comments or remarks for task which is already created or while creating new task eg[for multi-orchestration project add comment as this is an complicated task]'
}
{
'name':'change_priority',
'description':'Only Update the priority of existing task from [high/low/medium] eg[update the priority of multi-orchestration project to low]'
}
{
'name':'mark_complete',
'description':'Mark the status as completed for specific selected task only which already exist eg[change the status of multi-orchestration project to complete]'
}
]
