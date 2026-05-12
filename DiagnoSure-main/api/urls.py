from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.create_user),
    path('login/', views.login_user),
    path('analyze/', views.analyze),
    path('chatbot/', views.chatbot),
    path('reports/<int:user_id>/', views.user_reports),
    path('family/', views.manage_family),
]