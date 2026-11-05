"""双指针

总体思路：
- 用两个下标协同移动，把 O(n^2) 枚举压到 O(n) 或 O(n log n)
- 常见形态：左右指针（相向）、快慢指针（同向）
- 前提常是有序，或“窗口/位置关系”具有单调性

常见信号：有序数组配对、去重、回文、三数之和
"""


# 题目：给定升序整数数组和目标和，返回两个不同位置的下标 [left, right]（从 0 开始）；无解返回 [-1, -1]，多解时返回任一解。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert two_sum_sorted([2, 7, 11, 15], 9) == [0, 1]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert two_sum_sorted([3, 3], 6) == [0, 1]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert two_sum_sorted([], 1) == [-1, -1]
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


# 题目：给定升序数组，原地去重并返回新长度 k；仅前 k 个元素保证为去重后的升序结果，后续内容不作要求。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# a = [1, 1, 2, 2, 3]
# k = remove_duplicates(a)
# assert k == 3 and a[:k] == [1, 2, 3]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert remove_duplicates([]) == 0
# 测试案例 3（输入见调用参数，预期结果见断言）：
# a = [2, 2]
# assert remove_duplicates(a) == 1 and a[0] == 2
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


# 题目：给定数组，原地将所有 0 移到末尾，保持非零元素的相对顺序，并返回原数组对象。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# a = [0, 1, 0, 3, 12]
# assert move_zeros(a) is a
# assert a == [1, 3, 12, 0, 0]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert move_zeros([0, 0]) == [0, 0]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert move_zeros([]) == []
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


# 题目：给定字符串，忽略非字母数字字符和大小写后，判断其是否为回文；空字符串或仅含标点时返回 True。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert is_palindrome('A man, a plan, a canal: Panama') is True
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert is_palindrome('race a car') is False
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert is_palindrome('.,') is True
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


# 题目：给定整数数组，返回所有和为 0 的不重复三元组；三元组内部升序排列。本实现会原地排序输入，答案顺序不作要求。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert sorted(three_sum([-1, 0, 1, 2, -1, -4])) == [[-1, -1, 2], [-1, 0, 1]]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert three_sum([0, 0, 0, 0]) == [[0, 0, 0]]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert three_sum([]) == []
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
