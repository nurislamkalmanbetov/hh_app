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



import datetime
import json
import uuid
from datetime import date, timedelta
from applications.accounts.utils import user_directory_path
from applications.accounts.managers import *

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


from rest_framework_simplejwt.tokens import RefreshToken

from django.core.validators import MinValueValidator, MaxValueValidator




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


class Profile(models.Model):

    GENDER_CHOICES = (
        ("Мужской", "Men"),
        ("Женский", "Women"),
    )

    NATIONALITY_CHOICES = (
        ('Кыргызстан', _('Kyrgyzstan')),
        ('Россия', _('Russia')),
        ('Узбекистан', _('Uzbekistan')),
        ('Казахстан', _('Kazakhstan')),
        ('Таджикистан', _('Taikistan')),
        ('Другое', _('Another')),
    )

    KNOWLEGE_OF_LANGUAGES_CHOICES = (
        ('Русский', _('Russian')),
        ('Кыргызский', _('Kyrgyz')),
        ('Английский', _('English')),
        ('Немецкий', _('German')),
        ('Французский', _('French')),
        ('Турецкий', _('Turkish')),
        ('Китайский', _('Chinese')),
        ('Другое', _('Another')),
    )

    KNOWLEGE_OF_LANGUAGES_LEVEL_CHOICES = (
        ('A1', _('A1')),
        ('A2', _('A2')),
        ('B1', _('B1')),
        ('B2', _('B2')),
        ('C1', _('C1')),
        ('C2', _('C2')),
    )
    first_name = models.CharField(_('Имя'), max_length=50, blank=False)
    midlle_name = models.CharField(_('Отчество'), max_length=50, blank=True)
    last_name = models.CharField(_('Фамилия'), max_length=50, blank=False)
    user = models.OneToOneField(User, verbose_name=_('Пользователь'), related_name='profile', on_delete=models.CASCADE)
    
    profile_photo = models.ImageField(_('Фото профиля'), upload_to=user_directory_path, blank=True, null=True, validators=[validate_image_file_extension])
    gender = models.CharField(_('Пол'), max_length=10, choices=GENDER_CHOICES, blank=True)
    nationality = models.CharField(_('Национальность'), max_length=50, choices=NATIONALITY_CHOICES, blank=True)
    date_of_birth = models.DateField(_('Дата рождения'), blank=True, null=True)
    inn = models.CharField(_('ИНН'), max_length=50, blank=True)
    phone = models.CharField(_('Номер телефона'), max_length=50, blank=True, null=True, db_index=True)

    language = models.CharField(_('Язык'), max_length=50, choices=KNOWLEGE_OF_LANGUAGES_CHOICES, blank=True)
    language_level = models.CharField(_('Уровень языка'), max_length=50, choices=KNOWLEGE_OF_LANGUAGES_LEVEL_CHOICES, blank=True)
    whatsapp_phone_number = models.CharField(_('Номер Whatsapp'), max_length=50, blank=True)


    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('Профиль соискателя')
        verbose_name_plural = _('Профили соискателей')



class WorkSchedule(models.Model):

    TIME_CHOICES = (
        ('DAY', _('День (08:00-20:00)')),
        ('EVENING', _('Ночь (17:00-01:00)')),
        ('NIGHT', _('Вечер (20:00-08:00)')),
        ('ANY', _('Свой график')),
    )

    user = models.ForeignKey(Profile, verbose_name=_('Соискатель'), related_name='working_times', on_delete=models.CASCADE)
    
    monday = models.CharField(_('Понедельник'), max_length=50, choices=TIME_CHOICES, blank=True, default='DAY')
    tuesday = models.CharField(_('Вторник'), max_length=50, choices=TIME_CHOICES, blank=True, default='DAY')
    wednesday = models.CharField(_('Среда'), max_length=50, choices=TIME_CHOICES, blank=True, default='DAY')
    thursday = models.CharField(_('Четверг'), max_length=50, choices=TIME_CHOICES, blank=True, default='DAY')
    friday = models.CharField(_('Пятница'), max_length=50, choices=TIME_CHOICES, blank=True, default='DAY')
    saturday = models.CharField(_('Суббота'), max_length=50, choices=TIME_CHOICES, blank=True, default='DAY')
    sunday = models.CharField(_('Воскресенье'), max_length=50, choices=TIME_CHOICES, blank=True, default='DAY')
    custom = models.CharField(_('Свой график'), max_length=50, choices=TIME_CHOICES, blank=True)

    custom_start_time = models.TimeField(_('Начало работы (Свой график)'), blank=True, null=True, help_text=_('Введите время в формате HH:MM'))
    custom_end_time = models.TimeField(_('Окончание работы (Свой график)'), blank=True, null=True, help_text=_('Введите время в формате HH:MM'))


    def save(self, *args, **kwargs):
        if self.custom == 'ANY' and (self.custom_start_time is None or self.custom_end_time is None):
            raise ValueError('When custom schedule is selected, start and end times must be provided.')
        super().save(*args, **kwargs)
        
    
    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name = _('График работы')
        verbose_name_plural = _('Графики работ')


