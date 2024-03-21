from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="myapp/index.html"), name='index'),
    path('create/', views.create_view, name='create'),
    path('read/', views.read_view, name='read'),
    path('update/<uuid:pk>/', views.update_view, name='update'),
    path('delete/<uuid:pk>/', views.delete_view, name='delete'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('upload_photo/<uuid:pk>/', views.upload_photo, name='upload_photo'),
]

