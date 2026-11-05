"""KMP 字符串匹配

总体思路：
- 朴素匹配失配时主串指针可能回退；KMP 用 next 数组记录模式串自匹配信息
- 失配时模式串跳到 next[j-1]，主串不回退，整体 O(n+m)
- next[i] = 模式串前缀 pattern[0..i] 的最长相等真前后缀长度

常见信号：多处子串匹配、重复子串、字符串周期
"""


# 题目：给定模式串，返回每个前缀的最长相等真前后缀长度数组；真前后缀不包含整个前缀自身。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert build_next('ababaca') == [0, 0, 1, 2, 3, 0, 1]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert build_next('aaaa') == [0, 1, 2, 3]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert build_next('') == []
def build_next(pattern):
    """变体：构建 next 数组。

    思路：i 扫模式串，j 表示当前最长前后缀长度；失配时 j = next[j-1] 回退。
    """
    n = len(pattern)
    nxt = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and pattern[i] != pattern[j]:
            j = nxt[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        nxt[i] = j
    return nxt


# 题目：给定主串 text 和模式串 pattern，返回所有匹配起点下标，允许重叠；空模式匹配 0 到 len(text) 的所有位置。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert kmp_search('ababa', 'aba') == [0, 2]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert kmp_search('abc', 'd') == []
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert kmp_search('ab', '') == [0, 1, 2]
def kmp_search(text, pattern):
    """变体：找出所有匹配位置。

    思路：主串依次比对；失配按 next 跳转；完整匹配后记录起点，再按 next 继续找下一个。
    """
    if not pattern:
        return list(range(len(text) + 1))
    nxt = build_next(pattern)
    result = []
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = nxt[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            result.append(i - j + 1)
            j = nxt[j - 1]
    return result


# 题目：给定主串和模式串，返回首次匹配的起点下标；不存在返回 -1，空模式返回 0。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert kmp_first('hello', 'll') == 2
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert kmp_first('abc', 'd') == -1
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert kmp_first('', '') == 0
def kmp_first(text, pattern):
    """变体：只找第一次出现位置。

    思路：复用全量搜索，取第一个下标；没有匹配返回 -1。
    """
    positions = kmp_search(text, pattern)
    return positions[0] if positions else -1
