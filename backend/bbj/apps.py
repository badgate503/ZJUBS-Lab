from django.apps import AppConfig
class BbjConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bbj"
    
    def ready(self):
        from .tasks import print_task
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        from django_apscheduler.jobstores import DjangoJobStore
        from django_apscheduler.jobstores import DjangoJobExecution
        from django_apscheduler.models import DjangoJob

        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            print_task,
            trigger=CronTrigger(hour=18, minute=53),  # 每天午夜运行
            id="my_scheduled_job",  # 唯一ID
            max_instances=1,
            replace_existing=True,
        )
        scheduler.start()