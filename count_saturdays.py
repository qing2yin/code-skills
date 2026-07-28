"""
count_saturdays.py - 计算两个日期之间的周六数量

本模块提供计算两个给定日期之间（包含起止日期）共有多少个周六的功能。
使用 Python 标准库 datetime 模块实现，无需第三方依赖。

功能特点：
- 支持任意两个日期之间的周六计数
- 包含起止日期（闭区间）
- 完善的异常处理和输入验证
- 详细的中文注释说明
"""

from datetime import datetime, timedelta


def count_saturdays_between(start_date_str: str, end_date_str: str) -> int:
    """
    计算两个日期之间（包含起止日期）的周六数量。

    该函数接收两个日期字符串，返回这两个日期之间（含首尾）共有多少个星期六。
    使用逐日遍历的方式统计，逻辑清晰易懂。

    Args:
        start_date_str (str): 起始日期字符串，格式为 'YYYY-MM-DD'（如 '2024-01-01'）
        end_date_str (str): 结束日期字符串，格式为 'YYYY-MM-DD'（如 '2024-12-31'）

    Returns:
        int: 起始日期到结束日期之间（包含两端）的周六总数

    Raises:
        ValueError: 当日期格式不正确或起始日期晚于结束日期时抛出异常

    Example:
        >>> count_saturdays_between('2024-01-01', '2024-01-31')
        4  # 2024年1月有4个周六（6、13、20、27日）
    """
    # ========== 第一步：解析并验证输入日期 ==========
    try:
        # 尝试将字符串转换为 datetime 对象，指定格式为 年-月-日
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        # 同样解析结束日期字符串
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError as e:
        # 如果日期格式不符合要求或日期无效（如2024-02-30），抛出明确的异常
        raise ValueError(
            f"日期格式错误，请使用 'YYYY-MM-DD' 格式。"
            f"示例：'2024-01-01'。错误详情：{e}"
        ) from e

    # ========== 第二步：验证日期逻辑顺序 ==========
    if start_date > end_date:
        # 如果起始日期晚于结束日期，这在业务上不合理，抛出异常提示
        raise ValueError(
            f"起始日期 ({start_date_str}) 不能晚于结束日期 ({end_date_str})。"
            f"请确保第一个参数是较早的日期。"
        )

    # ========== 第三步：初始化计数器 ==========
    saturday_count = 0  # 用于累计周六数量的计数器，初始值为0

    # ========== 第四步：逐日遍历日期范围 ==========
    # 从起始日期开始，每次增加一天，直到超过结束日期为止
    current_date = start_date  # 当前遍历到的日期指针，初始指向起始日期
    while current_date <= end_date:  # 当当前日期未超过结束日期时，继续循环
        # datetime 的 weekday() 方法：周一返回0，周二返回1，...，周六返回5，周日返回6
        if current_date.weekday() == 5:  # 判断当前日期是否为周六（weekday == 5）
            saturday_count += 1  # 如果是周六，计数器加1

        # 将当前日期向后移动一天，使用 timedelta(days=1) 表示时间间隔为1天
        current_date += timedelta(days=1)

    # ========== 第五步：返回最终结果 ==========
    return saturday_count  # 返回统计得到的周六总数


