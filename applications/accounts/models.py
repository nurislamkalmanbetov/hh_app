from datetime import date, timedelta
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
from applications.accounts.managers import *




class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        (('is_employer'), _('Работодатель')),
        (('is_employee'), _('Сотрудник')),
        (('is_student'), _('Соискатель')),
    )

    email = models.EmailField(_('Email адрес'), unique=True, db_index=True)
    phone = models.CharField(_('Номер телефона'), max_length=50, blank=True, db_index=True)
    role = models.CharField(_('Роль'), max_length=50, choices=ROLE_CHOICES)
    is_staff = models.BooleanField(_('Сотрудник'), default=False)
    is_superuser = models.BooleanField(_('Суперпользователь'), default=False)
    is_active = models.BooleanField(_('Активен'), default=False)
    is_delete = models.BooleanField(_('Удален'), default=False)
    is_verified_email = models.BooleanField(_('Почта подтверждена'), default=False)
    verification_code = models.CharField(_('Код подтверждения'), max_length=6, blank=True, null=True)
    verification_code_created_at = models.DateTimeField(_('Дата создания кода подтверждения'), blank=True, null=True)
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

    GENDER_CHOICES_RU = (
        ("Мужской", _("Мужской")),
        ("Женский", _("Женский")),
    )

    GENDER_CHOICES_EN = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    GENDER_CHOICES_DE = (
        ("Männlich", "Männlich"),
        ("Weiblich", "Weiblich"),
    )

    KNOWLEGE_OF_LANGUAGES_CHOICES = (
        ('Russian', _('Русский')),
        ('Kyrgyz', _('Кыргызский')),
        ('English', _('Английский')),
        ('German', _('Немецкий')),
    )

    LANGUAGE_LEVEL_CHOICES = (
        ('1', 'Понимаю и разговариваю без проблем'),
        ('2', 'Если что-то не понимаю, то переспрашиваю'),
        ('3', 'Понимаю многое, но плохо говорю'),
        ('4', 'Понимаю немного, когда говорят очень медленно, но плохо говорю'),
        ('5', 'Не разговариваю совсем'),
    )

    LEVEL_CHOICES = (
        ('a1', 'A1'),
        ('a2', 'A2'),
        ('b1', 'B1'),
        ('b2', 'B2'),
        ('c1', 'C1'),
    )

    user = models.OneToOneField(User, verbose_name=_('Пользователь'), related_name='profile', on_delete=models.CASCADE)
    profile_photo = models.ImageField(_('Фото профиля'), upload_to='document/profile_photo', blank=True, null=True, validators=[validate_image_file_extension])

    first_name = models.CharField(_('Имя на латинице'), max_length=255, default='', blank=True)
    first_name_ru = models.CharField(_('Имя на кириллице'), max_length=255, default='', blank=True)
    first_name_de = models.CharField(_('Имя на немецком'), max_length=255, default='', blank=True)

    last_name = models.CharField(_('Фамилия на латинице'), max_length=255, default='', blank=True)
    last_name_ru = models.CharField(_('Фамилия на кирилице'), max_length=255, default='', blank=True)
    last_name_de = models.CharField(_('Фамилия на немецком'), max_length=255, default='', blank=True)

    middle_name = models.CharField(_('Отчество на латинице'), max_length=50, default='', blank=True)
    middle_name_ru = models.CharField(_('Отчество на кирилице'), max_length=50, default='', blank=True)
    middle_name_de = models.CharField(_('Отчество на немецком'), max_length=50, default='', blank=True)
    
    gender_ru = models.CharField(_('Пол на кириллице'), max_length=50, choices=GENDER_CHOICES_RU, blank=True)
    gender_en = models.CharField(_('Пол на латинице'), max_length=50, choices=GENDER_CHOICES_EN, blank=True)
    gender_de = models.CharField(_('Пол на немецком'), max_length=50, choices=GENDER_CHOICES_DE, blank=True)
    
    nationality_ru = models.CharField(_('Гражданство на кирилице'), max_length=50, blank=True)
    nationality_en = models.CharField(_('Гражданство на латинице'), max_length=50,  blank=True)
    nationality_de = models.CharField(_('Гражданство на немецком'), max_length=50, blank=True)

    birth_country_ru = models.CharField(_('Страна рождения на кириллице'), max_length=50, default='', blank=True)
    birth_country_en = models.CharField(_('Страна рождения на латинице'), max_length=50, default='', blank=True)
    birth_country_de = models.CharField(_('Страна рождения на немецком'), max_length=50, default='', blank=True) 

    birth_region_ru = models.CharField(_('Область рождения на кириллице'), max_length=50, default='', blank=True)
    birth_region_en = models.CharField(_('Область рождения на латинице'), max_length=50, default='', blank=True)
    birth_region_de = models.CharField(_('Область рождения на немецком'), max_length=50, default='', blank=True)   

    date_of_birth = models.DateField(_('Дата рождения'), blank=True, null=True)
    phone = models.CharField(_('Номер телефона'), max_length=50, blank=True, null=True, db_index=True)
    whatsapp_phone_number = models.CharField(_('Номер Whatsapp'), max_length=50, blank=True)

    german = models.CharField(_('Знание немецкого языка'),  max_length=30, choices=LANGUAGE_LEVEL_CHOICES, default='', blank=True)
    german_level = models.CharField(_('Уровень знания немецкого'), choices=LEVEL_CHOICES, max_length=40, default='', blank=True)
    english = models.CharField(_('Знание английского языка'),  max_length=30, choices=LANGUAGE_LEVEL_CHOICES, default='', blank=True)
    english_level = models.CharField(_('Уровень знания английского'), choices=LEVEL_CHOICES, max_length=40, default='', blank=True)
    turkish = models.CharField(_('Знание турецкого языка'),  max_length=30, choices=LANGUAGE_LEVEL_CHOICES, default='', blank=True)
    turkish_level = models.CharField(_('Уровень знания турецкого'), choices=LEVEL_CHOICES, max_length=40, default='', blank=True)
    russian = models.CharField(_('Знание русского языка'),  max_length=30, choices=LANGUAGE_LEVEL_CHOICES, default='', blank=True)
    russian_level = models.CharField(_('Уровень знания русского'), choices=LEVEL_CHOICES, max_length=40, default='', blank=True)
    chinese = models.CharField(_('Знание китайского языка'),  max_length=30, choices=LANGUAGE_LEVEL_CHOICES, default='', blank=True)
    chinese_level = models.CharField(_('Уровень знания китайского'), choices=LEVEL_CHOICES, max_length=40, default='', blank=True)


    def __str__(self):
        return self.user.email
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'gender_en','german','russian' ])

        ]

        verbose_name = _('Профиль соискателя')
        verbose_name_plural = _('Профили соискателей')



