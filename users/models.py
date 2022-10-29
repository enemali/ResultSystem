from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin'
        TEACHER = 'teacher'
        STUDENT = 'student'
    base_role = Role.TEACHER
    role = models.CharField(max_length=10, choices= Role.choices)

    def save (self , *args , **kwargs):
        if not self.id:
            self.role = self.base_role
        return super().save(*args, **kwargs)
    class Meta:
        db_table = 'auth_user'