from django.urls import path
from . import views


urlpatterns = [
    path('register_new_phone/', views.register_new_phone, name='register_new_phone'),
    path('report_detail/<str:slug>', views.report_detail, name='report_detail'),
    path('update_report/<str:slug>', views.update_report, name='update_report'),
    path('delete_report/<str:slug>', views.delete_report, name='delete_report'),
]