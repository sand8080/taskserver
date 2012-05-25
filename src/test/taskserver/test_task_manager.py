import os
import json
import unittest
import shutil

from test.root_test import RootTestCase
from taskserver.task_manager import TaskManager, Task, TaskFromFileLoadingError,\
    TaskFromJsonLoadingError
from taskserver.errors import UnknownTaskReceived, ResultTaskContentMismatch


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
    tasks_dir = os.path.join(c_dir, 'tasks', 'to_proc')
    r_t_dir = os.path.join(c_dir, 'tasks', 'ready')

    def test_tasks_to_proc(self):
        tm = TaskManager(self.tasks_dir, self.r_t_dir)
        exp_tasks = set(['1', 'one'])
        act_tasks = tm._tasks_to_proc()
        self.assertEquals(exp_tasks, act_tasks)

    def test_next_task_name(self):
        tm = TaskManager(self.tasks_dir, self.r_t_dir)
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

    def test_receive_task(self):
        # cleaning tasks_dirs
        tasks_dir = os.path.join(self.c_dir, 'test_receive_task')
        to_proc_dir = os.path.join(tasks_dir, 'to_proc')
        ready_dir = os.path.join(tasks_dir, 'ready')
        shutil.rmtree(tasks_dir, ignore_errors=True)
        # creating tasks
        os.makedirs(to_proc_dir)
        os.makedirs(ready_dir)
        task_name = '100'
        with open(os.path.join(to_proc_dir, task_name), 'w') as f:
            f.write('one\n')
            f.write('two\n')
        # testing task receive
        tm = TaskManager(to_proc_dir, ready_dir)
        self.assertTrue(task_name in os.listdir(to_proc_dir))
        self.assertTrue(task_name not in os.listdir(ready_dir))
        task = tm.next_task()
        self.assertEquals(1, len(tm.tasks_in_process))
        task.result = 'ready'
        tm.receive_task(task)
        self.assertTrue(task_name in os.listdir(to_proc_dir))
        self.assertTrue(task_name in os.listdir(ready_dir))
        self.assertEquals(0, len(tm.tasks_in_process))
        with open(os.path.join(ready_dir, task_name)) as f:
            self.assertEquals(task.result, f.read())

        # testing duplicate receive_task call
        task.result = 'new_%s' % task.result
        tm.receive_task(task)
        self.assertTrue(task_name in os.listdir(to_proc_dir))
        self.assertTrue(task_name in os.listdir(ready_dir))
        self.assertEquals(0, len(tm.tasks_in_process))
        with open(os.path.join(ready_dir, task_name)) as f:
            self.assertEquals(task.result, f.read())

        # cleaning tasks_dirs
        shutil.rmtree(tasks_dir, ignore_errors=True)

    def test_receive_task_failure(self):
        # cleaning tasks_dirs
        tasks_dir = os.path.join(self.c_dir, 'test_receive_task_failure')
        to_proc_dir = os.path.join(tasks_dir, 'to_proc')
        ready_dir = os.path.join(tasks_dir, 'ready')
        shutil.rmtree(tasks_dir, ignore_errors=True)
        # creating tasks
        os.makedirs(to_proc_dir)
        os.makedirs(ready_dir)
        task_name = '100'
        with open(os.path.join(to_proc_dir, task_name), 'w') as f:
            f.write('one\n')
            f.write('two\n')
        # testing task receive
        tm = TaskManager(to_proc_dir, ready_dir)
        self.assertTrue(task_name in os.listdir(to_proc_dir))
        self.assertTrue(task_name not in os.listdir(ready_dir))

        fake_task = Task('fake')
        self.assertRaises(UnknownTaskReceived, tm.receive_task, fake_task)

        wrong_content_task = Task.from_file(to_proc_dir, task_name)
        wrong_content_task.content = 'fake_%s' % wrong_content_task.content
        self.assertRaises(ResultTaskContentMismatch, tm.receive_task,
            wrong_content_task)

        # cleaning tasks_dirs
        shutil.rmtree(tasks_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()