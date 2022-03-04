from multiprocessing import context
from pipes import Template
from django.shortcuts import render
from django.http import HttpResponse
from .models import *

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.
class classList(ListView):
    model = all_class
    context_object_name = 'all_class'
    template_name = 'result/classList.html'
    
class classDetails(DetailView):
    model = all_class
    context_object_name = 'all_class'
    template_name = 'result/classDetails.html'
    
    
class subjectDetails(DetailView):
    model = subject
    context_object_name = 'subject'
    template_name = 'result/subjectDetails.html'
    