"""
简易计算器模块
==============
一个支持基本四则运算、幂运算和取余运算的命令行交互式计算器。

支持运算符：
    +  加法
    -  减法
    *  乘法
    /  除法（保留 2 位小数）
    ** 幂运算
    %  取余运算

用法：
    直接运行本脚本，按提示输入算式，输入 q 退出。

示例：
    >>> 2 + 3
    2 + 3 = 5
    >>> 5 ** 2
    5 ** 2 = 25.0
"""

import operator  # Python 标准库，提供运算符对应的函数（add, sub, mul 等）


# =============================================================================
# 运算符映射表：将用户输入的字符串映射为 (中文名称, 对应计算函数)
# =============================================================================
OPERATOR_MAP = {
    "+": ("加法", operator.add),        # operator.add(a, b) 等价于 a + b
    "-": ("减法", operator.sub),        # operator.sub(a, b) 等价于 a - b
    "*": ("乘法", operator.mul),        # operator.mul(a, b) 等价于 a * b
    "/": ("除法", operator.truediv),    # operator.truediv(a, b) 等价于 a / b，返回浮点数
    "**": ("幂运算", operator.pow),     # operator.pow(a, b) 等价于 a ** b
    "%": ("取余", operator.mod),        # operator.mod(a, b) 等价于 a % b
}


def parse_expression(user_input: str) -> tuple[float, str, float] | None:
    """解析用户输入的算式字符串，拆分为左操作数、运算符、右操作数。

    支持的输入格式：数字 运算符 数字（中间可有任意空格），例如 "2+3"、"5 ** 2"、"10  %  3"。

    Args:
        user_input: 用户输入的原始字符串（已去除首尾空白）

    Returns:
        成功时返回 (左操作数, 运算符字符串, 右操作数)，解析失败返回 None
    """
    # ---- 第一步：提取运算符 ----
    # 注意：需要先匹配双字符运算符（**），再匹配单字符运算符（*），避免把 ** 误拆成 * 和 *
    found_operator = None  # 记录找到的运算符

    for op_symbol in OPERATOR_MAP:                     # 遍历所有支持的运算符
        if op_symbol in user_input:                     # 检查运算符是否出现在输入中
            found_operator = op_symbol                  # 记录运算符
            break                                       # 找到第一个就停止（运算符按字典插入顺序）

    if found_operator is None:                          # 没找到任何支持的运算符
        print(f"[错误] 未找到合法运算符，支持的运算符：{' '.join(OPERATOR_MAP.keys())}")
        return None                                    # 返回 None 表示解析失败

    # ---- 第二步：按运算符拆分字符串为左右两部分 ----
    parts = user_input.split(found_operator, maxsplit=1)  # 只拆分一次，得到 [左半部分, 右半部分]

    if len(parts) != 2:                                 # 防御性检查，正常情况下不会发生
        print("[错误] 表达式格式不正确，应为：数字 运算符 数字")
        return None

    # ---- 第三步：将字符串转为数字 ----
    left_str = parts[0].strip()                         # 去除左半部分的前后空格
    right_str = parts[1].strip()                        # 去除右半部分的前后空格

    if not left_str or not right_str:                   # 任意一边为空（如 " + 3" 或 "2 + "）
        print("[错误] 操作数不能为空")
        return None

    try:
        left_num = float(left_str)                      # 将左操作数字符串转为浮点数
        right_num = float(right_str)                    # 将右操作数字符串转为浮点数
    except ValueError:                                  # 捕获"无法转为数字"的异常
        print(f"[错误] 无法识别的数字：'{left_str}' 或 '{right_str}'")
        return None

    return (left_num, found_operator, right_num)        # 返回解析结果元组


def calculate(left: float, operator_symbol: str, right: float) -> float | None:
    """根据运算符执行实际计算。

    Args:
        left: 左操作数
        operator_symbol: 运算符字符串（如 "+", "/" 等）
        right: 右操作数

    Returns:
        计算结果（float），出错时返回 None
    """
    op_name, op_func = OPERATOR_MAP[operator_symbol]    # 从映射表取出运算符名称和对应函数

    # ---- 特殊检查：除法 / 取余时，分母不能为零 ----
    if operator_symbol in ("/", "%") and right == 0:     # 仅除法和取余需要检查分母
        print(f"[错误] {op_name}运算中，分母不能为零")
        return None                                     # 返回 None 表示计算出错

    try:
        result = op_func(left, right)                   # 调用 operator 模块的函数执行计算
    except ZeroDivisionError:                            # 幂运算中可能出现 0 的负次方
        print("[错误] 数学错误：0 不能做负指数运算")
        return None
    except OverflowError:                                # 结果超出浮点数范围
        print("[错误] 计算结果溢出")
        return None

    return result                                       # 返回计算结果


