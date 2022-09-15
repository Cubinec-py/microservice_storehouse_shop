from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from core.settings import LOGIN_REDIRECT_URL

from user_authentication.forms import CustomUserCreationForm, CustomAuthenticationForm


def save_user_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            data['form_is_valid'] = True
            login(request, user)
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
    else:
        form = CustomUserCreationForm()
    return save_user_form(request, form, 'registration/signin.html')


def user_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
    else:
        form = CustomAuthenticationForm()
    return user_form(request, form, 'registration/login.html')


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name = 'registration/profile.html'
    success_url = reverse_lazy("user_authentication:profile")
    success_message = "Profile updated!"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


def change_password(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required(login_url=LOGIN_REDIRECT_URL)
def user_password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
    else:
        form = PasswordChangeForm(request.user)
    return change_password(request, form, 'registration/change_password.html')
