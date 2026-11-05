"""前缀和 & 哈希：练习模板

仅使用 Python 内置语法、函数及容器，不导入任何库。
请在 pass 处完成实现；下方注释案例给出输入与预期结果，包含常规及边界情况。
完成后可将对应案例复制到函数外运行；类方法的案例需放在类定义之后运行。
辅助函数和类方法的案例可能依赖同文件中的其他函数或方法。
"""


# 题目：给定整数数组，返回长度为 n+1 的前缀和数组，首项为 0，prefix[i] 表示前 i 个元素的和。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert prefix_sum([1, -2, 3]) == [0, 1, -1, 2]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert prefix_sum([]) == [0]
def prefix_sum(nums):
    pass


# 题目：给定由 prefix_sum 构造的前缀和及合法闭区间 0 <= left <= right < n，返回原数组该区间的和。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert range_sum([0, 1, -1, 2], 1, 2) == 1
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert range_sum([0, 5], 0, 0) == 5
def range_sum(prefix, left, right):
    pass


# 题目：给定整数数组（可含负数和 0）和整数 k，返回和恰好为 k 的非空连续子数组个数。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert subarray_sum_equals_k([1, 1, 1], 2) == 2
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert subarray_sum_equals_k([1, -1, 0], 0) == 3
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert subarray_sum_equals_k([], 0) == 0
def subarray_sum_equals_k(nums, k):
    pass


# 题目：给定无序整数数组和目标和，返回两个不同位置的下标；无解返回 [-1, -1]，多解时返回任一解。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert two_sum([2, 7, 11, 15], 9) == [0, 1]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert two_sum([3, 3], 6) == [0, 1]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert two_sum([1], 2) == [-1, -1]
def two_sum(nums, target):
    pass


# 题目：给定字符串数组，把字符及出现次数相同的字符串分为同一组；组间及组内顺序不作要求。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert sorted(sorted(g) for g in group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])) == [['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert group_anagrams(['', '']) == [['', '']]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert group_anagrams([]) == []
def group_anagrams(strs):
    pass


# 题目：给定无序整数数组，返回数值连续的最长序列长度；不要求原位置连续，重复值不重复计入。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert longest_consecutive([0, -1, 1, 1]) == 3
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert longest_consecutive([]) == 0
def longest_consecutive(nums):
    pass
