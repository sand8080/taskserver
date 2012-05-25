taskserver
==========

 Simple server for ditributed tasks processing.
 Works over http. Realized operations:
 + get_task
 + receive_task
 + stat
 + reload_tasks

For getting task operation just open http://localhost:11233/get_task.  
Task is json serialized dict in format `{'name': str, 'content': str}`.  
Result of task processing is json serialized dict in format `{'name': str, 'content': str, 'result': str}`.  
Usage sample is in `taskserver.client`.  