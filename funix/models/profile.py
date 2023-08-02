from django.db import models
from django.contrib.auth.models import User
from funix.models.course import Course

class FunixProfile(models.Model):
    user = models.OneToOneField(User,verbose_name="Funix Profile", related_name="funix", on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    
