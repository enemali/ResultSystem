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
                                                        
class classList(ListView):
    model = classArmTeacher
    # context_object_name = 'all_class'
    template_name = 'result/classList.html'
    

    def get_context_data(self, **kwargs):
        context = super(classList, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['all_class'] = classArmTeacher.objects.all()
        else:
            context['teacherSubject'] = allsubject.objects.filter(subjectTeacher=self.request.user)
            context['all_class'] = classArmTeacher.objects.filter(id__in=context['teacherSubject'].values_list('className', flat=True))
        return context
    
class classDetails(DetailView):
    model = classArmTeacher
    context_object_name = 'all_class'
    template_name = 'result/classDetails.html'

    def get_context_data(self, **kwargs):
        context = super(classDetails, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        if self.request.user.is_staff:
            context['subjects'] = allsubject.objects.filter(className_id = self.kwargs['pk'])
        else:
            context['subjects'] = allsubject.objects.filter(subjectTeacher = self.request.user , className_id = self.kwargs['pk'])
        context['students'] = students.objects.filter(classArm = self.get_object().classArm ,className = self.get_object().className)
        return context

class subjectDetails(CreateView):
    model = assessment
    template_name = 'result/subjectDetails.html'
    success_url = reverse_lazy('result:subjectDetails')
    
    def get(self, request,pk, *args, **kwargs):
        singleSubject = allsubject.objects.get(id=pk)
        assessment_query = assessment.objects.filter(subjectName=singleSubject.id)
        # students_in_assessment = students.objects.filter(id__in=assessment_query.values('student_id'))
        # student_query not in assessment_query
        students_query = students.objects.filter(className=singleSubject.className.className,
                                                classArm=singleSubject.className.classArm
                                                ).exclude(id__in=assessment_query.values('student_id'))
        if students_query.count() > 0:
            assessmentBulk = []
            for student in students_query:
                assessmentBulk.append(assessment(student=student, subjectName=singleSubject,className = singleSubject.className))
            assessment.objects.bulk_create(assessmentBulk)

        Form = SubjectstudentForm()
        Form.fields['subjectName'].choices = [(singleSubject.id, singleSubject.subjectName)]
        Form.fields['className'].choices = [(singleSubject.className.id, singleSubject.className)]
        Form.fields['student'].choices = [(student.id, student.last_name + ' ' + student.first_name + ' ' + student.middle_name) for student in students_query]
        
        context = {'form': Form,'singleSubject': singleSubject ,'assessment': assessment_query}
        return render(request, 'result/subjectDetails.html', context)
    
    def post(self, request,pk, *args, **kwargs):
        Form = SubjectstudentForm(request.POST)
        # assessmentForm = AssessmentForm(request.POST)
        if Form.is_valid():
            Form.save()
            return redirect('result:subjectDetails', pk=pk)
        # if assessmentForm.is_valid():
        #     instance = assessmentForm.save(commit=False)
        #     for assessmentForm in instance:
        #         assessmentForm.save()

            # return redirect('result:subjectDetails', pk=pk)
        else:
            print(Form.errors)
            return redirect('result:subjectDetails', pk=pk)
     
class assessmentEntry(UpdateView):
    model = assessment
    context_object_name = 'assessment'
    fields = 'firstCa','secondCa','exam'
    Form_class = AssessmentForm
    template_name = 'result/assessmentScore.html'

    def get_context_data(self, **kwargs):
        context = super(assessmentEntry, self).get_context_data(**kwargs)
        context['entryFormset'] = modelformset_factory(assessment, fields='__all__', extra=0)
        return context
    def get_success_url(self):
        return reverse_lazy('result:subjectDetails', kwargs={'pk': self.object.subjectName.id})
  
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

class subjectCreate(TemplateView):
    template_name = 'result/subjectCreate.html'

    def get_context_data(self, **kwargs):
        context = super(subjectCreate, self).get_context_data(**kwargs)
        context['allsubjects'] = allsubject.objects.all()
        context['subjectlist'] = subjectList.objects.all()
        context['subjectListForm'] = subjectListForm()
        context['subjectForm'] = SubjectForm()
        return context

    def post(self, request, *args, **kwargs):
        subjectListFrm = subjectListForm(request.POST)
        subjectFrm = SubjectForm(request.POST)
        if subjectListFrm.is_valid():
            subjectListFrm.save()
            return redirect('result:subjectCreate')
        if subjectFrm.is_valid():
            subjectFrm.save()
            return redirect('result:subjectCreate')

class CreateClassArm(CreateView):
    model = classArmTeacher
    form_class = ClassArmTeacherForm
    template_name = 'result/CreateClassArm.html'
    success_url = reverse_lazy('result:CreateClassArm')

    def get_context_data(self, **kwargs):
        context = super(CreateClassArm, self).get_context_data(**kwargs)
        context['classArms'] = classArmTeacher.objects.all()
        return context

class EditSubject(UpdateView):
    model = allsubject
    fields = "__all__"
    template_name = 'result/subjectCreate.html'
    success_url = reverse_lazy('result:subjectCreate')

    def get_context_data(self, **kwargs):
        context = super(EditSubject, self).get_context_data(**kwargs)
        context['subjectForm'] = SubjectForm
        return context

class deleteSubject(DeleteView):
    model = allsubject
    context_object_name = 'allsubject'
    template_name = 'result/Delete.html'
    success_url = reverse_lazy('result:subjectCreate')

class deleteSubjectList(DeleteView):
    model = subjectList
    context_object_name = 'subjectList'
    template_name = 'result/Delete.html'
    success_url = reverse_lazy('result:subjectCreate')

class deleteTeacher(DeleteView):
    model = User
    template_name = 'result/Delete.html'
    success_url = reverse_lazy('result:RegisterTeachers')

class DeleteArm(DeleteView):
    model = classArm
    template_name = 'result/DeleteArm.html'
    success_url = reverse_lazy('result:settings')

class deleteClass(DeleteView):
    model = all_class
    context_object_name = 'all_class'
    template_name = 'result/Delete.html'
    success_url = reverse_lazy('result:settings')

class deleteClassArm(DeleteView):
    model = classArmTeacher
    context_object_name = 'classArmTeacher'
    template_name = 'result/Delete.html'
    success_url = reverse_lazy('result:CreateClassArm')

class payment(TemplateView):
    template_name = 'result/payment.html'

    def get_context_data(self, **kwargs):
        context = super(payment, self).get_context_data(**kwargs)
        return context

class print(TemplateView):
    template_name = 'result/print.html'
    get_success_url = reverse_lazy('result:print')

def entry(request, pk):
    entry_formset = entryformset(queryset=assessment.objects.filter(subjectName=pk))
    helper = entryformsetHelper()
    subject = allsubject.objects.get(id=pk)
    for form in entry_formset:
        form.fields['student'].readonly = True
        form.fields['className'].readonly = True
        form.fields['firstCa'].widget.attrs['class'] = 'form-control'
        form.fields['secondCa'].widget.attrs['class'] = 'form-control'
        form.fields['exam'].widget.attrs['class'] = 'form-control'
        # form.fields['student'].queryset = students.objects.filter(className=1)
    if request.method == 'POST':
        entry_formset = entryformset(request.POST)
        if entry_formset.is_valid():
            entry_formset.save()
            return redirect('result:print')
    return render(request, 'result/entry.html', {'formset': entry_formset, 'helper': helper, 'subject': subject})
    