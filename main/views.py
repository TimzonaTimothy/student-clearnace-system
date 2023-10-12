from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.models import *
from django.contrib import auth
from django.contrib.auth import logout
# Create your views here.
def home(request):
    return render(request, 'index.html', {})

def sign_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            # if Account.objects.filter(email=email, is_active=False).exists():
            #     messages.warning(request, 'Please verify your mail')
            #     return redirect('/sign_in')
            
            user = auth.authenticate(email=email, password=password)

            if user is not None:
                user = get_object_or_404(Account, email=email)
                auth.login(request,user)
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('/sign_in')
        else:
            return render(request, 'login.html', {})

def sign_up(request):
    faculties = Faculty.objects.all()
    departments = Department.objects.all()
    sessions = Session.objects.all()
    context = {
        'faculties':faculties,
        'departments':departments,
        'sessions':sessions,
    }
    return render(request, 'reg_form.html',context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')