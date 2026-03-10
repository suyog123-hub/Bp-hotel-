from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('about/',about, name='about'),
    path('contact/',contact, name='contact'),
    path('gallery/',gallery, name='gallery'),
    path('',home, name='home'),
    path('menu/',menu, name='menu'),
    path('reserved/',reserved, name='reserved'),
    path('review/',review, name='review'),
    path('signin/',signin,name="signin"),
    path('signout/',signout,name='signout'),
    path('register/',register,name="register"),
    path('renewpass/',renewpass,name="renewpass"),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name="changepass"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]