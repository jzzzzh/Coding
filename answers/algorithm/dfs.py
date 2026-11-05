"""深度优先搜索 (DFS)

总体思路：
- 沿着一条路走到不能再走，再回溯换另一条路
- 可用递归（系统栈）或显式栈实现
- 适合连通性、路径搜索、树/图遍历、拓扑相关前置遍历

常见信号：能否到达、连通分量、路径枚举、岛屿数量
"""


# 题目：给定邻接表 graph 和起点 start，按邻居列表顺序深度优先遍历并返回访问序列；每个节点只访问一次。未列出的起点按孤立点处理。可传入 visited 集合记录已访问节点，调用时会更新该集合。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert dfs({'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}, 'A') == ['A', 'B', 'D', 'C']
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert dfs({0: [1, 1], 1: [0]}, 0) == [0, 1]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert dfs({}, 'A') == ['A']
def dfs(graph, start, visited=None):
    """变体：递归 DFS。

    思路：访问当前点后，立刻递归进入每个未访问邻居，天然形成“一条路走到底”。
    """
    if visited is None:
        visited = set()
    visited.add(start)
    order = [start]
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            order.extend(dfs(graph, neighbor, visited))
    return order


# 题目：给定邻接表 graph 和起点 start，按邻居列表顺序深度优先遍历并返回访问序列；每个节点只访问一次。未列出的起点按孤立点处理。要求用显式栈实现。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert dfs_iterative({'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}, 'A') == ['A', 'B', 'D', 'C']
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert dfs_iterative({0: [1, 1], 1: [0]}, 0) == [0, 1]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert dfs_iterative({}, 'A') == ['A']
def dfs_iterative(graph, start):
    """变体：迭代 DFS。

    思路：用栈模拟递归；为了让访问顺序接近递归版，邻居可按反序压栈。
    """
    visited = set()
    stack = [start]
    order = []
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                stack.append(neighbor)
    return order
