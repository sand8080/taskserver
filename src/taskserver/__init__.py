import os


def load_tasks(tasks_dir, processed_tasks_dir):
    '''
    loads tasks names from tasks_dir
    excludes task names from processed_tasks_dir from result
    returns set of tasks names
    '''
    def filter_dir(dir_path):
        tasks_names = filter(lambda x: os.path.isfile(os.path.join(dir_path, x)),
            os.listdir(dir_path))
        return set(tasks_names)
    tasks = filter_dir(tasks_dir)
    proc_tasks = filter_dir(processed_tasks_dir)
    return tasks - proc_tasks