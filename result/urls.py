from django.urls import path
from . import views
from .views import *
   
urlpatterns = [
    path('', index, name='index'),
    path('classList/', classList.as_view(), name='classList'),
    path('classDetails/<int:pk>/', classDetails.as_view(), name='classDetails'),
    path('subjectDetails/<int:pk>/', subjectDetails.as_view(), name='subjectDetails'),
    path('studentList/', studentList.as_view(), name='studentList'),
    path('settings/', settings.as_view(), name='settings'),
    path('studentDelete/<int:pk>/', studentDelete.as_view(), name='studentDelete'),
    path('uploadimage/', views.uploadimage, name='uploadimage'),
    path('deleteClass/<int:pk>/', deleteClass.as_view(), name='deleteClass'),
    path('assessmentScores/<int:pk>/', assessmentEntry.as_view(), name='assessmentScores'),
    path('RegisterTeachers', RegisterTeachers.as_view(), name='RegisterTeachers'),
    path('login/', loginPage, name='login'),
    path('logoutUser/', logoutUser.as_view(), name='logoutUser'),
    path('registerStudent/', RegisterStudent.as_view(), name='registerStudent'),
    path('deleteArm/<int:pk>/', DeleteArm.as_view(), name='deleteArm'),
    path('EditClass/<int:pk>/', EditClass.as_view(), name='EditClass'),
    path('editStudent/<int:pk>/', EditStudent.as_view(), name='editStudent'),
    path('editTeacher/<int:pk>/', EditTeacher.as_view(), name='editTeacher'),
    path('deleteTeacher/<int:pk>/', deleteTeacher.as_view(), name='deleteTeacher'),
    path('studentList/', studentList.as_view(), name='studentList'),   
    path('subjectCreate/', subjectCreate.as_view(), name='subjectCreate'),
    path('CreateClassArm/', CreateClassArm.as_view(), name='CreateClassArm'),
    path('deleteClassArm/<int:pk>/', deleteClassArm.as_view(), name='deleteClassArm'),
    path('deleteSubject/<int:pk>/', deleteSubject.as_view(), name='deleteSubject'),
    path('payment/', payment.as_view(), name='payment'),
    path('deleteSubjectList/<int:pk>/', deleteSubjectList.as_view(), name='deleteSubjectList'),
    path('EditSubject/<int:pk>/', EditSubject.as_view(), name='EditSubject'),
    path('print/', print.as_view(), name='print'),
    path('entry/', views.entry, name='entry')
]