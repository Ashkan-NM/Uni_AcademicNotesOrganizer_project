from django.urls import path
from . import views

app_name = 'notes'
urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/create/', views.course_create, name='course_create'),
    path('course/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('course/<int:pk>/delete/', views.course_delete, name='course_delete'),
    
    path('course/<int:course_id>/notes/', views.note_list, name='note_list'),
    path('course/<int:course_id>/notes/create/', views.note_create, name='note_create'),
    path('note/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
    
    path('search/', views.search_notes, name='search'),
]