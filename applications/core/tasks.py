
from celery import shared_task
from time import sleep

@shared_task
def print_upcoming_interview():
    sleep(15)
    print("у вас скоро собеседование")