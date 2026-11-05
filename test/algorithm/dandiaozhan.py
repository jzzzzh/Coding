"""单调栈：练习模板

仅使用 Python 内置语法、函数及容器，不导入任何库。
请在 pass 处完成实现；下方注释案例给出输入与预期结果，包含常规及边界情况。
完成后可将对应案例复制到函数外运行；类方法的案例需放在类定义之后运行。
辅助函数和类方法的案例可能依赖同文件中的其他函数或方法。
"""


# 题目：给定整数数组，对每个位置返回其右侧第一个严格更大的元素值；不存在则为 -1。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert next_greater_element([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert next_greater_element([2, 2]) == [-1, -1]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert next_greater_element([]) == []
def next_greater_element(nums):
    pass


# 题目：给定每日温度数组，返回每一天距离下一个更暖日的天数；后续不再升温则为 0。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert daily_temperatures([70, 70]) == [0, 0]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert daily_temperatures([]) == []
def daily_temperatures(temperatures):
    pass


# 题目：给定宽度均为 1 的非负柱高数组，返回柱状图中可形成的最大矩形面积。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert largest_rectangle_area([2, 2]) == 4
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert largest_rectangle_area([]) == 0
def largest_rectangle_area(heights):
    pass


# 题目：给定宽度均为 1 的非负柱高数组，返回降雨后能够接住的总水量。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert trap_rain_water([1, 2, 3]) == 0
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert trap_rain_water([]) == 0
def trap_rain_water(height):
    pass
