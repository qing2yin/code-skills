"""
华氏温度转摄氏温度模块。

使用公式 C = 5 * (F - 32) / 9 进行换算，结果保留两位小数。

Author: 编码者
Date: 2026-07-27
"""


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """将华氏温度转换为摄氏温度，结果保留两位小数。

    换算公式：C = 5 * (F - 32) / 9

    Args:
        fahrenheit: 华氏温度值，可为负数。

    Returns:
        摄氏温度值，四舍五入至两位小数。

    Examples:
        >>> fahrenheit_to_celsius(32)
        0.0
        >>> fahrenheit_to_celsius(212)
        100.0
        >>> fahrenheit_to_celsius(-40)
        -40.0
        >>> fahrenheit_to_celsius(98.6)
        37.0
    """
    # 先计算原始摄氏温度，再统一四舍五入到两位小数
    # round 使用银行家舍入（偶数舍入），对大多数场景足够精确
    celsius = 5 * (fahrenheit - 32) / 9
    return round(celsius, 2)
