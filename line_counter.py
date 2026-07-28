"""
文件行数统计工具
================
统计任意文本文件的行数，按类别输出：总行数、空行数、注释行数、代码行数。

支持：
    - 单个文件统计
    - 目录下批量统计（指定扩展名）
    - 自动识别 Python 注释（#）和通用空行

用法：
    python line_counter.py <文件路径或目录路径> [--ext .py .txt]

示例：
    python line_counter.py hello.py                 # 统计单个文件
    python line_counter.py ./src --ext .py .js      # 统计目录下所有 .py 和 .js 文件
"""

import os            # 文件路径操作（os.path.exists, os.path.isdir 等）
import sys           # 命令行参数读取（sys.argv）和退出（sys.exit）
import argparse      # 命令行参数解析器，比手动解析 sys.argv 更规范


def count_lines_in_file(filepath: str) -> dict[str, int] | None:
    """统计单个文件的行数，按类别返回。

    统计项说明：
        - total:  文件总行数（包含空行和注释）
        - blank:  空白行（只有空格/制表符的行）
        - comment: 注释行（以 # 开头的行，仅适用于 Python 风格注释）
        - code:   有效代码行（total - blank - comment）

    Args:
        filepath: 要统计的文件路径（支持相对路径和绝对路径）

    Returns:
        成功时返回字典 {'total': n, 'blank': n, 'comment': n, 'code': n}，
        读取失败时返回 None
    """
    result = {"total": 0, "blank": 0, "comment": 0, "code": 0}  # 初始化计数器

    try:
        with open(filepath, "r", encoding="utf-8") as f:         # 以 UTF-8 编码打开文件
            lines = f.readlines()                                 # 读取所有行到列表
    except FileNotFoundError:                                     # 文件不存在的错误
        print(f"[错误] 文件不存在: {filepath}")
        return None
    except PermissionError:                                       # 无权限读取的错误
        print(f"[错误] 没有读取权限: {filepath}")
        return None
    except UnicodeDecodeError:                                    # 编码不是 UTF-8 的错误
        # 尝试用系统默认编码重新读取
        try:
            with open(filepath, "r", encoding="gbk") as f:       # 中国 Windows 默认 GBK 编码
                lines = f.readlines()
        except Exception as e:                                    # 兜底：其他未知错误
            print(f"[错误] 无法读取文件 {filepath}: {e}")
            return None

    result["total"] = len(lines)                                  # 总行数 = 列表长度

    for line in lines:                                            # 逐行判断
        stripped = line.strip()                                   # 去除行首行尾空白字符

        if stripped == "":                                        # 空行：去除空白后为空字符串
            result["blank"] += 1
        elif stripped.startswith("#"):                             # 注释行：以 # 开头
            result["comment"] += 1
        # 其他行都算有效代码行
        # 注意：行内注释（如 x = 1  # 赋值）不会被单独识别为注释行

    result["code"] = result["total"] - result["blank"] - result["comment"]  # 代码行 = 总行 - 空行 - 注释行

    return result


def collect_files(path: str, extensions: list[str] | None = None) -> list[str]:
    """收集待统计的文件列表。

    如果 path 是文件，直接返回该文件。
    如果 path 是目录，递归收集该目录下所有文件（可选过滤扩展名）。

    Args:
        path: 文件路径或目录路径
        extensions: 需要统计的文件扩展名列表，如 ['.py', '.js']。
                    None 表示统计所有文件。

    Returns:
        符合条件的文件路径列表
    """
    files: list[str] = []                                         # 用于存放收集到的文件路径

    if os.path.isfile(path):                                      # path 是文件
        files.append(path)                                        # 直接加入列表
        return files

    if not os.path.isdir(path):                                   # path 既不是文件也不是目录
        print(f"[错误] 路径不存在或不是有效路径: {path}")
        return files                                              # 返回空列表

    # ---- 递归遍历目录 ----
    for root, dirs, filenames in os.walk(path):                   # os.walk 递归遍历目录树
        for filename in filenames:                                # 遍历当前目录下的所有文件名
            if extensions:                                        # 如果指定了扩展名过滤
                _, ext = os.path.splitext(filename)               # 分离文件名和扩展名，如 ('hello', '.py')
                if ext not in extensions:                         # 扩展名不在过滤列表中
                    continue                                      # 跳过该文件
            filepath = os.path.join(root, filename)               # 拼接完整路径
            files.append(filepath)                                # 加入结果列表

    return files


