from django.urls import path
from .views import (
    create_appointment, 
    get_my_appointments,
    get_all_appointments,
    get_appointment_detail,
    approve_appointment,
    reject_appointment,
    complete_appointment,
    get_appointment_queue,
    batch_review_appointments,
    get_visit_date_stats,
    get_announcements,
    create_announcement,
    update_announcement,
    delete_announcement
)

urlpatterns = [
    # 用户相关接口
    path('appointment/create/', create_appointment, name='create_appointment'),
    path('appointment/my/', get_my_appointments, name='get_my_appointments'),
    path('appointment/detail/<int:appointment_id>/', get_appointment_detail, name='get_appointment_detail'),
    path('appointment/queue/', get_appointment_queue, name='get_all_appointment_queues'),
    path('appointment/queue/<int:appointment_id>/', get_appointment_queue, name='get_appointment_queue'),
    
    # 管理员相关接口
    path('appointment/all/', get_all_appointments, name='get_all_appointments'),
    path('appointment/<int:appointment_id>/approve/', approve_appointment, name='approve_appointment'),
    path('appointment/<int:appointment_id>/reject/', reject_appointment, name='reject_appointment'),
    path('appointment/<int:appointment_id>/complete/', complete_appointment, name='complete_appointment'),
    path('appointment/batch-review/', batch_review_appointments, name='batch_review_appointments'),
    
    # 探访日统计接口
    path('appointment/visit-date-stats/', get_visit_date_stats, name='get_visit_date_stats'),
    
    # 公告相关接口
    path('announcements/', get_announcements, name='get_announcements'),
    path('announcement/create/', create_announcement, name='create_announcement'),
    path('announcement/<int:pk>/update/', update_announcement, name='update_announcement'),
    path('announcement/<int:pk>/delete/', delete_announcement, name='delete_announcement'),
]