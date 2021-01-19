from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('account/', views.accountSettings, name="account"),

    path('', views.home, name="home"),
    path('todo/', views.dashboard, name="dashboard"),
    path('about/', views.about, name="about"),
    path('del/<int:item_id>', views.remove, name="del"),

    path('password/', views.change_password, name='change_password'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="info/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="info/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="info/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="info/password_reset_done.html"),
         name="password_reset_complete"),
]