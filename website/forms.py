# This extends the user creation object to allow for email address upon signup
# See 'Sign up with extra fields':
# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from website.models import Profile
import datetime
import smtplib

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def profile_save(self, datas):
        user = User.objects.get(username=datas['username'])
        profile = Profile()
        profile.user = user
        profile.activation_key = datas['activation_key']
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()

    def send_email(self, datas):
        link = "http://rephotoeditor.com/activate/?key="+datas['activation_key']
        message = ("Hello ",datas['first_name'], " " ,datas['last_name'], 
        "Please click this link to activate your RePhotoEditor account: ",
        link)
        print(message)
        # smtp_obj = smtplib.SMTP('localhost')
        # smtp_obj.sendmail(no_reply@rephotoeditor.com, datas['email'], message)