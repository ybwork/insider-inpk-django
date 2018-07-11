from django.urls import path

from auth import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('confirm/email/<str:email_code>', views.confirm_email, name='confirm_email'),
    path('password/email', views.send_reset_link_email),
    path('password/reset/<str:password_code>', views.show_reset_password_form, name='show_reset_password_form'),
    path('password/reset', views.reset_password, name='reset_password'),

    # path('companies/<str:id>/users', views.get_company_users, name='companies_users'),
    #
    # path('users', views.User.as_view()),
    # path('users/<str:id>', views.User.as_view()),
]