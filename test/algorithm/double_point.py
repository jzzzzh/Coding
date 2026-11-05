"""双指针：练习模板

仅使用 Python 内置语法、函数及容器，不导入任何库。
请在 pass 处完成实现；下方注释案例给出输入与预期结果，包含常规及边界情况。
完成后可将对应案例复制到函数外运行；类方法的案例需放在类定义之后运行。
辅助函数和类方法的案例可能依赖同文件中的其他函数或方法。
"""


# 题目：给定升序整数数组和目标和，返回两个不同位置的下标 [left, right]（从 0 开始）；无解返回 [-1, -1]，多解时返回任一解。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert two_sum_sorted([2, 7, 11, 15], 9) == [0, 1]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert two_sum_sorted([3, 3], 6) == [0, 1]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert two_sum_sorted([], 1) == [-1, -1]
def two_sum_sorted(nums, target):
    pass


# 题目：给定升序数组，原地去重并返回新长度 k；仅前 k 个元素保证为去重后的升序结果，后续内容不作要求。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# a = [1, 1, 2, 2, 3]
# k = remove_duplicates(a)
# assert k == 3 and a[:k] == [1, 2, 3]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert remove_duplicates([]) == 0
# 测试案例 3（输入见调用参数，预期结果见断言）：
# a = [2, 2]
# assert remove_duplicates(a) == 1 and a[0] == 2
def remove_duplicates(nums):
    pass


# 题目：给定数组，原地将所有 0 移到末尾，保持非零元素的相对顺序，并返回原数组对象。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# a = [0, 1, 0, 3, 12]
# assert move_zeros(a) is a
# assert a == [1, 3, 12, 0, 0]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert move_zeros([0, 0]) == [0, 0]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert move_zeros([]) == []
def move_zeros(nums):
    pass


# 题目：给定字符串，忽略非字母数字字符和大小写后，判断其是否为回文；空字符串或仅含标点时返回 True。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert is_palindrome('A man, a plan, a canal: Panama') is True
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert is_palindrome('race a car') is False
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert is_palindrome('.,') is True
def is_palindrome(s):
    pass


# 题目：给定整数数组，返回所有和为 0 的不重复三元组；三元组内部升序排列。本实现会原地排序输入，答案顺序不作要求。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert sorted(three_sum([-1, 0, 1, 2, -1, -4])) == [[-1, -1, 2], [-1, 0, 1]]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert three_sum([0, 0, 0, 0]) == [[0, 0, 0]]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert three_sum([]) == []
def three_sum(nums):
    pass
