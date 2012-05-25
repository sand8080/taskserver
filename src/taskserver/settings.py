import os
import logging


c_dir = os.path.dirname(__file__)

tm_log_file = os.path.join(c_dir, '..', 'log', 'taskmanager.log')
tm_log_level = logging.DEBUG

tasks_dir = os.path.join(c_dir, '..', 'tasks', 'to_proc')
ready_tasks_dir = os.path.join(c_dir, '..', 'tasks', 'ready')