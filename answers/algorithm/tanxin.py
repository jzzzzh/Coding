"""贪心算法

总体思路：
- 每一步做当前看起来最优的选择，最终希望得到全局最优
- 关键要先排序，再按规则取舍；正确性通常依赖“交换论证”或题目性质
- 适合局部最优能推出全局最优的问题，不一定总能用

常见信号：区间选择、找零、跳跃、买卖股票累加收益
"""


# 题目：给定每日股价，可多次买卖但最多持有一股，且无手续费，返回最大总利润；每次卖出后才能再次买入。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert max_profit([7, 1, 5, 3, 6, 4]) == 7
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert max_profit([7, 6, 4, 3, 1]) == 0
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert max_profit([]) == 0
def max_profit(prices):
    """变体：买卖股票 II（可多次交易）。

    思路：只要明天比今天贵就今天买明天卖，把所有上涨段利润累加。
    """
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit


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
    """变体：跳跃游戏（能否到达终点）。

    思路：维护当前能到的最远下标 farthest；扫到 i > farthest 说明断掉，无法到达。
    """
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + jump)
    return True


# 题目：给定 start < end 的区间数组，返回使剩余区间互不重叠的最少删除数；端点相接不算重叠。本实现会按结束点原地排序输入。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert erase_overlap_intervals([[1, 2], [2, 3]]) == 0
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert erase_overlap_intervals([]) == 0
def erase_overlap_intervals(intervals):
    """变体：无重叠区间（最少删除）。

    思路：按右端点排序，尽量保留结束早的区间，与下一个冲突就删掉冲突者。
    """
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])
    end = intervals[0][1]
    remove = 0
    for i in range(1, len(intervals)):
        if intervals[i][0] < end:
            remove += 1
        else:
            end = intervals[i][1]
    return remove


# 题目：柠檬水每杯 5 元，顾客依次支付 5、10 或 20 元，初始无零钱，判断是否能依次正确找零。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert lemonade_change([5, 5, 5, 10, 20]) is True
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert lemonade_change([5, 5, 10, 10, 20]) is False
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert lemonade_change([]) is True
def lemonade_change(bills):
    """变体：柠檬水找零。

    思路：优先用大面额找零（有 10 先给 10+5，否则给三个 5），保证小面额尽量留着。
    """
    five = ten = 0
    for bill in bills:
        if bill == 5:
            five += 1
        elif bill == 10:
            if five == 0:
                return False
            five -= 1
            ten += 1
        else:
            if ten > 0 and five > 0:
                ten -= 1
                five -= 1
            elif five >= 3:
                five -= 3
            else:
                return False
    return True
