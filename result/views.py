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
from django.db.models import Count, Sum, Avg, Max, Min , F, Q , Subquery, OuterRef,FloatField , Value,Window, ExpressionWrapper, IntegerField
# import Round from math 
from django.db.models.functions import Round,Coalesce,Rank


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
        context = super(RegisterStudent, self).get_context_data(**kwargs)
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
        # context['settingForm'] = settingForm()
        
        context['allclass'] = all_class.objects.all()
        context['classArm'] = classArm.objects.all()
        context['sections'] = section.objects.all()
        context['img'] = Images.objects.all()
        context['settingtype'] = 'classsetting'
        context['studentCount'] = students.objects.all().count()
        return context
     
    def post(self, request, *args, **kwargs):
        classForm = allClassForm(request.POST)
        armForm = classArmForm(request.POST)
        SectionForm = sectionForm(request.POST)
        imageForm = ImageForm(request.POST, request.FILES)
        # AllsettingForm = settingForm(request.POST)

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
        # if AllsettingForm.is_valid():
        #     AllsettingForm.save()
        #     return redirect('result:settings')

        return render(request, 'result/settings.html', {'classForm': classForm, 
                                                        'sectionForm': sectionForm, 
                                                        'imageForm': imageForm,
                                                        # 'settingForm': AllsettingForm,
                                                        'armForm': armForm})
                                                        
