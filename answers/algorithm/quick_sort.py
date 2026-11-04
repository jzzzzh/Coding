"""快速排序

总体思路：
- 选一个基准 pivot，把数组分成“小于等于 pivot”和“大于 pivot”两段
- 再对左右两段递归排序（分治）
- 平均 O(n log n)，最坏 O(n^2)；可原地排序

常见信号：原地排序、快速选择第 K 大（partition 思想同源）
"""


def quick_sort(arr):
    """变体：原地快速排序入口。

    思路：对整个区间做 partition + 递归，直接修改原数组。
    """
    _quick_sort(arr, 0, len(arr) - 1)
    return arr


def _quick_sort(arr, left, right):
    """变体：区间递归排序。

    思路：区间长度 <= 1 结束；否则划分后分别处理左右子区间。
    """
    if left >= right:
        return
    pivot = _partition(arr, left, right)
    _quick_sort(arr, left, pivot - 1)
    _quick_sort(arr, pivot + 1, right)


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
