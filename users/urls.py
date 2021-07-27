from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    path('sign_up/', views.sign_up_page, name='sign_up'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('users_comments/', views.users_comments, name='users_comments'),
    path('users_update_profile/', views.users_update_profile, name='users_update_profile'),
    path('profile/', views.profile_page, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('activate/<uidb64>/<token>', views.verification_email, name='activate'),
    path('set_new_password/<uidb64>/<token>', views.set_new_password, name='set_new_password'),
    path('request_reset_email/', views.request_reset_email, name='request_reset_email'),

]