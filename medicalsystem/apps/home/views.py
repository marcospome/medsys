from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView, ListView
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.forms import UserCreationForm

class IndexView (TemplateView):
    template_name='home/index.html' # ruta donde se cuentra el template ¡Recordar que se ubica en la carpeta template a la altura del manage.py!

class CustomLoginView(View):
    template_name = 'home/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        error_message = None

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/admin/')  # Cambia 'pagina_principal' a la URL deseada.
        else:
            error_message = "Usuario o contraseña incorrectos"

        return render(request, self.template_name, {'error_message': error_message})


class RegisterView(View):
    template_name = 'home/register.html'
    form_class = UserCreationForm

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
            return redirect('/login/')  # Cambia 'pagina_principal' a la URL deseada.

        return render(request, self.template_name, {'form': form})
