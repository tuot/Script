#
# @lc app=leetcode.cn id=64 lang=python3
#
# [64] 最小路径和
#

# @lc code=start
from typing import List


class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dp = [[0 for i in range(n)] for j in range(m)]
        for i in range(m):
            for j in range(n):
                if i-1 >= 0 and j - 1 >= 0:
                    dp[i][j] += min(dp[i][j-1], dp[i-1][j])
                elif i-1 >= 0:
                    dp[i][j] += dp[i-1][j]
                elif j - 1 >= 0:
                    dp[i][j] += dp[i][j-1]
                dp[i][j] += grid[i][j]
        return dp[m-1][n-1]
# @lc code=end


grid = [[1,2,3],[4,5,6]]

a = Solution().minPathSum(grid)
print(a)
