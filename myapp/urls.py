from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_view, name='create'),
    path('read/', views.read_view, name='read'),
    path('update/<int:pk>/', views.update_view, name='update'),
    path('delete/<int:pk>/', views.delete_view, name='delete'),
]

