from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic import TemplateView,ListView,DetailView,UpdateView,DeleteView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreateForm,StudentForm
from django.urls import reverse_lazy
from .models import Student,Supervisior,Subject,Faculty,CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from django.db.models.query_utils import Q
from django.http import Http404
from django.views import View
# Create your views here.


class PageNotFoundMixin():
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # return custom template
            return render(request, 'no_object.html', status=404)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)



class HomePageView(TemplateView):
    template_name = 'home.html'


class SignUpView(CreateView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'



class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'



class StudentDetailView(LoginRequiredMixin, PageNotFoundMixin,DetailView):
    model = Student
    template_name = 'student_details.html'

    

class StudentDeleteView(LoginRequiredMixin,PageNotFoundMixin,DeleteView):
    model = Student
    template_name = 'student_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'
    

class StudentUpdateView(LoginRequiredMixin,PageNotFoundMixin,UpdateView):
    model = Student
    fields = '__all__'
    login_url = 'login'
    template_name = 'student_update.html'
    

class StudentCreateView(LoginRequiredMixin,CreateView):

    form_class = StudentForm
    template_name = 'create.html'
  
    login_url = 'login'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = 'Student'
        return context



class TeacherCreateView(LoginRequiredMixin,CreateView):
    model = Supervisior
    fields = '__all__'
    template_name = 'create.html'
   
    login_url = 'login'
    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = 'Teacher'
        return context

    
class SubjectCreateView(LoginRequiredMixin,CreateView):
    model = Subject
    fields = '__all__'
    template_name = 'create.html'
   
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = 'Subject'
        return context


class FacultyCreateView(LoginRequiredMixin,CreateView):
    model = Faculty
    fields = '__all__'
    template_name = 'create.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = 'Faculty'
        return context


class SearchResultView(ListView):
    template_name = 'create.html'

    def get_queryset(self):
        query = self.request.GET.get('name')
        object_list = Student.objects.filter(name__icontains=query)
        return object_list



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = CustomUser.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})