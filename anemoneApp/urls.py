from django.urls import path

from anemoneApp.forms import EmailAuthForm
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', 
         LoginView.as_view(
             template_name='registration/login.html',
             authentication_form=EmailAuthForm,
             redirect_authenticated_user=True
         ),
         name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('product/', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    #path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('signup/', views.signup_view, name='signup'),
    path('terms/', views.terms, name='terms'),
    path('about/', views.about, name='about'),
    path('custom/', views.custom, name='custom'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('search/', views.search, name='search'),
    # Preview endpoint (POST from custom form) — name changed to avoid clashes
    path('preview/', views.generate_preview, name='preview'),
]
