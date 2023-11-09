from .models import Vacancy, ReviewVacancy
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model


User = get_user_model()

@receiver(post_save, sender=Vacancy)
def send_vacancy_notification(sender, instance, created, **kwargs):
    if created:
        User = get_user_model() 
        subject = 'Новая вакансия доступна!'
        message = f'Новая вакансия: {instance.name}\nЗарплата: {instance.salary}\nГород: {instance.city}'
        from_email = settings.EMAIL_HOST_USER
        users = User.objects.filter(is_active=True, is_student=True)

        # Отправляем уведомление каждому активному студенту
        for user in users:
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

@receiver(post_save, sender=ReviewVacancy)
def send_email_notification(sender, instance, created, **kwargs):
    if created:
        return
    subject = 'Статус вашего отклика на вакансию обновлен'
    
    # Добавляем комментарий работодателя в сообщение, если он есть:
    if instance.employer_comment:
        comment = f"\n\nКомментарий от работодателя: {instance.employer_comment}"
    else:
        comment = ""

    message = f'Отклик на вакансию "{instance.vacancy.name}" обновлен до статуса "{instance.status}".' + comment
    from_email = 'your_email@example.com'  # Замените на ваш отправной email адрес
    recipient_list = [instance.applicant_profile.user.email]  # Email соискателя

    send_mail(subject, message, from_email, recipient_list)