from django.urls import path
from .views import user_register, user_login, user_logout, user_info, delete_user

urlpatterns = [
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('info/', user_info, name='user_info'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
]