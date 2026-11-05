"""回溯

总体思路：
- 在决策树上做 DFS：做选择 -> 递归 -> 撤销选择（回溯）
- 用约束剪枝，避免搜无效分支
- 适合排列、组合、子集、棋盘搜索等“枚举所有方案”

常见信号：求所有方案、N 皇后、括号生成、单词搜索
"""


# 题目：给定不含重复元素的数组，返回所有全排列；每个元素恰好使用一次，答案顺序不作要求。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert sorted(permute([1, 2, 3])) == [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert permute([1]) == [[1]]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert permute([]) == [[]]
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


# 题目：给定不含重复元素的数组，返回所有子集（包含空集）；每个子集中保持原数组相对顺序，答案顺序不作要求。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert sorted(subsets([1, 2])) == [[], [1], [1, 2], [2]]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert subsets([]) == [[]]
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


# 题目：给定不重复的正整数 candidates 和非负目标 target，返回和为目标的所有不重复组合，每个数可重复选；会原地排序候选数组，答案顺序不作要求。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert sorted(combination_sum([2, 3, 6, 7], 7)) == [[2, 2, 3], [7]]
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert combination_sum([2], 1) == []
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert combination_sum([], 0) == [[]]
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


# 题目：给定正整数 n，在 n×n 棋盘放置 n 个互不攻击的皇后，返回所有棋盘；Q 表示皇后，. 表示空位，答案顺序不作要求。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert sorted(solve_n_queens(4)) == sorted([['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']])
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert solve_n_queens(1) == [['Q']]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert solve_n_queens(2) == []
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
