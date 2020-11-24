from celery import shared_task

from celery.decorators import periodic_task
from celery.schedules import crontab

@periodic_task(run_every=(crontab(minute='*/1')), name='sdfsdfsf')
def my_first_task():
    print('This is my first task!')

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
