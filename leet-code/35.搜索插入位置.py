#
# @lc app=leetcode.cn id=35 lang=python3
#
# [35] 搜索插入位置
#


# @lc code=start
from typing import List


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:

        def s_data(nums, start, end, target):
            mid = (start + end) // 2
            if start >= end:
                if nums[start] >= target:
                    return start
                else:
                    return start + 1
            if nums[mid] == target:
                return mid
            elif nums[mid] > target:
                return s_data(nums, start, mid - 1, target)
            elif nums[mid] < target:
                return s_data(nums, mid + 1, end, target)

        return s_data(nums, 0, len(nums) - 1, target)




# @lc code=end
