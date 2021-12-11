from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from django import forms

from . import forms
from . import models

class SignInView(View):
    template_name = 'profile/signin.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.profile = None

        self.context = {
            'userForm': forms.UserFormCreate(data=self.request.POST or None),
            'profile': forms.ProfileForm(data=self.request.POST or None),
        }

        self.userForm = self.context['userForm']
        self.profile = self.context['profile']

        self.render = render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        if not self.userForm.is_valid() or not self.profile.is_valid():
            return self.render

        password = self.userForm.cleaned_data.get('password')
        
        user = self.userForm.save(commit=False)
        user.set_password(password)
        user.save()

        profile = self.profile.save(commit=False)
        profile.user = user
        profile.save()
        
        if password:
            authenticates = authenticate(
                self.request,
                username=user,
                password=password,
            )

            if authenticates:
                login(self.request, user=user)

                return redirect('home:index')

        return self.render
    
    def get(self, *args, **kwargs):
        return self.render

class LogoutView(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        
        return redirect('home:index')

class LogInView(View):
    template_name = 'profile/login.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request,
                'Usuário ou senha inválidos!'
            )
            return redirect('profile:login')

        user = authenticate(self.request, username=username, password=password)

        if not user:
            messages.error(
                self.request,
                'Usuário ou senha inválidos!'
            )
            return redirect('profile:login')

        login(self.request, user=user)

        return redirect('home:index')
        

class UpdateView(View):
    template_name = 'profile/update.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        
        self.profile = models.Profile.objects.filter(user=self.request.user).first()
        
        self.context = {
            'userForm': forms.UserFormUpdate(data=self.request.POST or None, user=self.request.user, instance=self.request.user),
            'profileForm': forms.ProfileForm(data=self.request.POST or None, instance=self.profile),
        }

        self.userForm = self.context['userForm']
        self.profileForm = self.context['profileForm']

        self.render = render(self.request, self.template_name, self.context)


    def post(self, *args, **kwargs):
        if not self.userForm.is_valid() or not self.profileForm.is_valid():
            return self.render
        else:
            username = self.userForm.cleaned_data.get('username')
            password = self.userForm.cleaned_data.get('password')
            email = self.userForm.cleaned_data.get('email')
            first_name = self.userForm.cleaned_data.get('first_name')
            last_name = self.userForm.cleaned_data.get('last_name')

            date = self.profileForm.cleaned_data.get('date')
            cpf = self.profileForm.cleaned_data.get('cpf')
            country = self.profileForm.cleaned_data.get('country')

            if self.request.user.is_authenticated:
                user = get_object_or_404(User, username=self.request.user.username)

                user.username = username

                if password:
                    user.set_password(password)

                user.email = email

                user.first_name = first_name
                user.last_name = last_name
                user.save()

                profile = models.Profile.objects.all().filter(user=user)
                profile.date = date
                profile.cpf = cpf
                profile.country = country
                self.profile.save()

            return redirect('profile:update')
    
    def get(self, *args, **kwargs):
        return self.render