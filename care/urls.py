from django.contrib import admin
from django.urls import path

from care.frontend import views as front_views

urlpatterns = [
    path('', front_views.index),
    path('admin/', admin.site.urls)
]
