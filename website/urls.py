from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'login', LoginView.as_view(template_name = 'login.html'), name='login'),
    url(r'logout', LogoutView.as_view(), name='logout'),
    url(r'signup', views.signup, name='signup'),
    url(r'activate/', views.activation, name='activation'),
    url(r'new-activation-link/', views.new_activation_link, name='new_activation_link'),
]