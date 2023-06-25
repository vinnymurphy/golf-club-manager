from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views

"""
https://stackoverflow.com/questions/47065438/attributeerror-module-django-contrib-auth-views-has-no-attribute
"""


urlpatterns = [
    path(r'^admin/', admin.site.urls),

    re_path(r'^accounts/login/$', auth_views.login, name='login'),
    re_path(r'^accounts/logout/$', auth_views.logout, name='logout'),
]
