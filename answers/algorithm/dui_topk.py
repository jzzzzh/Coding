"""堆 / Top-K

总体思路：
- 堆能在 O(log k) 维护当前最优的 k 个候选
- 求前 K 大用大小为 K 的小顶堆；求前 K 小用大小为 K 的大顶堆
- 比全排序更省：O(n log k) 而不是 O(n log n)

常见信号：第 K 大/小、前 K 高频、随时取极值
"""

# 题目：手写支持小顶堆和大顶堆的二叉堆，实现初始化、长度、插入、弹出和查看堆顶；不使用 heapq 等库。
class Heap:
    # 题目：初始化空二叉堆，is_min_heap=True 为小顶堆，False 为大顶堆；元素必须能相互比较。
    # 测试案例 1（输入见调用参数，预期结果见断言）：
    # h = Heap()
    # assert h.heap == [] and h.is_min_heap is True
    # 测试案例 2（输入见调用参数，预期结果见断言）：
    # h = Heap(False)
    # assert len(h) == 0 and h.is_min_heap is False
    def __init__(self, is_min_heap=True):
        self.heap = []
        self.is_min_heap = is_min_heap

    # 题目：返回当前堆中元素个数，支持 len(heap)。
    # 测试案例 1（输入见调用参数，预期结果见断言）：
    # h = Heap()
    # assert len(h) == 0
    # 测试案例 2（输入见调用参数，预期结果见断言）：
    # h = Heap()
    # h.push(3)
    # h.push(3)
    # assert len(h) == 2
    def __len__(self):
        return len(self.heap)

    # 题目：比较 a 是否应比 b 更靠近堆顶：小顶堆判断 a < b，大顶堆判断 a > b；相等时返回 False。
    # 测试案例 1（输入见调用参数，预期结果见断言）：
    # assert Heap()._compare(1, 2) is True
    # 测试案例 2（输入见调用参数，预期结果见断言）：
    # assert Heap(False)._compare(2, 1) is True
    # 测试案例 3（输入见调用参数，预期结果见断言）：
    # assert Heap()._compare(2, 2) is False
    def _compare(self, a, b):
        if self.is_min_heap:
            return a < b
        return a > b

    # 向上调整
    # 题目：假设除了合法下标 i 的元素可能比父节点更优，其余位置均满足堆性质；向上调整以恢复堆性质。
    # 测试案例 1（输入见调用参数，预期结果见断言）：
    # h = Heap()
    # h.heap = [2, 4, 1]
    # h._sift_up(2)
    # assert h.heap == [1, 4, 2]
    # 测试案例 2（输入见调用参数，预期结果见断言）：
    # h = Heap(False)
    # h.heap = [2, 1, 3]
    # h._sift_up(2)
    # assert h.heap == [3, 1, 2]
    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2

            if self._compare(self.heap[i], self.heap[parent]):
                self.heap[i], self.heap[parent] = (
                    self.heap[parent], self.heap[i]
                )
                i = parent
            else:
                break

    # 向下调整
    # 题目：假设合法下标 i 的左右子树已满足堆性质，而 i 可能比子节点更差；向下调整以恢复堆性质。
    # 测试案例 1（输入见调用参数，预期结果见断言）：
    # h = Heap()
    # h.heap = [5, 2, 3]
    # h._sift_down(0)
    # assert h.heap == [2, 5, 3]
    # 测试案例 2（输入见调用参数，预期结果见断言）：
    # h = Heap(False)
    # h.heap = [1, 5, 3]
    # h._sift_down(0)
    # assert h.heap == [5, 1, 3]
    def _sift_down(self, i):
        n = len(self.heap)

        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            best = i

            if left < n and self._compare(
                self.heap[left], self.heap[best]
            ):
                best = left

            if right < n and self._compare(
                self.heap[right], self.heap[best]
            ):
                best = right

            if best == i:
                break

            self.heap[i], self.heap[best] = (
                self.heap[best], self.heap[i]
            )
            i = best

    # 插入元素
    # 题目：向堆中插入一个可比较元素，保持小顶堆或大顶堆性质；重复值允许存在，时间 O(log n)。
    # 测试案例 1（输入见调用参数，预期结果见断言）：
    # h = Heap()
    # h.push(3)
    # h.push(1)
    # h.push(1)
    # assert h.peek() == 1 and len(h) == 3
    # 测试案例 2（输入见调用参数，预期结果见断言）：
    # h = Heap(False)
    # h.push(-2)
    # h.push(3)
    # assert h.peek() == 3
    def push(self, val):
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    # 弹出堆顶
    # 题目：删除并返回堆顶，随后恢复堆性质；空堆抛出 IndexError，时间 O(log n)。
    # 测试案例 1（输入见调用参数，预期结果见断言）：
    # h = Heap()
    # for x in [3, 1, 2, 1]:
    #     h.push(x)
    # assert [h.pop() for _ in range(4)] == [1, 1, 2, 3]
    # assert len(h) == 0
    # 测试案例 2（输入见调用参数，预期结果见断言）：
    # h = Heap(False)
    # for x in [3, 1, 2]:
    #     h.push(x)
    # assert [h.pop() for _ in range(3)] == [3, 2, 1]
    # 测试案例 3（输入见调用参数，预期结果见断言）：
    # try:
    #     Heap().pop()
    # except IndexError:
    #     pass
    # else:
    #     raise AssertionError('空堆应抛出 IndexError')
    def pop(self):
        if not self.heap:
            raise IndexError("pop from empty heap")

        if len(self.heap) == 1:
            return self.heap.pop()

        ans = self.heap[0]

        self.heap[0] = self.heap.pop()
        self._sift_down(0)

        return ans

    # 查看堆顶
    # 题目：返回堆顶但不删除元素；空堆抛出 IndexError，时间 O(1)。
    # 测试案例 1（输入见调用参数，预期结果见断言）：
    # h = Heap()
    # h.push(2)
    # h.push(1)
    # assert h.peek() == 1 and len(h) == 2
    # 测试案例 2（输入见调用参数，预期结果见断言）：
    # try:
    #     Heap().peek()
    # except IndexError:
    #     pass
    # else:
    #     raise AssertionError('空堆应抛出 IndexError')
    def peek(self):
        if not self.heap:
            raise IndexError("peek from empty heap")
        return self.heap[0]
