"""深度优先搜索 (DFS)

总体思路：
- 沿着一条路走到不能再走，再回溯换另一条路
- 可用递归（系统栈）或显式栈实现
- 适合连通性、路径搜索、树/图遍历、拓扑相关前置遍历

常见信号：能否到达、连通分量、路径枚举、岛屿数量
"""


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
