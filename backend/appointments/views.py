from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db import models
from django.db.models import Q
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentListSerializer
from .utils import get_next_available_visit_date, get_visit_date_for_month
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_appointment(request):
    """
    创建新的预约记录
    用户需要提供探访信息，包括探访人、戒毒人员信息、探访事由等
    系统会自动分配探访月份和排队位置
    """
    try:
        # 从请求中获取用户信息
        user = request.user
        
        # 将用户信息添加到请求数据中
        data = request.data.copy()
        data['user'] = user.id
        
        # 查找可用的预约月份
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month
        
        # 检查用户是否已有未完成的预约
        existing_pending = Appointment.objects.filter(
            user=user,
            status__in=['pending', 'approved', 'queued']
        ).exists()
        
        if existing_pending:
            return Response(
                {'detail': '您已有未完成的预约，请完成或取消现有预约后再创建新的预约'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 寻找可用的月份
        assigned_year = year
        assigned_month_num = month
        
        while True:
            # 计算月份代码 (YYYYMM)
            month_code = assigned_year * 100 + assigned_month_num
            
            # 计算该月份已批准的预约数量
            approved_count = Appointment.objects.filter(
                queue_month=month_code,
                status__in=['approved', 'completed']
            ).count()
            
            # 如果该月份未满，则使用该月份
            if approved_count < 1:  # 每个月份只允许一个预约
                assigned_month = month_code
                # 计算排队位置（在该月份中的位置）
                queue_position = Appointment.objects.filter(
                    queue_month=month_code,
                    status='queued'
                ).count() + 1
                break
            
            # 否则，检查下个月
            assigned_month_num += 1
            if assigned_month_num > 12:
                assigned_month_num = 1
                assigned_year += 1
        
        # 添加排队信息到数据中
        data['queue_month'] = assigned_month
        data['queue_position'] = queue_position
        data['status'] = 'queued' if queue_position > 1 else 'pending'  # 如果是第一个，则直接进入待审核
        
        # 创建序列化器并验证数据
        serializer = AppointmentSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            # 保存预约记录
            appointment = serializer.save()
            
            # 构建返回响应，包含预约月份和预计探访日期
            response_data = serializer.data
            try:
                visit_date = get_visit_date_for_month(assigned_year, assigned_month_num)
                response_data['estimated_visit_date'] = visit_date.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                # 如果无法计算探访日期，记录错误但不中断流程
                response_data['estimated_visit_date'] = None
                response_data['error_detail'] = str(e)
            
            response_data['assigned_month_text'] = f"{assigned_year}年{assigned_month_num}月"
            response_data['message'] = '预约提交成功'
            response_data['appointment_id'] = appointment.id
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_appointments(request):
    """获取我的预约列表接口"""
    try:
        # 获取当前用户的所有预约
        appointments = Appointment.objects.filter(user=request.user).order_by('-created_at')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_appointment_queue(request, appointment_id=None):
    """
    查询预约排队情况
    
    如果提供了appointment_id，则查询该预约的排队情况
    否则查询当前用户所有预约的排队情况
    """
    user = request.user
    
    try:
        if appointment_id:
            # 查询指定预约的排队情况
            appointment = Appointment.objects.get(id=appointment_id, user=user)
            
            if not appointment.queue_month:
                return Response(
                    {'error': '该预约尚未分配探访月份'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 获取该月份的所有预约（按创建时间排序）
            month_appointments = Appointment.objects.filter(
                queue_month=appointment.queue_month
            ).order_by('created_at')
            
            # 计算当前预约在队列中的位置
            queue_position = list(month_appointments).index(appointment) + 1
            
            # 计算已批准的预约数量
            approved_count = Appointment.objects.filter(
                queue_month=appointment.queue_month,
                status='approved'
            ).count()
            
            # 计算该月份的探访日期
            year = appointment.queue_month // 100
            month = appointment.queue_month % 100
            visit_date = get_visit_date_for_month(year, month)
            
            # 构建响应数据
            response_data = {
                'appointment_id': appointment.id,
                'assigned_month': appointment.queue_month,
                'assigned_month_text': f"{year}年{month}月",
                'visit_date': visit_date.strftime('%Y-%m-%d %H:%M:%S'),
                'current_status': appointment.status,
                'status_text': dict(appointment.STATUS_CHOICES).get(appointment.status, appointment.status),
                'queue_position': queue_position,
                'total_in_queue': month_appointments.count(),
                'approved_count': approved_count,
                'estimated_wait_months': 0  # 如果已经分配了月份，可以计算预计等待月数
            }
            
            # 计算预计等待月数
            current_date = datetime.now()
            current_year = current_date.year
            current_month = current_date.month
            current_month_code = current_year * 100 + current_month
            
            if appointment.queue_month > current_month_code:
                wait_months = (appointment.queue_month - current_month_code)
                response_data['estimated_wait_months'] = wait_months // 100 * 12 + wait_months % 100
            
            return Response(response_data)
        else:
            # 查询用户所有预约的排队情况
            user_appointments = Appointment.objects.filter(
                user=user,
                status__in=['pending', 'queued', 'approved']
            ).order_by('queue_month', 'queue_position')
            
            results = []
            for appointment in user_appointments:
                if appointment.queue_month:
                    # 获取该月份的所有预约
                    month_appointments = Appointment.objects.filter(
                        queue_month=appointment.queue_month
                    ).order_by('created_at')
                    
                    # 计算当前预约在队列中的位置
                    queue_position = list(month_appointments).index(appointment) + 1
                    
                    # 计算已批准的预约数量
                    approved_count = Appointment.objects.filter(
                        queue_month=appointment.queue_month,
                        status='approved'
                    ).count()
                    
                    # 计算该月份的探访日期
                    year = appointment.queue_month // 100
                    month = appointment.queue_month % 100
                    visit_date = get_visit_date_for_month(year, month)
                    
                    appointment_data = {
                        'appointment_id': appointment.id,
                        'assigned_month': appointment.queue_month,
                        'assigned_month_text': f"{year}年{month}月",
                        'visit_date': visit_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'current_status': appointment.status,
                        'status_text': dict(appointment.STATUS_CHOICES).get(appointment.status, appointment.status),
                        'queue_position': queue_position,
                        'total_in_queue': month_appointments.count(),
                        'approved_count': approved_count
                    }
                    results.append(appointment_data)
            
            return Response({
                'total_appointments': len(results),
                'appointments': results
            })
    except Appointment.DoesNotExist:
        return Response(
            {'error': '预约记录不存在或无权访问'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_appointments(request):
    """管理员获取所有预约列表接口"""
    try:
        # 简化权限验证，接受任何管理员token或允许无token访问用于测试
        auth_header = request.headers.get('Authorization', '')
        # 检查是否提供了有效token
        if auth_header and auth_header != 'Token admin_mock_token':
            return Response({'error': '无效的token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # 获取所有预约，可以添加过滤参数
        appointments = Appointment.objects.all().order_by('-created_at')
        
        # 处理过滤参数
        status_filter = request.query_params.get('status')
        if status_filter:
            appointments = appointments.filter(status=status_filter)
            
        month_filter = request.query_params.get('month')
        if month_filter:
            # 假设month格式为'2023-05'
            appointments = appointments.filter(appointment_time__year=month_filter[:4], 
                                              appointment_time__month=int(month_filter[5:]))
        
        search = request.query_params.get('search')
        if search:
            appointments = appointments.filter(
                models.Q(visitor_name__icontains=search) | 
                models.Q(prisoner_name__icontains=search) |
                models.Q(id__icontains=search)
            )
        
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_appointment_detail(request, appointment_id):
    """获取单个预约详情接口"""
    try:
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': '预约不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 所有用户均可访问，不需要身份验证
        # 移除权限检查，让已登录用户可以查看所有预约
        
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([AllowAny])
def approve_appointment(request, appointment_id):
    """管理员批准预约接口"""
    try:
        # 所有用户均可访问，不需要身份验证
        
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': '预约不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 检查状态是否为待审核
        if appointment.status != 'pending':
            return Response({'error': '只能批准待审核的预约'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新状态为approved
        old_status = appointment.status
        appointment.status = 'approved'
        
        # 记录请求数据，以便调试
        print(f"批准预约请求数据: {request.data}")
        
        # 获取并处理探访日期 - 这是核心逻辑，必须确保正确执行
        visit_date_str = request.data.get('visit_date')
        if not visit_date_str:
            print("错误: 未提供探访日期(visit_date)")
            return Response({'error': '批准预约时必须提供探访日期'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 确保正确解析探访日期
        from datetime import datetime
        date_formats = ['%Y-%m-%d %H:%M', '%Y-%m-%dT%H:%M', '%Y-%m-%d']
        visit_date = None
        
        for fmt in date_formats:
            try:
                visit_date = datetime.strptime(visit_date_str, fmt)
                print(f"成功解析探访日期: {visit_date}，使用格式: {fmt}")
                break
            except ValueError:
                continue
        
        if not visit_date:
            print(f"错误: 无法解析探访日期格式: {visit_date_str}")
            return Response({'error': '探访日期格式错误，请使用YYYY-MM-DD格式'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查实际探访日期所在月份是否已经有批准的预约
        visit_year = visit_date.year
        visit_month = visit_date.month
        
        print(f"检查月份: {visit_year}年{visit_month}月 是否已有批准的预约")
        # 直接查询数据库中是否有同一月份的已批准预约
        existing_approved = Appointment.objects.filter(
            status='approved',
            appointment_time__isnull=False,  # 确保有探访日期
            appointment_time__year=visit_year,
            appointment_time__month=visit_month
        ).exclude(id=appointment_id).exists()
        
        if existing_approved:
            print(f"月份 {visit_year}年{visit_month}月 已有批准的预约")
            return Response(
                {'error': f'{visit_year}年{visit_month}月的探访日已有批准的预约，每个探访日只能有一个预约'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 核心更新操作：将解析后的日期保存到appointment_time字段
        appointment.appointment_time = visit_date
        print(f"准备保存预约日期: {appointment.appointment_time} 到数据库")
        
        # 保存其他可能的审核信息
        if 'approval_info' in request.data:
            # 可以在这里扩展，保存更多审核相关信息
            pass
        
        # 保存预约对象到数据库
        appointment.save()
        print(f"预约 {appointment_id} 已保存，探访日期: {appointment.appointment_time}")
        
        # 处理排队队列：当一个预约被批准时，如果有排队中的预约，将其状态更新为pending
        if old_status != 'approved' and appointment.queue_month:
            # 查找同一月份的排队预约
            queued_appointments = Appointment.objects.filter(
                queue_month=appointment.queue_month,
                status='queued',
                created_at__gt=appointment.created_at
            ).order_by('created_at')
            
            # 如果有排队的预约，将第一个更新为pending
            if queued_appointments.exists():
                first_queued = queued_appointments.first()
                first_queued.status = 'pending'
                first_queued.save()
                
                # 更新其他预约的排队位置
                for i, queued in enumerate(queued_appointments[1:], start=1):
                    queued.queue_position = i
                    queued.save()
        
        return Response({'message': '预约已批准', 'appointment_id': appointment.id}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"批准预约异常: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([AllowAny])
def reject_appointment(request, appointment_id):
    """管理员拒绝预约接口"""
    try:
        # 所有用户均可访问，不需要身份验证
        
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': '预约不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 检查状态是否为待审核
        if appointment.status != 'pending':
            return Response({'error': '只能拒绝待审核的预约'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新状态
        appointment.status = 'rejected'
        
        # 保存拒绝原因
        if 'reason' in request.data:
            # 这里可以添加一个字段来保存拒绝原因，目前模型中没有此字段
            # appointment.rejection_reason = request.data['reason']
            pass
        
        appointment.save()
        
        return Response({'message': '预约已拒绝', 'appointment_id': appointment.id}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([AllowAny])
def complete_appointment(request, appointment_id):
    """管理员标记预约完成接口"""
    try:
        # 所有用户均可访问，不需要身份验证
        
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': '预约不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 检查状态是否为已批准
        if appointment.status != 'approved':
            return Response({'error': '只能标记已批准的预约为完成'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新状态
        appointment.status = 'completed'
        
        # 保存完成备注
        if 'notes' in request.data:
            # 这里可以创建VisitRecord记录
            from .models import VisitRecord
            VisitRecord.objects.create(
                appointment=appointment,
                visit_time=appointment.appointment_time,
                actual_visitor=appointment.visitor_name,
                notes=request.data['notes']
            )
        
        appointment.save()
        
        return Response({'message': '预约已标记为完成', 'appointment_id': appointment.id}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
