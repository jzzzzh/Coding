"""单调栈

总体思路：
- 栈里保持单调递增或单调递减，用来快速找“左边/右边第一个更大/更小”的元素
- 新元素破坏单调性时，不断弹栈并结算被弹出位置的答案
- 每个下标最多进栈出栈一次，整体 O(n)

常见信号：下一个更大元素、每日温度、柱状图最大矩形、接雨水
"""


# 题目：给定整数数组，对每个位置返回其右侧第一个严格更大的元素值；不存在则为 -1。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert next_greater_element([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert next_greater_element([2, 2]) == [-1, -1]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert next_greater_element([]) == []
def next_greater_element(nums):
    """变体：下一个更大元素。

    思路：维护下标单调递减栈；当前值更大时，弹出栈顶并记录它的下一个更大值。
    """
    n = len(nums)
    result = [-1] * n
    stack = []
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    return result


# 题目：给定每日温度数组，返回每一天距离下一个更暖日的天数；后续不再升温则为 0。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert daily_temperatures([70, 70]) == [0, 0]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert daily_temperatures([]) == []
def daily_temperatures(temperatures):
    """变体：每日温度。

    思路：与“下一个更大”相同，答案记成下标差（几天后升温）。
    """
    n = len(temperatures)
    result = [0] * n
    stack = []
    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)
    return result


# 题目：给定宽度均为 1 的非负柱高数组，返回柱状图中可形成的最大矩形面积。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert largest_rectangle_area([2, 2]) == 4
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert largest_rectangle_area([]) == 0
def largest_rectangle_area(heights):
    """变体：柱状图中最大的矩形。

    思路：单调递增栈找每个柱子左右第一个更矮位置，确定以它为高的最大宽度。
    末尾补 0 强制结算栈中剩余柱子。
    """
    stack = []
    max_area = 0
    heights = heights + [0]
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area


# 题目：给定宽度均为 1 的非负柱高数组，返回降雨后能够接住的总水量。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert trap_rain_water([1, 2, 3]) == 0
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert trap_rain_water([]) == 0
def trap_rain_water(height):
    """变体：接雨水。

    思路：单调递减栈；遇到更高柱子时，弹出凹槽底，用左右边界高度差乘宽度累加雨水。
    """
    stack = []
    water = 0
    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            bottom = stack.pop()
            if not stack:
                break
            left = stack[-1]
            width = i - left - 1
            bounded = min(h, height[left]) - height[bottom]
            water += width * bounded
        stack.append(i)
    return water
