from django.urls import path
from . import views

urlpatterns = [
    path('', views.match_list_view, name='match_list'),
]
