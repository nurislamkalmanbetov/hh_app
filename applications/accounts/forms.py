from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.forms.widgets import ChoiceWidget
from django.template import loader
from django.utils.safestring import mark_safe


User = get_user_model()

