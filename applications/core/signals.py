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



# class EmployerCompany(models.Model):
#     icon = models.ImageField(upload_to='company_icons/', blank=True, verbose_name=_('Изображение'))
#     # image_back = models.ImageField(upload_to='company_image_back/', blank=True, null=True, verbose_name='изображение')
#     user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, blank=True, verbose_name=_('Работодатель'))
#     name = models.CharField(verbose_name=_('Название'), blank=True, max_length=255)
#     country = models.CharField(_('страна'), max_length=128, blank=True, default='')
#     description = RichTextField(_('Описание'), blank=True, default='')

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = _('Работодатель')
#         verbose_name_plural = _('Работодатели')


# class Vacancy(models.Model):

#     LANGUAGE_CHOICES = (
#         ('de', _('Немецкий')),
#         ('ru', _('Руский')),
#         ('en', _('Английский')),
#     )

#     PROFICIENCY_LEVELS = (
#         ('A1', _('A1')),
#         ('A2', _('A2')),
#         ('B1', _('B1')),
#         ('B2', _('B2')),
#         ('C1', _('C1')),
#         ('C2', _('C2')),
#     )

#     EXCHANGE = (
#         ('RUB', _('RUB')),
#         ('USD', _('USD')),
#         ('EUR', _('EUR')),
#         ('KGS', _('KGS')),
#         ('KZT', _('KZT')),
#     )

#     language = models.CharField(_('Язык'), choices=LANGUAGE_CHOICES, max_length=2, blank=True, default='')
#     proficiency = models.CharField(_('Уровень владения'), choices=PROFICIENCY_LEVELS, max_length=2, blank=True, default='')

#     ACCOMODATION_TYPE_CHOICES = (
#         ('yes', _('Предоставляется')),
#         ('no', _('Не предоставляется')),
#     )
#     picture = models.ImageField(upload_to='vacancy_pics/', blank=True)
#     user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('Работодатель'))
#     employer_company = models.ForeignKey(EmployerCompany, verbose_name=_('Компания работодателя'),
#                                          on_delete=models.CASCADE, related_name='vacancies')

#     required_positions = models.PositiveIntegerField(_('Требуемое количество мест'), default=1)
#     required_positions_reviews = models.PositiveIntegerField(_('Колличество одобренных вакансии'), default=0)
#     exchange = models.CharField(max_length=10, choices=EXCHANGE, default='', blank=True)
#     name = models.CharField(_('Название вакансии'), max_length=255)
#     salary = models.IntegerField(_('Зарплата'), )
#     duty = RichTextField(_('Обязанности работника'), blank=True, default='')
#     city = models.CharField(_('Город'), max_length=128, blank=True, default='')
#     accomodation_type = models.CharField(_('Жилье'), choices=ACCOMODATION_TYPE_CHOICES, max_length=50,
#                                          default='', blank=True)
#     accomodation_cost = models.CharField(_('Стоимость жилья'), max_length=128, blank=True, default='')
#     is_vacancy_confirmed = models.BooleanField(_('Прошел на вакансию'), default=False)
#     insurance = models.BooleanField(_('Страховка'), default=False)
#     transport = models.CharField(_('Транспорт'), max_length=128, blank=True, default='')
#     contact_info = models.CharField(_('Контактные данные'), max_length=100,blank=True, default='')
#     destination_point = RichTextField(_('Пункт назначения'), blank=True, default='')
#     employer_dementions = models.CharField(_('Требования работодателя'), max_length=128, blank=True, default='')
#     extra_info = models.CharField(_('Доп. информация'), max_length=255, blank=True, default='')
#     created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата публикации'))
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Категория'), db_index=True)
#     subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Подкатегория'), db_index=True)


#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = _('Вакансия')
#         verbose_name_plural = _('Вакансии')


