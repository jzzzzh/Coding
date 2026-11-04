"""双指针

总体思路：
- 用两个下标协同移动，把 O(n^2) 枚举压到 O(n) 或 O(n log n)
- 常见形态：左右指针（相向）、快慢指针（同向）
- 前提常是有序，或“窗口/位置关系”具有单调性

常见信号：有序数组配对、去重、回文、三数之和
"""


def two_sum_sorted(nums, target):
    """变体：有序数组两数之和。

    思路：左右夹逼；和偏小左指针右移，和偏大右指针左移。
    """
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        if s < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]


def remove_duplicates(nums):
    """变体：有序数组原地去重。

    思路：慢指针指向下一个可写位置；快指针扫到新值就写过去。
    """
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1


def move_zeros(nums):
    """变体：移动零。

    思路：慢指针维护“非零区”末尾；快指针遇到非零就与慢指针交换。
    """
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
    return nums


def is_palindrome(s):
    """变体：验证回文串。

    思路：两端向中间走，跳过非字母数字，比较小写后是否相等。
    """
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


def three_sum(nums):
    """变体：三数之和。

    思路：先排序，固定一个数，剩余用左右指针做两数之和，并跳过重复值。
    """
    nums.sort()
    result = []
    n = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, n - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return result
