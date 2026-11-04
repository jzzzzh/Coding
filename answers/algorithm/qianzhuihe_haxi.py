"""前缀和 & 哈希

总体思路：
- 前缀和：用 O(n) 预处理，把任意区间和变成两次下标访问：sum[l..r] = prefix[r+1] - prefix[l]
- 哈希：用 O(1) 平均查找，把“是否出现过 / 出现几次 / 对应下标”记下来，避免二次枚举

常见信号：连续子数组的和、两数配对、分组去重、集合里查相邻元素
"""

from collections import defaultdict


def prefix_sum(nums):
    """变体：构建前缀和。

    思路：prefix[0]=0，prefix[i] 表示前 i 个数的和，方便统一用减法求区间。
    """
    prefix = [0] * (len(nums) + 1)
    for i, num in enumerate(nums):
        prefix[i + 1] = prefix[i] + num
    return prefix


def range_sum(prefix, left, right):
    """变体：区间和查询。

    思路：有了前缀和后，任意 [left, right] 一次减法即可，适合大量区间询问。
    """
    return prefix[right + 1] - prefix[left]


def subarray_sum_equals_k(nums, k):
    """变体：和为 k 的连续子数组个数（前缀和 + 哈希）。

    思路：若 prefix[j] - prefix[i] = k，则 [i..j-1] 之和为 k。
    边扫边用哈希统计“之前出现过多少次 prefix-k”。
    """
    count = 0
    prefix = 0
    seen = defaultdict(int)
    seen[0] = 1
    for num in nums:
        prefix += num
        count += seen[prefix - k]
        seen[prefix] += 1
    return count


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


def group_anagrams(strs):
    """变体：字母异位词分组。

    思路：把每个字符串排序后当作哈希 key，相同字母组成的词会落到同一组。
    """
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    return list(groups.values())


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
