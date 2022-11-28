from cProfile import label
from dataclasses import field
from tkinter import Widget
from django import forms
from django.forms import modelformset_factory , formset_factory , inlineformset_factory
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms.widgets import DateInput
from .models import students , all_class , section , allsubject , Images , setting , assessment , classArm,classArmTeacher,subjectList
from .widgets import DatePickerInput
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelChoiceField
from crispy_forms.helper import FormHelper, Layout

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

class loginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        field_classes = {'username': UsernameField}
     
class StudentForm(forms.ModelForm):
    class Meta:
        model = students
        fields = [ 'last_name','first_name', 'middle_name', 'className', 'classArm']
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
        fields = ['announcement',
                    'announcement_date',
                    'news'
                    ]
        widgets = {
            'announcement_date' : DatePickerInput(),
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
fields = ['className','student','firstCa','secondCa','exam'],
widgets= {'firstCa': forms.TextInput(attrs={'class':'form-control'}),
          'secondCa': forms.TextInput(attrs={'class':'form-control'}),
            'exam': forms.TextInput(attrs={'class':'form-control'}),
            # 'student': forms.Select(attrs={'disabled':True}),
          })
 # disable  dropdown for student, subjectName and className
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
        )
        
        self.template = 'bootstrap/table_inline_formset.html'


class subjectForm(forms.ModelForm):
    class Meta:
        model = allsubject
        fields = ['subjectName', 'className', 'subjectTeacher']
        
class SubjectForm(forms.ModelForm):
    class Meta:
        model = allsubject
        fields = ['subjectName', 'className', 'subjectTeacher']
      
class ClassArmTeacherForm(forms.ModelForm):
    class Meta:
        model = classArmTeacher
        fields = ['className', 'classArm', 'classTeacher']

# class subjectForm(forms.ModelForm):
#     class Meta:
#         model = allsubject
#         fields = ['subjectName', 'className']

class subjectListForm(forms.ModelForm):
    class Meta:
        model = subjectList
        fields = ['subjectName', 'subjectSection']