class University(models.Model):

    COURSE_YEAR = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('Other', _('Другое'))
    )

    TYPE_STUDY_RU = (
        ('Бакалавриат', _('Бакалавриат')),
        ('Магистратура', _('Магистратура')),
    )

    TYPE_STUDY_EN_DE = (
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'),
    )

    user = models.ForeignKey(Profile, verbose_name=_('Соискатель'), related_name='universities', on_delete=models.CASCADE)
    name_ru = models.CharField(_('Название университета на кириллице'), max_length=255, blank=True)
    name_en = models.CharField(_('Название университета на латинице'), max_length=255, blank=True)
    name_de = models.CharField(_('Название университета на немецком'), max_length=255, blank=True)

    degree_type_ru = models.CharField(_('Тип обучения на кириллице'), max_length=255, choices=TYPE_STUDY_RU, blank=True)
    degree_type_en = models.CharField(_('Тип обучения на латинице'), max_length=255, choices=TYPE_STUDY_EN_DE, blank=True)
    degree_type_de = models.CharField(_('Тип обучения на немецком'), max_length=255, choices=TYPE_STUDY_EN_DE, blank=True)

    faculty_ru = models.CharField(_('Факультет на кириллице'), max_length=255, blank=True)
    faculty_en = models.CharField(_('Факультет на латинице'), max_length=255, blank=True)
    faculty_de = models.CharField(_('Факультет на немецком'), max_length=255, blank=True)

    address_ru = models.CharField(_('Адрес на кириллице'), max_length=255, blank=True)
    address_en = models.CharField(_('Адрес на латинице'), max_length=255, blank=True)
    address_de = models.CharField(_('Адрес на немецком'), max_length=255, blank=True)

    phone_number_university_ru = models.CharField(_('Номер телефона университета'), max_length=50, blank=True)

    email_university = models.EmailField(_('Email университета'), blank=True)
    website_university = models.URLField(_('Сайт университета'), blank=True)

    start_date = models.DateField(_('Год поступления в университет'), blank=True, null=True)
    end_date = models.DateField(_('Год окончания университета'), blank=True, null=True)
    total_years = models.IntegerField(_('Общее количество лет'), blank=True, null=True)

    kurs_year = models.CharField(_('Курс'), max_length=5, choices=COURSE_YEAR, blank=True)

    start_holiday = models.DateField(_('Начало каникул'), blank=True, null=True)
    end_holiday = models.DateField(_('Конец каникул'), blank=True, null=True)


    def __str__(self):
        return self.user.user.email
    
    class Meta:
        indexes = [
            models.Index(fields=['user'])

        ]
        verbose_name = _('Университет')
        verbose_name_plural = _('Университеты')


