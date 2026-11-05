"""归并排序

总体思路：
- 先把数组对半拆到只剩一个元素，再两两有序合并
- 稳定排序，时间始终 O(n log n)，需要额外 O(n) 空间
- 合并过程天然适合“求逆序对”等统计问题

常见信号：稳定排序、逆序对、多路归并
"""


# 题目：给定可比较元素数组，返回升序排序结果；不修改输入数组。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# a = [3, 1, 2, 1]
# assert merge_sort(a) == [1, 1, 2, 3]
# assert a == [3, 1, 2, 1]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert merge_sort([]) == []
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert merge_sort([-1]) == [-1]
def merge_sort(arr):
    """变体：归并排序主流程。

    思路：分到长度为 1，再把左右有序数组合并成新数组返回。
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


# 题目：给定两个升序数组，合并成一个新的升序数组；相等时先取左侧元素，保持稳定性。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert _merge([1, 3], [2, 3]) == [1, 2, 3, 3]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert _merge([], [1]) == [1]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert _merge([], []) == []
def _merge(left, right):
    """变体：合并两个有序数组。

    思路：双指针每次取较小值；一边耗尽后把另一边剩余直接拼上。
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
