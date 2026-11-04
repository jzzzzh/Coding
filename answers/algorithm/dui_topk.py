"""堆 / Top-K

总体思路：
- 堆能在 O(log k) 维护当前最优的 k 个候选
- 求前 K 大用大小为 K 的小顶堆；求前 K 小用大小为 K 的大顶堆
- 比全排序更省：O(n log k) 而不是 O(n log n)

常见信号：第 K 大/小、前 K 高频、随时取极值
"""

import heapq


def top_k_largest(nums, k):
    """变体：前 K 大元素。

    思路：直接调用小顶堆选取最大的 k 个。
    """
    return heapq.nlargest(k, nums)


def top_k_smallest(nums, k):
    """变体：前 K 小元素。

    思路：直接调用堆选取最小的 k 个。
    """
    return heapq.nsmallest(k, nums)


def find_kth_largest(nums, k):
    """变体：第 K 大元素。

    思路：维护大小为 k 的小顶堆；堆顶就是当前第 k 大。
    """
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


def find_kth_smallest(nums, k):
    """变体：第 K 小元素。

    思路：Python 只有小顶堆，存负数模拟大顶堆；堆大小保持 k。
    """
    heap = []
    for num in nums:
        heapq.heappush(heap, -num)
        if len(heap) > k:
            heapq.heappop(heap)
    return -heap[0]
