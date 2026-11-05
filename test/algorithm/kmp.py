"""KMP 字符串匹配：练习模板

仅使用 Python 内置语法、函数及容器，不导入任何库。
请在 pass 处完成实现；下方注释案例给出输入与预期结果，包含常规及边界情况。
完成后可将对应案例复制到函数外运行；类方法的案例需放在类定义之后运行。
辅助函数和类方法的案例可能依赖同文件中的其他函数或方法。
"""


# 题目：给定模式串，返回每个前缀的最长相等真前后缀长度数组；真前后缀不包含整个前缀自身。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert build_next('ababaca') == [0, 0, 1, 2, 3, 0, 1]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert build_next('aaaa') == [0, 1, 2, 3]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert build_next('') == []
def build_next(pattern):
    pass


# 题目：给定主串 text 和模式串 pattern，返回所有匹配起点下标，允许重叠；空模式匹配 0 到 len(text) 的所有位置。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert kmp_search('ababa', 'aba') == [0, 2]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert kmp_search('abc', 'd') == []
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert kmp_search('ab', '') == [0, 1, 2]
def kmp_search(text, pattern):
    pass


# 题目：给定主串和模式串，返回首次匹配的起点下标；不存在返回 -1，空模式返回 0。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert kmp_first('hello', 'll') == 2
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert kmp_first('abc', 'd') == -1
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert kmp_first('', '') == 0
def kmp_first(text, pattern):
    pass
