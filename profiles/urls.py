from django.urls import path

from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.SignInView.as_view(), name='signin'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('update/', views.UpdateView.as_view(), name='update'),
]