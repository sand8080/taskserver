import os
import json
from taskserver.errors import TaskFromFileLoadingError, TaskFromJsonLoadingError,\
    NoTasksToProcess, UnknownTaskReceived, ResultTaskContentMismatch,\
    SavingResultTaskError
from taskserver.log import init_logger
from taskserver import settings


class Task:
    def __init__(self, name, content=None, result=None):
        self.name = name
        self.content = content
        self.result = result

    def as_json(self):
        return json.dumps({'name': self.name, 'content': self.content})

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.__dict__)

    @staticmethod
    def from_file(tasks_dir, task_name):
        try:
            with open(os.path.join(tasks_dir, task_name)) as f:
                content = f.read()
                return Task(task_name, content=content)
        except Exception:
            raise TaskFromFileLoadingError

    @staticmethod
    def from_json(raw_task):
        try:
            data = json.loads(raw_task)
            return Task(data['name'], content=data['content'],
                result=data['result'])
        except Exception:
            raise TaskFromJsonLoadingError


class TaskManager:
    def __init__(self, tasks_dir, processed_tasks_dir):
        self.tasks_dir = tasks_dir
        self.processed_tasks_dir = processed_tasks_dir
        self.tasks = self._tasks_to_proc()
        self.tasks_in_process = set()
        self.l = init_logger('taskmanager', settings.tm_log_file,
            settings.tm_log_level)
        self.l.info('Task manager initiated: %s', self)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.__dict__)

    def _tasks_to_proc(self):
        '''
        loads tasks names from tasks_dir
        excludes task names from processed_tasks_dir from result
        returns set of tasks names
        '''
        def filter_dir(dir_path):
            tasks_names = filter(lambda x: os.path.isfile(os.path.join(dir_path, x)),
                os.listdir(dir_path))
            return set(tasks_names)
        tasks = filter_dir(self.tasks_dir)
        proc_tasks = filter_dir(self.processed_tasks_dir)
        return tasks - proc_tasks

    def next_task_name(self):
        '''
        gets task name to process
        if no tasks in self.tasks swapping self.tasks with self.tasks_in_process
        '''
        self.l.debug('Fetching next task name')
        if len(self.tasks) == 0:
            self.l.info('Moving tasks in progress to tasks set')
            self.tasks = self.tasks_in_process
            self.tasks_in_process = set()
        try:
            task = self.tasks.pop()
            self.l.debug('Task "%s" is in process', task)
            self.tasks_in_process.add(task)
            self.l.debug('Got task "%s" to process', task)
            return task
        except KeyError:
            self.l.debug('No tasks to process')
            raise NoTasksToProcess

    def next_task(self):
        '''
        returns next Task to process
        '''
        t_name = self.next_task_name()
        try:
            return Task.from_file(self.tasks_dir, t_name)
        except TaskFromFileLoadingError, e:
            self.l.error('Task "%s" in tasks to proc, but not in file system')
            self.tasks.discard(t_name)
            self.tasks_in_process.discard(t_name)
            self.l.info('Removed task "%s" discarded in tasks set to proc')
            raise e

    def receive_task(self, task):
        self.l.debug('Task "%s" received', task.name)
        try:
            task_origin = Task.from_file(self.tasks_dir, task.name)
        except TaskFromFileLoadingError:
            self.l.error('Task "%s" is not found in "%s"', task.name, self.tasks_dir)
            raise UnknownTaskReceived

        if task_origin.content != task.content:
            self.l.error('Task "%s" with wrong content', task.name)
            raise ResultTaskContentMismatch

        try:
            self.l.debug('Saving task "%s"', task.name)
            with open(os.path.join(self.processed_tasks_dir, task.name), 'w') as f:
                f.write(task.result)

            self.l.debug('Removing task "%s" from tasks lists', task.name)
            self.tasks.discard(task.name)
            self.tasks_in_process.discard(task.name)
            self.l.debug('Task "%s" processed')
        except Exception:
            self.l.error('Task "%s" saving error', task.name)
            raise SavingResultTaskError