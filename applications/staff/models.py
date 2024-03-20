from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from applications.core.models import EmployerCompany, Branch

User = get_user_model()

class Notification(models.Model):
    data = models.JSONField()
    read = models.BooleanField(default=False)
    type_notification = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.data} - {self.read}"
    
    class Meta:
        indexes = [
            models.Index(fields=['read',]),
        ]
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'



class Employee(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    first_name = models.CharField(_('Имя'), max_length=50, blank=True)
    last_name = models.CharField(_('Фамилия'), max_length=50, blank=True)
    middle_name = models.CharField(_('Отчество'), max_length=50, blank=True)
    email = models.EmailField(_('Контактный Email'), blank=True)
    department = models.CharField(_('Отдел'), max_length=255, blank=True)
    position = models.CharField(_('Должность'), max_length=255, blank=True)
    birthday = models.DateField(_('Дата рождения'), blank=True, null=True)
    mobile_phone = models.CharField(_('Мобильный телефон'), max_length=20, blank=True)
    internal_phone = models.CharField(_('Внутренний телефон'), max_length=20, blank=True)
    is_created = models.BooleanField(_('Запись создана'), default=True)
    is_updated = models.BooleanField(_('Запись обновлена'), default=False)
    is_deleted = models.BooleanField(_('Запись удалена'), default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')



class OrderStudents(models.Model):

    employer_sender = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE, verbose_name=_('Работодатель отправитель'), related_name='sent_orders')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Филиал'))
    language_german_level = models.CharField(_('Уровень знания немецкого языка'), max_length=50)
    language_english_level = models.CharField(_('Уровень знания английского языка'), max_length=50)
    number_of_students = models.PositiveIntegerField(_('Количество студентов'))
    recipient_employee = models.ForeignKey('staff.Employee', on_delete=models.CASCADE, verbose_name=_('Сотрудник-получатель'), related_name='received_orders')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))


    def __str__(self):
        return f"Order for {self.number_of_students} students at {self.branch.name}"

    class Meta:
        verbose_name = _('Заказ студентов')
        verbose_name_plural = _('Заказы студентов')