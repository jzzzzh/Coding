"""快速排序：练习模板

仅使用 Python 内置语法、函数及容器，不导入任何库。
请在 pass 处完成实现；下方注释案例给出输入与预期结果，包含常规及边界情况。
完成后可将对应案例复制到函数外运行；类方法的案例需放在类定义之后运行。
辅助函数和类方法的案例可能依赖同文件中的其他函数或方法。
"""


# 题目：给定可比较元素数组，原地升序排序，并返回原数组对象。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# a = [3, 1, 2, 1]
# assert quick_sort(a) is a
# assert a == [1, 1, 2, 3]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert quick_sort([]) == []
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert quick_sort([-2, 0, -1]) == [-2, -1, 0]
def quick_sort(arr):
    pass


# 题目：对数组闭区间 [left, right] 原地升序排序，区间外保持不变，返回 None；left >= right 时不操作。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# a = [9, 3, 1, 2, 8]
# assert _quick_sort(a, 1, 3) is None
# assert a == [9, 1, 2, 3, 8]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# a = []
# _quick_sort(a, 0, -1)
# assert a == []
def _quick_sort(arr, left, right):
    pass


# 题目：对非空合法闭区间 [left, right] 以最右元素为基准原地划分，返回基准最终下标；左侧元素不大于基准，右侧元素大于基准。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# a = [9, 3, 1, 2, 8]
# p = _partition(a, 1, 3)
# assert p == 2 and a == [9, 1, 2, 3, 8]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# a = [5]
# assert _partition(a, 0, 0) == 0
# assert a == [5]
def _partition(arr, left, right):
    pass
