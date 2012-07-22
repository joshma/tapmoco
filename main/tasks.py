from celery import task
from models import UserProfile


@task()
def notify_status_change(user):
    urls = [d['url'] for d in UserProfile.objects.filter(url!='').values('url')]
    print urls
    return 'done'
