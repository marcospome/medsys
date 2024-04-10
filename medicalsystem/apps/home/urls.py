from django.urls import path
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.IndexView.as_view()),
    path('login', views.CustomLoginView.as_view(), name='custom_login'),  # Define una URL con nombre 'custom_login'.
    path('register', views.RegisterView.as_view(), name='register'),

]

if settings.DEBUG:
    from django.conf.urls.static import static
        #le decimos que accediendo a la URLPATTERNS si alguien quiere entrar a ver al fichero de turno, que lo pueda ver
        #importamos desde settings los archivos statics, le pasamos el docu root, donde debe ir abuscarlos
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)