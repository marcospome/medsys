from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponseForbidden, Http404

# ---------------------------- MANEJO DE ERRORES ---------------------------
def custom_500_view(request):
    return render(request, 'base/500.html', status=500)

def custom_404_view(request, exception=None):
    return render(request, 'base/404.html', status=404)

def custom_403_view(request):
    return HttpResponseForbidden()

# -------------------------------------------------------------------------



class IndexView(TemplateView):
    template_name = 'home/index.html'

class CustomLoginView(View):
    template_name = 'home/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('/admin/')  # Cambia 'pagina_principal' a la URL deseada.
            else:
                messages.error(request, "Este usuario no está autorizado para ingresar")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

        return render(request, self.template_name)


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Opcional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

class RegisterView(View):
    template_name = 'home/register.html'
    form_class = CustomUserCreationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/login')  # Cambia 'pagina_principal' a la URL deseada.

        return render(request, self.template_name, {'form': form})
