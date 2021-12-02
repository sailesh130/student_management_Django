from django.urls import path,reverse_lazy
from .views import (HomePageView,SignUpView, StudentCreateView,StudentDetailView,TeacherCreateView,FacultyCreateView,SubjectCreateView,
password_reset_request,StudentUpdateView,StudentDeleteView,StudentListView)
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('signup/',SignUpView.as_view(),name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login1.html'),name='login'),
    path('accounts/logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('change-password/',
        auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html',success_url=reverse_lazy('sucess')),name='change'),
    path('change-password/done',
        auth_views. PasswordChangeDoneView.as_view(template_name='registration/password_change_done1.html'),name='sucess'),
    path("accounts/password_reset/", password_reset_request, name="registration/password_reset"),    
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'), 
    path('student/<int:pk>',StudentDetailView.as_view(),name='student_details'),
     path('student_create',StudentCreateView.as_view(),name='student_create'),
    path('teacher_create',TeacherCreateView.as_view(),name='teacher_create'),
    path('subject_create',SubjectCreateView.as_view(),name='subject_create'),
    path('faculty_create',FacultyCreateView.as_view(),name='faculty_create'),
    path('student_update/<int:pk>',StudentUpdateView.as_view(),name='student_update'),
    path('student_delete/<int:pk>',StudentDeleteView.as_view(),name='student_delete'),
    path('student_list',StudentListView.as_view(),name='student_list'),
    path('student_detail/<int:pk>',StudentDetailView.as_view(),name='student_detail'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)