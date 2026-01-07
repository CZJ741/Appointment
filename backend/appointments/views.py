from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db import models
from django.db.models import Q
from .models import Appointment, Announcement
from .serializers import AppointmentSerializer, AppointmentListSerializer, AnnouncementSerializer
from .utils import get_next_available_visit_date, get_visit_date_for_month
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_appointment(request):
    """
    创建新的预约记录
    用户需要提供探访信息，包括探访人、戒毒人员信息、探访事由和探访日期等
    系统会根据用户指定的探访日期分配预约月份和排队位置
    """
    try:
        # 从请求中获取用户信息
        user = request.user
        
        # 将用户信息添加到请求数据中
        data = request.data.copy()
        data['user'] = user.id
        
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
        
        # 从请求数据中获取用户指定的探访日期
        visit_date_str = data.get('visit_date')
        if not visit_date_str:
            return Response(
                {'detail': '请指定探访日期'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 解析探访日期
        try:
            visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
            data['visit_date'] = visit_date
        except ValueError:
            return Response(
                {'detail': '探访日期格式无效，请使用YYYY-MM-DD格式'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查探访日期是否已过期
        if visit_date < datetime.now().date():
            return Response(
                {'detail': '探访日期不能是过去的日期'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 基于探访日期确定预约月份
        assigned_year = visit_date.year
        assigned_month_num = visit_date.month
        month_code = assigned_year * 100 + assigned_month_num
        
        # 计算排队位置（在该月份中的位置）
        queue_position = Appointment.objects.filter(
            queue_month=month_code,
            status='queued'
        ).count() + 1
        
        # 添加排队信息到数据中
        data['queue_month'] = month_code
        data['queue_position'] = queue_position
        data['status'] = 'queued' if queue_position > 1 else 'pending'  # 如果是第一个，则直接进入待审核
        
        # 创建序列化器并验证数据
        serializer = AppointmentSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            # 保存预约记录
            appointment = serializer.save()
            
            # 构建返回响应
            response_data = serializer.data
            response_data['assigned_month_text'] = f"{assigned_year}年{assigned_month_num}月"
            response_data['message'] = '预约提交成功'
            response_data['appointment_id'] = appointment.id
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 公告相关API视图
@api_view(['GET'])
@permission_classes([AllowAny])
def get_announcements(request):
    """
    获取所有公告列表（公开接口，无需登录）
    """
    try:
        # 获取所有公告，按发布时间倒序排列
        announcements = Announcement.objects.all().order_by('-publish_time')
        # 序列化公告数据
        serializer = AnnouncementSerializer(announcements, many=True)
        # 返回序列化后的数据
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_announcement(request):
    """
    创建新公告（需要登录）
    """
    
    try:
        # 序列化请求数据
        serializer = AnnouncementSerializer(data=request.data)
        # 验证数据是否有效
        if serializer.is_valid():
            # 保存公告
            serializer.save()
            # 返回成功响应
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 返回验证错误
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_announcement(request, pk):
    """
    更新公告（需要登录）
    """
    try:
        # 获取要更新的公告
        announcement = Announcement.objects.get(pk=pk)
        # 序列化请求数据
        serializer = AnnouncementSerializer(announcement, data=request.data)
        # 验证数据是否有效
        if serializer.is_valid():
            # 保存更新后的公告
            serializer.save()
            # 返回成功响应
            return Response(serializer.data, status=status.HTTP_200_OK)
        # 返回验证错误
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Announcement.DoesNotExist:
        return Response({'error': '公告不存在'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_announcement(request, pk):
    """
    删除公告（需要登录）
    """
    try:
        # 获取要删除的公告
        announcement = Announcement.objects.get(pk=pk)
        # 删除公告
        announcement.delete()
        # 返回成功响应
        return Response({'message': '公告删除成功'}, status=status.HTTP_204_NO_CONTENT)
    except Announcement.DoesNotExist:
        return Response({'error': '公告不存在'}, status=status.HTTP_404_NOT_FOUND)
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
@permission_classes([IsAuthenticated])
def get_all_appointments(request):
    """
    管理员获取所有预约列表接口
    """
    try:
        # 检查用户是否是管理员
        if not request.user.is_staff:
            return Response({'error': '权限不足，只有管理员可以访问此接口'}, status=status.HTTP_403_FORBIDDEN)
        
        # 获取所有预约，可以添加过滤参数
        appointments = Appointment.objects.all().order_by('-created_at')
        
        # 处理过滤参数
        status_filter = request.query_params.get('status')
        if status_filter:
            appointments = appointments.filter(status=status_filter)
            
        month_filter = request.query_params.get('month')
        if month_filter:
            # 假设month格式为'2023-05'
            appointments = appointments.filter(visit_date__year=month_filter[:4], 
                                              visit_date__month=int(month_filter[5:]))
        
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
@permission_classes([IsAuthenticated])
def get_appointment_detail(request, appointment_id):
    """获取单个预约详情接口"""
    try:
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': '预约不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 检查用户是否有权限访问该预约：只有管理员或预约所有者可以访问
        if not request.user.is_staff and request.user != appointment.user:
            return Response({'error': '权限不足，您只能查看自己的预约详情'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def approve_appointment(request, appointment_id):
    """
    管理员批准预约接口
    """
    try:
        # 检查用户是否是管理员
        if not request.user.is_staff:
            return Response({'error': '权限不足，只有管理员可以访问此接口'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': '预约不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 检查状态是否为待审核
        if appointment.status != 'pending':
            return Response({'error': '只能批准待审核的预约'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 记录请求数据，以便调试
        print(f"批准预约请求数据: {request.data}")
        
        # 获取管理员选择的时间段
        time_slot_str = request.data.get('time_slot')
        if not time_slot_str:
            return Response({'error': '请选择探访时间段'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证时间段格式（HH:MM-HH:MM）
        import re
        time_slot_pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]-([01]?[0-9]|2[0-3]):[0-5][0-9]$'
        if not re.match(time_slot_pattern, time_slot_str):
            return Response({'error': '时间段格式无效，请使用HH:MM-HH:MM格式'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查探访日期是否已由用户指定
        if not appointment.visit_date:
            return Response({'error': '探访日期尚未指定，请确保用户已选择探访日期'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新状态为approved
        old_status = appointment.status
        appointment.status = 'approved'
        
        # 保存时间段
        appointment.time_slot = time_slot_str
        
        # 保存审核信息
        if 'approval_notes' in request.data and request.data['approval_notes']:
            appointment.approval_notes = request.data['approval_notes'].strip()
        
        # 保存预约对象到数据库
        appointment.save()
        print(f"预约 {appointment_id} 已保存，探访日期: {appointment.visit_date}，时间段: {appointment.time_slot}")
        
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
        
        return Response({
            'message': '预约已批准', 
            'appointment_id': appointment.id,
            'visit_date': appointment.visit_date.strftime('%Y-%m-%d'),
            'time_slot': appointment.time_slot
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"批准预约异常: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reject_appointment(request, appointment_id):
    """
    管理员拒绝预约接口
    """
    try:
        # 检查用户是否是管理员
        if not request.user.is_staff:
            return Response({'error': '权限不足，只有管理员可以访问此接口'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': '预约不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 检查状态是否为待审核
        if appointment.status != 'pending':
            return Response({'error': '只能拒绝待审核的预约'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取审核备注
        approval_notes = request.data.get('approval_notes')
        if not approval_notes or not approval_notes.strip():
            return Response({'error': '拒绝预约时必须填写审核备注'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新状态和审核备注
        appointment.status = 'rejected'
        appointment.approval_notes = approval_notes.strip()
        
        appointment.save()
        
        # 处理排队队列：当一个预约被拒绝时，如果有排队中的预约，将其状态更新为pending
        if appointment.queue_month:
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
        
        return Response({'message': '预约已拒绝', 'appointment_id': appointment.id}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def complete_appointment(request, appointment_id):
    """
    管理员标记预约完成接口
    """
    try:
        # 检查用户是否是管理员
        if not request.user.is_staff:
            return Response({'error': '权限不足，只有管理员可以访问此接口'}, status=status.HTTP_403_FORBIDDEN)
        
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
            from datetime import datetime, time
            from django.utils.timezone import make_aware
            
            # 使用visit_date和time_slot创建visit_time
            visit_time = None
            if appointment.visit_date and appointment.time_slot:
                start_time_str = appointment.time_slot.split('-')[0]
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                visit_time = make_aware(datetime.combine(appointment.visit_date, start_time))
            
            VisitRecord.objects.create(
                appointment=appointment,
                visit_time=visit_time,
                actual_visitor=appointment.visitor_name,
                notes=request.data['notes']
            )
        
        appointment.save()
        
        return Response({'message': '预约已标记为完成', 'appointment_id': appointment.id}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def batch_review_appointments(request):
    """
    管理员批量审核预约接口
    
    请求参数格式：
    {
        "appointments": [
            {
                "id": "appointment_id_1",
                "status": "approved",
                "time_slot": "09:00-10:00",
                "approval_notes": "审核通过备注（可选）"
            },
            {
                "id": "appointment_id_2",
                "status": "rejected",
                "approval_notes": "拒绝原因（必填）"
            }
        ]
    }
    """
    try:
        # 检查用户是否是管理员
        if not request.user.is_staff:
            return Response({'error': '权限不足，只有管理员可以访问此接口'}, status=status.HTTP_403_FORBIDDEN)
        
        # 获取请求数据
        data = request.data
        if 'appointments' not in data or not isinstance(data['appointments'], list):
            return Response({'error': '请求格式错误，缺少appointments数组'}, status=status.HTTP_400_BAD_REQUEST)
        
        appointments_to_process = data['appointments']
        if not appointments_to_process:
            return Response({'error': '请选择要审核的预约'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 时间段格式验证正则
        import re
        time_slot_pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]-([01]?[0-9]|2[0-3]):[0-5][0-9]$'
        
        # 处理每个预约
        results = []
        processed_appointments = []
        
        for appointment_data in appointments_to_process:
            appointment_id = appointment_data.get('id')
            review_status = appointment_data.get('status')
            approval_notes = appointment_data.get('approval_notes')
            time_slot_str = appointment_data.get('time_slot')
            
            try:
                # 获取预约对象
                appointment = Appointment.objects.get(id=appointment_id)
                
                # 检查预约状态
                if appointment.status != 'pending':
                    results.append({
                        'id': appointment_id,
                        'status': 'error',
                        'message': '只能审核待审核状态的预约'
                    })
                    continue
                
                # 验证状态
                if review_status not in ['approved', 'rejected']:
                    results.append({
                        'id': appointment_id,
                        'status': 'error',
                        'message': '状态必须是approved或rejected'
                    })
                    continue
                
                # 拒绝时必须填写审核备注
                if review_status == 'rejected':
                    if not approval_notes or not approval_notes.strip():
                        results.append({
                            'id': appointment_id,
                            'status': 'error',
                            'message': '拒绝预约时必须填写审核备注'
                        })
                        continue
                
                # 批准时必须选择时间段
                if review_status == 'approved':
                    if not time_slot_str:
                        results.append({
                            'id': appointment_id,
                            'status': 'error',
                            'message': '批准预约时必须选择时间段'
                        })
                        continue
                    
                    # 验证时间段格式
                    if not re.match(time_slot_pattern, time_slot_str):
                        results.append({
                            'id': appointment_id,
                            'status': 'error',
                            'message': '时间段格式无效，请使用HH:MM-HH:MM格式'
                        })
                        continue
                    
                    # 检查探访日期是否已由用户指定
                    if not appointment.visit_date:
                        results.append({
                            'id': appointment_id,
                            'status': 'error',
                            'message': '探访日期尚未指定，请确保用户已选择探访日期'
                        })
                        continue
                
                # 处理审核
                old_status = appointment.status
                appointment.status = review_status
                
                # 保存审核备注
                if approval_notes:
                    appointment.approval_notes = approval_notes.strip()
                
                # 批准时保存时间段
                if review_status == 'approved':
                    appointment.time_slot = time_slot_str
                
                appointment.save()
                processed_appointments.append(appointment)
                
                results.append({
                    'id': appointment_id,
                    'status': 'success',
                    'message': f'预约已{"批准" if review_status == "approved" else "拒绝"}'
                })
                
            except Appointment.DoesNotExist:
                results.append({
                    'id': appointment_id,
                    'status': 'error',
                    'message': '预约不存在'
                })
            except Exception as e:
                results.append({
                    'id': appointment_id,
                    'status': 'error',
                    'message': str(e)
                })
        
        # 处理排队队列：更新相关预约的状态和排队位置
        for appointment in processed_appointments:
            if appointment.queue_month:
                # 获取同一月份的所有预约
                month_appointments = Appointment.objects.filter(
                    queue_month=appointment.queue_month
                ).order_by('created_at')
                
                # 更新状态和排队位置
                for i, appt in enumerate(month_appointments):
                    if appt.status == 'pending' and i > 0:
                        appt.status = 'queued'
                    appt.queue_position = i + 1
                    appt.save()
        
        return Response({
            'results': results,
            'message': '批量审核完成'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_visit_date_stats(request):
    """
    获取每个探访日的预约批次数统计
    
    返回格式：
    {
        "visit_date": "2026-01-14",
        "count": 5
    }
    """
    try:
        from django.db.models import Count
        
        # 按探访日期分组统计预约数量
        stats = Appointment.objects.values('visit_date').annotate(
            count=Count('id')
        ).order_by('visit_date')
        
        # 转换为字典格式，方便前端查询
        result = {str(item['visit_date']): item['count'] for item in stats}
        
        return Response(result, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
