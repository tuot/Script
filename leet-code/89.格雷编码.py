#
# @lc app=leetcode.cn id=89 lang=python3
#
# [89] 格雷编码
#

# @lc code=start
from typing import List


class Solution:
    def grayCode(self, n: int) -> List[int]:
        def btoint(l):
            a = []
            for i in l:
                a.append(
                    int(i, 2)
                )
            return a
        def f(result, k):
            if k == 0:
                return result
            tmp = []
            for i in result:
                tmp.append("0" + i)
            for i in reversed(result):
                tmp.append("1" + i)
            return f(tmp, k-1)
        result = []
        result.extend(['0', '1'])
        return btoint(f(result, n-1))
# @lc code=end


a = Solution().grayCode(10)
print(a)
