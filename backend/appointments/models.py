from django.db import models
from users.models import User

class Appointment(models.Model):
    """
    预约模型
    
    存储探访预约的基本信息，包括探访人信息、戒毒人员信息、预约时间和状态等。
    每个预约记录关联到一个用户，一个用户可以有多个预约记录。
    """
    # 预约状态选项
    STATUS_CHOICES = (
        ('pending', '待审核'),     # 刚提交的预约，等待管理员审核
        ('approved', '已批准'),     # 管理员已批准的预约
        ('rejected', '已拒绝'),     # 管理员已拒绝的预约
        ('completed', '已完成'),    # 已完成的探访
        ('cancelled', '已取消'),    # 已取消的预约
        ('queued', '排队中'),       # 在排队等待的预约
    )
    
    # 预约排队相关字段
    queue_month = models.IntegerField(
        verbose_name='预约月份',
        help_text='用户被分配的预约月份，格式为YYYYMM',
        null=True,
        blank=True
    )
    queue_position = models.IntegerField(
        verbose_name='排队位置',
        help_text='在该月份预约中的排队位置',
        default=0
    )
    
    # 关联到用户（预约创建者）
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='appointments',
        verbose_name='预约用户',
        help_text='创建该预约的用户'
    )
    
    # 探访人信息
    visitor_name = models.CharField(
        max_length=50, 
        verbose_name='探访人姓名',
        help_text='实际探访人的姓名'
    )
    visitor_gender = models.CharField(
        max_length=10, 
        verbose_name='性别',
        help_text='探访人性别，如：男、女'
    )
    visitor_id_card = models.CharField(
        max_length=18, 
        verbose_name='身份证号',
        help_text='探访人的身份证号码，用于身份验证'
    )
    visitor_phone = models.CharField(
        max_length=11, 
        verbose_name='联系电话',
        help_text='探访人的手机号码，用于联系'
    )
    visitor_address = models.CharField(
        max_length=200, 
        verbose_name='联系地址',
        help_text='探访人的详细联系地址'
    )
    
    # 戒毒人员信息
    prisoner_name = models.CharField(
        max_length=50, 
        verbose_name='戒毒人员姓名',
        help_text='被探访的戒毒人员姓名'
    )
    relationship = models.CharField(
        max_length=50, 
        verbose_name='与戒毒人员关系',
        help_text='探访人与戒毒人员的关系，如：父母、配偶、子女等'
    )
    appointment_reason = models.TextField(
        verbose_name='预约原因',
        help_text='预约探访的具体原因'
    )
    
    # 预约信息
    appointment_time = models.DateTimeField(
        verbose_name='预约时间',
        help_text='计划探访的日期和时间',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name='状态',
        help_text='预约的当前状态'
    )
    
    # 时间戳
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='创建时间',
        help_text='预约记录的创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='更新时间',
        help_text='预约记录的最后更新时间'
    )
    
    class Meta:
        verbose_name = '预约'
        verbose_name_plural = '预约'
        # 定义表名
        db_table = 'appointments'
        # 按创建时间倒序排列
        ordering = ['-created_at']
    
    def __str__(self):
        """
        返回预约的字符串表示
        格式：探访人姓名 - 戒毒人员姓名 - 预约时间
        """
        return f'{self.visitor_name} - {self.prisoner_name} - {self.appointment_time}'

class RelativeInfo(models.Model):
    """
    亲属信息模型
    
    存储随探访人一同前往的亲属信息。
    每个预约可以关联多个亲属信息记录。
    """
    # 关联到预约
    appointment = models.ForeignKey(
        Appointment, 
        on_delete=models.CASCADE, 
        related_name='relatives',
        verbose_name='关联预约',
        help_text='与该亲属信息关联的预约记录'
    )
    
    # 亲属信息
    name = models.CharField(
        max_length=50, 
        verbose_name='姓名',
        help_text='亲属的姓名'
    )
    gender = models.CharField(
        max_length=10, 
        verbose_name='性别',
        help_text='亲属的性别，如：男、女'
    )
    id_card = models.CharField(
        max_length=18, 
        verbose_name='身份证号',
        help_text='亲属的身份证号码，用于身份验证'
    )
    phone = models.CharField(
        max_length=11, 
        verbose_name='联系电话',
        help_text='亲属的手机号码'
    )
    relationship = models.CharField(
        max_length=50, 
        verbose_name='与戒毒人员关系',
        help_text='该亲属与戒毒人员的关系，如：父母、配偶、子女等'
    )
    
    class Meta:
        verbose_name = '亲属信息'
        verbose_name_plural = '亲属信息'
        # 定义表名
        db_table = 'relative_info'
    
    def __str__(self):
        """
        返回亲属信息的字符串表示
        格式：亲属姓名 - 与戒毒人员关系
        """
        return f'{self.name} - {self.relationship}'

class VisitRecord(models.Model):
    """
    探访记录模型
    
    存储实际探访的记录信息。
    每个预约可以关联多个探访记录（例如多次探访同一个戒毒人员）。
    """
    # 关联到预约
    appointment = models.ForeignKey(
        Appointment, 
        on_delete=models.CASCADE, 
        related_name='visit_records',
        verbose_name='关联预约',
        help_text='与该探访记录关联的预约记录'
    )
    
    # 探访记录信息
    visit_time = models.DateTimeField(
        verbose_name='探访时间',
        help_text='实际探访的日期和时间'
    )
    actual_visitor = models.CharField(
        max_length=50, 
        verbose_name='实际探访人',
        help_text='实际进行探访的人员姓名'
    )
    notes = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='备注',
        help_text='探访过程中的特殊情况或其他需要记录的信息'
    )
    
    class Meta:
        verbose_name = '探访记录'
        verbose_name_plural = '探访记录'
        # 定义表名
        db_table = 'visit_records'
        # 按探访时间倒序排列
        ordering = ['-visit_time']
    
    def __str__(self):
        """
        返回探访记录的字符串表示
        格式：关联预约 - 探访时间
        """
        return f'{self.appointment} - {self.visit_time}'
