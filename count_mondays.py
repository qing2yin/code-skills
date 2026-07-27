"""
计算两个日期之间有多少个周一
================================
算法思路:
  1. 先把日期区间规整为 [start, end] 且 start <= end
  2. 找到 >= start 的第一个周一 (first_monday)
  3. 若 first_monday > end, 说明区间内没有周一, 返回 0
  4. 否则, 区间内的周一数量 = (end - first_monday).days // 7 + 1
     解释: 从 first_monday 起, 每隔 7 天一个周一,
           末项 <= end, 共有 (days // 7 + 1) 个

关键点: datetime.date.weekday() 中, 周一=0, 周二=1, ..., 周日=6
"""

from datetime import date, timedelta


def count_mondays(start: date, end: date) -> int:
    """
    返回 [start, end] 闭区间内有多少个周一 (含两端).

    参数:
        start: 起始日期 (date 对象)
        end:   结束日期 (date 对象)

    返回:
        int: 区间内周一的个数

    说明:
        - 自动处理 start > end 的情况 (会自动交换)
        - 闭区间: 若 start 或 end 本身是周一, 也计入
    """
    # 规整: 保证 start <= end
    if start > end:
        start, end = end, start

    # 找到 >= start 的第一个周一
    # (0 - start.weekday()) % 7 给出"到下一个周一还需几天"
    # 当 start 本身是周一时, weekday()=0, 结果为 0, 第一个周一就是 start
    days_to_monday = (0 - start.weekday()) % 7
    first_monday = start + timedelta(days=days_to_monday)

    # 第一个周一已超出区间, 说明区间内没有周一
    if first_monday > end:
        return 0

    # 从 first_monday 到 end 之间, 每隔 7 天一个周一
    days_between = (end - first_monday).days
    return days_between // 7 + 1


# -------------------------------------------------------------------
# 工具函数: 用字符串日期更方便地调用
# -------------------------------------------------------------------
def count_mondays_str(start_str: str, end_str: str, fmt: str = "%Y-%m-%d") -> int:
    """
    用字符串表示日期, 返回区间内周一的个数.

    示例: count_mondays_str("2026-07-01", "2026-07-31")
    """
    start_date = datetime_str_to_date(start_str, fmt)
    end_date = datetime_str_to_date(end_str, fmt)
    return count_mondays(start_date, end_date)


def datetime_str_to_date(s: str, fmt: str = "%Y-%m-%d") -> date:
    """把 'YYYY-MM-DD' 字符串转成 date 对象."""
    return date(*map(int, s.split("-"))) if "-" in s else date.fromisoformat(s)


# -------------------------------------------------------------------
# 测试用例
# -------------------------------------------------------------------
if __name__ == "__main__":
    # 用例 1: 2026-07-01 (周三) ~ 2026-07-31 (周五)
    # 期间周一为: 07-06, 07-13, 07-20, 07-27  => 共 4 个
    assert count_mondays_str("2026-07-01", "2026-07-31") == 4

    # 用例 2: 起止都是同一个周一, 应为 1
    # 2026-07-06 是周一
    assert count_mondays_str("2026-07-06", "2026-07-06") == 1

    # 用例 3: 区间内没有周一
    # 2026-07-07 (周二) ~ 2026-07-05 (下周一之前的周二), 无周一
    assert count_mondays_str("2026-07-07", "2026-07-12") == 0  # 07-12 是周日

    # 用例 4: 反向传参 (start > end), 自动交换后结果一致
    assert count_mondays_str("2026-07-31", "2026-07-01") == 4

    # 用例 5: 跨年长区间 2026-01-01 (周四) ~ 2026-12-31 (周四)
    # 2026 年共 52 个周一 (2026-01-05 是第一个周一)
    assert count_mondays_str("2026-01-01", "2026-12-31") == 52

    # 用例 6: 起始就是周一 2026-07-06 ~ 2026-07-20, 周一: 06,13,20 => 3
    assert count_mondays_str("2026-07-06", "2026-07-20") == 3

    print("所有测试用例通过!")

    # 演示输出
    examples = [
        ("2026-07-01", "2026-07-31"),
        ("2026-07-06", "2026-07-06"),
        ("2026-07-07", "2026-07-12"),
        ("2026-01-01", "2026-12-31"),
    ]
    print("\n演示:")
    for s, e in examples:
        n = count_mondays_str(s, e)
        print(f"  {s} ~ {e} 之间有 {n} 个周一")
