from django.urls import path

from main.views import keks

urlpatterns = [
    path('keks/', keks, name='keks')
]
