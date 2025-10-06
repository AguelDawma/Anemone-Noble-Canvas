from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('product/', views.product, name='product'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('signup/', views.signup, name='signup'),
    path('terms/', views.terms, name='terms'),
    path('custom/', views.custom, name='custom'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]