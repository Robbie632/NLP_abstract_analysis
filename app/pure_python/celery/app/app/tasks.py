from .celery import app

@app.task
def add(x, y):
    sleep(10)

    return x + y