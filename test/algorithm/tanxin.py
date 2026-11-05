"""贪心算法：练习模板

仅使用 Python 内置语法、函数及容器，不导入任何库。
请在 pass 处完成实现；下方注释案例给出输入与预期结果，包含常规及边界情况。
完成后可将对应案例复制到函数外运行；类方法的案例需放在类定义之后运行。
辅助函数和类方法的案例可能依赖同文件中的其他函数或方法。
"""


# 题目：给定每日股价，可多次买卖但最多持有一股，且无手续费，返回最大总利润；每次卖出后才能再次买入。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert max_profit([7, 1, 5, 3, 6, 4]) == 7
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert max_profit([7, 6, 4, 3, 1]) == 0
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert max_profit([]) == 0
def max_profit(prices):
    pass


# 题目：给定非负整数数组，每个值表示从该位置最多能向后跳几步，判断能否从首项到达末项；本实现约定空数组返回 True。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert jump_game([2, 3, 1, 1, 4]) is True
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert jump_game([3, 2, 1, 0, 4]) is False
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert jump_game([0]) is True
# 测试案例 4（输入见调用参数，预期结果见断言）：
# assert jump_game([]) is True
def jump_game(nums):
    pass


# 题目：给定 start < end 的区间数组，返回使剩余区间互不重叠的最少删除数；端点相接不算重叠。本实现会按结束点原地排序输入。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert erase_overlap_intervals([[1, 2], [2, 3]]) == 0
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert erase_overlap_intervals([]) == 0
def erase_overlap_intervals(intervals):
    pass


# 题目：柠檬水每杯 5 元，顾客依次支付 5、10 或 20 元，初始无零钱，判断是否能依次正确找零。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert lemonade_change([5, 5, 5, 10, 20]) is True
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert lemonade_change([5, 5, 10, 10, 20]) is False
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert lemonade_change([]) is True
def lemonade_change(bills):
    pass
