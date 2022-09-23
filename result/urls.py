from django.urls import path
from . import views
from .views import (classDetails, 
                    classList,
                    subjectDetails,
                    studentList,
                    settings,
                    studentDelete,
                    index,
                    assessmentEntry,
                    deleteClass,
                    signUpPage,
                    loginPage,
                    logoutPage,
                    )
   
urlpatterns = [
    path('', index.as_view(), name='index'),
    path('classList/', classList.as_view(), name='classList'),
    path('classDetails/<int:pk>/', classDetails.as_view(), name='classDetails'),
    path('subjectDetails/<int:pk>/', subjectDetails.as_view(), name='subjectDetails'),
    path('studentList/', studentList.as_view(), name='studentList'),
    path('settings/', settings.as_view(), name='settings'),
    path('studentDelete/<int:pk>/', studentDelete.as_view(), name='studentDelete'),
    path('uploadimage/', views.uploadimage, name='uploadimage'),
    path('deleteClass/<int:pk>/', deleteClass.as_view(), name='deleteClass'),
    path('assessmentScores/<int:pk>/', assessmentEntry.as_view(), name='assessmentScores'),
    path('signUp/', signUpPage.as_view(), name='signUp'),
    path('login/', loginPage.as_view(), name='login'),
    path('logout/', logoutPage.as_view(), name='logout'),

    
]