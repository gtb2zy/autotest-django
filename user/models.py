from django.db import models
from django.utils import timezone


# Create your models here.
class LoginRecord(models.Model):
    login_num = models.IntegerField(default=0)
    login_time = models.DateField(default=timezone.now)
