from django.urls import path
from .views import classDetails, classList,subjectDetails
   
urlpatterns = [
    path('', classList.as_view(), name='classList'),
    path('classDetails/<int:pk>/', classDetails.as_view(), name='classDetails'),
    path('subjectDetails/<int:pk>/', subjectDetails.as_view(), name='subjectDetails'),
]