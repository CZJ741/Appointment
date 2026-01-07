from django.contrib import admin
from .models import Appointment, RelativeInfo, VisitRecord

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('visitor_name', 'prisoner_name', 'time_slot', 'status', 'user', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('visitor_name', 'prisoner_name', 'visitor_id_card')
    date_hierarchy = 'visit_date'
    # 按提交时间排序
    ordering = ['-created_at']

@admin.register(RelativeInfo)
class RelativeInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'relationship', 'appointment')
    search_fields = ('name', 'id_card')
    list_filter = ('relationship',)

@admin.register(VisitRecord)
class VisitRecordAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'visit_time', 'actual_visitor')
    date_hierarchy = 'visit_time'
    search_fields = ('actual_visitor',)
