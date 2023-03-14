from django.urls import path, include

from . import views

urlpatterns = [
    path('host_terminal', views.host_terminal, name='host_terminal'),
    path('containers/console/<slug:id>/', views.console, name='console'),
    path('containers/', views.containers, name='containers_index'),
    path('lessons_list/', views.lessons_list, name='lessons_list'),
    path('lessons_list/lessons/<slug:id>/', views.lessons, name='lessons'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('', views.home, name='home'),
    path('list', views.students_containers, name='students_containers'),
    path('view/<int:pk>', views.students_containers_view, name='students_containers_view'),
    path('new', views.students_containers_create, name='students_containers_new'),
    path('edit/<int:pk>', views.students_containers_update, name='students_containers_edit'),
    path('delete/<int:pk>', views.students_containers_delete, name='students_containers_delete'),
    path('mylist', views.my_containers, name='my_containers'),
    path('id', views.containers_id, name='containers_id'),
]