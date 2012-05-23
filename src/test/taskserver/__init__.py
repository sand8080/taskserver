import os
import unittest

from test.root_test import RootTestCase
from taskserver import load_tasks


class TaskServerTestCase(RootTestCase):
    def test_load_tasks(self):
        c_dir = os.path.dirname(__file__)
        t_dir = os.path.join(c_dir, 'tasks', 'to_proc')
        r_t_dir = os.path.join(c_dir, 'tasks', 'ready')
        exp_tasks = set(['1', 'one'])
        act_tasks = load_tasks(t_dir, r_t_dir)
        self.assertEquals(exp_tasks, act_tasks)


if __name__ == '__main__':
    unittest.main()