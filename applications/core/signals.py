from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Interviews

def send_interview_acceptance_email(instance):
    subject = "Поздравляем! Вас приняли на собеседование."
    message_template = "interview_acceptance_notification.html"

    for user_profile in instance.user.all():
        message = render_to_string(
            message_template,
            {"user": user_profile, "vacancy_position": instance.vacancy.position},
        )
        recipient_email = user_profile.user.email
        email = EmailMessage(subject, message, to=[recipient_email])
        email.content_subtype = "html"  # Установить тип содержимого как HTML
        email.send()

@receiver(post_save, sender=Interviews)
def handle_interview_acceptance(sender, instance, created, **kwargs):
    if not created and instance.is_accepted:
        send_interview_acceptance_email(instance)