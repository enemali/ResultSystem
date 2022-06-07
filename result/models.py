from django.db import models
from django.contrib.auth.models import User

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

class setting(models.Model):
    announcement = models.CharField(max_length=100,null=True)
    announcement_date = models.DateField(auto_now_add=False,null=True)
    news = models.CharField(max_length=100,null=True)
    
    
class NamesOfClasses(models.Model):
    className = models.CharField(max_length=100,null=True)
    
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    className = models.CharField(max_length=100 , unique=True)
    section = models.ForeignKey(section, on_delete=models.SET_NULL, null=True)
    complete = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.className
    
    class Meta:
        ordering = ['className']
              
class subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    className = models.ForeignKey(all_class, related_name="subjectclass", on_delete=models.SET_NULL, null=True)
    subjectName = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.subjectName
    
    class Meta:
        ordering = ['subjectName']
        
class students(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    className = models.ForeignKey(all_class, related_name = 'studentclass', on_delete=models.SET_NULL, null=True)
    fullname = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.fullname
    
    class Meta:
        ordering = ['fullname']

class assessment(models.Model):
    className = models.ForeignKey(all_class, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(students, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(subject, on_delete=models.SET_NULL, null=True)
    firstCa = models.IntegerField(default=0)
    secondCa = models.IntegerField(default=0)
    exam = models.IntegerField(default=0)
    section = models.CharField(max_length=100, choices=section_choices)
    term = models.CharField(max_length=100 , choices=term_choices)
    session = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.assessment
    
    class Meta:
        ordering = ['className']