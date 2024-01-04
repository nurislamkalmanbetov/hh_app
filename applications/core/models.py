from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils.translation import gettext, gettext_lazy as _


class EmployerCompany(models.Model):
    first_name = models.CharField(_('Имя'), max_length=50, )
    last_name = models.CharField(_('Фамилия'), max_length=50,)
    icon = models.ImageField(upload_to='company_icons/', blank=True, verbose_name=_('Изображение'))
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, blank=True, verbose_name=_('Работодатель'))
    name = models.CharField(verbose_name=_('Название'), max_length=255)
    iin = models.CharField(_('ИИН/БИН'), max_length=50)
    description = models.TextField(_('Описание'), blank=True, default='')
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Работодатель')
        verbose_name_plural = _('Работодатели')


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')

class Branch(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_('Город'))
    company = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE, verbose_name=_('Компания'))
    name = models.CharField(_('Название филлиала'), max_length=255)
    address = models.CharField(_('Текстовый адрес'), max_length=255, blank=True, default='')
    link_address = models.CharField(_('Ссылка на адрес'), max_length=255, blank=True, default='')    
    description = models.TextField(_('Описание как добраться'), blank=True, default='')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Филиал')
        verbose_name_plural = _('Филиалы')


class ReviewBranch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Филиал'))
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    review = models.TextField(_('Отзыв'), blank=True, default='')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата публикации'))

    def __str__(self):
        return self.review

    class Meta:
        verbose_name = _('Отзыв филиала')
        verbose_name_plural = _('Отзывы филиалов')



class RatingEmployerCompany(models.Model):
    RATING_CHOICES = (
        (1, _('1')),
        (2, _('2')),
        (3, _('3')),
        (4, _('4')),
        (5, _('5')),
    )
    company = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE, verbose_name=_('Компания'))
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    rating = models.PositiveIntegerField(_('Рейтинг'), choices=RATING_CHOICES, default=1)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата публикации'))

    def __str__(self):
        return self.rating

    class Meta:
        verbose_name = _('Рейтинг компании')
        verbose_name_plural = _('Рейтинги компаний')

class PositionEmployee(models.Model):
    employer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('Работодатель'))
    name = models.CharField(_('Название позиции'), max_length=255)

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = _('Позиция работника')
        verbose_name_plural = _('Позиция работников')

class DutyEmployee(models.Model):
    employer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('Работодатель'))
    name = models.CharField(_('Название обязанности'), max_length=255)
    description = models.TextField(_('Описание обязанности'), blank=True, default='')

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = _('Обязанность работника')
        verbose_name_plural = _('Обязанности работников')



class ClothingForm(models.Model):
    employer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('Работодатель'))
    name = models.CharField(_('Название формы одежды'), max_length=255)

 
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Форма одежды')
        verbose_name_plural = _('Формы одежды')



class Vacancy(models.Model):
    GENDER_CHOICES = (
        ('Мужской', _('Мужской')),
        ('Женский', _('Женский')),
        ('Неважно', _('Неважно')),
    
    )
    #чойсы согласен повысить зарплату если работник согласен да нет
    INCREASE_CHOICES = (
        ('Да', _('Да')),
        ('Нет', _('Нет')),
        )

    employer_company = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE, verbose_name=_('Работодатель'))
    name = models.CharField(_('Название вакансии'), max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name=_('Филиал'))
    position = models.ForeignKey(PositionEmployee, on_delete=models.PROTECT, verbose_name=_('Позиция'))
    duty = models.ForeignKey(DutyEmployee, on_delete=models.PROTECT, verbose_name=_('Обязанности'))
    experience = models.TextField(_('Опыт работы'),)
    clothingform = models.ForeignKey(ClothingForm, on_delete=models.PROTECT, verbose_name=_('Форма одежды'))
    employee_count = models.PositiveIntegerField(_('Количество работников'), default=1)
    gender = models.CharField(_('Пол'), max_length=50)
    time_start = models.TimeField(_('Время начала работы'))
    time_end = models.TimeField(_('Время окончания работы'))
    salary = models.PositiveIntegerField(_('Зарплата'))
    salary_increase = models.CharField(_('Повышение зарплаты'), max_length=5, choices=INCREASE_CHOICES)
    description = models.TextField(_('Коментарий'), blank=True, default='')
    views_vacancy = models.PositiveIntegerField(_('Количество просмотров'), default=0)
    
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Вакансия')
        verbose_name_plural = _('Вакансии')





