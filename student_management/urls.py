from django.urls import path
from . import views 

urlpatterns = [
    path("",views.index,name="index"),
    path("register",views.register,name='register'), 
    path("login",views.login_view,name='login'), 
    path('logout',views.logout_view,name='logout'), 
    path('add',views.add_student,name='add'),
    path('search',views.search_student,name='search'),
    path('delete',views.delete_student,name='delete'),
    path('update',views.update_student,name='update')
]
