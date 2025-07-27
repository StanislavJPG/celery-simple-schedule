import functools
from typing import Callable


def simplify_schedules(func: Callable[[], tuple]) -> Callable:
    """
    Wrapper that conveniently transform tuple of paths with crontabs and args to beat schedule API
    according to https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html#solar-schedules

    Example:
        @simplify_schedules
        def provide_tasks():
            return (
                ('server.apps.math_news.tasks.create_news_task', crontab(hour=7, minute=30)),
                ('server.apps.notifications.tasks.clear_expired_deleted_notifications', timedelta(days=3)),
                ('server.apps.todo_list.tasks.create_default_task', timedelta(days=5), (5, '1', True))
            )
    """

    @functools.wraps(func)
    def wrapper():
        args = func()

        def with_args(*t, args):
            return (
                t[0],
                (t[1], args),
            )

        args = [with_args(*arg, args=arg[-1]) if len(arg) == 3 else arg for arg in args]

        return {
            a.split('.')[-1]: {
                k: v
                for k, v in {
                    'task': a,
                    'schedule': b,
                    'args': b[1] if isinstance(b, tuple) else None,
                }.items()
                if v is not None
            }
            for a, b in args
        }

    return wrapper
