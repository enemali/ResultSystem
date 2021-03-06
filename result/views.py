from email.mime import image
from multiprocessing import context
from pyexpat import model
from re import template
from types import new_class
from django.forms import Form
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect 
from django.core.files.storage import FileSystemStorage
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.forms import CheckboxSelectMultiple, CheckboxInput, DateInput
from funky_sheets.formsets import HotView
from django.forms import modelformset_factory , formset_factory,inlineformset_factory

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
    
    def get(self, request,pk, *args, **kwargs):
        return render(request, 'result/classDetails.html',{'all_class': self.get_object()})
                        
    def post(self, request,pk, *args, **kwargs):
            classSubject = allsubject()
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

class subjectDetails(CreateView):
    model = assessment
    template_name = 'result/subjectDetails.html'
    
    def get(self, request,pk, *args, **kwargs):
        singleSubject = allsubject.objects.get(id=pk)
        assessment_query = assessment.objects.filter(subjectName=singleSubject.id)
        # students_in_assessment = students.objects.filter(id__in=assessment_query.values('student_id'))
        # student_query not in assessment_query
        students_query = students.objects.filter(className=singleSubject.className.id).exclude(id__in=assessment_query.values('student_id'))
        Form = SubjectstudentForm()
        Form.fields['subjectName'].choices = [(singleSubject.id, singleSubject.subjectName)]
        Form.fields['className'].choices = [(singleSubject.className.id, singleSubject.className.className)]
        Form.fields['student'].choices = [(student.id, student.fullname) for student in students_query]
        # assessmentForm = AssessmentForm(queryset=assessment_query)
        
        return render(request, 'result/subjectDetails.html',{'subject': singleSubject,
                                                            'Form': Form,
                                                            # 'assessmentForm': assessmentForm,
                                                            'assessment': assessment_query,
                                                             })
    
    def post(self, request,pk, *args, **kwargs):
        Form = SubjectstudentForm(request.POST)
        assessmentForm = AssessmentForm(request.POST)
        if Form.is_valid():
            Form.save()
            return redirect('result:subjectDetails', pk=pk)
        if assessmentForm.is_valid():
            instance = assessmentForm.save(commit=False)
            for assessmentForm in instance:
                assessmentForm.save()
            # assessmentForm.save()
            return redirect('result:subjectDetails', pk=pk)
        else:
            return redirect('result:subjectDetails', pk=pk)
        

class assessmentEntry(UpdateView):
    model = assessment
    fields = '__all__'
    Form_class = AssessmentForm
    template_name = 'result/assessmentScore.html'
    success_url = reverse_lazy('result:index')
    
            
            

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
