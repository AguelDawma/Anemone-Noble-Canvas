from django.urls import path

from anemoneApp.forms import EmailAuthForm
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', 
         LoginView.as_view(
             template_name='registration/login.html', # 🌟 1. Point to your custom template
             authentication_form=EmailAuthForm,       # 🌟 2. Use your custom form
             redirect_authenticated_user=True
         ),
         name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('product/', views.product, name='product'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('signup/', views.signup_view, name='signup'),
    path('terms/', views.terms, name='terms'),
    path('about/', views.about, name='about'),
    path('custom/', views.custom, name='custom'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]