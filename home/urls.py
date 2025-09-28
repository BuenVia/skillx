from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add_new/', views.add_new, name="add_new"),
    # CLIENTS
    path("clients/", views.client_list, name="client_list"),
    path("clients/create/", views.client_create, name="client_create"),
    path("clients/read/<int:client_id>", views.client_read, name="client_read"),
    path("clients/update/<int:client_id>", views.client_update, name="client_update"),
    path("clients/delete/<int:client_id>", views.client_delete, name="client_delete"),
    # USERS
    path("users/", views.user_list, name="user_list"),
    path("users/create/", views.user_create, name="user_create"),
    path("users/read/<int:user_id>", views.user_read, name="user_read"),
    path("users/update/<int:user_id>", views.user_update, name="user_update"),
    path("users/delete/<int:user_id>", views.user_delete, name="user_delete"),
]