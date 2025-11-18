from rest_framework import serializers
from .models import Appointment, RelativeInfo

class RelativeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelativeInfo
        fields = ('name', 'gender', 'id_card', 'phone', 'relationship')
        # 不包含appointment字段，因为它会在保存时自动关联

class AppointmentSerializer(serializers.ModelSerializer):
    # 嵌套序列化器，用于处理亲属信息
    relatives = RelativeInfoSerializer(many=True, required=False)
    
    class Meta:
        model = Appointment
        fields = (
            'id', 'visitor_name', 'visitor_gender', 'visitor_id_card', 
            'visitor_phone', 'visitor_address', 'prisoner_name', 
            'relationship', 'appointment_reason', 'appointment_time', 
            'status', 'created_at', 'updated_at', 'relatives'
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

class AppointmentListSerializer(serializers.ModelSerializer):
    # 用于列表展示的简化序列化器
    class Meta:
        model = Appointment
        fields = (
            'id', 'visitor_name', 'prisoner_name', 'appointment_time', 
            'status', 'created_at'
        )