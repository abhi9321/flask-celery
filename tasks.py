from celery import Celery
import time
BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6379/1'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)

@app.task
def reverse(string):
    time.sleep(2)
    return string[::-1]
