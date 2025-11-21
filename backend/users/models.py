from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    用户模型
    
    扩展Django的AbstractUser模型，用于存储探访预约系统的用户信息。
    继承自AbstractUser，已包含username、password、email、first_name、last_name、
    is_staff、is_active、date_joined等字段。
    """
    # 姓名字段，用于显示用户的真实姓名
    full_name = models.CharField(max_length=100, verbose_name='姓名', help_text='用户的真实姓名')
    
    # 电话号码字段，用于联系用户
    phone_number = models.CharField(max_length=11, verbose_name='电话号码', help_text='用户的手机号码', null=True, blank=True)
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        # 定义表名，默认会使用app_label + '_' + model_name
        db_table = 'users'
    
    def __str__(self):
        """
        返回用户的字符串表示
        格式：用户名 (姓名)
        """
        return f'{self.username} ({self.full_name})'
