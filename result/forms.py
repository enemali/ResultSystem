from cProfile import label
from dataclasses import field
from tkinter import Widget
from django import forms
from django.forms import modelformset_factory , formset_factory , inlineformset_factory
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms.widgets import DateInput
from .models import students , all_class , section , allsubject , Images , setting , assessment , classArm,classArmTeacher,subjectList,comment,parentsubject
from .widgets import DatePickerInput
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelChoiceField
from crispy_forms.helper import FormHelper, Layout
from django.core.validators import MinValueValidator, MaxValueValidator

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", 
                  "password1", 
                  "password2", 
                  "first_name", 
                  "last_name", 
                  "email", 
                  "is_staff",
                  'section',
                  )
        help_texts = { k:"" for k in fields }
        # cahnge labe for is_staff
        labels = { 'is_staff': 'Is Admin' }
        field_classes = {'username': UsernameField}

class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'section')
        help_texts = { k:"" for k in fields }
        field_classes = {'username': UsernameField}

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", 
                  "first_name", 
                  "last_name", 
                  "email", 
                  "is_staff",
                  'section',
                  )
        exclude = ('password',)
        help_texts = { k:"" for k in fields }
        # cahnge labe for is_staff
        labels = { 'is_staff': 'Is Admin' }
        field_classes = {'username': UsernameField}

class loginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        field_classes = {'username': UsernameField}
     
class StudentForm(forms.ModelForm):
    class Meta:
        model = students
        fields = "__all__"
        
        labels = {  'last_name': 'Surname Name', 
                     'first_name': 'First Name',  
                    'middle_name': 'Other Name'}
      
class allClassForm(forms.ModelForm):
    class Meta:
        model = all_class
        fields = ['section', 'className' ]

class classArmForm(forms.ModelForm):
    class Meta:
        model = classArm
        fields = ['armName']
        
class sectionForm(forms.ModelForm):
    class Meta:
        model = section
        fields = ['sectionName']
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image','caption','description']
        
class settingForm(forms.ModelForm):
    class Meta:
        model = setting
        fields = [
                    # 'current_Term', ----------
                    'setting_value',
                    # 'current_Session', -----------
                    # 'date_Term_Begin', 
                    # 'date_Term_End', 
                    # 'number_of_days_school_open', 
                    # 'next_term_begins'
                ]
        labels = {
            'setting_value': '',
        }
        widgets = {
            'announcement_date': DatePickerInput(),
            'next_term_begins': DatePickerInput(),
            'date_Term_Begin': DatePickerInput(),
            'date_Term_End': DatePickerInput(),
            # 'setting_value': forms.Select(choices=[(1,'1st Term'),(2,'2nd Term'),(3,'3rd Term')]),
            # 'current_Session': forms.Select(choices=[('2021/2022', '2021/2022'),
            #                                             ('2022/2023', '2022/2023'),
            #                                             ('2023/2024', '2023/2024'),
            #                                             ('2024/2025', '2024/2025'),
            #                                             ('2025/2026', '2025/2026'),
            #                                             ('2026/2027', '2026/2027'),
            #                                             ('2027/2028', '2027/2028'),
            #                                             ('2028/2029', '2028/2029'),
            #                                             ('2029/2030', '2029/2030')
            #                                             ])
        }

        
class SubjectstudentForm(forms.ModelForm):
    class Meta:
        model = assessment
        fields = ['className','student','subjectName']
        
class AssessmentForm(forms.ModelForm):
    class Meta:
        model = assessment
        fields = ['className','student','subjectName','firstCa','secondCa','exam']
        
        # disable  dropdown for student, subjectName and className
        widgets = { 'student': forms.HiddenInput(),
                    'subjectName': forms.HiddenInput(),
                    'className': forms.HiddenInput(),
                    }

entryformset = modelformset_factory(assessment , 
fields = ['className','student','firstCa','secondCa','exam','absentfirstCa','absentsecondCa','absentexam'],
 extra=0,
labels = {'absentfirstCa': '1st-CA Absent', 
            'absentsecondCa': '2nd-CA Absent', 
            'absentexam': 'Exam Absent',
            'exam': 'ExamScore',

            },
widgets = { 'student': forms.Select(attrs={'id': 'studentdrpdwn'}),
            'className': forms.Select(attrs={'id':'studentdrpdwn'}),
           }
)


class entryformsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(entryformsetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.layout = Layout(
            'className',
            'student',
            'firstCa',
            'secondCa',
            'exam',
            'absentfirstCa',
            'absentsecondCa',
            'absentexam',
        )
        
        self.template = 'bootstrap/table_inline_formset.html'

# class subjectForm(forms.ModelForm):
#     class Meta:
#         model = allsubject
#         fields = ['subjectName', 'className', 'subjectTeacher']
        
class subjectForm(forms.ModelForm):
    class Meta:
        model = allsubject
        # all fields except subjectTeacher
        fields = ['subjectTeacher', 
                'className',
                'subjectName',
                'parentSubject',
                'is_childSubject'
                    ]
        

class parentsubjectForm(forms.ModelForm):
    class Meta:
        model = parentsubject
        fields ='__all__' 

class ClassArmTeacherForm(forms.ModelForm):
    class Meta:
        model = classArmTeacher
        fields = ['className', 'classArm', 'classTeacher']

class subjectListForm(forms.ModelForm):
    class Meta:
        model = subjectList
        fields = ['subjectName', 'subjectSection']

class commentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = '__all__'
        widgets = {
            'firstCacomment': forms.Textarea(attrs={'rows': 3, 'cols': 40 , 'placeholder': 'Enter First CA Comment'}),
            'secondCacomment': forms.Textarea(attrs={'rows': 3, 'cols': 40 , 'placeholder': 'Enter Second CA Comment'}),
            'examcomment': forms.Textarea(attrs={'rows': 3, 'cols': 40 , 'placeholder': 'Enter Exam Comment'}),
            # date_Term_Begin is a select field with the value setting.objects.get(setting_type = 'Term_Begin').setting_value
           
           
            'date_Term_Begin': forms.DateInput(attrs={'type': 'date'}),
            'date_Term_End': forms.DateInput(attrs={'type': 'date'}),
            'number_of_days_school_open': forms.Select(choices=[(setting.objects.get(setting_type = 'Days_school_open').setting_value, setting.objects.get(setting_type = 'Days_school_open').setting_value)]),
            'next_term_begins': forms.DateInput(attrs={'type': 'date'}),
            'session': forms.Select(choices=[(setting.objects.get(setting_type = 'session').setting_value, setting.objects.get(setting_type = 'session').setting_value)]),
            'term': forms.Select(choices=[(setting.objects.get(setting_type = 'term').setting_value, setting.objects.get(setting_type = 'term').setting_value)]),
        }
    
commentformset = modelformset_factory(comment , fields= '__all__' , extra=0)
class commentformsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(commentformsetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.layout = Layout(
            'firstCacomment',
            'secondCacomment',
            'examcomment',
        )
        
        self.template = 'bootstrap/table_inline_formset.html'



