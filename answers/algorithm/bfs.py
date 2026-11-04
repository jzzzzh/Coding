"""广度优先搜索 (BFS)

总体思路：
- 用队列一层一层向外扩：先处理距离起点近的点，再处理更远的点
- 适合“最短步数 / 层序遍历 / 无权图最短路”这类问题
- 关键用 visited 避免重复入队

常见信号：求最少步数、二叉树层序、迷宫最短路径
"""

from collections import deque


def bfs(graph, start):
    """变体：图的 BFS 遍历。

    思路：队列存待访问节点，弹出后把未访问邻居入队，得到按层访问顺序。
    """
    visited = set([start])
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def bfs_shortest_path(graph, start, end):
    """变体：无权图最短路径长度。

    思路：队列里额外记录距离；第一次到达终点时就是最短步数（边权全为 1）。
    """
    if start == end:
        return 0
    visited = set([start])
    queue = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor == end:
                return dist + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1
