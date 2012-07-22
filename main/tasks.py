from celery import task


@task()
def notify_status_change(user, url):
    print url
