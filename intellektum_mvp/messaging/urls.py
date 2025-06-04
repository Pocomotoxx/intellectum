from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversation_list_view, name='conversation_list'),
    path('<int:conversation_id>/', views.conversation_detail_view, name='conversation_detail'),
    path('start/<int:user_id>/', views.start_conversation_view, name='start_conversation'),
]
