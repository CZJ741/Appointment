from django.urls import path
from .views import (
    create_appointment, 
    get_my_appointments,
    get_all_appointments,
    get_appointment_detail,
    approve_appointment,
    reject_appointment,
    complete_appointment
)

urlpatterns = [
    # 用户相关接口
    path('appointment/create/', create_appointment, name='create_appointment'),
    path('appointment/my/', get_my_appointments, name='get_my_appointments'),
    path('appointment/detail/<int:appointment_id>/', get_appointment_detail, name='get_appointment_detail'),
    
    # 管理员相关接口
    path('appointment/all/', get_all_appointments, name='get_all_appointments'),
    path('appointment/<int:appointment_id>/approve/', approve_appointment, name='approve_appointment'),
    path('appointment/<int:appointment_id>/reject/', reject_appointment, name='reject_appointment'),
    path('appointment/<int:appointment_id>/complete/', complete_appointment, name='complete_appointment'),
]