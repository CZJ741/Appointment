from datetime import datetime, timedelta
from calendar import Calendar, day_name


def get_third_wednesday(year, month):
    """
    获取指定年份和月份的第三个星期三
    
    参数:
        year: 年份
        month: 月份 (1-12)
    
    返回:
        datetime对象: 第三个星期三的日期和时间
    """
    # 创建日历实例
    cal = Calendar(firstweekday=0)  # 0表示周一为一周的开始
    
    # 获取指定月份的所有日期
    month_days = cal.itermonthdates(year, month)
    
    # 过滤出属于当前月份的星期三（3表示星期三）
    wednesdays = [day for day in month_days 
                 if day.month == month and day.weekday() == 2]
    
    # 返回第三个星期三（索引为2）
    if len(wednesdays) >= 3:
        # 返回当天上午10点作为探访开始时间
        # 使用datetime.combine来替代可能有问题的replace方法
        from datetime import time
        return datetime.combine(wednesdays[2], time(10, 0, 0, 0))
    else:
        raise ValueError(f"无法找到{year}年{month}月的第三个星期三")


def get_next_available_visit_date():
    """
    获取下一个可用的探访日期（每月第三个星期三）
    
    返回:
        datetime对象: 下一个可用的探访日期
    """
    today = datetime.now()
    year = today.year
    month = today.month
    
    # 计算当前月份的第三个星期三
    third_wednesday = get_third_wednesday(year, month)
    
    # 如果当前月份的第三个星期三已经过去，则返回下个月的第三个星期三
    if third_wednesday <= today:
        # 处理跨年度的情况
        month += 1
        if month > 12:
            month = 1
            year += 1
        third_wednesday = get_third_wednesday(year, month)
    
    return third_wednesday


def get_visit_date_for_month(year, month):
    """
    获取指定月份的探访日期（第三个星期三）
    
    参数:
        year: 年份
        month: 月份 (1-12)
    
    返回:
        datetime对象: 该月份的探访日期
    """
    return get_third_wednesday(year, month)