def format_result(left: float, operator_symbol: str, right: float, result: float) -> str:
    """将算式和结果格式化为人类可读的输出字符串。

    规则：结果为整数时去掉小数部分；除法结果保留 2 位小数。

    Args:
        left: 左操作数
        operator_symbol: 运算符
        right: 右操作数
        result: 计算结果

    Returns:
        格式化后的字符串，如 "2 + 3 = 5"
    """
    # ---- 格式化左操作数 ----
    left_display = int(left) if left == int(left) else left   # 整数去掉 .0

    # ---- 格式化右操作数 ----
    right_display = int(right) if right == int(right) else right

    # ---- 格式化结果 ----
    # 除法结果保留 2 位小数；幂运算和取余结果可能是浮点数，同样处理
    if operator_symbol == "/":                                  # 除法运算
        result_display = round(result, 2)                       # 保留 2 位小数
    elif result == int(result):                                 # 结果是整数
        result_display = int(result)                            # 去掉 .0
    else:
        result_display = round(result, 4)                       # 一般浮点数保留 4 位

    return f"{left_display} {operator_symbol} {right_display} = {result_display}"


def show_help() -> None:
    """打印使用帮助信息。"""
    print("\n" + "=" * 50)                                      # 分隔线
    print("  简易计算器 — 使用说明")
    print("=" * 50)
    print("  输入格式：数字 运算符 数字")
    print("  支持运算符：")
    for symbol, (name, _) in OPERATOR_MAP.items():              # 遍历运算符映射表
        print(f"    {symbol:<4} {name}")                         # 左对齐显示，占 4 字符宽度
    print("  输入 q 或 quit 退出")
    print("  输入 h 或 help  显示此帮助")
    print("=" * 50 + "\n")


def main() -> None:
    """命令行交互式计算器的主循环函数。

    持续接收用户输入，解析算式、计算结果并输出，直到用户输入 q 退出。
    """
    # ---- 启动提示 ----
    print("\n  简易计算器（输入 h 查看帮助，输入 q 退出）\n")

    # ---- 主循环 ----
    while True:                                                 # 无限循环，直到用户主动退出
        try:
            user_input = input(">>> ").strip()                  # 获取用户输入并去除首尾空格
        except (EOFError, KeyboardInterrupt):                    # 捕获 Ctrl+C 或 Ctrl+D
            print("\n  再见！")
            break                                               # 退出循环

        if not user_input:                                      # 空输入（直接回车），跳过
            continue

        lower_input = user_input.lower()                        # 转为小写，方便匹配命令

        # ---- 处理退出命令 ----
        if lower_input in ("q", "quit", "exit"):                # 匹配退出关键词
            print("  再见！")
            break                                               # 退出循环

        # ---- 处理帮助命令 ----
        if lower_input in ("h", "help"):                        # 匹配帮助关键词
            show_help()                                         # 显示帮助信息
            continue                                            # 回到循环开始，等待下次输入

        # ---- 解析表达式 ----
        parsed = parse_expression(user_input)                   # 调用解析函数
        if parsed is None:                                      # 解析失败
            continue                                            # 跳过本次，等待下次输入

        # ---- 执行计算 ----
        left, op_symbol, right = parsed                         # 解包解析结果
        result = calculate(left, op_symbol, right)              # 调用计算函数

        if result is None:                                      # 计算出错（如分母为 0）
            continue                                            # 跳过，等待下次输入

        # ---- 输出结果 ----
        print(f"  {format_result(left, op_symbol, right, result)}")


# =============================================================================
# 程序入口：直接运行脚本时执行 main()
# 如果作为模块被 import，则不会自动运行
# =============================================================================
if __name__ == "__main__":
    main()
