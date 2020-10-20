from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
    path('edit_user', views.edit_user),
    path('update_user', views.update_user),
    path('show_user/<int:user_id>', views.show_user),
    path('create_project', views.create_project),
    path('project_page/<int:project_id>', views.project_page),
    path('destroy_project/<int:project_id>', views.destroy_project),
]