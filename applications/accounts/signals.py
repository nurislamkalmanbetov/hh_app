import requests
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


