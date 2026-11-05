"""二分查找：练习模板

仅使用 Python 内置语法、函数及容器，不导入任何库。
请在 pass 处完成实现；下方注释案例给出输入与预期结果，包含常规及边界情况。
完成后可将对应案例复制到函数外运行；类方法的案例需放在类定义之后运行。
辅助函数和类方法的案例可能依赖同文件中的其他函数或方法。
"""


# 题目：给定升序数组和目标值，返回任一匹配元素的从 0 开始的下标；不存在返回 -1。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert binary_search([1, 3, 5, 7], 5) == 2
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert binary_search([1, 3], 2) == -1
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert binary_search([], 1) == -1
def binary_search(nums, target):
    pass


# 题目：给定升序数组，返回第一个大于等于 target 的位置；不存在则返回数组长度。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert lower_bound([1, 2, 2, 4], 2) == 1
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert lower_bound([1, 2], 3) == 2
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert lower_bound([], 1) == 0
def lower_bound(nums, target):
    pass


# 题目：给定升序数组，返回第一个严格大于 target 的位置；不存在则返回数组长度。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert upper_bound([1, 2, 2, 4], 2) == 3
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert upper_bound([1, 2], 2) == 2
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert upper_bound([], 1) == 0
def upper_bound(nums, target):
    pass


# 题目：给定升序数组和目标值，返回其首次和末次出现的下标 [first, last]；不存在返回 [-1, -1]。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert search_range([1, 2, 2, 2, 4], 2) == [1, 3]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert search_range([1, 3], 2) == [-1, -1]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert search_range([], 1) == [-1, -1]
def search_range(nums, target):
    pass
