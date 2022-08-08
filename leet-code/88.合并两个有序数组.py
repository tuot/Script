#
# @lc app=leetcode.cn id=88 lang=python3
#
# [88] 合并两个有序数组
#

# @lc code=start
from typing import List

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        i, j = m-1, n-1
        ii = m + n - 1
        while i >= 0 and j >= 0:
            if nums1[i] > nums2[j]:
                nums1[i], nums1[ii] = nums1[ii], nums1[i]
                i -= 1
                ii -= 1
            else:
                nums2[j], nums1[ii] = nums1[ii], nums2[j]
                ii -= 1
                j -= 1
        while j >= 0:
            nums1[ii] = nums2[j]
            ii -= 1
            j -= 1
# @lc code=end