import os
import unittest

from test.root_test import RootTestCase
from taskserver.task_manager import TaskManager, Task, TaskFromFileLoadingError,\
    TaskFromJsonLoadingError
import json


class TaskTestCase(RootTestCase):
    def test_from_file(self):
        c_dir = os.path.dirname(__file__)
        tasks_dir = os.path.join(c_dir, 'tasks', 'to_proc')
        task_name = 'one'
        t = Task.from_file(tasks_dir, task_name)
        exp_content = 'some content'
        self.assertEquals(task_name, t.name)
        self.assertEquals(exp_content, t.content)
        self.assertEquals(None, t.result)

    def test_from_file_loading_error(self):
        c_dir = os.path.dirname(__file__)
        tasks_dir = os.path.join(c_dir, 'tasks', 'to_proc')
        task_name = 'fake'
        self.assertRaises(TaskFromFileLoadingError, Task.from_file, tasks_dir, task_name)

    def test_from_json(self):
        name = 'a'
        content = 'cccdd o'
        result = 'res'
        json_task = json.dumps({'name': name, 'content': content,
            'result': result})
        t = Task.from_json(json_task)
        self.assertEquals(name, t.name)
        self.assertEquals(content, t.content)
        self.assertEquals(result, t.result)

    def test_from_json_loading_error(self):
        self.assertRaises(TaskFromJsonLoadingError, Task.from_json, 'na: 44')
        raw_task = json.dumps({'no': 'fields'})
        self.assertRaises(TaskFromJsonLoadingError, Task.from_json, raw_task)


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