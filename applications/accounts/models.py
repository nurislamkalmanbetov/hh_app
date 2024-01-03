import datetime
import json
import uuid
from datetime import date, timedelta

from applications.accounts.managers import ( UserManager)
from applications.core.models import (EmployerCompany, Vacancy)
from django.contrib.admin.models import LogEntry
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils import FieldTracker
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey
from ckeditor.fields import RichTextField



class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        (('is_employer'), _('Работодатель')),
        (('is_employee'), _('Соискатель')),
    )

    email = models.EmailField(_('Email адрес'), unique=True, db_index=True)
    phone = models.CharField(_('Номер телефона'), max_length=50, blank=True, db_index=True)
    role = models.CharField(_('Роль'), max_length=50, choices=ROLE_CHOICES)
    is_staff = models.BooleanField(_('Сотрудник'), default=False)
    is_superuser = models.BooleanField(_('Суперпользователь'), default=False)
    is_active = models.BooleanField(_('Активен'), default=False)
    is_delete = models.BooleanField(_('Удален'), default=False)
    is_verified_email = models.BooleanField('Почта подтверждена', default=False)
    verification_code = models.CharField('Код подтверждения', max_length=6, blank=True, null=True)
    verification_code_created_at = models.DateTimeField('Дата создания кода подтверждения', blank=True, null=True)
    registered_at = models.DateTimeField(_('Дата регистрации'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.email:
            raise ValueError('User must have an email')
        # if self.pk is None:  # если это новый объект
        #     self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.is_superuser:
            self.is_delete = True
            self.save()
        else:
            self.delete()
            
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')


def get_due_date():
    return date.today() + timedelta(days=60)


def is_staff_or_superuser(user_id):
    user = User.objects.get(pk=user_id)
    if not user.is_staff and not user.is_superuser:
        raise ValidationError("Only staff or superuser can be assigned as 'Оплату принял'")

