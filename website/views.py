# Django Packages
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
# Custom Django functions/classes
from website.forms import SignUpForm
from website.models import Profile
# Other Python packages
from random import randint
from hashlib import sha1
from datetime import timezone

def index(request):
    template = loader.get_template('mainpage.html')
    return HttpResponse(template.render())

def signup(request):
    if request.method == 'POST':# Basically means, after they click the sign in button on this view
        form = SignUpForm(request.POST)# Pull Sign Up data from Post request
        if form.is_valid():
            form.save()# Save new user to database
            datas = {}# Array that will contain new user data
            datas['username']=form.cleaned_data['username']
            datas['email']=form.cleaned_data['email']
            datas['password1']=form.cleaned_data['password1']
            datas['first_name']=form.cleaned_data['first_name']
            datas['last_name']=form.cleaned_data['last_name']
            
            hash_seed = str(randint(100000, 999999)).encode('utf-8')# 6 digit random number
            username_hash_seed = str(datas['username']).encode('utf-8')# Username will be hashed with random numbers 
            datas['activation_key'] = sha1(hash_seed+username_hash_seed).hexdigest()# Apply hash and save as activation key
            datas['email_subject'] = "RePhotoEditor: Please Activate your Email Account"# Email subject for activation email

            form.profile_save(datas)# Save hash to profile table (See forms.py to see method)
            form.send_email(datas)# Send email with activation link (See forms.py to see method)

            user = authenticate(username=datas['username'], password=datas['password1'])# Create user auth
            login(request, user)# Sign in user
            return redirect('../website')# Redirect to page after sign in
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

#View called from activation email. Activate user if link didn't expire (48h default), or offer to
#send a second link if the first expired.
def activation(request):
    key=request.GET.get('key', '')
    activation_expired = False
    already_active = False
    profile = get_object_or_404(Profile, activation_key=key)
    if profile.user.is_active == False:
        if timezone.now() > profile.key_expires:
            activation_expired = True #Display: offer the user to send a new activation link
            id_user = profile.user.id
        else: #Activation successful
            profile.user.is_active = True
            profile.user.save()

    #If user is already active, simply display error message
    else:
        already_active = True# Display : error message
    return render(request, 'activation.html', locals())# Locals passes all local variables to view

def new_activation_link(request, user_id):
    form = SignUpForm()
    datas={}
    user = User.objects.get(id=user_id)
    if user is not None and not user.is_active:
        datas['username']=user.username
        datas['email']=user.email
        datas['email_subject']="RePhotoEditor: Please Activate your Email Account"

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = datas['username']
        if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
        datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()

        profile = Profile.objects.get(user=user)
        profile.activation_key = datas['activation_key']
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()

        form.sendEmail(datas)
        request.session['new_link']=True #Display: new link sent

    return redirect('index')