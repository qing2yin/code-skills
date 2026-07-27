"""
判断输入的某年某月某日是这一年的第几天。
"""

def is_leap_year(year: int) -> bool:
    """判断是否为闰年"""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def day_of_year(year: int, month: int, day: int) -> int:
    """计算给定日期是当年的第几天

    Args:
        year: 年份（正整数）
        month: 月份（1-12）
        day: 日（1-31，取决于月份和年份）

    Returns:
        该日期是当年的第几天（1-366）

    Raises:
        ValueError: 当 year、month 或 day 超出有效范围时
    """
    # [AUDIT-FIX] 修复: C2 - day_of_year 函数缺少输入参数校验，
    # 当 month=0/>12、day<1/超范围时会返回错误结果
    if not isinstance(year, int) or year < 1:
        raise ValueError(f"年份必须为正整数，当前值: {year}")
    if not isinstance(month, int) or month < 1 or month > 12:
        raise ValueError(f"月份必须在 1-12 之间，当前值: {month}")

    # 平年每月天数
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # 闰年二月改为29天
    if is_leap_year(year):
        days_in_month[1] = 29

    # [AUDIT-FIX] 修复: C2 - 校验 day 是否在当月有效范围内
    if not isinstance(day, int) or day < 1 or day > days_in_month[month - 1]:
        raise ValueError(f"{year}年{month}月的天数范围为 1-{days_in_month[month - 1]}，当前值: {day}")

    # 累加前 (month - 1) 个月的天数，再加上当前月的 day
    return sum(days_in_month[: month - 1]) + day


def main():
    """主函数：交互式输入日期并计算该日期是当年的第几天"""
    print("=" * 40)
    print("  判断某一天是这一年的第几天")
    print("=" * 40)

    while True:
        try:
            date_str = input("\n请输入日期（格式：年-月-日，如 2026-7-24）：").strip()
            parts = date_str.replace("/", "-").split("-")

            if len(parts) != 3:
                print("格式错误，请按照 年-月-日 的格式输入！")
                continue

            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])

            if month < 1 or month > 12:
                print("月份必须在 1-12 之间！")
                continue

            max_days = [31, 29 if is_leap_year(year) else 28,
                        31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if day < 1 or day > max_days[month - 1]:
                print(f"{year}年{month}月最多只有 {max_days[month - 1]} 天！")
                continue

            result = day_of_year(year, month, day)
            leap_info = "（闰年）" if is_leap_year(year) else "（平年）"
            print(f"\n{year}年{month}月{day}日 是 {year}年 的第 {result} 天 {leap_info}")
            break

        except ValueError:
            print("输入格式有误，请输入数字！")
        except KeyboardInterrupt:
            print("\n\n已退出。")
            break


if __name__ == "__main__":
    main()
