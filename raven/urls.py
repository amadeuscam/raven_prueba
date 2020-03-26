from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.upload, name="upload"),
    path('remove-upload/', views.remove_upload, name="remove_upload"),
    path('signup/', views.SignUp.as_view(), name='signup'),
    # path('upload_list/', views.upload_list_rv,name="upload_list"),
]
