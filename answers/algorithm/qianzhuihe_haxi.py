"""前缀和 & 哈希

总体思路：
- 前缀和：用 O(n) 预处理，把任意区间和变成两次下标访问：sum[l..r] = prefix[r+1] - prefix[l]
- 哈希：用 O(1) 平均查找，把“是否出现过 / 出现几次 / 对应下标”记下来，避免二次枚举

常见信号：连续子数组的和、两数配对、分组去重、集合里查相邻元素
"""

# 题目：给定整数数组，返回长度为 n+1 的前缀和数组，首项为 0，prefix[i] 表示前 i 个元素的和。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert prefix_sum([1, -2, 3]) == [0, 1, -1, 2]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert prefix_sum([]) == [0]
def prefix_sum(nums):
    """变体：构建前缀和。

    思路：prefix[0]=0，prefix[i] 表示前 i 个数的和，方便统一用减法求区间。
    """
    prefix = [0] * (len(nums) + 1)
    for i, num in enumerate(nums):
        prefix[i + 1] = prefix[i] + num
    return prefix


# 题目：给定由 prefix_sum 构造的前缀和及合法闭区间 0 <= left <= right < n，返回原数组该区间的和。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert range_sum([0, 1, -1, 2], 1, 2) == 1
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert range_sum([0, 5], 0, 0) == 5
def range_sum(prefix, left, right):
    """变体：区间和查询。

    思路：有了前缀和后，任意 [left, right] 一次减法即可，适合大量区间询问。
    """
    return prefix[right + 1] - prefix[left]


# 题目：给定整数数组（可含负数和 0）和整数 k，返回和恰好为 k 的非空连续子数组个数。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert subarray_sum_equals_k([1, 1, 1], 2) == 2
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert subarray_sum_equals_k([1, -1, 0], 0) == 3
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert subarray_sum_equals_k([], 0) == 0
def subarray_sum_equals_k(nums, k):
    """变体：和为 k 的连续子数组个数（前缀和 + 哈希）。

    思路：若 prefix[j] - prefix[i] = k，则 [i..j-1] 之和为 k。
    边扫边用哈希统计“之前出现过多少次 prefix-k”。
    """
    count = 0
    prefix = 0
    seen = {0: 1}
    for num in nums:
        prefix += num
        count += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count


# 题目：给定无序整数数组和目标和，返回两个不同位置的下标；无解返回 [-1, -1]，多解时返回任一解。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert two_sum([2, 7, 11, 15], 9) == [0, 1]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert two_sum([3, 3], 6) == [0, 1]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert two_sum([1], 2) == [-1, -1]
def two_sum(nums, target):
    """变体：两数之和（哈希表）。

    思路：遍历时查 target-num 是否已出现；出现则配对成功，否则把当前数和下标存入哈希。
    """
    index_map = {}
    for i, num in enumerate(nums):
        need = target - num
        if need in index_map:
            return [index_map[need], i]
        index_map[num] = i
    return [-1, -1]


# 题目：给定字符串数组，把字符及出现次数相同的字符串分为同一组；组间及组内顺序不作要求。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert sorted(sorted(g) for g in group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])) == [['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert group_anagrams(['', '']) == [['', '']]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert group_anagrams([]) == []
def group_anagrams(strs):
    """变体：字母异位词分组。

    思路：把每个字符串排序后当作哈希 key，相同字母组成的词会落到同一组。
    """
    groups = {}
    for s in strs:
        key = "".join(sorted(s))
        if key not in groups:
            groups[key] = []
        groups[key].append(s)
    return list(groups.values())


# 题目：给定无序整数数组，返回数值连续的最长序列长度；不要求原位置连续，重复值不重复计入。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert longest_consecutive([0, -1, 1, 1]) == 3
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert longest_consecutive([]) == 0
def longest_consecutive(nums):
    """变体：最长连续序列。

    思路：先放进集合；只从“没有 num-1 的起点”开始向后延伸，保证每段只扫一次，整体 O(n)。
    """
    num_set = set(nums)
    best = 0
    for num in num_set:
        if num - 1 not in num_set:
            length = 1
            while num + length in num_set:
                length += 1
            best = max(best, length)
    return best