def count_saturdays_optimized(start_date_str: str, end_date_str: str) -> int:
    """
    使用优化算法计算两个日期之间的周六数量（数学方法，性能更优）。

    与逐日遍历不同，此函数通过数学计算直接得出结果，
    对于大跨度的日期范围效率显著更高。

    Args:
        start_date_str (str): 起始日期字符串，格式为 'YYYY-MM-DD'
        end_date_str (str): 结束日期字符串，格式为 'YYYY-MM-DD'

    Returns:
        int: 起始日期到结束日期之间（包含两端）的周六总数

    Raises:
        ValueError: 当日期格式不正确或起始日期晚于结束日期时抛出异常

    Algorithm:
        1. 找出从起始日期开始的第一个周六
        2. 找出从结束日期往前回溯的最后一个周六
        3. 计算这两个周六之间的完整周数 + 可能的余数天数
    """
    # ========== 解析并验证输入（与上面函数相同逻辑）==========
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(
            f"日期格式错误，请使用 'YYYY-MM-DD' 格式。错误详情：{e}"
        ) from e

    if start_date > end_date:
        raise ValueError(
            f"起始日期 ({start_date_str}) 不能晚于结束日期 ({end_date_str})。"
        )

    # ========== 数学优化算法核心逻辑 ==========

    # 计算起始日期是星期几（0=周一，5=周六，6=周日）
    start_weekday = start_date.weekday()  # 获取起始日期的星期几

    # 计算从起始日期到最近的一个周六需要多少天
    # 如果起始日期本身就是周六（weekday==5），偏移量为0
    # 如果是周日（weekday==6），偏移量为6（下一天就是周一，再过5天到周六）
    # 其他情况：(5 - start_weekday) % 7 得到到下一个周六的天数
    days_to_first_saturday = (5 - start_weekday) % 7

    # 根据偏移量计算出范围内第一个周六的日期
    first_saturday = start_date + timedelta(days=days_to_first_saturday)

    # 如果第一个周六已经超过了结束日期，说明范围内没有周六
    if first_saturday > end_date:
        return 0  # 直接返回0，无需继续计算

    # 计算从第一个周六到最后一个可能周六之间的总天数
    total_days = (end_date - first_saturday).days  # 日期相减得到 timedelta 对象，取 days 属性

    # 每周有一个周六，所以用总天数除以7得到完整的周数
    # 整数除法 // 自动向下取整
    full_weeks = total_days // 7

    # 周数 + 1（因为第一个周六本身也要算上）
    saturday_count = full_weeks + 1

    return saturday_count  # 返回优化算法计算的周六数量


# ========== 主程序入口（用于命令行测试）==========
if __name__ == "__main__":
    # 以下代码仅在直接运行此脚本时执行，被导入为模块时不执行
    print("=" * 60)
    print("  周六计数器 - 计算两个日期之间的周六数量")
    print("=" * 60)

    try:
        # 示例1：计算2024年1月1日至2024年1月31日的周六数
        start = "2024-01-01"  # 起始日期
        end = "2024-01-31"    # 结束日期
        result = count_saturdays_between(start, end)  # 调用基础版函数
        result_opt = count_saturdays_optimized(start, end)  # 调用优化版函数

        # 输出测试结果
        print(f"\n📅 测试范围：{start} 至 {end}")
        print(f"   基础算法结果：{result} 个周六")
        print(f"   优化算法结果：{result_opt} 个周六")
        print(f"   ✅ 算法一致性验证：{'通过' if result == result_opt else '失败'}")

        # 示例2：跨年测试（2023年到2024年）
        start2 = "2023-12-25"
        end2 = "2024-01-07"
        result2 = count_saturdays_between(start2, end2)

        print(f"\n📅 测试范围：{start2} 至 {end2}")
        print(f"   周六数量：{result2} 个")

        # 示例3：同一天测试（当天就是周六的情况）
        start3 = "2024-01-06"  # 这天是周六
        end3 = "2024-01-06"
        result3 = count_saturdays_between(start3, end3)

        print(f"\n📅 测试范围：{start3} 至 {end3}（同一天，且为周六）")
        print(f"   周六数量：{result3} 个")

        print("\n" + "=" * 60)
        print("  所有测试完成！")
        print("=" * 60)

    except ValueError as e:
        # 捕获并显示验证错误（如日期格式错误、日期顺序错误等）
        print(f"\n❌ 输入错误：{e}")
    except Exception as e:
        # 捕获其他未预期的异常，防止程序崩溃
        print(f"\n❌ 发生未知错误：{e}")
