from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_user, login, LoginView

app_name = 'user'
urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', LoginView.as_view(),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
