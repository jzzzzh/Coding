"""滑动窗口

总体思路：
- 维护一段连续区间 [left, right]，右端扩张纳入元素，左端收缩丢掉元素
- 定长窗口：每次进出一个元素；变长窗口：用条件控制 left 何时右移
- 适合子串/子数组在“连续区间”上的最值、计数问题

常见信号：最长/最短子串、覆盖、异位词、连续和
"""

# 题目：给定整数数组和窗口长度 k，返回长度恰好为 k 的连续子数组的最大和；k <= 0 或 k 超过数组长度时返回 0。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert max_sum_subarray([1, 4, 2, 10, 2, 3, 1, 0, 20], 4) == 24
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert max_sum_subarray([-5, -2, -3], 2) == -5
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert max_sum_subarray([1], 2) == 0
# 测试案例 4（输入见调用参数，预期结果见断言）：
# assert max_sum_subarray([1, 2, 3], -1) == 0
# 测试案例 5（输入见调用参数，预期结果见断言）：
# assert max_sum_subarray([], 0) == 0
def max_sum_subarray(nums, k):
    """变体：定长窗口最大和。

    思路：先算前 k 个和，之后每次加右边、减左边滑出的值。
    """
    if k <= 0 or len(nums) < k:
        return 0
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best


# 题目：给定字符串，返回不含重复字符的最长连续子串长度。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert length_of_longest_substring('abcabcbb') == 3
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert length_of_longest_substring('bbbbb') == 1
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert length_of_longest_substring('') == 0
def length_of_longest_substring(s):
    """变体：无重复字符的最长子串。

    思路：右端扩展；若出现重复，左端一直右移直到窗口内无重复。
    """
    seen = set()
    left = 0
    best = 0
    for right, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best


# 题目：给定字符串 s、t，返回 s 中覆盖 t 所有字符及其重复次数的最短子串；无解或 t 为空时返回空串，等长时取最早出现的窗口。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert min_window('ADOBECODEBANC', 'ABC') == 'BANC'
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert min_window('aa', 'aa') == 'aa'
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert min_window('a', 'aa') == ''
# 测试案例 4（输入见调用参数，预期结果见断言）：
# assert min_window('abc', '') == ''
# 测试案例 5（输入见调用参数，预期结果见断言）：
# assert min_window('', 'a') == ''
def min_window(s, t):
    """变体：最小覆盖子串。

    思路：右端扩展直到覆盖 t；再尽量收缩左端，记录最短合法窗口。
    """
    if not t or len(s) < len(t):
        return ""
    need = {}
    for ch in t:
        need[ch] = need.get(ch, 0) + 1
    missing = len(t)
    left = 0
    start = 0
    best = float("inf")
    for right, ch in enumerate(s):
        if need.get(ch, 0) > 0:
            missing -= 1
        need[ch] = need.get(ch, 0) - 1
        while missing == 0:
            if right - left + 1 < best:
                best = right - left + 1
                start = left
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return "" if best == float("inf") else s[start:start + best]


# 题目：给定主串 s 和模式串 p，返回 s 中所有与 p 字符计数相同的连续子串起点，允许重叠；p 为空时返回空列表。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert find_anagrams('cbaebabacd', 'abc') == [0, 6]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert find_anagrams('abab', 'ab') == [0, 1, 2]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert find_anagrams('a', 'aa') == []
# 测试案例 4（输入见调用参数，预期结果见断言）：
# assert find_anagrams('abc', '') == []
def find_anagrams(s, p):
    """变体：找到字符串中所有字母异位词。

    思路：定长窗口长度为 len(p)，比较窗口字符计数是否与 p 相同。
    """
    if not p or len(s) < len(p):
        return []
    need = {}
    for ch in p:
        need[ch] = need.get(ch, 0) + 1
    window = {}
    result = []
    left = 0
    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if right - left + 1 > len(p):
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        if window == need:
            result.append(left)
    return result
