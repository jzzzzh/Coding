"""动态规划 (DP)

总体思路：
- 把大问题拆成有重叠子问题的小问题，用数组记住答案避免重复计算
- 关键三步：定义状态 -> 找转移方程 -> 确定初始值与遍历顺序
- 适合最优值、方案数、能否凑出某状态

常见信号：最优、最多/最少、方案数、背包、序列递推
"""


# 题目：给定非负整数 n，返回斐波那契数 F(n)，其中 F(0)=0、F(1)=1。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert fibonacci(10) == 55
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert fibonacci(0) == 0
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert fibonacci(1) == 1
def fibonacci(n):
    """变体：斐波那契（最基础递推）。

    思路：dp[i] = dp[i-1] + dp[i-2]，滚动两个变量即可 O(1) 空间。
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# 题目：每次可爬 1 或 2 阶，给定非负整数 n，返回爬到第 n 阶的方法数；本实现约定 n=0 时返回 0。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert climb_stairs(5) == 8
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert climb_stairs(1) == 1
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert climb_stairs(0) == 0
def climb_stairs(n):
    """变体：爬楼梯。

    思路：到第 n 阶只能从 n-1 或 n-2 上来，转移同斐波那契。
    """
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


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
    """变体：0-1 背包。

    思路：每个物品只能选一次；倒序更新容量，保证同一物品不会被重复使用。
    dp[w] = 容量为 w 时的最大价值。
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    for i in range(n):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]


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
    """变体：完全背包。

    思路：每种物品可以重复选取；正序更新容量，使当前物品可被再次使用。
    dp[w] = 容量为 w 时的最大价值。
    """
    n = len(weights)

    dp = [0] * (W + 1)

    for i in range(n):
        for j in range(weights[i], W + 1):
            dp[j] = max(
                dp[j],
                dp[j - weights[i]] + values[i]
            )

    return dp[W]


# 题目：给定整数数组，返回严格递增子序列的最大长度；子序列不要求连续，空数组返回 0。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert longest_increasing_subsequence([2, 2, 2]) == 1
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert longest_increasing_subsequence([]) == 0
def longest_increasing_subsequence(nums):
    """变体：最长递增子序列 (LIS)。

    思路：dp[i] 表示以 nums[i] 结尾的 LIS 长度；
    枚举前面更小的 j，取 max(dp[j])+1。
    """
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


# 题目：给定正整数面额 coins 和非负金额 amount，每种硬币可重复使用，返回凑出金额的最少硬币数；无法凑出返回 -1。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert coin_change([1, 2, 5], 11) == 3
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert coin_change([2], 3) == -1
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert coin_change([], 0) == 0
def coin_change(coins, amount):
    """变体：零钱兑换（完全背包求最少个数）。

    思路：dp[x] = 凑出金额 x 的最少硬币数；硬币可重复用，容量正向遍历。
    """
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != float("inf") else -1
