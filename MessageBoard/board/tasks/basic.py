from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


#
# def get_subscribers(category):
#     user_emails = []
#     for user in user.all():
#         user_emails.append(user.email)
#     return user_emails


def new_comment_mail(instance):
    template = 'mail/new_comment.html'
    email_subject = f'New comment for your post "{instance.commentPost.title}"!'
    user_email = [instance.commentPost.author.authorUser.email]

    html = render_to_string(
        template_name=template,
        context={
            'post': instance.commentPost,
            'comment': instance,
        }
    )
    msg: EmailMultiAlternatives = EmailMultiAlternatives(
        subject=email_subject,
        body='',
        from_email='info@messageboard.com',
        to=user_email,
    )

    msg.attach_alternative(html, 'text/html')
    msg.send()


def comment_accepted_mail(comment):
    template = 'mail/comment_accepted.html'
    email_subject = f'our comment for post "{comment.commentPost.title}" accepted!'
    user_email = [comment.commentUser.email]

    html = render_to_string(
        template_name=template,
        context={
            'post': comment.commentPost,
            'comment': comment,
        }
    )
    msg: EmailMultiAlternatives = EmailMultiAlternatives(
        subject=email_subject,
        body='',
        from_email='info@messageboard.com',
        to=user_email,
    )

    msg.attach_alternative(html, 'text/html')
    msg.send()
