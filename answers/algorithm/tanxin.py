"""贪心算法

总体思路：
- 每一步做当前看起来最优的选择，最终希望得到全局最优
- 关键要先排序，再按规则取舍；正确性通常依赖“交换论证”或题目性质
- 适合局部最优能推出全局最优的问题，不一定总能用

常见信号：区间选择、找零、跳跃、买卖股票累加收益
"""


def max_profit(prices):
    """变体：买卖股票 II（可多次交易）。

    思路：只要明天比今天贵就今天买明天卖，把所有上涨段利润累加。
    """
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit


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
