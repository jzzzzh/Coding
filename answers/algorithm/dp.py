"""动态规划 (DP)

总体思路：
- 把大问题拆成有重叠子问题的小问题，用数组记住答案避免重复计算
- 关键三步：定义状态 -> 找转移方程 -> 确定初始值与遍历顺序
- 适合最优值、方案数、能否凑出某状态

常见信号：最优、最多/最少、方案数、背包、序列递推
"""


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