class classList(ListView):
    model = classArmTeacher
    template_name = 'result/classList.html'
    
    def get_context_data(self, **kwargs):
        context = super(classList, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['setting'] = setting.objects.all()
        context['settingForm'] = settingForm()
        if self.request.user.is_staff:
            context["btn"] = "Edit Termlly Settings"
            context['all_class'] = classArmTeacher.objects.annotate(
                commentCount = Count('comment__student__id', distinct=True),
                student_in_assessment = Count('assessment__student__id', distinct=True),
                latestCommentdate = Max('comment__date'),
                latestAssessmentdate = Max('assessment__date')
                )
        else:
            context['all_class'] = classArmTeacher.objects.filter(className__section__sectionName = self.request.user.section).annotate(
                commentCount = Count('comment__id', distinct=True),
                student_in_assessment = Count('assessment__student__id', distinct=True),
                latestCommentdate = Max('comment__date'),
                latestAssessmentdate = Max('assessment__date')
            )
    
            # context['sectionSubjects'] = allsubject.objects.filter(className__className__section__sectionName = self.request.user.section).values('className__className').distinct()
        return context

    def post(self, request, *args, **kwargs):
        TermlysettingForm = settingForm(request.POST)
        if TermlysettingForm.is_valid():
            TermlysettingForm.save()
            return redirect('result:classList')
        return render(request, 'result/classList.html', {'settingForm': settingForm})

class classDetails(DetailView):
    model = classArmTeacher
    context_object_name = 'all_class'
    template_name = 'result/classDetails.html'

    def get_context_data(self, **kwargs):
        context = super(classDetails, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        # if self.request.user.is_staff:
        #     context['subjects'] = allsubject.objects.filter(className_id = self.kwargs['pk'])
        # else:
        #     context['subjects'] = allsubject.objects.filter(subjectTeacher = self.request.user , className_id = self.kwargs['pk'])
        context['subjects'] = allsubject.objects.filter(className_id = self.kwargs['pk'])
       
        context['students'] = students.objects.filter(classArm = self.get_object().classArm ,className = self.get_object().className)
        context['assessment'] = assessment.objects.filter(className_id = self.kwargs['pk'])
        context['firstCAEntry']= context['subjects'].annotate(
                                 firstCa_Count =Count('assessment', filter=Q(assessment__firstCa__gt=0, assessment__term__isnull=False)),
                                 secondCa_Count =Count('assessment', filter=Q(assessment__secondCa__gt=0)),
                                 exam_Count =Count('assessment', filter=Q(assessment__exam__gt=0)),
                                 student_Count =Count('assessment')
                                 )
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

        if Form.is_valid():
            Form.save()
            return redirect('result:subjectDetails', pk=pk)
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
    form_class = UserChangeForm
    success_url = reverse_lazy('result:settings')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        id = self.object.id
        form = UserChangeForm(instance=self.object)
        Button = 'Update Teacher'
        setting = settings.objects.all()
        return render(request, 'result/Edit.html', {'form': form, 'id': id, 'Button': Button, 'setting': setting})

class studentList(ListView):
    model = students
    context_object_name = 'students'
    template_name = 'result/studentList.html'

    def get(self, request, *args, **kwargs):
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
        context['form'] = subjectForm()
        context['parentsbjForm'] = parentsubjectForm()
        return context

    def post(self, request, *args, **kwargs):
        subjectListFrm = subjectListForm(request.POST)
        form = subjectForm(request.POST)
        parentsbjForm = parentsubjectForm(request.POST)
        if subjectListFrm.is_valid():
            subjectListFrm.save()
            return redirect('result:subjectCreate')
        if form.is_valid():
            form.save()
            return redirect('result:subjectCreate')
        if parentsbjForm.is_valid():
            parentsbjForm.save()
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

class editClassArm(UpdateView):
    model = classArmTeacher
    form_class = ClassArmTeacherForm
    template_name = 'result/CreateClassArm.html'
    success_url = reverse_lazy('result:CreateClassArm')

class EditSubject(UpdateView):
    model = allsubject
    form_class = subjectForm
    template_name = 'result/subjectCreate.html'
    success_url = reverse_lazy('result:index')

    # def get_context_data(self, **kwargs):
    #     context = super(EditSubject, self).get_context_data(**kwargs)
    #     context['subjectForm'] = self.form_class
    #     return context

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
    
    if request.method == 'POST':
        entry_formset = entryformset(request.POST)
        if entry_formset.is_valid():
            entry_formset.save()
            return redirect('result:classDetails', pk=singleSubject.className.id)
    return render(request, 'result/entry.html', {'formset': entry_formset, 'helper': helper, 'subject': subject})
    
class searchStudent(TemplateView):
    template_name = 'result/searchStudent.html'

    def get_context_data(self, **kwargs):
        context = super(searchStudent, self).get_context_data(**kwargs)
        context["allStudents"] = students.objects.all()
        return context

class addComment(CreateView):
    model = comment
    template_name = 'result/addComment.html'

    def get (self, request, pk ,*args, **kwargs):
        form = commentForm()
        form.fields['className'].queryset = classArmTeacher.objects.filter(pk = pk )
        assessments = assessment.objects.all().filter(className = pk )
        students_in_assessment = students.objects.filter(id__in=assessments.values('student_id'))
        comments = comment.objects.all().filter(className = pk )
        form.fields['student'].queryset = students_in_assessment.exclude(id__in=comments.values('student_id'))
        return render(request, self.template_name, {'form': form , 'assessment': assessments, 'comments': comments})
    
    def post(self, request, pk , *args, **kwargs):
        form = commentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('result:addComment', pk = pk )
        return render(request, self.template_name, {'form': form})

class deleteComment(DeleteView):
    model = comment
    template_name = 'result/Delete.html'
    def get_success_url(self):
        return reverse_lazy('result:addComment', kwargs={'pk': self.object.className.id})

class editComment(UpdateView):
    model = comment
    template_name = 'result/addComment.html'
    form_class = commentForm
    
    def get_success_url(self):
        return reverse_lazy('result:addComment', kwargs={'pk': self.object.className.id})

class examResult(TemplateView):
    template_name = 'result/examResult.html'

    def get_context_data(self, **kwargs):
        context = super(examResult, self).get_context_data(**kwargs)
        student_ids = students.objects.filter(id__in=assessment.objects.filter(className=self.kwargs['pk']).values('student_id'))
        
        
        context['highestexamTotal'] = allsubject.objects.filter(className=self.kwargs['pk']).annotate(highest = Max(F('assessment__firstCa') + F('assessment__secondCa') + F('assessment__exam'))).order_by('-highest')
        context['lowestexamTotal'] = allsubject.objects.filter(className=self.kwargs['pk']).annotate(lowest = Min(F('assessment__firstCa') + F('assessment__secondCa') + F('assessment__exam'))).order_by('lowest')
        context['subjectAverage'] = allsubject.objects.filter(className=self.kwargs['pk']).annotate(average = Round(Avg(F('assessment__firstCa') + F('assessment__secondCa') + F('assessment__exam'), output_field=FloatField()), 2))
        context['setting'] = setting.objects.all()
        
        context['allScores'] = assessment.objects.filter(className=self.kwargs['pk']).annotate(
            Subjectexamtotal= F('firstCa') + F('secondCa') + F('exam'),
            position = Window(expression=Rank(), partition_by=[F('subjectName_id')], order_by=F('Subjectexamtotal').desc()),

            )

        context["all_students"] = student_ids.annotate(
                # examtotal=Sum(F('assessment__firstCa') + F('assessment__secondCa') + F('assessment__exam'), output_field=FloatField()),
                examaverage=Round(Avg(F('assessment__firstCa') + F('assessment__secondCa') + F('assessment__exam'), output_field=FloatField()), 2),
                assessmentCount=Count('assessment__id'),
                examObtainable=Count('assessment__id') * 100,
                # position = context['allScores'].filter(student_id=OuterRef('id')).values('position'),
                studentsection = section.objects.filter(id=OuterRef('className__section_id')).values('sectionName'),
                studentclass = classArmTeacher.objects.filter(className=OuterRef('className_id')).values('className__className'),
                # failedAssessment = context['allScores'].filter(student_id=OuterRef('id'), examtotal__lt=40).values('subjectName__subjectName'),
                )
                # studentclass = classArmTeacher.objects.filter(className=OuterRef('className_id')).values('className__className'),
            
        context["highestAverage"] = context["all_students"].order_by('-examaverage')[:1]
        context["lowestAverage"] = context["all_students"].order_by('examaverage')[:1]
        context["classAverage"] = context["all_students"].aggregate(classAvg=Round(Avg('examaverage'), 2))
        
        context["allComments"] = comment.objects.filter(className=self.kwargs['pk'], student = OuterRef('id')).annotate(
            )
    

    
        ALLstudents = students.objects.filter(id__in=assessment.objects.filter(className=self.kwargs['pk']).values('student_id'))
        
        final_assessments = []

        class_main_assessment = assessment.objects.filter(className=self.kwargs['pk'],subjectName__is_childSubject=False).annotate(
            total=Sum(F('firstCa') + F('secondCa') + F('exam')))
        class_parent_assessment = assessment.objects.filter(
            className=self.kwargs['pk'],subjectName__is_childSubject=True
                ).annotate(
                    parentSubjectTOTAL=Sum(F('firstCa') + F('secondCa') + F('exam')),
                    parentSubjectAVEREG= Avg(F('firstCa') + F('secondCa') + F('exam')),

                    )
        

        for student in ALLstudents:
            student_main_assessments = class_main_assessment.filter(student=student)
            student_parent_assessments = class_parent_assessment.filter(student=student
                ).values('student', 
                        'subjectName__parentSubject__parentSubjectName',
                        'parentSubjectTOTAL',
                        'parentSubjectAVEREG',
                        ).annotate(
                        TOTAL = (Sum('firstCa')/2) + (Sum('secondCa') /2)+ Sum('exam'),
                        firstCa = Sum('firstCa')/2,
                        secondCa = Sum('secondCa')/2,
                        exam = Sum('exam'),
                        )

        #     # add student_main_assessments dict to student_parent_assessments dict
            # parent_subject = student_parent_assessments[0]['TOTAL']
            if len(student_parent_assessments) > 0:
                student_total = student_main_assessments.aggregate(TOTAL=Sum(F('total')))['TOTAL'] + student_parent_assessments[0]['TOTAL']
                student_subjects_count = student_main_assessments.count() + student_parent_assessments.count()
            else:
                student_total = student_main_assessments.aggregate(TOTAL=Sum(F('total')))['TOTAL']
                student_subjects_count = student_main_assessments.count()

            student_average = round(student_total / student_subjects_count, 2)
            examObtainable = int(student_subjects_count) * 100
            final_assessments.append({
                                        'student': student, 
                                        'subjects': student_main_assessments, 
                                        'parent_subjects': student_parent_assessments,
                                        'studenttotal': student_total,
                                        'studentaverage': student_average,
                                        'student_subjects_count': student_subjects_count,
                                        'examObtainable': examObtainable,
                                        })
        context['final_assessments'] = final_assessments
        return context
        

        # multi line comments


    

class editSettings(UpdateView):
    model = setting
    template_name = 'result/editTermsetting.html'
    form_class = settingForm
    
    def get_success_url(self):
        return reverse_lazy('result:classList')
