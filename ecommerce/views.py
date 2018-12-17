from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model

from .forms import ContactForm
from .forms import LoginForm
from .forms import RegisterForm


def home_page(request):
    context = {
        'title': 'hello there!',
        'content': 'this is main page yall'
    }
    if request.user.is_authenticated():
        context['premium_content'] = "only register user can see this!"
    return render(request, 'home_page.html', context)


def about_page(request):
    context = {
        'title': 'this is about page',
        'content': 'this is about page yall'
    }
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': 'this is contact page',
        'content': 'this is contact page yall',
        'form': contact_form,
        'brand': 'new Hocmax'
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    return render(request, 'contact/view.html', context)


def login_page(request):
    login_form = LoginForm(request.POST or None)
    print(request.user.is_authenticated())
    context = {
        'form': login_form
    }
    if login_form.is_valid():
        # print(login_form.cleaned_data)
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(request.user.is_authenticated())
            # redirect to a success page
            return redirect('/')
        else:
            print("error!")
    return render(request, 'auth/login.html', context)


User = get_user_model()


def register_page(request):
    register_form = RegisterForm(request.POST or None)
    context = {
        'form': register_form
    }
    if register_form.is_valid():
        print(register_form.cleaned_data)
        username = register_form.cleaned_data.get('username')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password')
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
    return render(request, 'auth/register.html', context)