class Rating(models.Model):
    STAR_CHOICES = [
        (1, _('1 звезда')),
        (2, _('2 звезды')),
        (3, _('3 звезды')),
        (4, _('4 звезды')),
        (5, _('5 звезд')),
    ]

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ratings_received', verbose_name=_('Соискатель'))
    value_rating = models.IntegerField(_('Значение рейтинга'), choices=STAR_CHOICES, default=1)
    rating_date = models.DateTimeField(_('Дата рейтинга'), auto_now_add=True)
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given', verbose_name=_('Работодатель'))

    def __str__(self):
        return f"{self.employer.email} rated {self.user.email} - {self.get_value_rating_display()}"

    def get_star_display(self):
        return f"{self.value_rating} звезд"
    
    class Meta:
        verbose_name = _('Рейтинг')
        verbose_name_plural = _('Рейтинги')



class Review(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('Соискатель'))
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews', verbose_name=_('Работодатель'))
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name='reviews')  
    text = models.TextField(_('Текст отзыва'), blank=True)
    creation_date = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.rating.value_rating}"

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')


class WorkExperience(models.Model):

    TYPE_OF_COMPANY_CHOICES = (
        ('Отель', _('Hotel')),
        ('Ресторан', _('Restaurant')),
        ('Кафе', _('Cafe')),
        ('Фабрика', _('Factory')),
        ('Салон', _('Salon')),
        ('Продажи', _('Sales')),
        ('Другое', _('Other')),
    )

    JOB_TITLE_CHOICES = (
        ('Менеджер', _('Manager')),
        ('Официант', _('Waiter')),
        ('Повар', _('Cook')),
        ('Продавец', _('Seller')),
        ('Водитель', _('Driver')),
        ('Кассир', _('Cashier')),
        ('Строитель', _('Builder')),
        ('Мясник', _('Butcher')),
        ('Пекарь', _('Backer')),
        ('Другое', _('Other')),
    )

    

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='work_experiences', verbose_name=_('Соискатель'))
    type_company = models.CharField(_('Тип компании'), max_length=50, choices=TYPE_OF_COMPANY_CHOICES, blank=True)
    company = models.CharField(_('Компания'), max_length=255, blank=True)
    position = models.CharField(_('Должность'), max_length=50, choices=JOB_TITLE_CHOICES, blank=True)
    start_date = models.DateField(_('Дата начала'), blank=True, null=True)
    end_date = models.DateField(_('Дата окончания'), blank=True, null=True)
    responsibilities = models.TextField(_('Обязанности'), blank=True)
    country = models.CharField(_('Страна'), max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.company}"

    class Meta:
        verbose_name = _('Опыт работы')
        verbose_name_plural = _('Опыт работы')



def get_due_date():
    return date.today() + timedelta(days=60)


def is_staff_or_superuser(user_id):
    user = User.objects.get(pk=user_id)
    if not user.is_staff and not user.is_superuser:
        raise ValidationError("Only staff or superuser can be assigned as 'Оплату принял'")
    



class City(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name
    
    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')


def get_due_date():
    return date.today() + timedelta(days=60)


def is_staff_or_superuser(user_id):
    user = User.objects.get(pk=user_id)
    if not user.is_staff and not user.is_superuser:
        raise ValidationError("Only staff or superuser can be assigned as 'Оплату принял'")

