"""动态规划 (DP)：练习模板

仅使用 Python 内置语法、函数及容器，不导入任何库。
请在 pass 处完成实现；下方注释案例给出输入与预期结果，包含常规及边界情况。
完成后可将对应案例复制到函数外运行；类方法的案例需放在类定义之后运行。
辅助函数和类方法的案例可能依赖同文件中的其他函数或方法。
"""


# 题目：给定非负整数 n，返回斐波那契数 F(n)，其中 F(0)=0、F(1)=1。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert fibonacci(10) == 55
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert fibonacci(0) == 0
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert fibonacci(1) == 1
def fibonacci(n):
    pass


# 题目：每次可爬 1 或 2 阶，给定非负整数 n，返回爬到第 n 阶的方法数；本实现约定 n=0 时返回 0。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert climb_stairs(5) == 8
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert climb_stairs(1) == 1
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert climb_stairs(0) == 0
def climb_stairs(n):
    pass


# 题目：给定等长的正整数重量 weights、非负价值 values 和非负容量 capacity，每件物品最多选一次，返回不超过容量的最大总价值。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert knapsack([1, 3, 4], [15, 20, 30], 4) == 35
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert knapsack([2], [3], 4) == 3
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert knapsack([], [], 5) == 0
# 测试案例 4（输入见调用参数，预期结果见断言）：
# assert knapsack([2], [3], 0) == 0
def knapsack(weights, values, capacity):
    pass


# 题目：给定等长的正整数重量 weights、非负价值 values 和非负容量 W，每种物品可重复选取，返回不超过容量的最大总价值。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert complete_knapsack([1, 3, 4], [15, 20, 30], 4) == 60
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert complete_knapsack([2], [3], 4) == 6
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert complete_knapsack([], [], 5) == 0
# 测试案例 4（输入见调用参数，预期结果见断言）：
# assert complete_knapsack([2], [3], 0) == 0
def complete_knapsack(weights, values, W):
    pass


# 题目：给定整数数组，返回严格递增子序列的最大长度；子序列不要求连续，空数组返回 0。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert longest_increasing_subsequence([2, 2, 2]) == 1
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert longest_increasing_subsequence([]) == 0
def longest_increasing_subsequence(nums):
    pass


# 题目：给定正整数面额 coins 和非负金额 amount，每种硬币可重复使用，返回凑出金额的最少硬币数；无法凑出返回 -1。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert coin_change([1, 2, 5], 11) == 3
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert coin_change([2], 3) == -1
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert coin_change([], 0) == 0
def coin_change(coins, amount):
    pass
