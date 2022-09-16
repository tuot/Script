#
# @lc app=leetcode.cn id=134 lang=python3
#
# [134] 加油站
#

# @lc code=start
from typing import List


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        diff_list = []
        total = 0
        for i in range(len(gas)):
            diff = gas[i] - cost[i]
            total += diff
            diff_list.append(diff)
        if total < 0:
            return -1
        the_min_index = 0
        the_min = diff_list[0] if diff_list[0] < 0 else 0
        start = diff_list[0]
        for i in range(1, len(diff_list)):
            start += diff_list[i]
            if start < the_min:
                the_min_index = i
                the_min = start
        return  (the_min_index + 1) % len(diff_list) if the_min < 0 else the_min_index

# @lc code=end


# gas = [2, 3, 4]
# cost = [3, 4, 3]


gas =  [1,2,3,4,5]
cost = [3,4,5,1,2]

# gas = [6,1,4,3,5]
# cost = [3,8,2,4,2]


# gas = [2]
# cost = [2]

gas = [1,2]
cost = [2,1]


a = Solution().canCompleteCircuit(gas=gas, cost=cost)
print(a)