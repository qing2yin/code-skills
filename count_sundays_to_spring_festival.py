"""
计算从今天到下一个春节（过年）之间有多少个周日的模块。

本模块提供两个核心函数：
  - get_next_spring_festival：根据内置春节日期表，返回给定日期之后的下一个春节
  - count_sundays_to_spring_festival：计算从今天（或指定起始日）到下一个春节之间的周日数量

算法采用纯数学方式（定位首个周日 + 整周计数），无需逐日遍历，效率为 O(1)。
"""

from datetime import date, timedelta
from typing import Optional


# 农历正月初一（春节）对应的公历日期表（2020-2035）
# 春节是农历节日，公历日期每年不同，无简单公式，故采用查表法
SPRING_FESTIVAL_DATES = {
    2020: date(2020, 1, 25),
    2021: date(2021, 2, 12),
    2022: date(2022, 2, 1),
    2023: date(2023, 1, 22),
    2024: date(2024, 2, 10),
    2025: date(2025, 1, 29),
    2026: date(2026, 2, 17),
    2027: date(2027, 2, 6),
    2028: date(2028, 1, 26),
    2029: date(2029, 2, 13),
    2030: date(2030, 2, 3),
    2031: date(2031, 1, 23),
    2032: date(2032, 2, 11),
    2033: date(2033, 1, 31),
    2034: date(2034, 2, 19),
    2035: date(2035, 2, 8),
}


def get_next_spring_festival(today: Optional[date] = None) -> date:
    """
    根据内置春节日期表，返回给定日期之后的下一个春节日期。

    Args:
        today: 起始日期，默认为系统当前日期。该日期本身若是春节，
               仍视为"已到本年春节"，返回下一年的春节。

    Returns:
        datetime.date: 给定日期之后的下一个春节日期。

    Raises:
        ValueError: 当起始日期超出春节表覆盖范围（2020-2035）时抛出。
    """
    # 未传入起始日期时，使用系统当前日期
    if today is None:
        today = date.today()

    # 遍历春节表（按年份升序），找出第一个严格晚于 today 的春节
    for year in sorted(SPRING_FESTIVAL_DATES.keys()):
        festival = SPRING_FESTIVAL_DATES[year]
        # 严格大于：若 today 本身是春节，返回下一年春节
        if festival > today:
            return festival

    # 超出表覆盖范围，抛出异常提示
    raise ValueError(
        f"起始日期 {today} 超出春节表覆盖范围（2020-2035），"
        f"请在 SPRING_FESTIVAL_DATES 中补充更多年份"
    )


def count_sundays_to_spring_festival(today: Optional[date] = None) -> int:
    """
    计算从今天（或指定起始日）到下一个春节之间有多少个周日。

    采用闭区间 [起始日, 春节] 计数：起始日或春节当天若为周日，也计入。

    Args:
        today: 起始日期，默认为系统当前日期。

    Returns:
        int: 闭区间内的周日数量（非负数）。

    Raises:
        ValueError: 起始日期超出春节表覆盖范围时抛出。

    Examples:
        >>> from datetime import date
        >>> count_sundays_to_spring_festival(date(2026, 7, 27))
        27
    """
    # 确定起始日期（默认今天）
    if today is None:
        today = date.today()

    # 获取下一个春节日期作为区间终点
    spring_festival = get_next_spring_festival(today)

    # 确保区间方向正确（start <= end），此处按逻辑 start 必然 <= end
    start = today
    end = spring_festival
    if start > end:
        start, end = end, start

    # date.weekday() 返回值：周一=0, 周二=1, ..., 周日=6
    # 计算从 start 起到下一个（含当天）周日的天数偏移
    # 若 start 本身是周日（weekday()==6），偏移为 0
    # 公式：(6 - start.weekday()) % 7
    days_to_first_sunday = (6 - start.weekday()) % 7
    first_sunday = start + timedelta(days=days_to_first_sunday)

    # 若首个周日已超出区间终点（即区间内无周日），返回 0
    if first_sunday > end:
        return 0

    # 计算从首个周日到终点之间还有多少个完整的 7 天周期，加上首个周日本身
    # 闭区间计数：+1 把首个周日算进去
    return (end - first_sunday).days // 7 + 1


if __name__ == "__main__":
    # ===== 测试与演示 =====
    print("=== 测试与演示 ===\n")

    # 用例 1：今天（系统当前日期）到下一个春节
    today = date.today()
    next_sf = get_next_spring_festival(today)
    sundays = count_sundays_to_spring_festival(today)
    print(f"今天：{today}（{['周一','周二','周三','周四','周五','周六','周日'][today.weekday()]}）")
    print(f"下一个春节：{next_sf}（{['周一','周二','周三','周四','周五','周六','周日'][next_sf.weekday()]}）")
    print(f"从今天到下一个春节（含两端）共有 {sundays} 个周日\n")

    # 用例 2：固定日期 2026-07-27（周一）到 2027-02-06（春节，周六）
    result2 = count_sundays_to_spring_festival(date(2026, 7, 27))
    print(f"2026-07-27（周一）→ 2027-02-06（春节，周六）：{result2} 个周日")  # 预期：27

    # 用例 3：起始日本身就是周日 —— 2026-08-02 是周日
    result3 = count_sundays_to_spring_festival(date(2026, 8, 2))
    print(f"2026-08-02（周日，起始日为周日）→ 2027-02-06：{result3} 个周日")  # 预期：27

    # 用例 4：春节当天是周日 —— 2028-01-26（春节）是周二，换一个验证
    # 2033-01-31 是周一，区间极短边界用例：起始日就是春节前一天
    # 这里验证"起始日本身就是春节"时应返回下一年春节的周日数
    result4 = count_sundays_to_spring_festival(date(2026, 2, 17))  # 2026 春节当天
    print(f"2026-02-17（2026春节当天）→ 2027-02-06：{result4} 个周日")

    # 用例 5：区间内无周日的极短边界（用 mock 验证逻辑）
    # 2026-07-27（周一）到 2026-07-31（周五），区间内无周日
    # 由于 count_sundays_to_spring_festival 只能算到春节，这里单独测算法
    from datetime import date as _date
    start, end = _date(2026, 7, 27), _date(2026, 7, 31)
    off = (6 - start.weekday()) % 7
    fs = start + timedelta(days=off)
    manual = 0 if fs > end else (end - fs).days // 7 + 1
    print(f"算法自测：2026-07-27 → 2026-07-31（5天，无周日）：{manual} 个周日")  # 预期：0
