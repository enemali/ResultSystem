from secrets import choice
from django.db import models
# import AUTH_USER_MODEL from settings.py
from django.contrib.auth import get_user_model
from django.conf import settings
from multiselectfield import MultiSelectField
from django.db.models import Count, Sum, Avg, Max, Min , F, Q , Subquery, OuterRef,FloatField , Window, ExpressionWrapper, Value, IntegerField
from django.core.validators import MinValueValidator, MaxValueValidator

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
                    ('1', '1st-Term'),
                    ('2', '2nd-Term'),
                    ('3', '3rd-Term'),
                   )
gender_choise = ( ('Male', 'male') , ('Female', 'female'))
comment_choise = ( ('A', 'A') , ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'))

class setting(models.Model):
    announcement = models.CharField(max_length=100,null=True)
    announcement_date = models.DateField(auto_now_add=False,null=True)
    news = models.CharField(max_length=100,null=True)
    current_Term = models.CharField(max_length=100,choices=term_choices,null=True)
    current_Session = models.CharField(max_length=100,null=True)
    date_Term_Begin = models.DateField(auto_now_add=False,null=True)
    date_Term_End = models.DateField(auto_now_add=False,null=True)
    number_of_days_school_open = models.IntegerField(null=True)
    next_term_begins = models.DateField(auto_now_add=False,null=True)
    setting_type = models.CharField(max_length=100,null=True)
    setting_value = models.CharField(max_length=100,null=True)
    is_current_setting = models.BooleanField(default=False)

    class Meta:
        constraints = [ 
                        models.UniqueConstraint(
                        fields=['is_current_setting'], 
                        condition=Q(is_current_setting=True), 
                        name='unique_is_current_setting'
                        ) 
                        ]
 
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
    
class subjectList(models.Model):
    subjectName = models.CharField(max_length=100,null=True)
    subjectSection = models.ForeignKey('section',on_delete=models.CASCADE,null=True)
    def __str__(self):
        return str(self.subjectName)

class all_class(models.Model):
    className = models.CharField(max_length=100 , unique=True)
    section = models.ForeignKey(section, on_delete=models.CASCADE, null=True)
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
    className = models.ForeignKey(all_class, on_delete=models.CASCADE, null=True)
    classArm = models.ForeignKey(classArm, related_name='classArm', on_delete=models.CASCADE, null=True)
    classTeacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.className) + ' ' + str(self.classArm) 
    class Meta:
        ordering = ['className']

class parentsubject(models.Model):
    parentSubjectName = models.CharField(max_length=100, null=True)
    def __str__(self):
        return str(self.parentSubjectName)

class allsubject(models.Model):
    subjectTeacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    className = models.ForeignKey(classArmTeacher, related_name="subjectclass", on_delete=models.CASCADE, null=True)
    subjectName = models.ForeignKey(subjectList, on_delete=models.CASCADE, null=True)
    is_childSubject = models.BooleanField(default=False)
    parentSubject = models.ForeignKey(parentsubject, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.subjectName)
    
    class Meta:
        ordering = ['className']
        
