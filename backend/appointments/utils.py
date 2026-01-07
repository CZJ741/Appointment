from datetime import datetime, timedelta, time
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
        # 返回当天上午9点作为探访开始时间
        return datetime.combine(wednesdays[2], time(9, 0, 0, 0))
    else:
        raise ValueError(f"无法找到{year}年{month}月的第三个星期三")


def get_next_available_visit_date(start_year=None, start_month=None):
    """
    获取下一个可用的探访日期（每月第三个星期三）
    
    参数:
        start_year: 开始查找的年份
        start_month: 开始查找的月份
    
    返回:
        datetime对象: 下一个可用的探访日期
    """
    today = datetime.now()
    if start_year and start_month:
        year = start_year
        month = start_month
    else:
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


def generate_time_slots(visit_date):
    """
    生成指定探访日的所有时间段
    
    参数:
        visit_date: 探访日期（datetime对象）
    
    返回:
        list: 时间段列表，每个元素包含时间段名称、开始时间、结束时间
    """
    # 探访时间段设置
    # 上午9:00-11:30，每30分钟一个时间段
    # 下午14:30-17:00，每30分钟一个时间段
    time_slots = []
    
    # 上午时间段
    start_time = time(9, 0)
    end_time = time(11, 30)
    current_time = datetime.combine(visit_date, start_time)
    end_datetime = datetime.combine(visit_date, end_time)
    
    while current_time < end_datetime:
        slot_start = current_time.time()
        slot_end = (current_time + timedelta(minutes=30)).time()
        slot_name = f"{slot_start.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}"
        time_slots.append({
            'time_slot': slot_name,
            'start_time': slot_start,
            'end_time': slot_end
        })
        current_time += timedelta(minutes=30)
    
    # 下午时间段
    start_time = time(14, 30)
    end_time = time(17, 0)
    current_time = datetime.combine(visit_date, start_time)
    end_datetime = datetime.combine(visit_date, end_time)
    
    while current_time < end_datetime:
        slot_start = current_time.time()
        slot_end = (current_time + timedelta(minutes=30)).time()
        slot_name = f"{slot_start.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}"
        time_slots.append({
            'time_slot': slot_name,
            'start_time': slot_start,
            'end_time': slot_end
        })
        current_time += timedelta(minutes=30)
    
    return time_slots








