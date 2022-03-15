from multiprocessing import context
from pipes import Template
from types import new_class
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse ,JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect 
from .models import *
from .forms import *

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

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
    
    
# class studentCreate(CreateView):
#     model = students
#     template_name = 'result/studentCreate.html'
#     form_class = StudentForm
#     students = students.objects.all()
    
#     def post(self, request):
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('result:studentCreate')
#         else:
#             return render(request, 'result/studentCreate.html',{'students': students})
#     # retrieve data from student
    
def studentCreate(request):
        form = StudentForm()
        myclass = all_class.objects.all()
        return render(request, 'result/studentCreate.html',{'form': form})
    
class settings(TemplateView):
    form1 = SettingsForm()
    form2 = sectionForm()
    model = NamesOfClasses
    model2 = section
    def get(self, request):
        return render(request,'result/settings.html',{'classform': self.form1 , 
                                                      'sectionForm': self.form2,
                                                      'allclass': self.model.objects.all(),
                                                      'sections': self.model2.objects.all()
                                                      })
    def post(self, request):
        classform = SettingsForm(request.POST)
        sectionform = sectionForm(request.POST)
        if classform.is_valid():
            classform.save()
            return redirect('result:settings')
        elif sectionform.is_valid():
            sectionform.save()
            return redirect('result:settings')
        else:
            return render(request,'result/settings.html',{'classform': classform , 
                                                      'sectionForm': sectionform,
                                                      'allclass': self.model.objects.all(),
                                                      'sections': self.model2.objects.all()
                                                      })
        

    # template_name = 'result/settings.html'
    # form_class = SettingsForm
    
    # def post(self, request):
    #     form = SettingsForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('result:studentCreate')
    #     else:
    #         return render(request, 'result/settings.html',{'form': form})
    
   
    
    
    
    
        # form = StudentForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     currentStudent = students.objects.filter(pk=form.instance.pk)
        #     return render(request, 'result/studentCreate.html', {'form': form, 'AllStudent': students.objects.all()})
    

# @require_http_methods(['POST'])
# def studentList(request):
#     student = None
#     childname = request.POST.get('fullname','')
#     student = students.objects.create(fullname=childname)
#     return render(request, 'result/studentCreate.html', {'student': student})

# def studentList(request):
#     if request.method == 'POST': 
#         return render(request, 'result/studentList.html')
    
class studentList(ListView):
    def post(self, request):
        student = None
        childname = request.POST.get('fullname','')
        student = students.objects.create(fullname=childname)
        return render(request, 'result/studentList.html', {'student': student})
        
    