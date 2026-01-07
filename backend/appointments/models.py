from django.db import models
from users.models import User
from datetime import datetime



class Appointment(models.Model):
    """
    预约模型
    
    存储探访预约的基本信息，包括探访人信息、戒毒人员信息、预约时间和状态等。
    每个预约记录关联到一个用户，一个用户可以有多个预约记录。
    """
    # 将id字段改为CharField，用于存储自定义格式的预约号
    id = models.CharField(
        max_length=20,
        primary_key=True,
        verbose_name='预约号',
        help_text='预约号，格式：年+月+当日提交顺序号（例如2025121213）'
    )
    
    # 预约状态选项
    STATUS_CHOICES = (
        ('pending', '待审核'),     # 刚提交的预约，等待管理员审核
        ('approved', '已批准'),     # 管理员已批准的预约
        ('rejected', '已拒绝'),     # 管理员已拒绝的预约
        ('completed', '已完成'),    # 已完成的探访
        ('cancelled', '已取消'),    # 已取消的预约
        ('queued', '排队中'),       # 在排队等待的预约
        ('expired', '已过期'),      # 已过期的预约
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
    visit_date = models.DateField(
        verbose_name='探访日期',
        help_text='探访人指定的探访日期',
        null=True,
        blank=True
    )
    time_slot = models.CharField(
        max_length=20,
        verbose_name='时间段',
        help_text='管理员选择的探访时间段（格式：HH:MM-HH:MM）',
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
    
    # 审核信息
    approval_notes = models.TextField(
        verbose_name='审核备注',
        help_text='管理员审核预约时的备注信息，拒绝预约时为必填项',
        null=True,
        blank=True
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
        格式：探访人姓名 - 戒毒人员姓名 - 探访日期
        """
        return f'{self.visitor_name} - {self.prisoner_name} - {self.visit_date}'
    
    def save(self, *args, **kwargs):
        """
        保存时自动生成预约号
        格式：年+月+日+当日提交顺序号（例如2025121213）
        """
        # 如果是新记录（没有id），生成预约号
        if not self.id:
            # 获取当前时间
            now = datetime.now()
            
            # 计算日期部分（年+月+日）
            date_str = now.strftime('%Y%m%d')
            
            # 获取当天的开始和结束时间
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            # 计算当天已有的预约数量
            today_count = Appointment.objects.filter(
                created_at__range=(today_start, today_end)
            ).count()
            
            # 生成顺序号（当天已有的预约数量 + 1）
            order_number = today_count + 1
            
            # 生成预约号
            self.id = f'{date_str}{order_number}'
        
        # 调用父类的save方法
        super().save(*args, **kwargs)

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


class Announcement(models.Model):
    """
    公告模型
    
    存储系统公告信息，包括标题、发布时间、正文和发布机关等。
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name='公告ID',
        help_text='公告的唯一标识'
    )
    
    title = models.CharField(
        max_length=100,
        verbose_name='公告标题',
        help_text='公告的标题，最多100个字符'
    )
    
    publish_time = models.DateTimeField(
        verbose_name='发布时间',
        help_text='公告的发布时间',
        auto_now_add=True
    )
    
    content = models.TextField(
        verbose_name='公告内容',
        help_text='公告的详细内容'
    )
    
    issuing_authority = models.CharField(
        max_length=50,
        verbose_name='发布机关',
        help_text='发布公告的机关或部门'
    )
    
    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'
        # 定义表名
        db_table = 'announcements'
        # 按发布时间倒序排列
        ordering = ['-publish_time']
    
    def __str__(self):
        """
        返回公告的字符串表示
        格式：公告标题 - 发布时间
        """
        return f'{self.title} - {self.publish_time}'
