from django.urls import path,include
from .views import StudentList,StudentDetail,TeacherDetail,TeacherList,FacultyList,FacultyDetail,SubjectList,SubjectDetail

urlpatterns = [
    
    path('',StudentList.as_view()),
    path('<int:pk>/', StudentDetail.as_view()),
    path('teacher',TeacherList.as_view()),
    path('teacher/<int:pk>/', TeacherDetail.as_view()),
    path('faculty',FacultyList.as_view()),
    path('faculty/<int:pk>/', FacultyDetail.as_view()),
    path('subject',SubjectList.as_view()),
    path('subject/<int:pk>/', SubjectDetail.as_view()),
   
]
