from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

@shared_task
def send_custom_email_task(email, subject, template_name, context):
    html_message = render_to_string(template_name, context)
    send_mail(
        subject,
        None,
        'nurislam.iwex@gmail.com',
        [email],
        html_message=html_message,
        fail_silently=False,
    )
    print("Письмо отправлено")
    