class PassportAndTerm(models.Model):
    user = models.ForeignKey(Profile, verbose_name=_('Соискатель'), related_name='passport_data', on_delete=models.CASCADE)
    number_id_passport = models.CharField(_('Номер ID паспорта'), max_length=50, blank=True)
    inn = models.CharField(_('ИНН'), max_length=50, blank=True)
    passport_number = models.CharField(_('Номер загран паспорта'), max_length=50, blank=True)
    passport_date_of_issue = models.DateField(_('Дата выдачи паспорта'), blank=True, null=True)
    passport_end_time = models.DateField(_('Дата окончания загранпаспорта'), blank=True, null=True)
    pnr_code = models.CharField(_('PNR код'), max_length=50, blank=True)
    pdf_file = models.FileField(_('PDF файл'), upload_to='document/PDF file', blank=True, null=True)
    term_date_time = models.DateTimeField(_('Дата и время термина'), blank=True, null=True)

    def __str__(self):
        return self.user.user.email

    class Meta:
        indexes = [
            models.Index(fields=['user'])

        ]
        verbose_name = _('Паспортные данные и термин')
        verbose_name_plural = _('Паспортные данные и термины')






class Payment(models.Model):
    FULLY_PAID_CHOICES = [
        ('ДА', _('ДА')),
        ('НЕТ', _('НЕТ')),
    ]
    user = models.ForeignKey(Profile, verbose_name=_('Соискатель'), related_name='payments', on_delete=models.CASCADE)
    total_amount = models.IntegerField(_('Общая сумма'), blank=True, null=True)
    total_amount_in_words = models.CharField(_('Общая сумма прописью'), max_length=255, blank=True)
    initial_fee = models.IntegerField(_('Первоначальный взнос'), blank=True, null=True)
    initial_fee_in_words = models.CharField(_('Первоначальный взнос прописью'), max_length=255, blank=True)
    average_fee = models.IntegerField(_('Средний взнос'), blank=True, null=True)
    average_fee_in_words = models.CharField(_('Средний взнос прописью'), max_length=255, blank=True)
    final_fee = models.IntegerField(_('Окончательный взнос'), blank=True, null=True)
    final_fee_in_words = models.CharField(_('Окончательный взнос прописью'), max_length=255, blank=True)
    debt = models.IntegerField(_('Долг'), blank=True, null=True)
    debt_in_words = models.CharField(_('Долг прописью'), max_length=255, blank=True)
    payment_date = models.DateTimeField(_('Дата оплаты'), blank=True, null=True)
    payment_accepted_by = models.ForeignKey(User, verbose_name=_('Оплату принял'), related_name='payments_accepted', on_delete=models.CASCADE,blank=True, null=True)
    fully_paid = models.CharField(_('Полностью оплатил'), max_length=3, choices=FULLY_PAID_CHOICES, blank=True, null=True)
    payment_accepted_date = models.DateTimeField(_('Дата принятия оплаты'), blank=True, null=True)
    payment_accepted = models.BooleanField(_('Оплата принята'), default=False)

    def __str__(self):
        return self.user.user.email

    class Meta:
        verbose_name = _('Оплата')
        verbose_name_plural = _('Оплаты')

        
