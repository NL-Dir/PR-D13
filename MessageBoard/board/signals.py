from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from .tasks.basic import new_comment_mail


@receiver(post_save, sender=Comment)
def new_comment_notification(sender, instance, **kwargs):
    new_comment_mail(instance)
