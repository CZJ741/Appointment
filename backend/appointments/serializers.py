from rest_framework import serializers
from .models import Appointment, RelativeInfo, VisitRecord, Announcement

class RelativeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelativeInfo
        fields = ('name', 'gender', 'id_card', 'phone', 'relationship')
        # 不包含appointment字段，因为它会在保存时自动关联



class VisitRecordSerializer(serializers.ModelSerializer):
    """
    探访记录序列化器，处理探访记录数据的序列化
    """
    class Meta:
        model = VisitRecord
        fields = ('id', 'visit_time', 'actual_visitor', 'notes')
        read_only_fields = ('id',)

class AppointmentSerializer(serializers.ModelSerializer):
    """
    预约序列化器，处理预约数据的序列化和反序列化
    """
    # 嵌套序列化器，用于处理亲属信息
    relatives = RelativeInfoSerializer(many=True, required=False)
    
    # 嵌套序列化器，用于处理探访记录信息
    visit_records = VisitRecordSerializer(many=True, read_only=True)
    
    # 自定义visit_date字段，返回格式化的日期
    visit_date = serializers.DateField(format='%Y-%m-%d', required=False)
    
    # 添加嵌套字段，显示关联的用户信息
    user_info = serializers.SerializerMethodField()
    
    # 添加嵌套字段，显示预约状态的中文描述
    status_text = serializers.SerializerMethodField()
    
    # 添加预约月份的中文显示
    queue_month_text = serializers.SerializerMethodField()
    
    # 添加visitor对象，匹配前端期望的结构
    visitor = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = (
            'id', 'visitor_name', 'visitor_gender', 'visitor_id_card', 
            'visitor_phone', 'visitor_address', 'prisoner_name', 
            'relationship', 'appointment_reason', 
            'status', 'status_text', 'created_at', 'updated_at', 'relatives',
            'queue_month', 'queue_position', 'queue_month_text', 'user_info',
            'visitor', 'time_slot', 'visit_date', 'visit_records', 'approval_notes'
        )
        read_only_fields = ('id', 'status', 'created_at', 'updated_at', 'user')
    
    def create(self, validated_data):
        # 获取当前用户
        user = self.context['request'].user
        # 从validated_data中提取亲属信息
        relatives_data = validated_data.pop('relatives', [])
        # 创建预约记录，关联到当前用户
        appointment = Appointment.objects.create(user=user, **validated_data)
        # 创建亲属信息记录，关联到刚刚创建的预约
        for relative_data in relatives_data:
            RelativeInfo.objects.create(appointment=appointment, **relative_data)
        return appointment
    
    def get_user_info(self, obj):
        """
        获取关联的用户信息
        """
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email,
            'phone': obj.visitor_phone
        }
    
    def get_status_text(self, obj):
        """
        获取预约状态的中文描述
        """
        # 使用字典推导式从STATUS_CHOICES中创建映射
        status_map = dict(Appointment.STATUS_CHOICES)
        return status_map.get(obj.status, obj.status)
    
    def get_queue_month_text(self, obj):
        """
        获取预约月份的中文描述
        """
        if obj.queue_month:
            # 将YYYYMM格式转换为YYYY年MM月
            year = obj.queue_month // 100
            month = obj.queue_month % 100
            return f"{year}年{month}月"
        return None
    
    def get_visitor(self, obj):
        """
        创建visitor对象，包含探访人信息，匹配前端期望的结构
        """
        return {
            'name': obj.visitor_name,
            'gender': obj.visitor_gender,
            'idCard': obj.visitor_id_card,
            'phone': obj.visitor_phone,
            'address': obj.visitor_address,
            'relationship': obj.relationship
        }

class AppointmentListSerializer(serializers.ModelSerializer):
    # 用于列表展示的简化序列化器
    status_text = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = (
            'id', 'visitor_name', 'prisoner_name', 
            'status', 'status_text', 'created_at', 'time_slot', 'visit_date', 'approval_notes'
        )
    
    def get_status_text(self, obj):
        """
        获取预约状态的中文描述
        """
        status_map = dict(Appointment.STATUS_CHOICES)
        return status_map.get(obj.status, obj.status)


class AnnouncementSerializer(serializers.ModelSerializer):
    """
    公告序列化器，处理公告数据的序列化和反序列化
    """
    # 格式化发布时间，创建时可选
    publish_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    
    class Meta:
        model = Announcement
        fields = ('id', 'title', 'publish_time', 'content', 'issuing_authority')
        read_only_fields = ('id',)