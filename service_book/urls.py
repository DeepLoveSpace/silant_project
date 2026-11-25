from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('machine/<int:pk>/', views.machine_detail, name='machine_detail'),
    path('maintenance/<int:pk>/', views.maintenance_detail, name='maintenance_detail'),
    path('claim/<int:pk>/', views.claim_detail, name='claim_detail'),
    
    path('machine/create/', views.machine_create, name='machine_create'),
    path('maintenance/create/', views.maintenance_create, name='maintenance_create'),
    path('claim/create/', views.claim_create, name='claim_create'),
    
    path('machine/<int:pk>/edit/', views.machine_edit, name='machine_edit'),
    path('maintenance/<int:pk>/edit/', views.maintenance_edit, name='maintenance_edit'),
    path('claim/<int:pk>/edit/', views.claim_edit, name='claim_edit'),
]