import json

from taskserver import settings
from taskserver.task_manager import TaskManager, Task
from taskserver.errors import NoTasksToProcess, TaskFromJsonLoadingError,\
    UnknownTaskReceived, ResultTaskContentMismatch, SavingResultTaskError,\
    TaskFromFileLoadingError


tm = TaskManager(settings.tasks_dir, settings.ready_tasks_dir)


def unknown_action(_, __):
    return {'action': 'exit_client', 'reason': 'unknown_action'}


def get_task(tm, env):
    try:
        task = tm.next_task()
        result = {'action': 'process_task', 'task': task.as_dict()}

    except NoTasksToProcess:
        result = {'action': 'exit_client', 'reason': 'no tasks to process'}
    except TaskFromFileLoadingError:
        result = {'action': 'get_task'}
    return result


def stat(tm, _):
    return {'tasks_to_proc': len(tm.tasks),
        'tasks_in_proc': len(tm.tasks_in_process)}


def receive_task(tm, env):
    try:
        raw_data = env['wsgi.input'].read()
        task = Task.from_json(raw_data)
        tm.receive_task(task)
        result = {'action': 'get_task'}
    except TaskFromJsonLoadingError:
        result = {'action': 'exit_client', 'reason': 'wrong request format'}
    except (UnknownTaskReceived, ResultTaskContentMismatch, SavingResultTaskError):
        result = {'action': 'get_task'}
    return result


def get_action(env):
    uri = env['REQUEST_URI']
    uri = uri.strip('/')
    p_uri = uri.split('/')
    a = p_uri[0]
    actions = {'get_task': get_task, 'receive_task': receive_task, 'stat': stat}
    return actions.get(a, unknown_action)


def application(env, start_response):
    func = get_action(env)
    result = func(tm, env)
    start_response('200 OK', [('Content-Type','text/html')])
    return json.dumps(result)