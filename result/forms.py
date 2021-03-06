from dataclasses import field
from django import forms
from django.forms import modelformset_factory , formset_factory
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms.widgets import DateInput
from .models import students , all_class , section , allsubject , Images , setting , assessment
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput

class subjectForm(forms.ModelForm):
    class Meta:
        model = allsubject
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


        