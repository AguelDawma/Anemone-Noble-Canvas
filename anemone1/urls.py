"""
URL configuration for anemone1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import include
from django.urls import path
from django.contrib.auth.views import LoginView
from anemoneApp.forms import EmailAuthForm # 🌟 Import your custom form
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('anemoneApp.urls')),
    path('login/', 
         LoginView.as_view(
             template_name='registration/login.html', # 🌟 1. Point to your custom template
             authentication_form=EmailAuthForm,
             redirect_authenticated_user=True
         ), 
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(),
         name='logout'),

    # Add this line for all built-in auth URLs (login, logout, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
