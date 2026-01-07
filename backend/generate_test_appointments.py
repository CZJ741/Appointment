#!/usr/bin/env python3
"""
生成预约测试数据脚本

该脚本用于生成300条状态为pending的预约数据，包括随机的提交时间和探访日期。
"""

import os
import sys
import django
import random
from datetime import date, datetime, timedelta

# 添加项目路径到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appointment_system.settings')

# 初始化Django
django.setup()

from appointments.models import Appointment, RelativeInfo
from users.models import User

def generate_random_id_card():
    """生成随机身份证号"""
    area_code = random.randint(110000, 659000)
    birth_year = random.randint(1960, 2000)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    sequence = random.randint(100, 999)
    return f'{area_code}{birth_year:04d}{birth_month:02d}{birth_day:02d}{sequence:03d}'

def generate_random_phone():
    """生成随机手机号"""
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                 '150', '151', '152', '153', '155', '156', '157', '158', '159',
                 '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
    prefix = random.choice(prefixes)
    suffix = random.randint(10000000, 99999999)
    return f'{prefix}{suffix}'

def generate_random_visit_date():
    """从2026年探访日列表中随机选择探访日期"""
    visit_dates = [
        '2026-01-14', '2026-02-10', '2026-03-18', '2026-04-15',
        '2026-05-13', '2026-06-17', '2026-07-15', '2026-08-12',
        '2026-09-16', '2026-10-14', '2026-11-18', '2026-12-16'
    ]
    selected_date = random.choice(visit_dates)
    return datetime.strptime(selected_date, '%Y-%m-%d').date()

def generate_random_created_at():
    """生成随机提交时间（过去30天内）"""
    days_ago = random.randint(0, 30)
    hours_ago = random.randint(0, 23)
    minutes_ago = random.randint(0, 59)
    return datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)

