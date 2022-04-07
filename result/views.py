from email.mime import image
from multiprocessing import context
from pyexpat import model
from re import template
from types import new_class
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect 
from django.core.files.storage import FileSystemStorage
from .models import *
from .forms import *

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

# Create your views here.
class index(TemplateView):
    queryset = setting.objects.first()
    template_name = 'result/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        context['img'] = Images.objects.all()
        context['setting'] = setting.objects.first()
        return context
    
class settings(ListView):
    template_name = 'result/settings.html'
    queryset = all_class.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(settings, self).get_context_data(**kwargs)
        context['form1'] = allClassForm()
        context['form2'] = sectionForm()
        context['imageForm'] = ImageForm()
        context['settingForm'] = settingForm()
        context['allclass'] = all_class.objects.all()
        context['sections'] = section.objects.all()
        context['img'] = Images.objects.all()
        context['setting'] = setting.objects.all()
        return context
     
    def post(self, request, *args, **kwargs):
        form1 = allClassForm(request.POST)
        form2 = sectionForm(request.POST)
        imageForm = ImageForm(request.POST, request.FILES)
        AllsettingForm = settingForm(request.POST)
        if form1.is_valid():
            form1.save()
            return redirect('result:settings')
        if form2.is_valid():
            form2.save()
            return redirect('result:settings')
        if imageForm.is_valid():
            imageForm.save()
        if AllsettingForm.is_valid():
            AllsettingForm.save()
            return redirect('result:settings')
        return render(request, 'result/settings.html', {'form1': form1, 
                                                        'form2': form2, 
                                                        'imageForm': imageForm,
                                                        'settingForm': AllsettingForm
                                                        })
       
class deleteClass(DeleteView):
    model = all_class
    context_object_name = 'all_class'
    template_name = 'result/deleteClass.html'
    success_url = reverse_lazy('result:settings')
    
    
            # return render(request, 'result/index.html',{'imageForm': imageForm, 'obj': obj})            
            # context = {}
            # uploaded_file = request.FILES['document']
            # fs = FileSystemStorage()
            # name = fs.save(uploaded_file.name, uploaded_file)
            # url = fs.url(name)
            # context['url'] = fs.url(name)
            
            
        
  

    
class classList(ListView):
    model = all_class
    context_object_name = 'all_class'
    template_name = 'result/classList.html'
    
class classDetails(DetailView):
    model = all_class
    context_object_name = 'all_class'
    subjectform = subjectForm

    def get(self, request,pk, *args, **kwargs):
        # subjectform = subjectForm(initial={'className': pk})
        return render(request, 'result/classDetails.html',{'all_class': self.get_object()})
                          
    def post(self, request,pk, *args, **kwargs):
            classSubject = subject()
            classStudent = students()
            if request.POST.get('subjectName'):
                classSubject.subjectName = request.POST.get('subjectName')
                classSubject.className = all_class.objects.get(id=pk)
                classSubject.save()
                return redirect('result:classDetails', pk=pk)
            elif request.POST.get('studentName'):
                classStudent.fullname = request.POST.get('studentName')
                classStudent.className = all_class.objects.get(id=pk)
                classStudent.save()
                student_id = students.objects.latest('id')
                return redirect('result:classDetails', pk=pk)
            else:
                return render(request, 'result/classDetails.html',{'all_class': self.get_object()})

class subjectDetails(DetailView):
    model = subject
    context_object_name = 'subject'
    template_name = 'result/subjectDetails.html'

class studentDelete(DeleteView):
    model = students
    template_name = 'result/studentDelete.html'
    def get_success_url(self):
        className = self.object.className
        return render('result:classDetails', kwargs={'pk': className.id})
    
    
    
        
class studentList(ListView):
    def post(self, request):
        student = None
        childname = request.POST.get('fullname','')
        student = students.objects.create(fullname=childname)
        return render(request, 'result/studentList.html', {'student': student})
    
def uploadimage(request):
    if request.method == 'POST' and request.FILES['document']:
        uploaded_file = request.FILES['document']
        print(uploaded_file.name)
    return render(request, 'result/uploadimage.html')
    