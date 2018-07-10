from django.urls import path

from auth import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('confirm/email/<str:email_code>', views.confirm_email, name='confirm_email'),
    path('password/email', views.send_reset_link_on_email),

    path('companies/<str:id>/users', views.get_company_users, name='companies_users'),

    path('users', views.User.as_view()),
    path('users/<str:id>', views.User.as_view()),
]
