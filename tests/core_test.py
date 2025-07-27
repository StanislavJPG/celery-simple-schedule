import datetime
import unittest
from datetime import timedelta

from celery_simple_schedule import simplify_schedules


@simplify_schedules
def provide_tasks():
    return (
        ('server.apps.math_news.tasks.create_news_task', timedelta(days=1)),
        ('server.apps.notifications.tasks.clear_expired_deleted_notifications', timedelta(days=3)),
        ('server.apps.todo_list.tasks.create_default_task', timedelta(days=5), (5, '1', True)),
    )


_test_func = provide_tasks()


class TestSimpleSchedules(unittest.TestCase):
    def test_default_values(self):
        self.assertIsInstance(_test_func, dict)

    def test_values_compliance(self):
        self.assertEqual(
            _test_func,
            {
                'clear_expired_deleted_notifications': {
                    'schedule': datetime.timedelta(days=3),
                    'task': 'server.apps.notifications.tasks.clear_expired_deleted_notifications',
                },
                'create_default_task': {
                    'args': (5, '1', True),
                    'schedule': (datetime.timedelta(days=5), (5, '1', True)),
                    'task': 'server.apps.todo_list.tasks.create_default_task',
                },
                'create_news_task': {
                    'schedule': datetime.timedelta(days=1),
                    'task': 'server.apps.math_news.tasks.create_news_task',
                },
            },
        )
