import os


class NoTasksToProcess(Exception):
    pass


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
        if len(self.tasks)==0:
            self.tasks = self.tasks_in_process
            self.tasks_in_process = set()
        try:
            task = self.tasks.pop()
            self.tasks_in_process.add(task)
            return task
        except KeyError:
            raise NoTasksToProcess


    def get_task(self):
        pass
        pass
