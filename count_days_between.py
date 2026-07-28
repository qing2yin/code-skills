"""
计算两个日期之间相隔天数的模块。

本模块提供一个函数 count_days_between，用于计算两个日期之间相隔的天数，
支持字符串（多种常见格式）和 datetime.date 对象作为输入，并自动处理反向传参与闭区间。
"""

from datetime import date, datetime
from typing import Union


def _parse_date(input_date: Union[str, date, datetime]) -> date:
    """
    将输入统一转换为 datetime.date 对象。

    支持以下输入类型：
        - date 对象：直接返回；
        - datetime 对象：取其 date() 部分；
        - 字符串：尝试多种常见格式解析（见下方 formats 列表）。

    Args:
        input_date: 输入日期，可以是字符串、date 或 datetime 对象。

    Returns:
        datetime.date: 转换后的日期对象。

    Raises:
        ValueError: 当字符串无法被任何已知格式解析时抛出。
        TypeError: 当输入类型不被支持时抛出。
    """
    # 情况 1：输入已经是 date 对象（但不能是 datetime，datetime 是 date 子类需先排除）
    if isinstance(input_date, date) and not isinstance(input_date, datetime):
        return input_date

    # 情况 2：输入是 datetime 对象，取其 date 部分
    if isinstance(input_date, datetime):
        return input_date.date()

    # 情况 3：输入是字符串，尝试多种常见格式解析
    if isinstance(input_date, str):
        # 定义常见日期格式列表，按优先级排序
        formats = [
            "%Y-%m-%d",     # 2026-07-27
            "%Y/%m/%d",     # 2026/07/27
            "%Y%m%d",       # 20260727
            "%Y年%m月%d日",  # 2026年7月27日
            "%d-%m-%Y",     # 27-07-2026
            "%d/%m/%Y",     # 27/07/2026
        ]
        # 遍历所有格式，逐一尝试解析
        for fmt in formats:
            try:
                # 用当前格式解析字符串（strip 去除首尾空白）
                return datetime.strptime(input_date.strip(), fmt).date()
            except ValueError:
                # 当前格式不匹配，继续尝试下一个
                continue
        # 所有格式都失败，抛出带提示信息的异常
        raise ValueError(
            f"无法解析日期字符串 '{input_date}'，"
            f"支持的格式包括：YYYY-MM-DD, YYYY/MM/DD, YYYYMMDD, YYYY年MM月DD日 等"
        )

    # 输入类型不支持，抛出 TypeError
    raise TypeError(
        f"不支持的日期类型：{type(input_date).__name__}，"
        f"请传入字符串或 date/datetime 对象"
    )


def count_days_between(
    start_date: Union[str, date, datetime],
    end_date: Union[str, date, datetime],
    inclusive: bool = False
) -> int:
    """
    计算两个日期之间相隔的天数。

    Args:
        start_date: 起始日期，支持字符串或 date/datetime 对象。
        end_date: 结束日期，支持字符串或 date/datetime 对象。
        inclusive: 是否按闭区间计算（两端都算在内）。
            - False（默认）：开区间，返回 end - start 的差值；
            - True：闭区间，返回 end - start + 1。

    Returns:
        int: 两个日期之间相隔的天数（非负数，反向传参自动取绝对值）。

    Raises:
        ValueError: 日期字符串格式无法解析时抛出。
        TypeError: 输入类型不支持时抛出。

    Examples:
        >>> count_days_between("2026-07-01", "2026-07-27")
        26
        >>> count_days_between("2026-07-27", "2026-07-01")  # 反向传参自动取绝对值
        26
        >>> count_days_between("2026-07-01", "2026-07-01")  # 同一天（开区间）
        0
        >>> count_days_between("2026-07-01", "2026-07-01", inclusive=True)  # 同一天（闭区间）
        1
    """
    # 将两个输入统一解析为 date 对象
    start = _parse_date(start_date)
    end = _parse_date(end_date)

    # 计算日期差值并取绝对值，保证结果为非负数（反向传参也能正确返回）
    delta = abs((end - start).days)

    # 如果要求闭区间（含两端），天数加 1
    if inclusive:
        delta += 1

    return delta


if __name__ == "__main__":
    # ===== 测试用例 =====
    print("=== 测试用例 ===")

    # 用例 1：普通区间，2026-07-01 到 2026-07-27 相差 26 天
    result1 = count_days_between("2026-07-01", "2026-07-27")
    print(f"2026-07-01 ~ 2026-07-27 相差 {result1} 天")  # 预期：26

    # 用例 2：反向传参，自动取绝对值，结果仍为 26
    result2 = count_days_between("2026-07-27", "2026-07-01")
    print(f"2026-07-27 ~ 2026-07-01 相差 {result2} 天（反向）")  # 预期：26

    # 用例 3：同一天，开区间为 0
    result3 = count_days_between("2026-07-01", "2026-07-01")
    print(f"2026-07-01 ~ 2026-07-01 相差 {result3} 天")  # 预期：0

    # 用例 4：同一天，闭区间为 1（两端都算）
    result4 = count_days_between("2026-07-01", "2026-07-01", inclusive=True)
    print(f"2026-07-01 ~ 2026-07-01（含两端）相差 {result4} 天")  # 预期：1

    # 用例 5：跨年长区间，2026 全年
    result5 = count_days_between("2026-01-01", "2026-12-31")
    print(f"2026-01-01 ~ 2026-12-31 相差 {result5} 天")  # 预期：364

    # 用例 6：闰年 2 月，2024-02-28 到 2024-03-01（中间隔着 2-29）
    result6 = count_days_between("2024-02-28", "2024-03-01")
    print(f"2024-02-28 ~ 2024-03-01 相差 {result6} 天（闰年）")  # 预期：2

    # 用例 7：直接传入 date 对象
    result7 = count_days_between(date(2026, 1, 1), date(2026, 1, 11))
    print(f"date 对象 2026-01-01 ~ 2026-01-11 相差 {result7} 天")  # 预期：10

    # 用例 8：闭区间跨年，2026 全年含两端
    result8 = count_days_between("2026-01-01", "2026-12-31", inclusive=True)
    print(f"2026-01-01 ~ 2026-12-31（含两端）相差 {result8} 天")  # 预期：365
