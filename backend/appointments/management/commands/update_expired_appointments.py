from django.core.management.base import BaseCommand
from django.utils import timezone
from appointments.models import Appointment


class Command(BaseCommand):
    """
    更新过期预约状态的管理命令
    
    功能：
    1. 将已过期的"已批准"(approved)状态的预约更新为"已完成"(completed)
    2. 将已过期的"待审核"(pending)状态的预约更新为"已过期"(expired)
    """
    help = '更新过期预约的状态'

    def handle(self, *args, **options):
        # 获取当前日期
        today = timezone.now().date()
        
        # 统计更新的预约数量
        approved_updated_count = 0
        pending_updated_count = 0
        
        # 1. 更新已过期的"已批准"状态的预约为"已完成"
        approved_expired_appointments = Appointment.objects.filter(
            visit_date__lt=today,
            status='approved'
        )
        approved_updated_count = approved_expired_appointments.update(status='completed')
        
        # 2. 更新已过期的"待审核"状态的预约为"已过期"
        pending_expired_appointments = Appointment.objects.filter(
            visit_date__lt=today,
            status='pending'
        )
        pending_updated_count = pending_expired_appointments.update(status='expired')
        
        # 输出更新结果
        self.stdout.write(self.style.SUCCESS(f'成功更新 {approved_updated_count} 个已批准的过期预约为已完成'))
        self.stdout.write(self.style.SUCCESS(f'成功更新 {pending_updated_count} 个待审核的过期预约为已过期'))
        self.stdout.write(self.style.SUCCESS(f'总计更新 {approved_updated_count + pending_updated_count} 个过期预约'))
