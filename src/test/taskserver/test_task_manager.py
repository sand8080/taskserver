import os
import unittest

from test.root_test import RootTestCase
#from taskserver import load_tasks
from taskserver.task_manager import TaskManager


class TaskManagerTestCase(RootTestCase):
    c_dir = os.path.dirname(__file__)
    t_dir = os.path.join(c_dir, 'tasks', 'to_proc')
    r_t_dir = os.path.join(c_dir, 'tasks', 'ready')

    def test_tasks_to_proc(self):
        tm = TaskManager(self.t_dir, self.r_t_dir)
        exp_tasks = set(['1', 'one'])
        act_tasks = tm._tasks_to_proc()
        self.assertEquals(exp_tasks, act_tasks)

    def test_next_task_name(self):
        tm = TaskManager(self.t_dir, self.r_t_dir)
        tasks_num = len(tm.tasks)
        self.assertTrue(tasks_num>0)
        self.assertTrue(len(tm.tasks_in_process)==0)
        for _ in range(tasks_num):
            t_name = tm.next_task_name()
            self.assertTrue(t_name in tm.tasks_in_process)
            self.assertTrue(t_name not in tm.tasks)

        # checking tasks_in_process switching with tasks
        self.assertEquals(0, len(tm.tasks))
        self.assertEquals(tasks_num, len(tm.tasks_in_process))
        t_name = tm.next_task_name()
        self.assertEquals(tasks_num - 1, len(tm.tasks))
        self.assertEquals(1, len(tm.tasks_in_process))
        self.assertTrue(t_name in tm.tasks_in_process)
        self.assertTrue(t_name not in tm.tasks)




if __name__ == '__main__':
    unittest.main()