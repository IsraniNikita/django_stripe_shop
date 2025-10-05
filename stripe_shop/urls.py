from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('signup/', views.signup, name='signup'),
    
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='shop:index'), name='logout'),
]
