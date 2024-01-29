#импортируем что необходимо для фильтров
import django_filters
from django.contrib.auth import get_user_model
from .models import Profile
from applications.core.models import Vacancy
from django.db.models import Q



class ProfileFilter(django_filters.FilterSet):
    gender = django_filters.ChoiceFilter(choices=Profile.GENDER_CHOICES_RU, field_name='gender_ru')
    german = django_filters.ChoiceFilter(choices=Profile.KNOWLEGE_OF_LANGUAGES_LEVEL_CHOICES, field_name='german')
    english = django_filters.ChoiceFilter(choices=Profile.KNOWLEGE_OF_LANGUAGES_LEVEL_CHOICES, field_name='english')
    

    class Meta:
        model = Profile
        fields = ['gender', 'german', 'english', ]
