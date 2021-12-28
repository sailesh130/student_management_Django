from django.urls import path,include
from .views import StudentList,StudentDetail,TeacherDetail,TeacherList,FacultyList,FacultyDetail,SubjectList,SubjectDetail

urlpatterns = [
    
    path('',StudentList.as_view(),name='student'),
    path('<int:pk>/', StudentDetail.as_view(),name='student_details'),
    path('teacher',TeacherList.as_view(),name='teacher'),
    path('teacher/<int:pk>/', TeacherDetail.as_view(),name='teacher_details'),
    path('faculty',FacultyList.as_view(),name='faculty'),
    path('faculty/<int:pk>/', FacultyDetail.as_view(),name='faculty_details'),
    path('subject',SubjectList.as_view(),name='subject'),
    path('subject/<int:pk>/', SubjectDetail.as_view(),name='subject_details'),
   
]
