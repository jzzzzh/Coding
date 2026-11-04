"""二分查找

总体思路：
- 在有序（或答案具有单调性）的区间上，每次砍掉一半搜索空间
- 核心是写对边界：找精确值、第一个满足、最后一个满足
- 也可对答案二分（如最小容量、最短时间）

常见信号：有序数组查找、边界位置、最小化最大值
"""


def binary_search(nums, target):
    """变体：标准二分查找。

    思路：中间值等于目标返回；偏小查右半，偏大查左半。
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def lower_bound(nums, target):
    """变体：第一个 >= target 的位置（下界）。

    思路：nums[mid] < target 时左边界右移，否则右边界收缩到 mid。
    """
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


def upper_bound(nums, target):
    """变体：第一个 > target 的位置（上界）。

    思路：nums[mid] <= target 时继续往右找，否则收缩右边界。
    """
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left


def search_range(nums, target):
    """变体：查找元素的第一个和最后一个位置。

    思路：用 lower_bound 找起点，upper_bound-1 找终点；不存在则返回 [-1,-1]。
    """
    left = lower_bound(nums, target)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    right = upper_bound(nums, target) - 1
    return [left, right]
