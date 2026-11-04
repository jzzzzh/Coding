"""滑动窗口

总体思路：
- 维护一段连续区间 [left, right]，右端扩张纳入元素，左端收缩丢掉元素
- 定长窗口：每次进出一个元素；变长窗口：用条件控制 left 何时右移
- 适合子串/子数组在“连续区间”上的最值、计数问题

常见信号：最长/最短子串、覆盖、异位词、连续和
"""

from collections import defaultdict


def max_sum_subarray(nums, k):
    """变体：定长窗口最大和。

    思路：先算前 k 个和，之后每次加右边、减左边滑出的值。
    """
    if len(nums) < k:
        return 0
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best


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


def min_window(s, t):
    """变体：最小覆盖子串。

    思路：右端扩展直到覆盖 t；再尽量收缩左端，记录最短合法窗口。
    """
    need = defaultdict(int)
    for ch in t:
        need[ch] += 1
    missing = len(t)
    left = 0
    start = 0
    best = float("inf")
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right - left + 1 < best:
                best = right - left + 1
                start = left
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return "" if best == float("inf") else s[start:start + best]


def find_anagrams(s, p):
    """变体：找到字符串中所有字母异位词。

    思路：定长窗口长度为 len(p)，比较窗口字符计数是否与 p 相同。
    """
    if len(s) < len(p):
        return []
    need = defaultdict(int)
    for ch in p:
        need[ch] += 1
    window = defaultdict(int)
    result = []
    left = 0
    for right, ch in enumerate(s):
        window[ch] += 1
        if right - left + 1 > len(p):
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        if window == need:
            result.append(left)
    return result
