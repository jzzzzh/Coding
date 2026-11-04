"""回溯

总体思路：
- 在决策树上做 DFS：做选择 -> 递归 -> 撤销选择（回溯）
- 用约束剪枝，避免搜无效分支
- 适合排列、组合、子集、棋盘搜索等“枚举所有方案”

常见信号：求所有方案、N 皇后、括号生成、单词搜索
"""


def permute(nums):
    """变体：全排列。

    思路：路径长度等于 n 时收结果；用 used 标记已选下标，避免重复使用。
    """
    result = []

    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i, num in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(num)
            backtrack(path, used)
            path.pop()
            used[i] = False

    backtrack([], [False] * len(nums))
    return result


def subsets(nums):
    """变体：子集。

    思路：每个位置都是一种合法方案；从 start 往后选，保证元素相对顺序、不重复。
    """
    result = []

    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result


def combination_sum(candidates, target):
    """变体：组合总和（元素可重复选）。

    思路：递归时仍从当前下标 i 开始（可再用自己）；数字超过剩余值则剪枝。
    """
    result = []

    def backtrack(start, remain, path):
        if remain == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break
            path.append(candidates[i])
            backtrack(i, remain - candidates[i], path)
            path.pop()

    candidates.sort()
    backtrack(0, target, [])
    return result


def solve_n_queens(n):
    """变体：N 皇后。

    思路：按行放皇后；用列、主对角、副对角三个集合判冲突，冲突则跳过。
    """
    result = []
    board = [["."] * n for _ in range(n)]
    cols = set()
    diag1 = set()
    diag2 = set()

    def backtrack(row):
        if row == n:
            result.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or row - col in diag1 or row + col in diag2:
                continue
            board[row][col] = "Q"
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            backtrack(row + 1)
            board[row][col] = "."
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return result
