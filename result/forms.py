from dataclasses import field
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import students , NamesOfClasses , section


class StudentForm(forms.ModelForm):
    class Meta:
        model = students
        fields = ['fullname', 'className']
        
class SettingsForm(forms.ModelForm):
    class Meta:
        model = NamesOfClasses
        fields = ['className']
        
class sectionForm(forms.ModelForm):
    class Meta:
        model = section
        fields = ['sectionName']
        
    