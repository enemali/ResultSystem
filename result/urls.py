from django.urls import path
from . import views
from .views import classDetails, classList,subjectDetails,studentCreate,studentList,settings
   
urlpatterns = [
    path('', classList.as_view(), name='classList'),
    path('classDetails/<int:pk>/', classDetails.as_view(), name='classDetails'),
    path('subjectDetails/<int:pk>/', subjectDetails.as_view(), name='subjectDetails'),
    path('studentCreate/', views.studentCreate, name='studentCreate'),
    path('studentList/', studentList.as_view(), name='studentList'),
    path('settings/', settings.as_view(), name='settings'),
]