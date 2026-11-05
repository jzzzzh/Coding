"""滑动窗口：练习模板

仅使用 Python 内置语法、函数及容器，不导入任何库。
请在 pass 处完成实现；下方注释案例给出输入与预期结果，包含常规及边界情况。
完成后可将对应案例复制到函数外运行；类方法的案例需放在类定义之后运行。
辅助函数和类方法的案例可能依赖同文件中的其他函数或方法。
"""


# 题目：给定整数数组和窗口长度 k，返回长度恰好为 k 的连续子数组的最大和；k <= 0 或 k 超过数组长度时返回 0。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert max_sum_subarray([1, 4, 2, 10, 2, 3, 1, 0, 20], 4) == 24
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert max_sum_subarray([-5, -2, -3], 2) == -5
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert max_sum_subarray([1], 2) == 0
# 测试案例 4（输入见调用参数，预期结果见断言）：
# assert max_sum_subarray([1, 2, 3], -1) == 0
# 测试案例 5（输入见调用参数，预期结果见断言）：
# assert max_sum_subarray([], 0) == 0
def max_sum_subarray(nums, k):
    pass


# 题目：给定字符串，返回不含重复字符的最长连续子串长度。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert length_of_longest_substring('abcabcbb') == 3
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert length_of_longest_substring('bbbbb') == 1
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert length_of_longest_substring('') == 0
def length_of_longest_substring(s):
    pass


# 题目：给定字符串 s、t，返回 s 中覆盖 t 所有字符及其重复次数的最短子串；无解或 t 为空时返回空串，等长时取最早出现的窗口。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert min_window('ADOBECODEBANC', 'ABC') == 'BANC'
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert min_window('aa', 'aa') == 'aa'
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert min_window('a', 'aa') == ''
# 测试案例 4（输入见调用参数，预期结果见断言）：
# assert min_window('abc', '') == ''
# 测试案例 5（输入见调用参数，预期结果见断言）：
# assert min_window('', 'a') == ''
def min_window(s, t):
    pass


# 题目：给定主串 s 和模式串 p，返回 s 中所有与 p 字符计数相同的连续子串起点，允许重叠；p 为空时返回空列表。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert find_anagrams('cbaebabacd', 'abc') == [0, 6]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert find_anagrams('abab', 'ab') == [0, 1, 2]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert find_anagrams('a', 'aa') == []
# 测试案例 4（输入见调用参数，预期结果见断言）：
# assert find_anagrams('abc', '') == []
def find_anagrams(s, p):
    pass
