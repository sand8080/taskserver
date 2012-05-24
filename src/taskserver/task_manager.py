import os
import hashlib
import json


class NoTasksToProcess(Exception):
    pass


class Task:
    def __init__(self, tasks_dir, task_name):
        self.name = task_name
        self.t_dir = tasks_dir
        self.hash, self.content = self._load_task()

    def _load_task(self):
        with open(os.path.join(self.t_dir, self.name)) as f:
            content = f.read()
            md5 = hashlib.md5(content)
            return md5.hexdigest(), content

    def as_json(self):
        return json.dumps({'name': self.name, 'hash': self.hash,
            'content': self.content})


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