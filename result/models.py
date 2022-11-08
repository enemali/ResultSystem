from secrets import choice
from django.db import models
# import AUTH_USER_MODEL from settings.py
from django.contrib.auth import get_user_model
from django.conf import settings
from multiselectfield import MultiSelectField

# from users.models import User
User = get_user_model()
# Create your models here.
section_choices = (
                    ('Nusery', 'Nusery'),
                    ('Primary', 'Primary'),
                    ('Secondary', 'Secondary'),
                   )
allclass_choices = (
                    ('Nursery1', 'Nursery1'),
                    ('Nursery2', 'Nursery2'),
                    ('Nursery3', 'Nursery3'),
                    ('Primary1', 'Primary1'),
                    ('Primary2', 'Primary2'),
                    ('Primary3', 'Primary3'),
                    ('Primary4', 'Primary4'),
                    ('Primary5', 'Primary5'),
                    ('Primary6', 'Primary6'),
                    ('JSS1', 'JSS1'),
                    ('JSS2', 'JSS2'),
                    ('JSS3', 'JSS3'),
                    ('SS1', 'SS1'),
                    ('SS2', 'SS2'),
                    ('SS3', 'SS3'),
                   )
term_choices = (
                    ('1st-Term', '1st-Term'),
                    ('2nd-Term', '2nd-Term'),
                    ('3rd-Term', '3rd-Term'),
                   )
gender_choise = ( ('Male', 'male') , ('Female', 'female'))

class setting(models.Model):
    announcement = models.CharField(max_length=100,null=True)
    announcement_date = models.DateField(auto_now_add=False,null=True)
    news = models.CharField(max_length=100,null=True)
 
class Images(models.Model):
    image = models.ImageField(null=True,blank=True)
    caption = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=100,null=True)
    
    class Meta:
        ordering = ['-id']

class section(models.Model):
    sectionName = models.CharField(max_length=100 , unique=True)
    def __str__(self):
        return self.sectionName
    
class all_class(models.Model):
    className = models.CharField(max_length=100 , unique=True)
    section = models.ForeignKey(section, on_delete=models.SET_NULL, null=True)
    complete = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.className
    
    class Meta:
        ordering = ['className']

class classArm(models.Model):
    armName = models.CharField(max_length=100 , unique=True)
    def __str__(self):
        return self.armName
    
    class Meta:
        ordering = ['armName']

class classArmTeacher(models.Model):
    className = models.ForeignKey(all_class, on_delete=models.SET_NULL, null=True)
    classArm = models.ForeignKey(classArm, on_delete=models.SET_NULL, null=True)
    classTeacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.className) + ' ' + str(self.classArm) 
    class Meta:
        ordering = ['className']

class allsubject(models.Model):
    subjectTeacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    className = models.ForeignKey(classArmTeacher, related_name="subjectclass", on_delete=models.SET_NULL, null=True)
    subjectName = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.subjectName
    
    class Meta:
        ordering = ['subjectName']
        
class students(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank = True)
    gender = models.CharField(max_length=100 , choices= gender_choise)
    className = models.ForeignKey(all_class, related_name="studentclass", on_delete=models.SET_NULL, null=True)
    classArm = models.ForeignKey(classArm, related_name="studentclassArm", on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ['last_name']

class assessment(models.Model):
    className = models.ForeignKey(all_class, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(students, on_delete=models.SET_NULL, null=True)
    subjectName = models.ForeignKey(allsubject, on_delete=models.SET_NULL, null=True)
    firstCa = models.IntegerField(default=0)
    secondCa = models.IntegerField(default=0)
    exam = models.IntegerField(default=0)
    section = models.CharField(max_length=100, choices=section_choices)
    term = models.CharField(max_length=100 , choices=term_choices)
    session = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.className)
    class Meta:
        ordering = ['className']

class subjectList(models.Model):
    subjectName = models.CharField(max_length=100,null=True)
    subjectSection = models.ForeignKey('section',on_delete=models.CASCADE,null=True)