class Deal(models.Model):
    user = models.ForeignKey(Profile, verbose_name=_('Соискатель'), related_name='deals', on_delete=models.CASCADE)
    phone_number = models.CharField(_('Номер телефона'), max_length=50, blank=True)
    participant = models.CharField(_('Участник'), max_length=50, blank=True)
    flight_date = models.DateField(_('Дата полета в Германию'), blank=True, null=True)
    steuer_id = models.CharField(_('Steuer ID - Налоговый номер'), max_length=50, blank=True)
    name = models.CharField(_('Имя'), max_length=50, blank=True)
    stage = models.CharField(_('Стадия сделки'), max_length=50, blank=True)
    program = models.CharField(_('Программа'), max_length=50, blank=True)
    contract_date = models.DateField(_('Дата заключения договора'), blank=True, null=True)
    inn = models.CharField(_('ИНН'), max_length=50, blank=True)
    comment = models.CharField(_('Комментарий'), max_length=50, blank=True)
    hijab = models.CharField(_('Носит Хиджаб'), max_length=50, blank=True)

    def __str__(self):
        return self.user.user.email

    class Meta:
        verbose_name = _('Сделка')
        verbose_name_plural = _('Сделки')


class WorkExperience(models.Model):

    TYPE_OF_COMPANY_CHOICES = (
        ('Hotel', _('Отель')),
        ('Restaurant', _('Ресторан')),
        ('Cafe', _('Кафе')),
        ('Factory', _('Фабрика')),
        ('Salon', _('Салон')),
        ('Sales', _('Продажи')),
        ('Other', _('Другое')),
    )

    JOB_TITLE_CHOICES = (
        ('Manager', _('Менеджер')),
        ('Waiter', _('Официант')),
        ('Cook', _('Повар')),
        ('Seller', _('Продавец')),
        ('Driver', _('Водитель')),
        ('Cashier', _('Кассир')),
        ('Builder', _('Строитель')),
        ('Butcher', _('Мясник')),
        ('Backer', _('Пекарь')),
        ('Other', _('Другое')),
    )

    user = models.ForeignKey(Profile, verbose_name=_('Профиль'), related_name='work_experiences', on_delete=models.CASCADE)
    company = models.CharField(_('Название компания'), max_length=255, blank=True)
    type_company = models.CharField(_('Тип компании'), max_length=50, choices=TYPE_OF_COMPANY_CHOICES, blank=True)
    position = models.CharField(_('Должность'), max_length=50, choices=JOB_TITLE_CHOICES, blank=True)
    start_date = models.DateField(_('Дата начала работы'), null=True, blank=True)
    end_date = models.DateField(_('Дата окончания работы'), null=True, blank=True) 
    description_de = models.TextField(_('Описание (на немецком)'), blank=True)
    description_ru = models.TextField(_('Описание (на кириллице)'), blank=True)
    description_en = models.TextField(_('Описание (на латинице)'), blank=True)
    achievements_de = models.TextField(_('Достижения и успехи (на немецком)'), blank=True)
    achievements_ru = models.TextField(_('Достижения и успехи (на кириллице)'), blank=True)
    achievements_en = models.TextField(_('Достижения и успехи (на латинице)'), blank=True)
    location_city_de = models.CharField(_('Город работы (на немецком)'), max_length=255, blank=True)
    location_city_ru = models.CharField(_('Город работы (на кириллице)'), max_length=255, blank=True)
    location_city_en = models.CharField(_('Город работы (на латинице)'), max_length=255, blank=True)
    location_country_de = models.CharField(_('Страна работы (на немецком)'), max_length=255, blank=True)
    location_country_ru = models.CharField(_('Страна работы (на кириллице)'), max_length=255, blank=True)
    location_country_en = models.CharField(_('Страна работы (на латинице)'), max_length=255, blank=True)
    salary = models.CharField(_('Заработная плата'), max_length=255, null=True, blank=True)    

    class Meta:
        verbose_name = _('Опыт работы')
        verbose_name_plural = _('Опыт работы')

    def __str__(self):
        return f'{self.company} - {self.position}'



