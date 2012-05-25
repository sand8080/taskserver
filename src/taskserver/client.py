import urllib2
import json
import time


def get_task(server_url):
    print '### getting task'
    f = urllib2.urlopen('%s/get_task' % server_url)
    raw_task = f.read()
    return json.loads(raw_task)


def receive_task(server_url, task):
    print '### receiveing task', task
    f = urllib2.urlopen('%s/receive_task' % server_url, data=json.dumps(task))
    raw_task = f.read()
    return json.loads(raw_task)


class StopProcessing(Exception):
    pass


class NextTask(Exception):
    pass


def check_action(task):
    action = task['action']
    if action == 'exit_client':
        print '### exiting client:', task['reason']
        raise StopProcessing
    elif action == 'get_task':
        print '### getting next task'
        raise NextTask
    elif action == 'process_task':
        print '### processing action'
    else:
        print '### exiting client. unknown action:', action
        raise StopProcessing


def process_task(task):
    result = dict(task['task'])
    result['result'] = 'ok'
    return result


if __name__ == '__main__':
    server_url = 'http://localhost:11233/'
    server_pause = 1
    print '### processing started'
    while(True):
        try:
            task = get_task(server_url)
            check_action(task)

            result = process_task(task)
            task = receive_task(server_url, result)
            check_action(task)
        except urllib2.URLError:
            print '### server unavailable sleeping'
            time.sleep(server_pause)
        except StopProcessing:
            break
        except NextTask:
            pass

    print '### processing finished'