def print_single_result(filepath: str, stats: dict[str, int]) -> None:
    """打印单个文件的统计结果（格式化输出）。

    Args:
        filepath: 文件路径
        stats: count_lines_in_file 返回的统计字典
    """
    total = stats["total"]                                        # 总行数
    code = stats["code"]                                          # 代码行数
    blank = stats["blank"]                                        # 空行数
    comment = stats["comment"]                                    # 注释行数

    # ---- 计算百分比 ----
    code_pct = (code / total * 100) if total > 0 else 0           # 代码行占比（避免除零）
    comment_pct = (comment / total * 100) if total > 0 else 0     # 注释行占比
    blank_pct = (blank / total * 100) if total > 0 else 0         # 空行占比

    # ---- 输出格式化结果 ----
    print(f"\n{'='*55}")                                           # 顶部分隔线
    print(f"  文件: {filepath}")
    print(f"{'-'*55}")                                             # 次分隔线
    print(f"  总行数:   {total:>6}  (100.0%)")                     # `:>6` 右对齐占6字符
    print(f"  代码行:   {code:>6}  ({code_pct:5.1f}%)")           # `:5.1f` 保留1位小数
    print(f"  注释行:   {comment:>6}  ({comment_pct:5.1f}%)")
    print(f"  空行:     {blank:>6}  ({blank_pct:5.1f}%)")
    print(f"{'='*55}")                                             # 底部分隔线


def print_summary(file_results: list[tuple[str, dict]]) -> None:
    """打印多条统计结果的汇总信息。

    Args:
        file_results: [(文件路径, 统计字典), ...] 的列表
    """
    if len(file_results) == 0:                                    # 没有结果，无需汇总
        return

    if len(file_results) == 1:                                    # 只有一个文件，已在单文件输出中展示
        return

    # ---- 汇总所有文件的统计值 ----
    total_lines = sum(r["total"] for _, r in file_results)        # 所有文件总行数加总
    total_code = sum(r["code"] for _, r in file_results)          # 所有文件代码行加总
    total_blank = sum(r["blank"] for _, r in file_results)        # 所有文件空行加总
    total_comment = sum(r["comment"] for _, r in file_results)    # 所有文件注释行加总

    # ---- 计算汇总百分比 ----
    code_pct = (total_code / total_lines * 100) if total_lines > 0 else 0
    comment_pct = (total_comment / total_lines * 100) if total_lines > 0 else 0
    blank_pct = (total_blank / total_lines * 100) if total_lines > 0 else 0

    # ---- 输出汇总结果 ----
    print(f"\n{'='*55}")
    print(f"  汇总 (共 {len(file_results)} 个文件)")
    print(f"{'-'*55}")
    print(f"  总行数:   {total_lines:>6}  (100.0%)")
    print(f"  代码行:   {total_code:>6}  ({code_pct:5.1f}%)")
    print(f"  注释行:   {total_comment:>6}  ({comment_pct:5.1f}%)")
    print(f"  空行:     {total_blank:>6}  ({blank_pct:5.1f}%)")
    print(f"{'='*55}")


def main() -> None:
    """程序主入口。

    解析命令行参数，收集文件，逐个统计并输出结果和汇总。
    """
    # ---- 创建命令行参数解析器 ----
    parser = argparse.ArgumentParser(
        description="统计文件行数：总行数、空行数、注释行数、代码行数",
        epilog="示例: python line_counter.py test.py --ext .py .txt"
    )

    # 位置参数：必填，要统计的文件或目录路径
    parser.add_argument("path", help="要统计的文件路径或目录路径")

    # 可选参数：多值，指定文件扩展名过滤（仅对目录有效）
    parser.add_argument("--ext", nargs="+", default=None,
                        help="要统计的文件扩展名，如 --ext .py .js .ts")

    args = parser.parse_args()                                    # 解析命令行参数
    target_path = args.path                                       # 获取目标路径
    extensions = args.ext                                         # 获取扩展名过滤列表

    # ---- 收集文件 ----
    files = collect_files(target_path, extensions)                # 根据路径收集文件列表

    if not files:                                                 # 没有找到可统计的文件
        print("[提示] 没有找到可统计的文件")
        sys.exit(0)                                               # 正常退出

    # ---- 逐个统计每个文件 ----
    results: list[tuple[str, dict]] = []                          # 用于汇总，存储 (路径, 统计结果)
    for filepath in files:                                        # 遍历每个文件
        stats = count_lines_in_file(filepath)                     # 统计该文件行数
        if stats is None:                                         # 统计失败（如文件不存在）
            continue                                              # 跳过
        print_single_result(filepath, stats)                      # 打印单文件统计结果
        results.append((filepath, stats))                         # 记录到汇总列表

    # ---- 输出汇总（多文件时） ----
    print_summary(results)                                        # 打印汇总信息


# =============================================================================
# 程序入口：直接运行脚本时执行 main()
# =============================================================================
if __name__ == "__main__":
    main()
