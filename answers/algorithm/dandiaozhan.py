"""单调栈

总体思路：
- 栈里保持单调递增或单调递减，用来快速找“左边/右边第一个更大/更小”的元素
- 新元素破坏单调性时，不断弹栈并结算被弹出位置的答案
- 每个下标最多进栈出栈一次，整体 O(n)

常见信号：下一个更大元素、每日温度、柱状图最大矩形、接雨水
"""


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
