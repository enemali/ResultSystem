from dataclasses import field
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import students , all_class , section , subject


class subjectForm(forms.ModelForm):
    class Meta:
        model = subject
        fields = ['subjectName', 'className']
        
        
class StudentForm(forms.ModelForm):
    class Meta:
        model = students
        fields = ['fullname', 'className']
        
class allClassForm(forms.ModelForm):
    class Meta:
        model = all_class
        fields = ['className','section']
        
class sectionForm(forms.ModelForm):
    class Meta:
        model = section
        fields = ['sectionName']
        
    