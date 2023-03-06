#
# @lc app=leetcode.cn id=947 lang=python3
#
# [947] 移除最多的同行或同列石头
#

from typing import List
# @lc code=start
class Solution:
    def removeStones(self, stones: List[List[int]]) -> int:
        l = len(stones)
        m, n = -1, -1
        for i in stones:
            m = max(m, i[0])
            n = max(n, i[0])
        m += 1
        n += 1
        res = []
        arr_stone = [ [ 0 for i in range(n) ] for j in range(m)]
        for i in stones:
            arr_stone[i[0]][i[1]] = 1

        x, y = [-1, -1]
        start_flag = False
        for i in range(m):
            for j in range(n):
                if arr_stone[i][j]:
                    x, y = [i, j]
                    start_flag = True
                    break
            if start_flag:
                break

        def remove_stone(x, y, res):
            for i in range(x+1, m):
                if arr_stone[i][y]:
                    res.append(1)
                    arr_stone[i][y] = 0
                    remove_stone(i, y, res)
            for j in range(y+1, n):
                if arr_stone[x][j]:
                    res.append(1)
                    arr_stone[x][j] = 0
                    remove_stone(x, j, res)
            for j in range(y-1, -1, -1):
                if arr_stone[x][j]:
                    res.append(1)
                    arr_stone[x][j] = 0
                    remove_stone(x, j, res)

        remove_stone(x, y, res)

        return len(res)
# @lc code=end

stones = [[0,1],[1,0],[1,1]]
print(Solution().removeStones(stones))