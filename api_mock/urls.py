from django.urls import path 
from . import views

app_name = 'api_mock'

urlpatterns = [
    path('', views.MockResponse , name='MockResponse'),
]
