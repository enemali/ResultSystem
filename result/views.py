from email.mime import image
from multiprocessing import context
from pydoc import classname
from pyexpat import model
from re import sub, template
from types import new_class
from django.forms import Form
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect 
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic import View
from django.forms import modelformset_factory , formset_factory,inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .decorators import unauthenticated_user
from django.contrib.auth.forms import AuthenticationForm
from .filters import studentFilter
from .models import User





# class index(TemplateView):
#     queryset = setting.objects.first()
#     template_name = 'result/index.html'
    
#     def get_context_data(self, **kwargs):
#         context = super(index, self).get_context_data(**kwargs)
#         context['img'] = Images.objects.all()
#         context['setting'] = setting.objects.first()
#         return context

def index(request):
    user = request.user
    img = Images.objects.all()
    settings = setting.objects.first()
    return render(request, 'result/index.html', {'img':img,
                                                    'setting':settings,
                                                    'user':user})
    
class RegisterTeachers(CreateView):
    form_class = UserCreateForm
    template_name = 'result/addTeachers.html'
    success_url = reverse_lazy('result:RegisterTeachers')

    def get_context_data(self, **kwargs):
        context = super(RegisterTeachers, self).get_context_data(**kwargs)
        context['teachers'] = User.objects.all()
        return context

class RegisterStudent(CreateView):
    form_class = StudentForm
    template_name = 'result/add.html'
    success_url = reverse_lazy('result:registerStudent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["studentForm"] = StudentForm()
        context["allStudents"] = students.objects.all()
        return context
    

def loginPage(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("result:index")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="result/login.html", context={"login_form":form})

class logoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('result:index')
 

class settings(LoginRequiredMixin, TemplateView):
    login_url = 'result:login'
    template_name = 'result/settings.html'
    queryset = all_class.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(settings, self).get_context_data(**kwargs)
        context['classForm'] = allClassForm()
        context['armForm'] = classArmForm()
        context['sectionForm'] = sectionForm()
        context['imageForm'] = ImageForm()
        context['settingForm'] = settingForm()
        context['allclass'] = all_class.objects.all()
        context['classArm'] = classArm.objects.all()
        context['sections'] = section.objects.all()
        context['img'] = Images.objects.all()
        context['setting'] = setting.objects.all()
        context['studentCount'] = students.objects.all().count()
        return context
     
    def post(self, request, *args, **kwargs):

        classForm = allClassForm(request.POST)
        armForm = classArmForm(request.POST)
        SectionForm = sectionForm(request.POST)
        imageForm = ImageForm(request.POST, request.FILES)
        AllsettingForm = settingForm(request.POST)

        if classForm.is_valid():
            classForm.save()
            return redirect('result:settings')
        if armForm.is_valid():
            armForm.save()
            return redirect('result:settings')
        if SectionForm.is_valid():
            SectionForm.save()
            return redirect('result:settings')
        if imageForm.is_valid():
            imageForm.save()
        if AllsettingForm.is_valid():
            AllsettingForm.save()
            return redirect('result:settings')

        return render(request, 'result/settings.html', {'classForm': classForm, 
                                                        'sectionForm': sectionForm, 
                                                        'imageForm': imageForm,
                                                        'settingForm': AllsettingForm,
                                                        'armForm': armForm})
                                                        
class deleteClass(DeleteView):
    model = all_class
    context_object_name = 'all_class'
    template_name = 'result/deleteClass.html'
    success_url = reverse_lazy('result:settings')

class classList(ListView):
    model = all_class
    context_object_name = 'all_class'
    template_name = 'result/classList.html'
    
class classDetails(DetailView):
    model = all_class
    context_object_name = 'all_class'

    def get(self, request,pk, *args, **kwargs):
        Form = subjectForm()
        Form.fields['className'].choices = [(self.kwargs['pk'], self.get_object().className)]
        return render(request, 'result/classDetails.html',
                        {'all_class': self.get_object(),'form': Form})
                        
    def post(self, request,pk, *args, **kwargs):
        form = subjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.class_name = self.get_object()
            subject.save()
            return redirect('result:classDetails', pk=pk)
        return render(request, 'result/classDetails.html',
                        {'all_class': self.get_object(),
                         'form': self.form_class()}
                         )

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
        Form.fields['student'].choices = [(student.id, student.last_name + ' ' + student.first_name + ' ' + student.middle_name) for student in students_query]
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

class deleteSubject(DeleteView):
    model = allsubject
    context_object_name = 'allsubject'
    template_name = 'result/deleteSubject.html'
    success_url = reverse_lazy('result:settings')
        
class assessmentEntry(UpdateView):
    model = assessment
    fields = '__all__'
    Form_class = AssessmentForm
    template_name = 'result/assessmentScore.html'
    success_url = reverse_lazy('result:index')
    
class studentDelete(DeleteView):
    model = students
    template_name = 'result/Delete.html'
    def get_success_url(self):
        return reverse_lazy('result:registerStudent')
        
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

class DeleteArm(DeleteView):
    model = classArm
    template_name = 'result/DeleteArm.html'
    success_url = reverse_lazy('result:settings')
  
class EditClass(UpdateView):
    model = all_class
    form_class = allClassForm
    success_url = reverse_lazy('result:settings')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        id = self.object.id
        form = allClassForm(instance=self.object)
        Button = 'Update Class'
        return render(request, 'result/Edit.html', {'form': form, 'id': id, 'Button': Button})

class EditStudent(UpdateView):
    model = students
    form_class = StudentForm
    success_url = reverse_lazy('result:registerStudent')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        id = self.object.id
        form = StudentForm(instance=self.object)
        Button = 'Update Student'
        return render(request, 'result/Edit.html', {'form': form, 'id': id, 'Button': Button})

class EditTeacher(UpdateView):
    model = User
    form_class = RegistrationForm
    form_class.base_fields.pop('password')
    success_url = reverse_lazy('result:settings')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        id = self.object.id
        form = RegistrationForm(instance=self.object)
        Button = 'Update Teacher'
        return render(request, 'result/Edit.html', {'form': form, 'id': id, 'Button': Button})

class deleteTeacher(DeleteView):
    model = User
    template_name = 'result/delete.html'
    def get_success_url(self):
        return reverse_lazy('result:RegisterTeachers')

class studentList(ListView):
    model = students
    context_object_name = 'students'
    template_name = 'result/studentList.html'

    
    def get(self, request, *args, **kwargs):
        # student = students.objects.filter(className=all_class.id)
        student = students.objects.all()

        studentFilters = studentFilter(request.GET, queryset=student)
        student = studentFilters.qs
        classname = student.first()
        if classname:
            arm = classname.classArm
            classname = classname.className
        else:
            classname = ''
            arm = ''

        

        return render(request, 'result/studentList.html', {'students': student, 
                                                            'studentFilters': studentFilters,
                                                            'classname': classname,
                                                            'classarm': arm,
                                                            })