def generate_test_appointments():
    """
    生成300条状态为pending的预约数据
    包括随机的提交时间和探访日期
    """
    print("开始生成测试数据...")
    
    # 1. 创建测试用户（如果不存在）
    try:
        test_user = User.objects.get(username='test_user')
        print("使用现有测试用户")
    except User.DoesNotExist:
        test_user = User.objects.create_user(
            username='test_user',
            password='test123456',
            full_name='测试用户',
            phone_number='13800138000',
            email='test@example.com'
        )
        print("创建测试用户成功")
    
    # 2. 生成300条预约记录，包含不同状态和探访日期
    appointment_count = 0
    visitor_names = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十',
                     '郑十一', '王十二', '冯十三', '陈十四', '褚十五', '卫十六',
                     '蒋十七', '沈十八', '韩十九', '杨二十', '朱二十一', '秦二十二']
    
    prisoner_names = ['戒毒人员A', '戒毒人员B', '戒毒人员C', '戒毒人员D', '戒毒人员E',
                      '戒毒人员F', '戒毒人员G', '戒毒人员H', '戒毒人员I', '戒毒人员J']
    
    relationships = ['父母', '配偶', '子女', '兄弟', '姐妹', '其他亲属']
    
    addresses = [
        '黄冈市黄州区东门路',
        '黄冈市黄州区赤壁大道',
        '黄冈市黄州区西湖一路',
        '黄冈市黄州区西湖二路',
        '黄冈市黄州区西湖三路',
        '黄冈市黄州区宝塔大道',
        '黄冈市黄州区新港大道',
        '黄冈市黄州区沿江路',
        '黄冈市黄州区胜利街',
        '黄冈市黄州区八一路',
        '黄冈市黄州区体育路',
        '黄冈市黄州区文化路',
        '黄冈市黄州区教育路',
        '黄冈市黄州区科技路',
        '黄冈市黄州区发展大道',
        '黄冈市黄州区创业路',
        '黄冈市黄州区建设路',
        '黄冈市黄州区和平路',
        '黄冈市黄州区解放路',
        '黄冈市黄州区人民路',
        '黄冈市黄州区民主路',
        '黄冈市黄州区自由路',
        '黄冈市黄州区幸福路',
        '黄冈市黄州区光明路',
        '黄冈市黄州区朝阳路',
        '黄冈市黄州区复兴路',
        '黄冈市黄州区振兴路',
        '黄冈市黄州区繁荣路',
        '黄冈市黄州区富强路',
        '黄冈市黄州区文明路'
    ]
    
    reasons = ['常规探访', '了解情况', '心理疏导', '家庭团聚', '节日探访',
               '特殊情况说明', '关心近况', '政策咨询']
    
    # 用于跟踪每天的预约数量
    daily_appointment_count = {}
    
    for i in range(300):
        # 生成随机提交时间
        created_at = generate_random_created_at()
        
        # 生成随机预约号（基于提交时间，按照正确的逻辑）
        date_str = created_at.strftime('%Y%m%d')
        
        # 获取该日期已有的预约数量
        if date_str not in daily_appointment_count:
            daily_appointment_count[date_str] = 0
        daily_appointment_count[date_str] += 1
        
        # 生成顺序号（该日期已有的预约数量）
        order_number = daily_appointment_count[date_str]
        
        # 生成预约号
        appointment_id = f'{date_str}{order_number}'
        
        # 随机生成探访日期：约30%的概率生成已过期的日期，70%的概率生成未来日期
        if random.random() < 0.3:
            # 生成过去的日期（已过期）
            days_ago = random.randint(1, 365)
            visit_date = date.today() - timedelta(days=days_ago)
        else:
            # 生成随机探访日期（用户选择的探访日）
            visit_date = generate_random_visit_date()
        
        # 生成随机抵达时间（8:00-17:00之间）
        arrival_hour = random.randint(8, 17)
        arrival_minute = random.choice([0, 15, 30, 45])
        arrival_time = f'{arrival_hour:02d}:{arrival_minute:02d}'
        
        # 生成随机探访时间诉求（抵达时间后15-60分钟）
        visit_hour = arrival_hour
        visit_minute = arrival_minute + random.randint(15, 60)
        if visit_minute >= 60:
            visit_hour += 1
            visit_minute -= 60
        visit_time = f'{visit_hour:02d}:{visit_minute:02d}'
        
        # 生成预约备注（包含预约原因和时间诉求）
        base_reason = random.choice(reasons)
        appointment_reason = f'{base_reason}，{visit_date} {arrival_time} 抵达戒毒所，期望{visit_time} 探访'
        
        # 随机生成1-3个探访人（1个预约人 + 最多2个随行人员）
        visitor_count = random.randint(1, 3)
        
        # 随机生成预约状态：约40%的概率为pending，40%的概率为approved，20%的概率为其他状态
        status_prob = random.random()
        if status_prob < 0.4:
            status = 'pending'
        elif status_prob < 0.8:
            status = 'approved'
        else:
            # 其他状态（rejected, cancelled, queued）
            status = random.choice(['rejected', 'cancelled', 'queued'])
        
        # 创建预约（模拟用户提交预约信息）
        appointment = Appointment.objects.create(
            id=appointment_id,
            user=test_user,
            visitor_name=f'{random.choice(visitor_names)}{i + 1}',
            visitor_gender=random.choice(['男', '女']),
            visitor_id_card=generate_random_id_card(),
            visitor_phone=generate_random_phone(),
            visitor_address=random.choice(addresses),
            prisoner_name=random.choice(prisoner_names),
            relationship=random.choice(relationships),
            appointment_reason=appointment_reason,
            visit_date=visit_date,
            time_slot=None,
            status=status,
            queue_month=None,
            queue_position=0,
            created_at=created_at
        )
        
        # 创建随行亲属信息（包括主探访人）
        for j in range(visitor_count):
            RelativeInfo.objects.create(
                appointment=appointment,
                name=f'{random.choice(visitor_names)}{i + 1}-{j + 1}',
                gender=random.choice(['男', '女']),
                id_card=generate_random_id_card(),
                phone=generate_random_phone(),
                relationship=random.choice(relationships)
            )
        
        if (i + 1) % 50 == 0:
            print(f"已创建 {i + 1} 条预约记录...")
        
        appointment_count += 1
    
    print(f"\n测试数据生成完成！共生成 {appointment_count} 条状态为pending的预约记录")
    print(f"提交时间范围：过去30天内随机分布")
    print(f"探访日期：从2026年探访日列表中随机选择")

if __name__ == '__main__':
    generate_test_appointments()
