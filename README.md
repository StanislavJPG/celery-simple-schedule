celery-simple-schedule
=====
[![PyPI Downloads](https://static.pepy.tech/badge/celery-simple-schedule)](https://pepy.tech/projects/celery-simple-schedule)

A lightweight Python utility that simplifies defining Celery Beat schedules using a clean, declarative function-based API.

Just return a list of (task_path, schedule, optional_args) tuples — and get a fully compatible CELERY_BEAT_SCHEDULE dictionary.

*Installation*
---
```bash
pip install celery-simple-schedule
```

*Usage*
----
1. Define your task schedule in a separate module, e.g. celery_tasks.py::
```python
from celery_simple_schedule import simplify_schedules
from datetime import timedelta
from celery.schedules import crontab

@simplify_schedules
def provide_tasks():
    """
    Pattern: (task_dir, schedule, args(optionally))
    """
    
    return (
        ('server.apps.math_news.tasks.create_news_task', timedelta(days=1)),
        ('server.apps.notifications.tasks.clear_expired_deleted_notifications', timedelta(days=3)),
        ('server.apps.todo_list.tasks.create_default_task', timedelta(days=5), (5, '1', True)),
    )
```

2. Wire it into your Celery app (celery.py):
```python
from celery import Celery
from server.apps.celery_tasks import provide_tasks

app = Celery('my_project', broker=broker)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = provide_tasks()  # 🧠 This is the magic
```

*And that's it! You now have a clean and maintainable way to manage your periodic task schedule — with zero boilerplate and maximum clarity.*