class students(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank = True)
    gender = models.CharField(max_length=100 , choices= gender_choise)
    className = models.ForeignKey(all_class, related_name="studentclass", on_delete=models.CASCADE, null=True)
    classArm = models.ForeignKey(classArm, related_name="studentclassArm", on_delete=models.CASCADE, null=True)
    admission_number = models.CharField(max_length=100, unique=True , null=True , blank=True,default="")
    house = models.CharField(max_length=100, blank = True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name
    
    class Meta:
        ordering = ['last_name']

class assessment(models.Model):
    className = models.ForeignKey(classArmTeacher, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(students, on_delete=models.CASCADE, null=True)
    subjectName = models.ForeignKey(allsubject, on_delete=models.CASCADE, null=True)
    firstCa = models.IntegerField(default=0 , validators=[MaxValueValidator(20) , MinValueValidator(0)])
    secondCa = models.IntegerField(default=0 , validators=[MaxValueValidator(20) , MinValueValidator(0)])
    exam = models.IntegerField(default=0 , validators=[MaxValueValidator(100) , MinValueValidator(0)])
    section = models.CharField(max_length=100, choices=section_choices)
    term = models.CharField(max_length=100 , choices=term_choices)
    session = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    absentfirstCa = models.BooleanField(default=False)
    absentsecondCa = models.BooleanField(default=False)
    absentexam = models.BooleanField(default=False)
    recordedBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # to_field = 'classTeacher'
    
    @property
    def caTotal(self):
        return self.firstCa + self.secondCa

    @property
    def examTotal(self):
        return self.firstCa + self.secondCa + self.exam

    # @property
    # def is_childSubject(self):
    #     return self.subjectName.is_childSubject

    # @property
    # def parentSubject(self):
    #     return self.subjectName.parentSubject

    # @property
    # def ranking(self):
    #     total  = self.firstCa + self.secondCa + self.exam
    #     count = assessment.objects.filter(
    #         className=self.className, 
    #         subjectName=self.subjectName, 
    #         section=self.section, 
    #         term=self.term, 
    #         session=self.session
    #     ).filter(examTotal__gt=total
    #     ).count()
    #     return count + 1


    def __str__(self):
        return str(self.className)+ ' ' + str(self.student) + ' ' + str(self.subjectName)
    class Meta:
        ordering = ['className']

class comment(models.Model):
    className = models.ForeignKey(classArmTeacher, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(students, on_delete=models.CASCADE, null=True)
    term = models.CharField(max_length=100 , choices=term_choices)
    session = models.CharField(max_length=1000,default='2022/2023')
    date = models.DateTimeField(auto_now_add=True)
    # firstCacomment = models.CharField(max_length=1000, blank=True, null=True)
    # secondCacomment = models.CharField(max_length=1000, blank=True, null=True)
    examcomment = models.CharField(max_length=1000, blank=True, null=True)
    # Aesthetic_Appreciation = models.CharField(max_length=100 , choices=comment_choise, blank=True)
    Attendance_in_Class =models.CharField(max_length=100 , choices=comment_choise, blank=True)
    Creativity = models.CharField(max_length=100 , choices=comment_choise, blank=True)
    Honesty = models.CharField(max_length=100 , choices=comment_choise, blank=True)
    Leadership_Role = models.CharField(max_length=100 , choices=comment_choise, blank=True)
    Neatness = models.CharField(max_length=100 , choices=comment_choise, blank=True)
    Obedience = models.CharField(max_length=100 , choices=comment_choise, blank=True)
    # Politeness = models.CharField(max_length=100 , choices=comment_choise, blank=True)
    Punctuality = models.CharField(max_length=100 , choices=comment_choise, blank=True)
    Self_Control = models.CharField(max_length=100 , choices=comment_choise, blank=True)
    Sense_of_Responsibility = models.CharField(max_length=100 , choices=comment_choise, blank=True)
    Sociability = models.CharField(max_length=100 , choices=comment_choise, blank=True)
    # Games = models.CharField(max_length=1000, choices=comment_choise, blank=True)
    Sports = models.CharField(max_length=1000, choices=comment_choise, blank=True)
    # Handling_of_Tools = models.CharField(max_length=1000, choices=comment_choise, blank=True)
    # Handwriting = models.CharField(max_length=1000, choices=comment_choise, blank=True)
    Fluency = models.CharField(max_length=1000, choices=comment_choise, blank=True)
    # Painting_and_Drawing =  models.CharField(max_length=1000, choices=comment_choise, blank=True)
    # Musical_Skills = models.CharField(max_length=1000, choices=comment_choise, blank=True)
    # Crafts = models.CharField(max_length=1000, choices=comment_choise, blank=True)
    Number_of_Times_Present = models.IntegerField(default=0)
    
    @property
    def daysAbsent(self):
        return setting.objects.first().number_of_days_school_open - self.Number_of_Times_Present
    
    
    
    def __str__(self):
        return str(self.className)+ ' ' + str(self.student) + ' ' + str(self.comment)
    class Meta:
        ordering = ['className']