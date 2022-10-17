from cProfile import label
from dataclasses import field
from tkinter import Widget
from django import forms
from django.forms import modelformset_factory , formset_factory
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms.widgets import DateInput
from .models import students , all_class , section , allsubject , Images , setting , assessment , classArm
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
          # remove help_text
        help_texts = { k:"" for k in fields }

        field_classes = {'username': UsernameField}
      


# class RegisterStudentForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     class Meta:
#         model = students
#         fields = ('username', 
#                 'first_name',
#                 'last_name',
#                   'password1', 
#                   'password2',
#                   )
#         # remove help text
#         help_texts = {
#             'username': None,
#             'password1': None,
#             'password2': None,
#         }
#         def save(self, commit=True):
#             user = super(RegisterStudentForm, self).save(commit=False)
#             user.email = self.cleaned_data['email']
#             if commit:
#                 user.save()
#             return user


#         def save(self, commit=True):
#             user = super(RegisterStudent, self).save(commit=False)
#             user.email = self.cleaned_data['email']
#             if commit:
#                 user.save()
#             return user

# class signUpForm(UserCreationForm):
#     class Meta:
#         model = get_user_model()
#         fields = ("username", "email", "password1", "password2")
#         field_classes = {'username': UsernameField}

class loginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        field_classes = {'username': UsernameField}


class subjectForm(forms.ModelForm):
    class Meta:
        model = allsubject
        fields = ['subjectName', 'className']
        
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
        fields = ['section', 'className']

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


        