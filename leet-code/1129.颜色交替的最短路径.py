#
# @lc app=leetcode.cn id=1129 lang=python3
#
# [1129] 颜色交替的最短路径
#

from typing import List
# @lc code=start
class Solution:
    def shortestAlternatingPaths(self, n: int, redEdges: List[List[int]], blueEdges: List[List[int]]) -> List[int]:
        def get_map(mmap):
            x_map = {}
            for i in mmap:
                a, b = i
                if a in x_map:
                    x_map[a].append(b)
                else:
                    x_map[a] = [b]
            return x_map
        red_map = get_map(redEdges)
        blue_map = get_map(blueEdges)

        def insert_to_queue(queue, result, l_node, f, color):
            for i in l_node:
                if result[i] == -1:
                    result[i] =  f
                queue.append([i, color, f])
        result ={ i: -1 for i in range(n)}
        result[0] = 0
        queue = [[0, None, 0]]
        while len(queue) > 0:
            node, color, f = queue[0]
            queue = queue[1:]
            if node in red_map and color != 'red':
                insert_to_queue(queue, result, red_map.pop(node), f+1, 'red')
            if node in blue_map and color != 'blue':
                insert_to_queue(queue, result, blue_map.pop(node), f+1, 'blue')

        return list(result.values())

# @lc code=end

n = 5
red_edges = [[0,1],[1,2], [2,3], [3,4]]
blue_edges = [[1,2], [2,3], [3,1]]


res = Solution().shortestAlternatingPaths(n, red_edges, blue_edges)
print(res)