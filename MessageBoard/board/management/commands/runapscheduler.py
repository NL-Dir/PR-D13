import logging
from datetime import timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils import timezone

from board.models import Post

logger = logging.getLogger(__name__)


def get_subscribers():
    user_emails = []
    for user in User.objects.all():
        user_emails.append(user.email)
    return user_emails


def weekly_post_mail():

    template = 'mail/weekly_update.html'

    new_posts = []
    new_posts = Post.objects.filter(creationDate__gte=timezone.now()-timedelta(days=7))
    if new_posts:
        email_subject = f'Weekly updates for from MessageBoard!'
        user_emails = get_subscribers()

        html = render_to_string(
            template_name=template,
            context={
                'posts': new_posts,

            }
        )
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email='info@messageboard.com',
            to=user_emails,
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()
    else:
        print(f'No updates this week')


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            weekly_post_mail,
            # trigger=CronTrigger(second="*/10"),
            trigger=CronTrigger(day_of_week="mon", hour="09", minute="00"),
            # То же самое что и интервал, но задача тригера таким образом более понятна django
            id="weekly_post_mail",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_post_mail'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не
            # надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
