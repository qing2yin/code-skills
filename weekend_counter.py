"""
周末天数计算模块。

计算两个日期之间的周末天数（周六 + 周日）及完整周末对数。
使用数学公式 O(1) 计算，无需逐日遍历。

Author: 编码者
Date: 2026-07-27
"""

from datetime import date


def count_weekend_days(start: date, end: date) -> int:
    """计算两个日期之间（含首尾）的周末天数。

    周末定义为周六和周日。使用整周数 + 余数分解的数学方法，
    时间复杂度 O(1)，适合任意大跨度日期。

    Args:
        start: 起始日期（含）。
        end: 结束日期（含）。

    Returns:
        周末天数（周六 + 周日的总天数）。

    Raises:
        TypeError: 当参数不是 date 类型时抛出。
        ValueError: 当 start > end 时抛出。

    Examples:
        >>> count_weekend_days(date(2026, 7, 1), date(2026, 7, 31))
        9
        >>> count_weekend_days(date(2026, 7, 4), date(2026, 7, 5))
        2
        >>> count_weekend_days(date(2026, 7, 6), date(2026, 7, 6))
        0
    """
    if not isinstance(start, date):
        raise TypeError(f"start 应为 date 类型，收到 {type(start).__name__}")
    if not isinstance(end, date):
        raise TypeError(f"end 应为 date 类型，收到 {type(end).__name__}")
    if start > end:
        raise ValueError(f"起始日期 {start} 不能晚于结束日期 {end}")

    # 含首尾的总天数
    total_days = (end - start).days + 1

    # 拆分为完整周数和剩余天数
    # 完整周每周固定贡献 2 个周末日
    full_weeks = total_days // 7
    remaining_days = total_days % 7
    weekend_count = full_weeks * 2

    # 处理剩余不足一周的天数：检查每一天是否落在周末
    # weekday() 返回 0(周一) ~ 6(周日)，5=周六 6=周日
    start_weekday = start.weekday()
    for i in range(remaining_days):
        if (start_weekday + i) % 7 >= 5:
            weekend_count += 1

    return weekend_count


def count_complete_weekends(start: date, end: date) -> int:
    """计算两个日期之间完整的周末对数（周六+周日成对计入）。

    一个"完整周末"指范围内同时包含周六及其紧接的周日。
    若范围内只有周六没有周日（或反之），不计为完整周末。

    Args:
        start: 起始日期（含）。
        end: 结束日期（含）。

    Returns:
        完整周末的对数（1 对 = 1 个周六 + 1 个周日）。

    Raises:
        TypeError: 当参数不是 date 类型时抛出。
        ValueError: 当 start > end 时抛出。

    Examples:
        >>> count_complete_weekends(date(2026, 7, 1), date(2026, 7, 31))
        4
        >>> count_complete_weekends(date(2026, 7, 4), date(2026, 7, 5))
        1
        >>> count_complete_weekends(date(2026, 7, 4), date(2026, 7, 4))
        0
    """
    if not isinstance(start, date):
        raise TypeError(f"start 应为 date 类型，收到 {type(start).__name__}")
    if not isinstance(end, date):
        raise TypeError(f"end 应为 date 类型，收到 {type(end).__name__}")
    if start > end:
        raise ValueError(f"起始日期 {start} 不能晚于结束日期 {end}")

    total_days = (end - start).days + 1
    full_weeks = total_days // 7
    remaining_days = total_days % 7

    # 完整周每周贡献 1 个完整周末
    complete = full_weeks

    # 检查剩余天数中是否同时包含周六和周日
    start_weekday = start.weekday()
    has_saturday = False
    has_sunday = False
    for i in range(remaining_days):
        day_weekday = (start_weekday + i) % 7
        if day_weekday == 5:
            has_saturday = True
        elif day_weekday == 6:
            has_sunday = True

    # 只有周六和周日都出现，才算一个完整周末
    if has_saturday and has_sunday:
        complete += 1

    return complete
