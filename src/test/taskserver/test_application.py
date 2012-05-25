import unittest

from test.root_test import RootTestCase
from taskserver.application import get_action, get_task, unknown_action, stat,\
    receive_task, reload_tasks


class ApplicationTestCase(RootTestCase):
    def test_get_action(self):
        self.assertEquals(get_task, get_action({'REQUEST_URI': '/get_task'}))
        self.assertEquals(get_task, get_action({'REQUEST_URI': 'get_task'}))
        self.assertEquals(get_task, get_action({'REQUEST_URI': 'get_task/'}))
        self.assertEquals(get_task, get_action({'REQUEST_URI': '/get_task/'}))
        self.assertEquals(unknown_action, get_action({'REQUEST_URI': '/'}))
        self.assertEquals(unknown_action, get_action({'REQUEST_URI': ''}))
        self.assertEquals(stat, get_action({'REQUEST_URI': 'stat'}))
        self.assertEquals(receive_task, get_action({'REQUEST_URI': 'receive_task'}))
        self.assertEquals(reload_tasks, get_action({'REQUEST_URI': 'reload_tasks'}))


if __name__ == '__main__':
    unittest.main()