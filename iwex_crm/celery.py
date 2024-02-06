# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем переменную окружения, указывающую Django на наш файл настроек
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iwex_crm.settings')

# Создаем экземпляр приложения Celery
app = Celery('iwex_crm')

# Загружаем конфигурацию из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим и регистрируем задачи из файлов tasks.py в приложениях Django
app.autodiscover_tasks()
