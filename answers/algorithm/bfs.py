"""广度优先搜索 (BFS)

总体思路：
- 用队列一层一层向外扩：先处理距离起点近的点，再处理更远的点
- 适合“最短步数 / 层序遍历 / 无权图最短路”这类问题
- 关键用 visited 避免重复入队

常见信号：求最少步数、二叉树层序、迷宫最短路径
"""

# 题目：给定邻接表 graph 和起点 start，按邻居列表顺序进行广度优先遍历，返回访问序列；环和重复边不应造成重复访问。未列在邻接表中的起点按孤立点处理。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert bfs({'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}, 'A') == ['A', 'B', 'C', 'D']
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert bfs({0: [1, 1], 1: [0]}, 0) == [0, 1]
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert bfs({}, 'A') == ['A']
def bfs(graph, start):
    """变体：图的 BFS 遍历。

    思路：队列存待访问节点，弹出后把未访问邻居入队，得到按层访问顺序。
    """
    visited = set([start])
    # 列表保存队列，队头下标递增，避免 pop(0) 搬移元素。
    queue = [start]
    head = 0
    order = []
    while head < len(queue):
        node = queue[head]
        head += 1
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


# 题目：给定无权图邻接表和起终点，返回最短路径的边数；不可达返回 -1，起终点相同返回 0。
# 测试案例 1（输入见调用参数，预期结果见断言）：
# assert bfs_shortest_path({0: [1, 2], 1: [3], 2: [3]}, 0, 3) == 2
# 测试案例 2（输入见调用参数，预期结果见断言）：
# assert bfs_shortest_path({0: [1], 1: [0]}, 0, 2) == -1
# 测试案例 3（输入见调用参数，预期结果见断言）：
# assert bfs_shortest_path({}, 'A', 'A') == 0
def bfs_shortest_path(graph, start, end):
    """变体：无权图最短路径长度。

    思路：队列里额外记录距离；第一次到达终点时就是最短步数（边权全为 1）。
    """
    if start == end:
        return 0
    visited = set([start])
    queue = [(start, 0)]
    head = 0
    while head < len(queue):
        node, dist = queue[head]
        head += 1
        for neighbor in graph.get(node, []):
            if neighbor == end:
                return dist + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1
