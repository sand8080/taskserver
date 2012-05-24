import os
import json


class TaskException(Exception):
    pass


class NoTasksToProcess(TaskException):
    pass


class TaskFromJsonLoadingError(TaskException):
    pass


class TaskFromFileLoadingError(TaskException):
    pass


class Task:
    def __init__(self, name, content=None, result=None):
        self.name = name
        self.content = content
        self.result = result

    def as_json(self):
        return json.dumps({'name': self.name, 'content': self.content})

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
        self.t_dir = tasks_dir
        self.p_t_dir = processed_tasks_dir
        self.tasks = self._tasks_to_proc()
        self.tasks_in_process = set()

    def _tasks_to_proc(self):
        '''
        loads tasks names from tasks_dir
        excludes task names from processed_tasks_dir from result
        returns deque of tasks names
        '''
        def filter_dir(dir_path):
            tasks_names = filter(lambda x: os.path.isfile(os.path.join(dir_path, x)),
                os.listdir(dir_path))
            return set(tasks_names)
        tasks = filter_dir(self.t_dir)
        proc_tasks = filter_dir(self.p_t_dir)
        return tasks - proc_tasks

    def next_task_name(self):
        '''
        gets task name to process
        if no tasks in self.tasks swapping self.tasks with self.tasks_in_process
        '''
        if len(self.tasks)==0:
            self.tasks = self.tasks_in_process
            self.tasks_in_process = set()
        try:
            task = self.tasks.pop()
            self.tasks_in_process.add(task)
            return task
        except KeyError:
            raise NoTasksToProcess

    def next_task(self):
        '''
        returns next Task to process
        '''
        t_name = self.next_task_name()
        Task(self.t_dir, t_name)

    def receive_task(self):
        pass