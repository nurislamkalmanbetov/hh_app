from django.db import models

class Notification(models.Model):
    data = models.JSONField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.data} - {self.read}"
    
    class Meta:
        indexes = [
            models.Index(fields=['read',]),
        ]
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

