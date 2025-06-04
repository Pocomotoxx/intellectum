from django.urls import path
from . import views

urlpatterns = [
    path('', views.swipe_view, name='swipe_view'),
]
