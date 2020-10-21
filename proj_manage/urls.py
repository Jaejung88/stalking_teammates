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
    path('add_member/<int:this_project_id>', views.add_member),
    path('destroy_project/<int:project_id>', views.destroy_project),
    path('create_task/<int:project_id>', views.create_task),
    path('destroy_task/<int:project_id>/<int:task_id>', views.destroy_task),
    path('post_message/<int:this_project_id>', views.post_message),
    path('post_comment/<int:message_id>/<int:this_project_id>', views.post_comment),
]