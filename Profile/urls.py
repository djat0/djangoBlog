from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit-profile', views.editProfile, name='edit-profile'),
    path('profile/reset-password', views.resetPassword, name='reset-password'),

]
