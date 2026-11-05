"""快速排序

总体思路：
- 选一个基准 pivot，把数组分成“小于等于 pivot”和“大于 pivot”两段
- 再对左右两段递归排序（分治）
- 平均 O(n log n)，最坏 O(n^2)；可原地排序

常见信号：原地排序、快速选择第 K 大（partition 思想同源）
"""


# 题目：给定可比较元素数组，原地升序排序，并返回原数组对象。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# a = [3, 1, 2, 1]
# assert quick_sort(a) is a
# assert a == [1, 1, 2, 3]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert quick_sort([]) == []
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert quick_sort([-2, 0, -1]) == [-2, -1, 0]
def quick_sort(arr):
    """变体：原地快速排序入口。

    思路：对整个区间做 partition + 递归，直接修改原数组。
    """
    _quick_sort(arr, 0, len(arr) - 1)
    return arr


# 题目：对数组闭区间 [left, right] 原地升序排序，区间外保持不变，返回 None；left >= right 时不操作。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# a = [9, 3, 1, 2, 8]
# assert _quick_sort(a, 1, 3) is None
# assert a == [9, 1, 2, 3, 8]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# a = []
# _quick_sort(a, 0, -1)
# assert a == []
def _quick_sort(arr, left, right):
    """变体：区间递归排序。

    思路：区间长度 <= 1 结束；否则划分后分别处理左右子区间。
    """
    if left >= right:
        return
    pivot = _partition(arr, left, right)
    _quick_sort(arr, left, pivot - 1)
    _quick_sort(arr, pivot + 1, right)


# 题目：对非空合法闭区间 [left, right] 以最右元素为基准原地划分，返回基准最终下标；左侧元素不大于基准，右侧元素大于基准。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# a = [9, 3, 1, 2, 8]
# p = _partition(a, 1, 3)
# assert p == 2 and a == [9, 1, 2, 3, 8]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# a = [5]
# assert _partition(a, 0, 0) == 0
# assert a == [5]
def _partition(arr, left, right):
    """变体：划分（以右端为 pivot）。

    思路：把小于等于 pivot 的元素依次换到左边，最后把 pivot 放到分界位置。
    """
    pivot = arr[right]
    i = left
    for j in range(left, right):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[right] = arr[right], arr[i]
    return i
