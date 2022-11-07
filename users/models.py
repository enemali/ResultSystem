from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin'
        TEACHER = 'teacher'
        STUDENT = 'student'
    base_role = Role.TEACHER
    role = models.CharField(max_length=10, choices= Role.choices , null=True, blank=True)
    section = models.ForeignKey('result.section', on_delete=models.SET_NULL, null=True , blank=True)
    
    def save (self , *args , **kwargs):
        if not self.id:
            self.role = self.base_role
        return super().save(*args, **kwargs)
    class Meta:
        db_table = 'auth_user'
    def __str__(self):
        return self.username 